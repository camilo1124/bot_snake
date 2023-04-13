from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import time


def setup():
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/fbx?fbx=snake_arcade')
    driver.maximize_window()
    wait = WebDriverWait(driver,10)
    boton = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div/div[4]/div[2]/img')))
    boton.click()
    driver.implicitly_wait(10)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ARROW_UP)
    actions.perform()
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(2)

    return driver, actions