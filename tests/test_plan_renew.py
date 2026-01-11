import time
import re
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from UI import shared_data
from UI.shared_data import customer_data
from pages import renew_discount_logic



customer_info_plan_subscription=shared_data.customer_data

print(customer_data)

from utils.test_decorator import test_logger  # Import decorator

@pytest.mark.regression
@test_logger
def test_plan_renew1(driver):
    autopay_checkbox=driver.find_element(By.ID, "allow_autopay_discount")
    if autopay_checkbox.is_enabled():
        autopay_checkbox.click()
        autopay_discount_path=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "autopay_discount_amount")))
        autopay_discount_value=autopay_discount_path.get_attribute("value") or "0"
        print("Autopay discount amount=" +autopay_discount_value)
        #renew_discount_logic(driver)


    element_plan_cost = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "plan_cost")))
    plan_cost = element_plan_cost.get_attribute("value") or "0"
    print("plan_cost=" + plan_cost)

    element_additional_charge= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "additionalCharges_amount")))
    additional_charge=element_additional_charge.get_attribute("value") or "0"
    print("Additional charge amount=", additional_charge)

    discount = driver.find_element(By.ID, "sys_config_discount_amount").get_attribute("value") or "0"
    print("discount=" + discount)

    coupon_discount = driver.find_element(By.ID, "finalCouponAmount").get_attribute("value") or "0"
    print("Coupon Discount=" + coupon_discount)

    total_tax_value = driver.find_element(By.ID, "TAX_AMOUNT_NEW").get_attribute("value") or "0"
    print("tax=" + total_tax_value)

    # element_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "later_autopay_data_html")))
    # text = element_text.text.strip()
    # print("Extracted text:", text)

    tax_locater= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "plan_tax_amount")))
    tax=tax_locater.get_attribute("value") or "0"
    print("tax value=" +tax)

    # match = re.search(r"[-+]?\d*\.\d+|\d+", text)
    # amount = match.group() if match else "0"
    # print("amount=" + amount)

    tax_included_handle= driver.find_element(By.XPATH, '//span[@id="tax_included_html"]')
    if tax_included_handle.is_displayed():
        final_tax=round(float(total_tax_value)-float(tax),2)
        print("Final tax amount", final_tax)
        print("tax=", tax)
        print("total tax=", total_tax_value)
        total_amount = round(
            float(plan_cost) - float(discount) + float(final_tax) + float(additional_charge) - float(coupon_discount) - float(
                autopay_discount_value), 2)
        print(f"total_amount={total_amount}")
    else:
        total_amount = round(
            float(plan_cost) - float(discount) + float(tax) + float(additional_charge) - float(coupon_discount) - float(
                autopay_discount_value), 2)
        print(f"total_amount={total_amount}")




    csr_total_amount_val = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "amount"))).get_attribute("value") or "0"
    print("csr_total_amount_val=" + csr_total_amount_val)

    assert float(total_amount) == float(csr_total_amount_val), (
        f"Mismatch! Expected: {total_amount}, CSR: {csr_total_amount_val}"
    )
    print("Case Total amount matched successfully")
    print("All scripts succesfully done")
