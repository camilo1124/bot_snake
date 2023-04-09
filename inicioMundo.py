from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import time


def setup():
    chrome_options=Options()
    chrome_options.add_experimental_option("detach",True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)
    driver.get('https://www.google.com/fbx?fbx=snake_arcade')
    driver.maximize_window()
    #time.sleep(1)
    #boton = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[4]/div[2]')
    wait = WebDriverWait(driver,30)
    boton = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div/div[4]/div[2]')))
    boton.click()
    actions = ActionChains(driver)
    actions.send_keys(Keys.ARROW_UP)
    actions.perform()
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(2)

    return driver, actions