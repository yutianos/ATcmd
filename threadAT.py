#!/usr/bin/env python3.5

import serial
import os
import time
import queue
import threading
from pdu import decodepdu

cmdsettxt = 'AT+CMGF=1\r\n'
cmdreadmsg = 'AT+CMGR=37\r\n'
cmdsetpud = 'AT+CMGF=0\r\n'
trg_recmsgcmd = '+CMTI:'
delmsgcmd = 'AT+CMGD='

def logg(data):
    print(data)


'''
cmdfindusb = 'dmesg |grep cp210x|grep tty'
sdf = os.popen(cmdfindusb).read()
print(sdf)
'''
class A6handle:
    qmsg = queue.Queue()
    qpdu = queue.Queue()

    def __init__(self,com):
        self.com = com
        pass

    def waitfor(self):
        for i in range(20) :
            res = ''
            breakflag = 0
            time.sleep(0.4)
            if self.com.in_waiting:
                breakflag = 1
                res = self.com.read(self.com.in_waiting).decode()

            #print("res :",res)
            if breakflag :
                resp=res.split() 
                return resp
        return 1 

    def delmsg(self,index):
        cmd = delmsgcmd + index + '\r\n'
        self.com.write(cmd.encode())
        #print(cmd)

        resp = self.waitfor()
        logg(resp)
                        

    def trg_recmsg(self):
        while True :
            res = ''
            breakflag = 0
            print(self.com.in_waiting,end='')
            if self.com.in_waiting:
                breakflag = 1
                res = self.com.read(self.com.in_waiting).decode()

            if breakflag:
                resp = res.split()
                print(resp[0],'-->',trg_recmsgcmd)
                #logg(resp)
                if resp[0] == trg_recmsgcmd :
                    A6handle.qmsg.put(resp[1].split(',')[1])
                    print(resp)
                    return 0
            time.sleep(0.5) 
            
    def getmsgfromQ(self):
        index = A6handle.qmsg.get()
        print('recv index is',index)
        pdu = self.getmsg(index)
        A6handle.qpdu.put(pdu)
        logg('--->>>PDU:')
        logg(pdu)
        
    def isconnect(self):
        self.com.write('AT\r\n'.encode())
        res = self.waitfor()
        print(type(res))
        if res== 1:
            print("A6 is lost")
            return 1
        else:
            if res[1]=='OK':
                print("A6 is connceting")
                return 0
            else :
                print("A6 is lost")
                return 1



    def setpdumode(self):
        self.com.write(cmdsetpud.encode())
        res = self.waitfor()
        

    def getmsg(self,index):
        cmd = 'AT+CMGR=' + index + '\r\n'
        self.com.write(cmd.encode()) 
        res = self.waitfor()
        res = res[3:-1]
        str = '\n'.join(res)
        demsg = decodepdu(str)
        demsg = '\n'.join(demsg)
        f = open("msg.txt",'a')
        f.write('\r\n\r\n')
        f.write(demsg)
        f.write('\r\n\r\n')
        f.close()
        print('str:',str)
        self.delmsg(index)
        return demsg 
    
    def sendtestmsg(self):
        self.setpdumode()
        self.com.write('AT+CMGS=14\r\n'.encode())
        res = self.waitfor()
        logg(res)
        self.com.write('00010005810110F0000004633C9B0D'.encode())
        self.com.write(b'\x1A')
        res = self.waitfor()
        logg(res)
        res = self.waitfor()
        logg(res)
        
    def thread_test1(self):
        print("this is thread 1")
        time.sleep(1)

    def thread_test2(self):
        print("this is thread 2")
        time.sleep(2)


res = ''
trgmsgflag = threading.Event()
msggotflag = threading.Event()
trgmsgflag.clear()
msggotflag.set()


def cp2102_open(device="/dev/ttyUSB0"):
    return serial.Serial(device,115200)
def waitformsg():
    while True:
        msggotflag.wait()
        msggotflag.clear()
        #handle.thread_test1()
        handle.trg_recmsg()
        trgmsgflag.set()

def readmsg():
    while True:
        trgmsgflag.wait() 
        trgmsgflag.clear()
        #handle.thread_test2()
        handle.getmsgfromQ()
        msggotflag.set()

cp2102 = cp2102_open()
handle = A6handle(cp2102)

handle.isconnect()

t1 = threading.Thread(target=waitformsg)
t2 = threading.Thread(target=readmsg)

handle.sendtestmsg()
time.sleep(2)
t1.start()
t2.start()
while True:
    readq = handle.qpdu.get()
    print("PDU from Q:",readq)

'''
handle.sendtestmsg()
while True :
    handle.trg_recmsg()
    handle.getmsgfromQ()

''' 
