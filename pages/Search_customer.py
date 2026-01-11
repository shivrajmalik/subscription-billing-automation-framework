from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.plan_renew import open_plan_renew_page
from UI import shared_data
import time
from selenium.webdriver.chrome.options import Options


def after_cust_open(driver):
    wait = WebDriverWait(driver, 20)
    try:
        print("[DEBUG] Fetching customer state...")
        state = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table.customer_information tbody tr:nth-of-type(3) td")
        )).text
        print("Customer State:", state)

        try:
            print("[DEBUG] Clicking on all-lines icon...")
            all_lines_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//section[1]/h1/a[2]")
            ))
            all_lines_btn.click()

            print("[DEBUG] Opening parent line...")
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//section[2]//table/tbody/tr[1]/td[2]")
            )).click()
        except TimeoutException:
            print("[DEBUG] All-lines icon not clickable. Skipping parent line click.")

        print("[DEBUG] Fetching plan name...")
        plan = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//th[text()=' Plan']/following-sibling::td")
        )).text
        print("Plan Name:", plan)

        print("[DEBUG] Navigating to Plan Renew page...")
        open_plan_renew_page(driver)

        return plan, state
    except (TimeoutException, NoSuchElementException) as e:
        print(f"[ERROR] Failed during active customer lookup: {e}")
        return None, None


def code_to_open_active_customer_TG5(driver):
    wait = WebDriverWait(driver, 20)

    if shared_data.customer_option == "manual":
        customer_id = shared_data.customer_id
        search_textbox = driver.find_element(By.ID, "searchHeader")
        search_textbox.click()
        search_textbox.send_keys(customer_id)
        driver.find_element(By.ID, "dropdown-toggle-header-search").click()
        after_cust_open(driver)

    elif shared_data.customer_option == "active_one":
        try:
            print("[DEBUG] Waiting for 'searchHeader' to be clickable...")
            wait.until(EC.element_to_be_clickable((By.ID, "searchHeader"))).click()

            print("[DEBUG] Clicking on Advanced Search...")
            wait.until(EC.element_to_be_clickable((By.ID, "advance_search"))).click()

            print("[DEBUG] Selecting 'Active' from acc_status dropdown...")
            select = Select(wait.until(EC.element_to_be_clickable((By.ID, "acc_status"))))
            select.select_by_value("Active")

            print("[DEBUG] Clicking Search...")
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[3]/button")
            )).click()

            print("[DEBUG] Clicking first active customer row...")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr[1]/td[1]"))).click()

            return after_cust_open(driver)

        except (TimeoutException, NoSuchElementException) as e:
            print(f"[ERROR] Failed during active customer lookup: {e}")
            return None, None


    elif shared_data.customer_option == "active_all":

        print("active_all")

        try:

            print("[DEBUG] Waiting for 'searchHeader' to be clickable...")

            wait.until(EC.element_to_be_clickable((By.ID, "searchHeader"))).click()

            print("[DEBUG] Clicking on Advanced Search...")

            wait.until(EC.element_to_be_clickable((By.ID, "advance_search"))).click()

            print("[DEBUG] Selecting 'Active' from acc_status dropdown...")

            select = Select(wait.until(EC.element_to_be_clickable((By.ID, "acc_status"))))

            select.select_by_value("Active")

            print("[DEBUG] Clicking Search...")

            wait.until(EC.element_to_be_clickable(

                (By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[3]/button")

            )).click()

            time.sleep(3)

            while True:

                print("[INFO] Fetching all customer rows on current page...")

                rows = driver.find_elements(By.CSS_SELECTOR, "#example_body > tr")

                customer_links = []

                for index, row in enumerate(rows, start=1):

                    try:

                        data_url = row.get_attribute("data-url")

                        if not data_url:
                            print(f"[WARN] No data-url for row {index}, skipping...")

                            continue

                        full_url = f"url/{data_url}"

                        customer_links.append(full_url)


                    except Exception as e:

                        print(f"[WARN] Could not fetch URL from row {index}: {e}")

                        continue

                print(f"[INFO] Found {len(customer_links)} customers to process...")

                for customer_url in customer_links:
                    print(f"[INFO] Opening customer: {customer_url}")

                    driver.get(customer_url)

                    time.sleep(2)

                    after_cust_open(driver)

                    print("[INFO] Going back to customer list...")

                    driver.back()

                    time.sleep(2)

                # After processing all customers on page, click next

                try:

                    next_btn = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/section/div/div/div/div[3]/ul/li/a")

                    if "disabled" in next_btn.get_attribute("class"):

                        print("[INFO] No more pages. Stopping.")

                        break

                    else:

                        print("[INFO] Clicking Next page...")

                        next_btn.click()

                        time.sleep(3)


                except NoSuchElementException:

                    print("[INFO] 'Next' button not found. Possibly last page.")

                    break


                except Exception as e:

                    print(f"[ERROR] Error handling Next button: {e}")

                    break


        except Exception as e:

            print(f"[ERROR] Failed during active_all process: {e}")


    elif shared_data.customer_option == "suspended_one":
        print("suspended_one (not implemented yet)")

    elif shared_data.customer_option == "suspended_all":
        print("suspended_all (not implemented yet)")

