#!/bin/bash
### BEGIN INIT INFO
# Provides:	     startCheck.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon to system check
# Description:	     Enable service provided by daemon.
### END INIT INFO

#Upper code is for systemd auto start script You can Ignore code or if you want to use systemd use upper code

# Define Variable
shdir="/home/pi/ICT" # define script file location
sense="$shdir/check/usingSense.py" # temperature and humidity check python file
camera="$shdir/check/CameraTest.sh" # camera test script
date=$(date '+%y-%m-%d') # return year-month-day
date2=$(date '+%y-%m-%d %H:%M:%S') # return hour:minuite:second
dir="$shdir/$date" # define drectory named $date 
log="$date.log" # log file include sensehat.sh and cameratest.sh's result 
logdir="$dir/$log" # define log file location

# Define CCTV excute Program location 
cctv="$shdir/check/StartCCTV.sh"

# Wait 30 second to connect internets
echo "Wait to check time..."
#sleep 30

# Time Zone Resetting (Default Setting is UTC+09)
# If you want to change other time zone, please check https://support.ntp.org/Servers/NTPPoolServers
#sudo timedatectl set-timezone Asia/Seoul
sudo ntpdate -u 3 kr.pool.ntp.org

# Upload Camera Driver to pi camera. (to use pi camera as usb camera)
sudo modprobe bcm2835-v4l2

# Find or create log file and default record file location
if [ ! -d $dir ]; then
    echo "$date Folder Doesn't exist Creating..."
    mkdir $dir
    touch $logdir
else
    echo "$date Folder exist"
    touch $logdir
fi

# Check Temperature and Humidity using SenseHat
# If you don't want to use this function or you don't have sensehat, You can comment below line to python3~
# Check python file exist
if [ ! -f $sense ]; then
    echo "[$date2] Unable Temperature and Humidity Test" | tee -a $logdir
    echo "[$date2] Please Check Python File at $sense" | tee -a $logdir
    exit 1
fi
# Execute Temperature and Humidity check python file
python3 $sense | tee -a $logdir 

# Check Pi camera and webcam Test Script
if [ ! -f $camera ]; then
    echo "[$date2] Unable Camera Test" | tee -a  $logdir
    echo "[$date2] Please Check Script File at $camera" | tee -a $logdir
    exit 1 
fi
# Execute camera check script
bash $camera | tee -a $logdir 

# Check CCTV script is exist

if [ ! -f $cctv ]; then
    echo "[$date2] Unable to find CCTV Execute Program Location" | tee -a $cctv
    echo "[$date2] Please Check Script File at $cctv" | tee -a $cctv
    open $shdir
    exit 1
fi
# Execute CCTV script
bash $cctv | tee -a $logdir 

#sleep 5
