import pytest
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Import shared data
sys.path.append(r"C:path\automation_framework\UI")
from UI.shared_data import client, instance, customer_id, url

CHROMEDRIVER_PATH = r"C:path\chromedriver.exe"

print("Running test for:", client, instance, customer_id, url)

@pytest.fixture(scope="function")
def browser():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")  # <---- Important for opening new tabs
    options.add_argument("--disable-notifications")    # (Optional) To block notifications
    # options.add_argument("--headless")               # (Optional) if you want no browser popup

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def login(browser):
    username = "username"
    password = "password"

    browser.get(url)
    time.sleep(2)

    try:
        print("[DEBUG] Entering login credentials...")
        browser.find_element(By.ID, "email_input").send_keys(username)
        browser.find_element(By.ID, "chkYes").send_keys(password)
        browser.find_element(By.ID, "submit_button").click()
        time.sleep(3)

        # Simple check: verify if dashboard or some element loaded
        if "Dashboard" not in browser.page_source:
            print("[WARN] Dashboard not detected after login, check manually.")
        else:
            print("[INFO] Login successful!")

    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        raise
