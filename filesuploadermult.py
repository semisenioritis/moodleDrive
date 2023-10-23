import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import os.path
from zipfile import ZipFile


chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : 'C:\\Users\\ATHARVA\\PycharmProjects\\moodleDrive\\temp\\'}
chrome_options.add_experimental_option('prefs', prefs)


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



def moodle_uploader(uusername, ppassword, no_of_files, finfilename,access):
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
  time.sleep(4)
  # try catch here if page has loaded and provide option to redo the process
  driver.get("http://moodle.apsit.org.in/moodle/blog/edit.php?action=add")
  time.sleep(4)
  blog_title = driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[1]/div[2]/input[@id='id_subject']")
  blog_title[0].send_keys("uusername")
  blog_entry = driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div")
  blog_entry[0].send_keys("blog body")
  time.sleep(10)
  place_to_add_files=driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[3]/div[2]/div/div[4]")
  pplc=place_to_add_files[0]
  basefilepath=os.getcwd()+"/seg"

  for i in range(int(no_of_files)):
    file_path=basefilepath+finfilename+"____"+str(i+1)
    pplc.drop_files(file_path)
  # select the access here. Is public or private




  download_all_button_list = driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[3]/a")
  download_all_button=download_all_button_list[0]
  download_all_button.click()
  # click on the download all button
  with ZipFile("C:\\Users\\ATHARVA\\PycharmProjects\\moodleDrive\\temp\\Files.zip", 'r') as zObject:
    zObject.extractall(path="C:\\Users\\ATHARVA\\PycharmProjects\\moodleDrive\\temp")
  #     the issue of the path here is that the path is not dynamic. pls make sure u solve that.
  # unzip file
  os.remove("C:\\Users\\ATHARVA\\PycharmProjects\\moodleDrive\\temp\\Files.zip")
  #     again the path is not dynamic. pls solve this when u are not dead
  # delete the zip file
  oldfiletitle=finfilename+"____"
  filemerger(oldfiletitle, no_of_files, "C:\\Users\\ATHARVA\\PycharmProjects\\moodleDrive\\temp")

  # compile all files into master file
  # open master file

  ans = input('Is the file opening? (y/n)\n')
  if ans==("y" or "Y"):
    submit_button = driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[3]/div/div[1]/div/input[1]")
    submit_button[0].click()
    time.sleep(4)
  elif ans==("n" or "N"):
    print("Please restart the process")
    exit()
  # if master file is satisfactory proceed else reupload




moodle_uploader("20102060", "20102060@Apsit",21,"myfiledone",1)
