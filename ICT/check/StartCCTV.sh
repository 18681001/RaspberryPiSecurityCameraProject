#!/bin/bash

# Define Variable

location="/home/pi/ICT/raspberry-pi" # python files' location
date2=$(date '+%y-%m-%d %H:%M:%S') # Time Data for logging

video1py="motiondetectrec.py" ## object detection code
video0py="objectdetect.py" ## motion detection code 

tflite="efficientdet_lite0.tflite" ## model file for tensorflow lite

startsh="setup.sh" ## model download script file (Internet connection Required)

if [ ! -d $location ]; then
    echo "[$date2] CCTV Script Directory Doesn't Exist. Please check $location"
    exit 1
else
    echo "[$date2] $location exist. Move to $location"
    cd $location
fi    

if [ -f $tflite ] && [ -f $startsh ]; then
    echo "[$date2] Data model exist. Continuing..."
elif [ ! -f $tflite ] && [ -f $startsh ]; then
    echo "[$date2] Data model doesn't exist. Start $startsh."
    sudo chmod 755 $startsh
    bash $startsh

else #  $startsh doesn't exist
    read -p "[$date2] Can't Find $startsh. Do you want to download It via internet? (y/n)" yn
    case $yn in
	[Yy]* ) git clone https://github.com/tensorflow/examples
            echo "Download Complete. Copy $startsh to $location and Start $startsh"
	        cp ./examples/lite/examples/object_detection/raspberry_pi/$startsh ./$startsh
            cp ./examples/lite/examples/object_detection/raspberry_pi/requirements.txt ./requirements.txt
            sudo rm -R ./examples
	    sudo chmod 755 $startsh	
            bash $startsh
            # if you don't want to use improve model, you can delete file using below line
            #sudo rm efficientdet_lite0_edgetpu.tflite
	    echo "[$date2] Complete Downloading Model Files. Reboot now... (Ctrl + C to quit)"
	    sleep 10;
	    sudo shutdown -r now
            ;;
	[Nn]* ) "[$date2] $startsh Doesn't exist. Please download files at https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi "
            exit 1 ;;
    esac
    exit 1
fi

if [ ! -f $video1py ] || [ ! -f $video0py ]; then
    echo "[$date2] Files ($video1py , $video0py) doesn't Exist. Please check files at $location"
    exit 1
else
    echo "[$date2] Start CCTV Program..."
    python3 $video1py | tee -a $logdir
fi
