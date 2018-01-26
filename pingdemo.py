#!/usr/bin/env python3.5

import os,sys,re
import subprocess

def Netchk(ip='8.8.8.8'):
    p = subprocess.Popen( [ "ping -c 1 -w 1 " + ip ] ,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out = p.stdout.read().decode()
    #print('out:',out)
    #print('err:',p.stderr.read())

    match = re.findall('100% packet loss',out)
    
    #print(match)

    #print('len:',len(match))
    if len(match) :
        print('net is lost')
        return 1
    else :
        print('net is connect')
        return 0

#Netchk()
#Netchk("8.8.8.8")

