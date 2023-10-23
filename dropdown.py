from selenium.webdriver.support.ui import Select

Select drpCountry = new Select(driver.findElement(By.name("country")));
drpCountry.selectByVisibleText("ANTARCTICA");


import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement
import os.path
from zipfile import ZipFile
import shutil

def moodle_creds_checker(uusername, ppassword):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    og_moodle_link = "http://moodle.apsit.org.in/moodle/login/index.php"
    driver.get(og_moodle_link)
    time.sleep(14)
    login_form_username = driver.find_elements(By.XPATH,"//input[@name='username'][@id='username'][@type='text']")
    login_form_password = driver.find_elements(By.XPATH,"//input[@name='password'][@id='password'][@type='password']")
    login_form_username[0].send_keys(uusername)
    login_form_password[0].send_keys(ppassword)
    login_form_button = driver.find_elements(By.XPATH,"//input[@id='loginbtn']")
    login_form_button[0].click()
    time.sleep(14)
    invalid_tag= driver.find_elements(By.XPATH,"/html/body/div[2]/div/section/div/div/div/div[1]/div[1]/a")
    if len(invalid_tag)==0:
        print("Valid Credentials!\n")
    else:
        print("Invalid Credentials Genius. I mean smh '_'")
  driver.get("http://moodle.apsit.org.in/moodle/blog/edit.php?action=add")

  x = driver.find_element_by_id('RESULT_RadioButton-9')
  drop = Select(x)


  return None
