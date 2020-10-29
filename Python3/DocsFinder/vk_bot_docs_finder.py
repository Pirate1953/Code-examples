#Standard Python modules
import random
import time

#VK modules
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

#Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command

def write_msg(user_id, message):
    """
    Calls method to send the message to the user
    'user_id' - user id
    'message' - the meassage to send
    """
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64)})
    return

def findJavaDocsFirefox(req, driver):
    """
    Displays Java documentation web page and simulates search using Firefox browser, then returns url of result page
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
    return driver.current_url

def findCppDocsFirefox(req, driver):
    """
    Displays Cpp documentation web page and simulates search using Firefox browser, then returns url of result page
    'req' - text to input for search on the site
    'driver' - web driver object
    """
    driver.get("https://en.cppreference.com/w/")

    inputElement = driver.find_element_by_id("searchInput")
    inputElement = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#searchInput")))
    inputElement.clear()
    inputElement.send_keys(req)
    inputElement.send_keys(Keys.ENTER)
    time.sleep(1)
    return driver.current_url

def findPythonDocsFirefox(req, driver):
    """
    Displays Python documentation web page and simulates search using Firefox browser, then returns url of result page
    'req' - text to input for search on the site
    'driver' - web driver object
    """
    driver.get("https://docs.python.org/3/")

    inputElement = driver.find_element_by_name("q")
    #inputElement = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#q")))
    inputElement.clear()
    inputElement.send_keys(req)
    inputElement.send_keys(Keys.ENTER)
    time.sleep(1)
    return driver.current_url

def quitDriver(driver):
    """
    Quits the driver and close every associated window
    'driver' - web driver object
    """
    driver.quit()
    return

def sendResponse(event, driver):
    """
    Checks name of given programming language and sends the search result url
    'event' - Event class object
    """
    request = event.text
    if request.split(' ', maxsplit = 1)[0] == "!java":
        keyword = request.split(' ', maxsplit = 1)[1]
        write_msg(event.user_id, findJavaDocsFirefox(keyword, driver))
    elif request.split(' ', maxsplit = 1)[0] == "!cpp":
        keyword = request.split(' ', maxsplit = 1)[1]
        write_msg(event.user_id, findCppDocsFirefox(keyword, driver))
    elif request.split(' ', maxsplit = 1)[0] == "!py":
        keyword = request.split(' ', maxsplit = 1)[1]
        write_msg(event.user_id, findPythonDocsFirefox(keyword, driver))
    else:
        write_msg(event.user_id, "Syntax: <!Lang name> <Class name>")
        return

token = ""
vk = vk_api.VkApi(token = token)
longpoll = VkLongPoll(vk)

driver = webdriver.Firefox() #Calls Firefox webdriver

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            sendResponse(event, driver)
