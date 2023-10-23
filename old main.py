import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

# remember to add return None to all functions that dont return
# remember to exit() all menus
# remember to add a back option to menus?????
# add encryption to files


uusername= input('Enter username:\n')

ppassword= input('Enter password:\n')


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
    print("Valid Credentials!")
  else:
    print("Invalid Credentials Genius. I mean smh '_'")
  return None


def next_action():
  action = input('These are the available options:\n 0.    Upload\n 1.    Download\n 2.    Exit\n')

  if action == "0":
    upload_file()

  elif action == "1":
    download_file()

  elif action == "2":
    exit_app()

  elif action != "0" or "1" or "2":
    print("Invalid input\n\n\n")
    next_action()
    exit()




def upload_file():
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
  segloc=currentcodepath+"/seg"
  os.mkdir(segloc)
  temploc = currentcodepath + "/temp"
  os.mkdir(temploc)
  no_of_files=filesplitter(fileloc, currentcodepath, finfilename)

  moodle_uploader(uusername, ppassword, no_of_files, finfilename, access)
  #   uppload
  resloc=currentcodepath+"/res"


  #   redouwnload and compile and check
  #   if workss proceed if not repeat

  filecleaner(segloc,resloc,temploc)
  # if works delete entire seg folder adn recompiled new file
  print("Successfully Uploaded File to MoodleDrive!")
  #   if it is a public file, get the link to the file
  # say success



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
  os.remove(segloc)
  os.remove(resloc)
  os.remove(temploc)

def exit_app():
  answer=input("Are you sure? (y/n)")
  if answer==("y" or "Y"):
    # write the code to logout from the browser or just close everything so that it is deleted
    exit()
  elif answer==("n" or "N"):
    next_action()
  else:
    print("Decide Shell-for-brains!")
    exit_app()
  exit()


def download_file():
  action=input("Is the file you want to download from your own Drive or someone else's?\n 1. Mine\n 2. Others'\n")
  if action == "1":



  elif action == "2":
    # take in the url to their shared url


  elif action != "1" or "2":
    print("Invalid input\n\n\n")
    download_file()
    exit()


# if download:

#    show all possible files available with index number beside them (if index number is 0 show title in list )

#    if a valid index number is entered, download all files with the given title:

#    compile the files into single binary file
def filemerger(oldfiletitle, no_of_files, segpath):
  old_file=oldfiletitle
  new_file=oldfiletitle.split("----")[0]
  new_file= "res/"+ new_file
  extension=oldfiletitle.split("----")[1].split("____")[0]
  currentcodepath = os.getcwd()
  new_file= currentcodepath+ new_file
  n=no_of_files
  for i in range(n):
    segfile=segpath+old_file+str(i+1)
    with open(segfile, 'rb') as fromfile:
      chunk = fromfile.read()
      finfile = open(new_file, 'ab')
      finfile.write(chunk)
  new_name = new_file+"."+extension
  os.rename(new_file, new_name)

#    convert the file back into the given og file type
  os.remove(segpath)
#    delete old sectioned binary files

  os.startfile(new_name, 'open')
#    auto open compiled file in default app


#write another fn to find howmany files there are to merge
