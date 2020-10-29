import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command

def findDocsFirefox(req, driver):
    """
    Displays documentation web page and simulates search using Firefox browser, then returns url of result page
    'req' - text to input for search on the site
    'driver' - web driver object
    """
    driver.get("https://docs.oracle.com/en/java/javase/15/docs/api/index.html")

    inputElement = driver.find_element_by_id("search")
    inputElement = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#search")))
    inputElement.clear()
    inputElement.send_keys(req)
    inputElement.send_keys(Keys.ARROW_DOWN)
    inputElement.send_keys(Keys.ENTER)
    time.sleep(1)
    """ Doesn't work
    if driver.current_url == "https://docs.oracle.com/en/java/javase/15/docs/api/index.html":
        "No such class"
    else:
    """
    return driver.current_url

def quitDriver(driver):
    """
    Quits the driver and close every associated window
    'driver' - web driver object
    """
    driver.quit()

while (1 == 1):
    req = input()
    driver = webdriver.Firefox()
    print(findDocsFirefox(req, driver))
    quitDriver(driver)
