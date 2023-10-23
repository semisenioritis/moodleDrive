from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys








def moodle_scrapper(uusername, ppassword):
  driver = webdriver.Chrome(ChromeDriverManager().install())
  og_moodle_link = "http://moodle.apsit.org.in/moodle/login/index.php"
  driver.get(og_moodle_link)


  time.sleep(4)

  login_form_username = driver.find_elements(By.XPATH,"//input[@name='username'][@id='username'][@type='text']")

  login_form_password = driver.find_elements(By.XPATH,"//input[@name='password'][@id='password'][@type='password']")
  login_form_username[0].send_keys(uusername)
  login_form_password[0].send_keys(ppassword)
  login_form_button = driver.find_elements(By.XPATH,"//input[@id='loginbtn']")
  login_form_button[0].click()

  time.sleep(4)
  # try catch here if page has loaded and provide option to redo the process
  # driver.get("http://moodle.apsit.org.in/moodle/blog/index.php?"); this is for all possible open blogs
  driver.get("http://moodle.apsit.org.in/moodle/user/profile.php?")
  time.sleep(4)

  blog_page = driver.find_elements(By.XPATH,"/html/body/div[2]/div[2]/div/div/div/section/div/div/div/section[3]/ul/li[1]/span/a")
  blog_page[0].click()
  time.sleep(4)
  valid_downloadable_files= driver.find_elements(By.XPATH, "//div[@class='subject']/a")
  # for i in range(len(valid_downloadable_files)):
  #   print(valid_downloadable_files[i].text)
  #   print("\n---------------")



  moodle_soup = BeautifulSoup(driver.page_source, 'html.parser')
  time.sleep(50)
  driver.quit()

  return None

moodle_scrapper("20102060", "20102060@Apsit")