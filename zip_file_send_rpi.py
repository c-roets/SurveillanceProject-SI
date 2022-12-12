#Code created by Group 4 from practica Smart Instrumentation Ghent University

import os
import zipfile
from zipfile import ZipFile
import time
import datetime
import shutil
import paramiko

def zipzipfile(directory_to_zip, zip_filename):
  # create a ZipFile object
  zip_file = zipfile.ZipFile(zip_filename, 'w')
  print(f"Zip file created with zip_filename {zip_filename}")

  # walk through the directory and add all the files to the zip file
  for root, directories, files in os.walk(directory_to_zip):
      for filename in files:
          # create the full filepath by joining the root directory and the filename
          filepath = os.path.join(root, filename)
          # add the file to the zip file
          zip_file.write(filepath)
  
  # close the zip file
  zip_file.close()
  
  print("Zip file filling finished")

def send_file(ip, username, password, localpath, remotepath):
  # Set connection
  print("connection is being set")
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  # Connect to receiver
  ssh.connect(ip, username=username, password=password)
  sftp = ssh.open_sftp()

  # Send file
  print("file is being send")
  sftp.put(localpath, remotepath)

  # Close connection
  sftp.close()
  ssh.close()
  
  print("Transfer succesful")

def remove_file(localpath):
  # Check path existens, remove zip file from sender
  print("file is being removed")
  if os.path.exists(localpath):
    os.remove(localpath)
  print("file is removed succesfully")

# directory to zip
directory_to_zip = '/home/pi/Motionpicam'

# Ontvanger parameters
ip = '192.168.1.102'
username = 'pi'
password = 'raspberry'

# Mic variables
folder_path = '/home/pi/Motionpicam'

files = os.listdir(folder_path)
num_files = len(files)
sent_today = False

while True:
    #print('ik zit in de while true loop')
    # get current time and day
    now = datetime.datetime.now()
    today = datetime.datetime.today()
    current_time = now.strftime("%H-%M-%S")
    current_hour = now.strftime("%H")
    #print(current_hour)
    current_min = now.strftime("%M")
    #print(current_min)
    current_day = now.strftime("%d-%m-%Y")
    
    if int(current_hour) == 16 and int(current_min) == 14:
        sent_today = False

    # check if it is midnight
    #print("If-statement controleren")
    if int(current_hour) == 16 and int(current_min) == 53 and sent_today == False:
      sent_today = True
      
      print("If-statement is correct")  
      # remove one day from current date
      current = today - datetime.timedelta(days=1)
      current_day = current.strftime("%d-%m-%Y")

      # zip_filename
      zip_filename = f'{current_day}.zip'

      # Pad ophalen/zenden
      localpath = rf"/home/pi/Desktop/{zip_filename}"
      remotepath = rf"/home/pi/CameraZips/{zip_filename}"

      # zip the file from yesterday
      zipzipfile(directory_to_zip, zip_filename)

      # send file just created
      send_file(ip, username, password, localpath, remotepath)

      #remove file from sender
      remove_file(localpath)
      
      #bestanden uit map verwijderen
      for bestandnaam in os.listdir('/home/pi/Motionpicam'):
          file_pad = os.path.join('/home/pi/Motionpicam', bestandnaam)
          try:
              if os.path.isfile(file_pad) or os.path.islink(file_pad):
                  os.unlink(file_pad)
          except Exceptions as e:
              print("Fout bij verwijderen")
    
    
    # Mic
    files = os.listdir(folder_path)
    num_files_now = len(files)
    
    if num_files_now > num_files:
        current_time = str(datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S"))
        os.system(f"arecord -D 'plughw:2,0' -f S16_LE -r 16000 -d 5 -t wav /home/pi/Motionpicam/{current_time}.wav")
        time.sleep(15)
        num_files = num_files_now
    