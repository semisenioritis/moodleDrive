


def filemerger(filetitle, no_of_files):
  new_file="filetitle"
  # gotta work on this too


  n=int(no_of_files)
  for i in range(n):
    segfile="seg/"+filetitle+str(i+1)
    with open(segfile, 'rb') as fromfile:
      chunk = fromfile.read()
      finfile = open(new_file, 'ab')
      finfile.write(chunk)

filemerger("myfiledone____","21")

def filesplitter(image_file, split_loc, finfilename):
  CHUNK_SIZE = 900000
  new_file_loc = split_loc + '/seg/myfile' + finfilename + "____"
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
  return None


filesplitter("C:/Users/ATHARVA/PycharmProjects/moodleDrive/OJT06449.JPG","C:/Users/ATHARVA/PycharmProjects/moodleDrive", "done")