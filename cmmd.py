#!/usr/bin/env python3.5

import serial
import os
import time

class A6handle:
    
    def __init__(self,com):
        self.com = com

    def sendcmd(self,cmd):
        cmd +='\r\n'
        self.com.write(cmd.encode())

    def getres(self):
        while True:
            res = ''
            list = []
            breakflag = 0
            time.sleep(0.4)
            #while self.com.in_waiting:
            if self.com.in_waiting :
                breakflag = 1
                try:
                    res = self.com.read(self.com.in_waiting)
                    list.append(self.com.read(self.com.in_waiting).decode())
                except UnicodeDecodeError as e :
                    print(e)

            if breakflag :
                print(list)
                try :
                    res = res.decode('gb2312')
                except UnicodeDecodeError as e :
                    print(e)
                print(res)
                break

def cp2102_open(device="/dev/ttyUSB0"):
    return serial.Serial(device,115200)

cp2102 = cp2102_open()
handle = A6handle(cp2102)

while True :

    print(">>",end='')
    cmd = input()
    handle.sendcmd(cmd)
    handle.getres()

