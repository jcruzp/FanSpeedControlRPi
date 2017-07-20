#!/usr/bin/env python3
# Author: Jose Cruz
# Original Code: Andreas Spiess
import os
import time
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO


fanPin = 17 # The pin ID, edit here to change it

desiredTemp = 44 # The maximum temperature in Celsius after which we trigger the fan

fanSpeed=100
sum=0
pTemp=15
iTemp=0.4

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    #print("temp is {0}".format(temp)) #Uncomment here for testing
    return temp
def fanOFF():
    myPWM.ChangeDutyCycle(0)   # switch fan off
    return()
def handleFan():
    global fanSpeed,sum
    actualTemp = float(getCPUtemperature())
    diff=actualTemp-desiredTemp
    sum=sum+diff
    pDiff=diff*pTemp
    iDiff=sum*iTemp
    fanSpeed=pDiff +iDiff
    if fanSpeed>100:
        fanSpeed=100
    if fanSpeed<15:
        fanSpeed=0
    if sum>100:
        sum=100
    if sum<-100:
        sum=-100
    #print("actualTemp %4.2f TempDiff %4.2f pDiff %4.2f iDiff %4.2f fanSpeed %5d" % (actualTemp,diff,pDiff,iDiff,fanSpeed))
    myPWM.ChangeDutyCycle(fanSpeed)
    return()
try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fanPin, GPIO.OUT)
    myPWM=GPIO.PWM(fanPin,50)
    myPWM.start(50)
    fanOFF()
    while True:
        handleFan()
        sleep(1) # Read the temperature every 5 sec, increase or decrease this limit if you want 
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt 
    fanOFF()
    GPIO.cleanup() # resets all GPIO ports used by this program
