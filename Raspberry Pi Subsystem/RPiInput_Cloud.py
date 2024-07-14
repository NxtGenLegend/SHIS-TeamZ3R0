from urllib.request import HTTPPasswordMgrWithDefaultRealm
import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BCM)     
GPIO.setup(7, GPIO.IN) 
GPIO.setup(18, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(17, GPIO.IN) 
GPIO.setup(27, GPIO.IN)
GPIO.setup(23, GPIO.IN) 
GPIO.setup(13, GPIO.IN)

def input():
    ultra = GPIO.input(18)
    ldr = GPIO.input(7)
    sm = GPIO.input(16)
    humtem = GPIO.input(22)
    den = GPIO.input(17)
    pres = GPIO.input(27)
    aq = GPIO.input(23)
    cam = GPIO.input(13)