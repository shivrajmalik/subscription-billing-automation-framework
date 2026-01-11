from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

from UI import shared_data
from pages.Search_customer import code_to_open_active_customer_TG5 as active_customer


def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))


def get_driver():
    """For preventing GOOGLE CAPTCHA .... Launch Chrome using Selenium Manager — no driver mismatch issues."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        return driver

    except Exception as e:
        print("[!] Critical error launching Chrome:", e)
        return None


def test_plan_renew_flow(max_retries=3):
    url = shared_data.url
    username = shared_data.username
    password = shared_data.password

    driver = None      # <-- avoids UnboundLocalError
    retry_count = 0
    success = False

    try:
        driver = get_driver()
        if not driver:
            print("[!] Driver failed to start")
            return

        wait = WebDriverWait(driver, 15)

        # To retry 3 times for login Google Captcha
        while retry_count < max_retries and not success:
            print("Opening URL...")
            driver.get(url)
            time.sleep(2)
            try:
                print("Filling login form...")

                username_field = wait.until(EC.presence_of_element_located((By.ID, 'email_input')))
                human_typing(username_field, username)

                password_field = wait.until(EC.presence_of_element_located((By.ID, 'chkYes')))
                human_typing(password_field, password)

                login_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit_button')))
                login_button.click()

                time.sleep(3)

                # Check if login failed
                try:
                    error = driver.find_element(By.ID, "error_message")
                    print(f"[!] Login failed: {error.text}")
                    retry_count += 1
                except NoSuchElementException:
                    print("[+] Login successful!")
                    success = True

            except Exception as form_error:
                print(f"[!] Error during login attempt: {form_error}")
                retry_count += 1

    except Exception as main_error:
        print("[!] Unexpected error:", main_error)

    finally:
        if driver:
            try:
                active_customer(driver)
            except Exception as e:
                print("[!] Error in active customer function:", e)

            driver.quit()

    if not success:
        print("[X] Max retries reached. Login failed.")
    else:
        print("[✓] Login flow completed & returned to main.")


def main():
    test_plan_renew_flow()
