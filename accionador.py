from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get('https://www.google.com/fbx?fbx=snake_arcade')
driver.maximize_window()
time.sleep(3)



actions = ActionChains(driver)
actions.send_keys(Keys.ENTER)
actions.perform()
time.sleep(2)
for i in range(10):
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()
    time.sleep(0.1)
    actions.send_keys(Keys.ARROW_UP)
    actions.perform()
time.sleep(10)

driver.quit