import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)


def safe_click(driver, actions, elem, max_attempts=3):
    """Click an element with retries; close popups if they intercept clicks."""
    for _ in range(max_attempts):
        try:
            elem.click()
            return True
        except ElementClickInterceptedException:
            try:
                driver.find_element(By.CLASS_NAME, "pop-up-template__close").click()
            except Exception:
                pass

            try:
                actions.move_to_element(driver.find_element(By.CLASS_NAME, "icon--kialo-logo")).perform()
            except Exception:
                pass
            time.sleep(0.5)
    return False


def close_initial_dialogs(driver):
    """Best-effort close for Kialo dialogs that can appear on first load."""
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "pop-up-content__inner-modal-wrapper"))
        )
        wrapper = driver.find_element(By.CLASS_NAME, "pop-up-content__inner-modal-wrapper")
        wrapper.find_element(By.CLASS_NAME, "discussion-info-dialog-header__close").click()
        time.sleep(0.5)
    except Exception:
        pass


def get_selected_claim_text(driver):
    """Returns the selected claim text ('statement')."""
    try:
        return (
            driver.find_element(By.CLASS_NAME, "selected-claim")
            .find_element(By.CLASS_NAME, "claim-text__content")
            .text
        )
    except Exception:
        return driver.find_element(By.CLASS_NAME, "selected-claim").text


def open_voting_stats(driver, actions):
    """Open the Voting Stats panel from the claim context menu."""
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "claim-controls__control-item"))
    )
    button = driver.find_element(By.CLASS_NAME, "claim-controls__control-item")

    if not safe_click(driver, actions, button):
        raise RuntimeError("Could not click claim controls button.")

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "context-menu"))
    )

    items = driver.find_element(By.CLASS_NAME, "context-menu").find_elements(
        By.CLASS_NAME, "context-menu-item__text"
    )
    for it in items:
        if it.text.strip() == "Voting Stats":
            if not safe_click(driver, actions, it):
                raise RuntimeError("Could not click Voting Stats menu item.")
            return

    raise RuntimeError("Voting Stats item not found in context menu.")


def read_votes(driver):
    """
    Reads the vote counts from the voters histogram.
    Returns a list of strings (as on the page), e.g. ["12", "5", "0", ...]
    """
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "voters-histogram__voters-bar-container"))
    )
    histogram = driver.find_elements(By.CLASS_NAME, "voters-histogram__voters-bar-container")
    votes = []
    for bar in histogram:
        try:
            votes.append(bar.find_element(By.CLASS_NAME, "icon__counter").text.strip())
        except NoSuchElementException:
            votes.append("")
    return votes


def scrape_one_link_to_json(link, out_dir="./outputs", out_name=None, headless=True,
):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    if out_name is None:
        out_name = link.rstrip("/").split("/")[-1]

    firefox_options = webdriver.FirefoxOptions()
    if headless:
        firefox_options.add_argument("--headless")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    firefox_options.add_argument("--disable-notifications")
    firefox_options.add_argument("--disable-popup-blocking")

    driver = webdriver.Firefox(options=firefox_options)
    actions = ActionChains(driver)

    try:
        driver.get(link)
        time.sleep(2)
        close_initial_dialogs(driver)

        statement = get_selected_claim_text(driver)

        open_voting_stats(driver, actions)
        votes = read_votes(driver)

        result = {
            "url": link,
            "statement": statement,
            "votes": votes,
        }

        json_file = out_path / f"{out_name}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Saved: {json_file}")
        return result

    finally:
        driver.quit()


if __name__ == "__main__":
    # put link here:
    URL = "https://www.kialo.com/should-there-be-a-universal-basic-income-ubi-1634"
    scrape_one_link_to_json(URL, out_dir="./outputs")