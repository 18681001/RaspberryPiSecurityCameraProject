#!/bin/bash

autostart="/etc/xdg/lxsession/LXDE-pi/autostart"
autostart2="/etc/modules"
startsh="@lxterminal --command=/home/pi/RaspberryPiSecurityCameraProject/ICT/check/startCheck.sh"
raspiconfig="readMeRaspiconfig.txt"


echo "This Project is targeted for Raspbery Pi 3 B, Raspberry Pi OS Legacy."

echo "Execute update and upgrade."

# Checking Package's Update 

sudo apt-get update
sudo apt-get -y upgrade

# Install for System Checking

echo "Install Package for System Checking"

sudo apt-get install -y sense-hat
sudo apt-get install -y fswebcam
sudo apt-get install -y ntpdate

# Install Package For OpenCV

echo "Install Package for OpenCV"

sudo apt-get -y install build-essential cmake

sudo apt-get -y install libjpeg-dev libtiff5-dev libpng-dev

sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libxine2-dev

sudo apt-get -y install libv4l-dev v4l-utils

sudo apt-get -y install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly

sudo apt-get -y install libgtk-3-dev

sudo apt-get -y install libatlas-base-dev gfortran libeigen3-dev

sudo apt-get -y install python3-dev python3-numpy

sudo apt-get -y install libjasper-dev libpng12-dev

sudo apt-get -y install qt4-dev-tools

# Install opencv and tf_lite

echo "Install OpenCV and TensorFlow Lite"

# opencv version is recommend 4.5.3.56
# If you want to build opencv yourself or installing later, please ㅊheck this link comment processing below code.
sudo pip3 install opencv-python=="4.5.3.56"
sudo pip3 install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp39-cp39-linux_armv7l.whl
sudo python3 -m pip install tflite-support=="0.4.3"
sudo python3 -m pip install tflite-runtime=="2.11.0"

# To prevent cv2 error install libopenblas
sudo apt-get install -y libopenblas-base

#
# add auto start sctipt
echo "Add below command at $autostart"
echo "$startsh" | sudo tee -a $autostart

# add import pi camera driver when booting
echo "Add below command at $autostart2"
echo "bcm2835-v4l2" | sudo tee -a $autostart2

echo "Please Enable Legacy Camera and Change Grapic Memory to 256MB at raspi-config" | sudo tee -a $raspiconfig
echo "Open LxTerminal > sudo raspi-config > 3. Interface Option > I1 Legacy Camera > Yes" | sudo tee -a $raspiconfig
echo "Open LxTerminal > sudo raspi-config > 4. Performance Option > P2 GPU Memory > 256" | sudo tee -a $raspiconfig
sleep 15
echo "This Project Recommend Use Swap Memory 2GB" | sudo tee -a $raspiconfig
echo "First, Please Stop Sawp service : sudo service dphys-swapfile stop" | sudo tee -a $raspiconfig
echo "Please Open vi / nano / emacs at : /etc/dphys-swapfile" | sudo tee -a $raspiconfig
echo "And Change CONF_SWAPSIZE=128 to CONF_SWAPSIZE=2048" | sudo tee -a $raspiconfig
sleep 30
echo "If you change the setting, Please Start Swap service : sudo service dphys-swapfile start" | sudo tee -a $raspiconfig
echo "All Done. For The System stability, Please Reboot System."
echo "Setting Guide is saved at $raspiconfig"
sleep 30
