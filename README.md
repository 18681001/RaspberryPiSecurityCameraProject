# Motion and Object Detection Recording Security Camera Project Using Raspberry Pi 3

** This Page Is Imcomplete **

Please Don't Ask Me Because, I'm so busy to fix the problem both README.md and Project.

This Project is delevloped Recording the boxes' movement and surrounded Object to record the Video Using Raspberry Pi 3.
It record videos using Pi Camera and Webcam.
Pi Camera is Record when Object is Detected, and Webcam is Record When Motion is Detected.
So. It Required OPenCV and TensorFlow Lite.
It also checking Temperature and Humidity to Inform You The Area's Envirement is safe or bad to using.

## Before You Start

This Project was delevoped for below hardware systems.

- Raspberry Pi 3 model b
- 64GB Micro SD Card
- SenseHat V1
- Pi Camera V1
- Compatible USB Webcam

It requires Legacy Camera Option to use Picamera at OpenCV so Please use Raspberry Pi OS Legacy (BullsEye).

It also requires SenseHat V1 to check Temperature and Humidity.
But If you don't want using this function or If you don't have SenseHat, Please Comment Processing Below Line at startCheck.sh

```bash

if [ ! -f $sense ]; then
    echo "[$date2] Unable Temperature and Humidity Test" | tee -a $logdir
    echo "[$date2] Please Check Python File at $sense" | tee -a $logdir
    exit 1
fi
# Execute Temperature and Humidity check python file
python3 $sense | tee -a $logdir 

```

## Installation

1. Please write this commend at LXTerminal 
```bash
git clone https://github.com/18681001/RaspberryPiSecurityCameraProject.git
```
2. Please Run PLEASERUNFIRST.sh using Terminal to install and setting the auto start system.

```bash
cd RaspberryPiSecurityCameraProject/ICT
bash PLEASERUNFIRST.sh
```

If you don't want using this script files. Please install software written at PLEASERUNFIRST.sh.

The Requirements Opencv and TensorFlow Lite version is:
- OpenCV (opencv-python): 4.5.3.56
- TF Lite Support: 0.4.3
- TF Lite Runtime: 2.11.0

3. If PLEASERUNFIRST.sh is suspended, Please Set Legacy Camera Option using raspi-config

```bash
sudo raspi-config
```
- 3. Interface Option > I1 Legacy Camera > Yes

4. And, It also recommend Extention of Video Memory and swap size.
Please Extened Video Memory 256MB.

```bash
sudo raspi-config
```

- 4. Performance Option > P2 GPU Memory > 256

5. And Please Set Swap Size to 2048MB

```bash
sudo service dphys-swapfile stop # Suspend Swap Service
sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=128 to CONF_SWAPSIZE=2048
sudo service dphys-swapfile start # Start Swap Service
```
6. If This Setting is Complete, please change script file permission.
```bash
sudo chmod 755 check/startCheck.sh
```
   
7. All Done. Please Reboot System. It Start Autoimatically.


## Based Code

<a href="https://hyongdoc.tistory.com/410">[Motion Detect]

<a href="https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi">[Object Detect (TFLite Example)]
