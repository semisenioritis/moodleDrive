# files that i have picked from:


# main
# filesuploadermult
# ------------------------

# Bugs that i need to fix
'''
  PRIORITY:
downloading system function
  in all available files download, do i also show author?
select if file is private or public
find a way to identify if all fies have been uploaded and only then download zip file
make a system to check if zip file is fully downloaded and only then unzip it
find an alternative to time.sleep for waiting until page loads
  "driver.implicit wait" apparently this waits for things to load and then proceeds after that
add metadata to blog body especially the number of file segments


  NOT SO IMPORTANT:
keeping browser minimized

  FUTURE SCOPE:
remember to add return None to all functions that dont return
remember to exit() all menus
remember to add a back option to menus?????
add encryption to files
how do i ensure that titles are unique? do i have to?
maybe write code to logout from the browser

  DONE:
make the zip file paths dynamic rather than hardcoding them
'''


# libraries
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement
import os.path
from zipfile import ZipFile
import shutil
# ------------------------

# Extra me not defined functions


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



# ------------------------

# Defined functions

def moodle_creds_checker(uusername, ppassword):
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
  invalid_tag= driver.find_elements(By.XPATH,"/html/body/div[2]/div/section/div/div/div/div[1]/div[1]/a")
  if len(invalid_tag)==0:
    print("Valid Credentials!\n")
  else:
    print("Invalid Credentials Genius. I mean smh '_'")
    exit()
  return None

def filesplitter(image_file, split_loc, finfilename):
  CHUNK_SIZE = 900000
  new_file_loc = split_loc + '/seg/' + finfilename + "____"
  filenum = 0
  with open(image_file, 'rb') as infile:
    while True:
      chunk = infile.read(CHUNK_SIZE)
      if not chunk: break
      filenum = filenum + 1
      tempfileloc = new_file_loc + str(filenum)
      tempfile = open(tempfileloc, 'wb')
      tempfile.write(chunk)
      tempfile.close()
  infile.close()
  return filenum

def filecleaner(segloc,resloc,temploc):
  print(segloc,"\n",resloc,"\n",temploc)
  shutil.rmtree(segloc)
  shutil.rmtree(resloc)
  shutil.rmtree(temploc)

def filemerger(oldfiletitle, no_of_files, segpath):
  old_file=oldfiletitle
  new_file=oldfiletitle.split("----")[0]

  new_file= "\\res\\"+ new_file
  currentcodepath = os.getcwd()
  new_file= currentcodepath+ new_file
  a=open(new_file, 'wb')
  a.close()
  extension=oldfiletitle.split("----")[1].split("____")[0]
  n=no_of_files
  for i in range(n):
    segfile=segpath+old_file+str(i+1)
    with open(segfile, 'rb') as fromfile:
      chunk = fromfile.read()
      finfile = open(new_file, 'ab')
      finfile.write(chunk)
  new_name = new_file+"."+extension
  finfile.close()
  os.rename(new_file, new_name)

#    convert the file back into the given og file type
#   os.remove(segpath)
#    delete old sectioned binary files

  os.startfile(new_name, 'open')

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
  blog_title[0].send_keys(finfilename)
  blog_entry = driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div")
  blog_entry[0].send_keys("blog body")

  place_to_add_files=driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[3]/div[2]/div/div[4]")
  pplc=place_to_add_files[0]
  basefilepath=os.getcwd()+"\\seg\\"

  for i in range(int(no_of_files)):
    file_path=basefilepath+finfilename+"____"+str(i+1)
    pplc.drop_files(file_path)
    time.sleep(0.3)
  # select the access here. Is public or private

  time.sleep(20)

  # write code to check if all files have been uploaded correctly and proceed only when done

  download_all_button_list = driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/section/div/form/fieldset[1]/div/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[3]/a")
  download_all_button=download_all_button_list[0]
  download_all_button.click()
  time.sleep(15)
  # write better code to wait unitl the zip file has been downloaded (write it modularly so that you can call the same function again later in the actual downloading part)
  # click on the download all button
  zippfile=os.getcwd()+"\\temp\\Files.zip"
  zipploc=os.getcwd()+"\\temp\\"
  with ZipFile(zippfile, 'r') as zObject:
    zObject.extractall(path=zipploc)
  #     the issue of the path here is that the path is not dynamic. pls make sure u solve that.
  # unzip file
  os.remove(zippfile)
  #     again the path is not dynamic. pls solve this when u are not dead
  # delete the zip file
  oldfiletitle=finfilename+"____"
  filemerger(oldfiletitle, no_of_files, zipploc)

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

def upload_file(uusername, ppassword):
  fileloc=input("Please enter the correct path of the file.(no slashes at start in colab)\n\n")
  title=input("Please enter the title of the file.\n\n")
  access=input("Please enter if the file should be Public or Private: \n\n1.Public \n2.Private\n")
  if access== str(1):
    print("Public\n")
  elif access== str(2):
    print("Private\n")
  else:
    print("Invalid input\n")
    upload_file()
    exit()
  extension=str(fileloc.split(".")[-1])
  finfilename=title+"----"+extension
  currentcodepath= os.getcwd()
  segloc=currentcodepath+"\\seg"
  os.mkdir(segloc)
  temploc = currentcodepath + "\\temp"
  os.mkdir(temploc)
  no_of_files=filesplitter(fileloc, currentcodepath, finfilename)
  resloc=currentcodepath+"\\res"
  os.mkdir(resloc)
  moodle_uploader(uusername, ppassword, no_of_files, finfilename, access)
  #   uppload


  #   redouwnload and compile and check
  #   if workss proceed if not repeat

  filecleaner(segloc,resloc,temploc)
  # if works delete entire seg folder adn recompiled new file
  print("Successfully Uploaded File to MoodleDrive!")
  #   if it is a public file, get the link to the file
  # say success

def exit_app(uusername, ppasword):
  answer=input("Are you sure? (y/n)")
  if answer==("y" or "Y"):
    # write the code to logout from the browser or just close everything so that it is deleted
    exit()
  elif answer==("n" or "N"):
    next_action(uusername, ppassword)
  else:
    print("Decide Shell-for-brains!")
    exit_app(uusername,ppassword)
  exit()

def next_action(uusername, ppassword):
  action = input('These are the available options:\n 0.    Upload\n 1.    Download\n 2.    Exit\n')

  if action == "0":
    upload_file(uusername, ppassword)

  elif action == "1":
    # download_file()
    exit()
  elif action == "2":
    exit_app(uusername,ppassword)

  elif action != "0" or "1" or "2":
    print("Invalid input\n\n\n")
    next_action(uusername,ppassword)
    exit()


# -------------------------


# Flow of calling fucntions


uusername= input('Enter username:\n')

ppassword= input('Enter password:\n')

moodle_creds_checker(uusername, ppassword)

next_action(uusername, ppassword)