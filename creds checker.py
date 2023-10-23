


from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : 'C:\\Users\\ATHARVA\\PycharmProjects\\moodleDrive\\seg\\'}
chrome_options.add_experimental_option('prefs', prefs)



def moodle_creds_checker(uusername, ppassword):
  driver = webdriver.Chrome(chrome_options=chrome_options)
  og_moodle_link = "http://moodle.apsit.org.in/moodle/login/index.php"
  driver.get(og_moodle_link)


  time.sleep(4)

  login_form_username = driver.find_elements(By.XPATH,"//input[@name='username'][@id='username'][@type='text']")

  login_form_password = driver.find_elements(By.XPATH,"//input[@name='password'][@id='password'][@type='password']")
  login_form_username[0].send_keys(uusername)
  login_form_password[0].send_keys(ppassword)
  login_form_button = driver.find_elements(By.XPATH,"//input[@id='loginbtn']")
  login_form_button[0].click()

  time.sleep(40)
  invalid_tag= driver.find_elements(By.XPATH,"/html/body/div[2]/div/section/div/div/div/div[1]/div[1]/a")
  if len(invalid_tag)==0:
    print("Valid Credentials!")
  else:
    print("Invalid Credentials Genius. I mean smh '_'")
  return None

moodle_creds_checker("20102060", "20102060@Apsit")

