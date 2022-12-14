# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 13:43:04 2022

@author: thibo
"""

import wget
import time
import os
import datetime
from skimage.metrics import structural_similarity as compare_ssim
import cv2
import shutil 
#
url = 'http://192.168.1.221/jpg/image.jpg'
url_video = 'rtsp://admin:admin@192.168.1.221/video.mp4'
outputdirectory = '/home/pi/Securitycam/IpCamera/'
imageCapture = wget.download(url,outputdirectory)
videoLenght =5
imagePath = ""

def SafeImageCapture(url, outputdirectory):
    try:
        dayfolder = str(datetime.date.today().strftime('%Y-%m-%d'))                    #folder van de dag
        tempfolder = outputdirectory + dayfolder +"/"
        #print(tempfolder)
        print(os.path.exists(tempfolder))
        if not os.path.exists(tempfolder):
            path = os.path.join(tempfolder)
            os.mkdir(path)
            
        outputdirectory = tempfolder
        #print(outputdirectory)
        filename = wget.download(url, outputdirectory)                             #download image from ip camera
        current_time: str = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))   #create variable with current datetime
        #print(current_time)
        old_name = outputdirectory + "image.jpg"                 #name that has to get changed
        #nprint(old_name)
        new_name = outputdirectory + current_time + ".jpg"       #new name, that contains the datetime
        #print(new_name)
        os.rename(old_name, new_name)                                               #rename the image.jpg to the current datetime
       
        #print(datetime.date.today().strftime('%Y-%m-%d'))#wait a min
    except:
        print("fout")
    return new_name

def CheckImageChange(imageA, imageB):
    """ Inladen van de foto's: """
    imageA = cv2.imread(imageA)
    imageB = cv2.imread(imageB)
    
    """ Omzetten naar grijswaarden: """
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    
    """ Verschil berekenen: """
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    #print("SSIM: {}".format(score))
    
    if score < 0.9:
        return False
    else:
        return True


def RecordVideo(url_video, videoLenght):
    #Aanmaken directory:
    dayString = str(datetime.date.today().strftime('%Y_%m_%d'))                    #folder van de dag
    current_time: str = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    tempfolder = outputdirectory + dayString +'/'
    #print(tempfolder)
    print(os.path.exists(tempfolder))
    if not os.path.exists(tempfolder):
        path = os.path.join(tempfolder)
        os.mkdir(path)
    print("Recording:\n")
    print(dayString)
    print(tempfolder)
    # aanmaken videocapture object
    vid = cv2.VideoCapture(url_video) 
    print("checkvid")
    #VideoWriter object aanmaken
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(outputdirectory + current_time + ".mp4",fourcc, 20.0, (640,480))
    #starttijd vastleggen
    timeStart = time.perf_counter() 
    print("checktimestart")
    #gedurende periode van de videolengte blijft de camera filmen
    while(time.perf_counter() < timeStart + videoLenght): 
        ret, frame = vid.read()
        if ret == True: 
            # Frame wegschrijven
            out.write(frame) 
    # aangemaakte objecten vrijmaken
    vid.release() 
    out.release()
    print("Done Recording:\n")
    output = [outputdirectory, tempfolder, current_time + '.mp4']
    return output

def SafeVideo():
    print("check1")
    #specifying the destination folder 
    list_input = RecordVideo(url_video, videoLenght) 
    
    #specifying the source of the video file 
    src = list_input[0] + list_input[2]
    dst = list_input[1]
    video_name = list_input[2]
    print(list_input[0])
    print()
    print("check2")
    #copying the video file to the destination folder 
    shutil.copy(src, dst) 

    #confirming the file is in the folder 
    if os.path.exists(dst + video_name):
        print('File successfully moved to the destination folder.')
    else: print('Error moving file.') 
    
    print(list_input[0])    
    map_name = list_input[0] 
    file_name = list_input[2]

    os.remove(os.path.join(map_name, file_name))
    print("check3")
    
#SafeVideo()
while 1:
    last_image = SafeImageCapture(url, outputdirectory)
    time.sleep(5)
    new_image = SafeImageCapture(url, outputdirectory)
    try:
        if CheckImageChange(last_image, new_image):
            print("Er is geen verandering van beeld!\n")
        else: 
            print("Er is een verandering van beeld!\n")
            SafeVideo()
    except:
        print("Mooi geprobeert snoepertjes...\n")
    
    

