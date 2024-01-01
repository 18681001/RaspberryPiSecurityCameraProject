#!/bin/bash

# Define Directory to save temp.jpg
tempdir="/home/pi/ICT/temp"
# Define temp.jpg the result of fswebcam
temp="/home/pi/ICT/temp/temp.jpg"

#https://inhwangjeong.tistory.com/m/43
# Return time data to logging
date=$(date '+%y-%m-%d %H:%M:%S')

# Check temp directory is exist
if [ ! -d $tempdir ]; then
    sudo mkdir $tempdir
    sudo chmod -R 777 $tempdir
else
    echo ""
fi

# Check Pi Camera
echo "[$date] fswebcam video0 test Start."

#Default Device of /dev/video0 is usb webcam but driver is loaded at pi camera, /dev/video0 is pi camera
fswebcam -d /dev/video0 -r 640*480 $temp 2> /dev/null 

# find temp.jpg if temp.jpg doesn't exist, reboot after 10 second.
if [ -e $temp ]; then
    echo "[$date] fswebcam video0 activate successful"
    rm $temp
else
    echo "[$date] fswebcam video0 didn't activate. Please Check Raspi's Camera." 
    echo "[$date] System will be restart in 10 seconds. (Ctrl + C to quit)"
    sleep 10
    sudo shutdown -r now
fi

echo "[$date] fswebcam video1 test start"

# Check Webcam
#Default Device is /dev/video0 but usb webcam is defined /dev/video1 because of pi camera
fswebcam -d /dev/video1 -r 640*480 $temp 2> /dev/null 

# find temp.jpg if temp.jpg doesn't exist, reboot after 10 second.
if [ -e $temp ]; then
    echo "[$date] fswebcam video1 activation successful"
    rm $temp
else
    echo "[$date] fswebcam didn't activate. Please Check USB Webcam Again."
    echo "[$date] System will be restart in 10 seconds. (Ctrl + C to quit)"
    sleep 10
    sudo shutdown -r now
fi
# If Two Camera Work Normally
echo "[$date] It seems both camera worked normally."
