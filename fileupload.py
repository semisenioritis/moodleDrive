import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.remote.webelement import WebElement
import os.path

JS_DROP_FILES = "var k=arguments,d=k[0],g=k[1],c=k[2],m=d.ownerDocument||document;for(var e=0;;){var f=d.getBoundingClientRect(),b=f.left+(g||(f.width/2)),a=f.top+(c||(f.height/2)),h=m.elementFromPoint(b,a);if(h&&d.contains(h)){break}if(++e>1){var j=new Error('Element not interactable');j.code=15;throw j}d.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var l=m.createElement('INPUT');l.setAttribute('type','file');l.setAttribute('multiple','');l.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');l.onchange=function(q){l.parentElement.removeChild(l);q.stopPropagation();var r={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:l.files,setData:function u(){},getData:function o(){},clearData:function s(){},setDragImage:function i(){}};if(window.DataTransferItemList){r.items=Object.setPrototypeOf(Array.prototype.map.call(l.files,function(x){return{constructor:DataTransferItem,kind:'file',type:x.type,getAsFile:function v(){return x},getAsString:function y(A){var z=new FileReader();z.onload=function(B){A(B.target.result)};z.readAsText(x)},webkitGetAsEntry:function w(){return{constructor:FileSystemFileEntry,name:x.name,fullPath:'/'+x.name,isFile:true,isDirectory:false,file:function z(A){A(x)}}}}}),{constructor:DataTransferItemList,add:function t(){},clear:function p(){},remove:function n(){}})}['dragenter','dragover','drop'].forEach(function(v){var w=m.createEvent('DragEvent');w.initMouseEvent(v,true,true,m.defaultView,0,0,0,b,a,false,false,false,false,0,null);Object.setPrototypeOf(w,null);w.dataTransfer=r;Object.setPrototypeOf(w,DragEvent.prototype);h.dispatchEvent(w)})};m.documentElement.appendChild(l);l.getBoundingClientRect();return l"


def drop_files(element, files, offsetX=0, offsetY=0):
  driver = element.parent
  isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
  paths = []

  # ensure files are present, and upload to the remote server if session is remote
  for file in (files if isinstance(files, list) else [files]):
    if not os.path.isfile(file):
      raise FileNotFoundError(file)
    paths.append(file if isLocal else element._upload(file))

  value = '\n'.join(paths)
  elm_input = driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
  elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})


WebElement.drop_files = drop_files

# ==============================================================================

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
  driver.get("http://moodle.apsit.org.in/moodle/blog/edit.php?action=add")
  time.sleep(4)

  blog_title = driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[1]/div[2]/input[@id='id_subject']")
  blog_title[0].send_keys("uusername")
  blog_entry = driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div")
  blog_entry[0].send_keys("blog body")
  time.sleep(10)
  # place_to_add_files=driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[3]/div[2]/div/div[4]/div[1]/div[1]")
  place_to_add_files=driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[3]/div[2]/div/div[4]")
  file_path="C:/Users/ATHARVA/Downloads/test/test.txt"
  file_path_2="C:/Users/ATHARVA/Downloads/test/myfile1"
  pplc=place_to_add_files[0]
  print(pplc)
  print(pplc.get_attribute("class"))
  # ActionChains(driver).drag_and_drop(pplc, file_path).perform()
  pplc.drop_files(file_path_2)
  print("done")
  time.sleep(40)



moodle_scrapper("20102060", "20102060@Apsit")





#
# upload_file = driver.findElement(By.xpath("//input[@id='file_up']"));
#
# upload_file.sendKeys("C:/Users/Sonali/Desktop/upload.png");





