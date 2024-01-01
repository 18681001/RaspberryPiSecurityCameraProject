#!/usr/bin/python3

from sense_hat import SenseHat
import datetime

sense = SenseHat()
sense.clear

Temp = sense.get_temperature()
Humi = sense.get_humidity()
temp2 = int(Temp)
humi2 = int(Humi)
print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Checking Temperature and Humidity")

print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Temperature in this area: " + str(temp2) + ".C") 
print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Humidity in this area: "+ str(humi2) + "%")

if (temp2 > 29 or temp2 < 1):
    print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Temperture in this area might occurs problem." + str(temp2) + ".C")
    print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Make sure this system works innormally")
else:
    print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] OK. All system's are good")


