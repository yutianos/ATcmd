#!/usr/bin/env python3.5

import serial
import os
import time


class A6handle:

    def __init__(self,com):
        self.com = com
        pass
    def sendcmd(self,cmd):
	cmd +='\r\n'
        self.com.write(cmd.encode())
		
    def getres(self,data):
	while True :
	    res = ''
	    breakflag = 0
	    time.sleep(0.4)
	    while self.com.in_waiting:
		breakflag = 1
		res += self.com.read().decode()
			
	    if breakflag :
			
	    print(res)
	    break;

def cp2102_open(device="/dev/ttyUSB0"):
    return serial.Serial(device,115200)				

handle = A6handle(cp2102_open())
while True :

    cmd = input(>>)
    handle.sendcmd(cmd)
    getres()
			
			









