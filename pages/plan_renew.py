from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from tests.test_plan_renew import test_plan_renew1
import UI.shared_data as shared_data
from db_queries import get_subscription_by_account





def open_plan_renew_page(driver):
    try:
        if shared_data.instance=="QA":
            print("[DEBUG] Waiting for 'Plan renew (PC519)' link to be clickable...")
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.LINK_TEXT, "Plan renew (PC519)"))).click()
            print("Plan renew section opened")

        else:
            print("[DEBUG] Waiting for 'Plan Renew (PC519)' link to be clickable...")
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.LINK_TEXT, "Plan Renew (PC519)"))).click()
            print("Plan renew section opened")






        try:
            print("[DEBUG] Clicking on checkbox to add plan from IOT...")
            driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/section[2]/div/div[1]/div/div/div/div[2]/div/div/ul/li/div/form/div/div/div[19]/div/p/span/a").click()
            test_plan_renew1(driver)


        except (TimeoutException, NoSuchElementException):
            print("[DEBUG] Plan names section or checkbox not found. Skipping this step.")
            print("1st plan renew test executed")
            test_plan_renew1(driver)
            customer_id = shared_data.customer_id
            get_subscription_by_account(customer_id)
            print(shared_data.customer_data)


    except Exception as e:
        print(f"[ERROR] Failed to interact with Plan Renew page: {e}")
