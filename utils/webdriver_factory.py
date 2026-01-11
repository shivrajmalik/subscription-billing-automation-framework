from selenium import webdriver

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Add more options if needed
    driver = webdriver.Chrome(options=options)
    return driver
