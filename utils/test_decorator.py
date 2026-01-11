import functools
from utils.logger import take_full_page_screenshot, write_html_report

def test_logger(test_func):
    @functools.wraps(test_func)
    def wrapper(driver, *args, **kwargs):
        test_name = test_func.__name__

        try:
            test_func(driver, *args, **kwargs)
            screenshot = take_full_page_screenshot(driver, test_name)
            write_html_report(test_name, "PASS", "Test passed successfully", screenshot)

        except AssertionError as ae:
            screenshot = take_full_page_screenshot(driver, f"{test_name}_fail")
            write_html_report(test_name, "FAIL", str(ae), screenshot)
            raise

        except Exception as e:
            screenshot = take_full_page_screenshot(driver, f"{test_name}_error")
            write_html_report(test_name, "ERROR", str(e), screenshot)
            raise

    return wrapper
