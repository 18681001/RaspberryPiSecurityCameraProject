from configparser import ExtendedInterpolation
import cv2
import os
import datetime
import sys
import numpy as np
#import detect1 as dt
import subprocess

# Based Code: https://hyongdoc.tistory.com/410

# Define Variables
# Define Time Data to access Default Directory

# return Years-Months-Days
dateday = datetime.datetime.now().strftime('%y-%m-%d') 
# return Years-Months-Days_Hours:Minutes:Seconds to define file name
datenow = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S') 

#Set Video File Property
# User Defined Saving video location
# Please change your-directory-name to your real External Device
# You can check name using LXTerminal opening at External Device
dirloc = '/media/your-directory-name/' + dateday 

# if you want to make directory automatically please use below codes.
# if not os.path.exist(dirloc):
#   os.makedir(dirloc)
# else
#   print("Directory Already Exist or Invalid Directory")

#Check Pi camera is usable # Using GPT
def initialize_camera():
    # Add error handling
    #Pi camera's location id /dev/video0, Webcam Location is /dev/video1
    capture = cv2.VideoCapture(1) 
    if not capture.isOpened():
        print("Camera Device Didn't active!")
        sys.exit()
    return capture
capture = initialize_camera() 

# Define Codec (default Setting is XVID)
fourcc = cv2.VideoWriter_fourcc(*'XVID') 

# Change Default Directory thay defined directory isn't exist
if not os.path.exists(dirloc):
    print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Defined Directory doesn't exist at " + dirloc)
    dirloc = '/home/pi/RaspberryPiSecurityCameraProject/ICT/' + dateday #Video save location
    if not os.path.exists(dirloc):
        print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Create Default Directory at " + dirloc)
        os.makedirs(dirloc)
    else:
        print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Default Directory " + dirloc + " exists.")
    
# video0 device activation script location
picam_script_path = 'objectdetect.py'

#That Code #1
#Define row value (default is 640)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# Define height value (default is 480)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
# Define valur to record the video
video_record = False
# Define Threshhold to ignore camera noises
thresh = 25
# define max difference to motion detect
max_diff = 5 

# Define Three Frames to compare images
frame_a, frame_b, frame_c = None, None, None 

# Define with and height values to record the video
width = int(capture.get(3))
height = int(capture.get(4))

# Define file extension (default Setting is avi)
ext = "avi"

#Define Video Files Saving Location 
videofileloc = os.path.join(dirloc, f"motion_{datenow}.{ext}")

# Define File save type
out = cv2.VideoWriter(videofileloc, fourcc, 15.0, (width,height))

# main code
if capture.isOpened():
    ret, frame_a = capture.read()
    ret, frame_b = capture.read()

    while ret:
        # define draw to show and record script
        ret, frame_c = capture.read()
        draw = frame_c.copy() # 영상 저장 시 c와 관련된 것들을 저장할것

        if not ret:
            print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Error Occured while capture the frame")
            break
        
        # Define GrayScale frame
        frame_a_gray = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
        frame_b_gray = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
        frame_c_gray = cv2.cvtColor(frame_c, cv2.COLOR_BGR2GRAY) 

        # Define binary operation
        diff1 = cv2.absdiff(frame_a_gray, frame_b_gray)
        diff2 = cv2.absdiff(frame_b_gray, frame_c_gray) 

        # Convert GrayScale frame to binarization
        ret, diff1_t = cv2.threshold(diff1, thresh, 255, cv2.THRESH_BINARY)
        ret, diff2_t = cv2.threshold(diff2, thresh, 255, cv2.THRESH_BINARY) 

        # Calculatinh bitwise
        diff = cv2.bitwise_and(diff1_t, diff2_t) 

        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k) 
        
        # Draw Time data with Yellow color 
        cv2.putText(draw, datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S'), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 255))
        # Draw device name with yellow text
        cv2.putText(draw, 'webcam', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255)) 

        # Define diff_cnt to compare GrayScale Value and max_diff
        diff_cnt = cv2.countNonZero(diff)
        # if motion is detected
        if diff_cnt > max_diff: 
            datenow
            nzero = np.nonzero(diff) # nzero: diff size is same as Camera's Frame, It mean difference of frame_a and frame_b.
            # make square frame
            cv2.rectangle(draw, (min(nzero[1]), min(nzero[0])),(max(nzero[1]), max(nzero[0])), (0, 255, 0), 2)
            # Draw "Motion Detected!!"
            cv2.putText(draw, "Motion Detected!!", (10, 90), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0)) 
            video_record = True
            # Execute object detection python file using subprocess
            if not 'picam_process' in locals():
                print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Executing picam record")
                picam_process = subprocess.Popen(['python3', picam_script_path])
            # If motion detection accured again, ignor it.
            elif 'picam_process' in locals():
                pass
            
        # Video Recording
        if video_record:
            # Add Recording Code
            cv2.putText(draw, "Start Recording...", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0)) 
            out.write(draw)
            
        # Stopped the recording When Motion is not Detected
        if diff_cnt <= max_diff:
            datenow
            cv2.putText(draw, "Record Stopped!", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255)) # Show Record Stop text
            video_record = False

        
        stacked = np.hstack((draw, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR))) 
        cv2.imshow('webcam "Press Esc to EXIT!"', draw) 
        frame_a = frame_b
        frame_b = frame_c
        # Press 'esc' to exit
        if cv2.waitKey(1) & 0xFF == 27: 
            print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Motion Detect Record System Terminating...")
            break

# Release Resource
capture.release() # release capture's memory
out.release() # release filesystem's memory
picam_process.kill()
cv2.destroyAllWindows()
