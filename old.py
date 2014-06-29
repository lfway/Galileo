__author__ = 'ilya'

import serial
from threading import Thread
from time import sleep
import time
import datetime

import os

import requests

import ftplib

os.system("kill -9 $(jobs -p)")
sleep(1)
os.system("kill -9 $(jobs -p)")
sleep(1)
os.system("kill -9 $(jobs -p)")


r = requests.get('http://192.168.0.47/test.php')
os.system("rm -rf /root/pictures/")
os.system("mkdir /root/pictures/")

ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
#ser.close()
#ser.open()
#ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
print("connected to: " + ser.portstr)

def thread_f1():
    print "go1"
    session = ftplib.FTP('192.168.0.47','12345','12345')
    print "go2"
    ctr = 0
    str1 = "Press ENTER 3 times to start interactive setup"
    str2 = "Calibrating barometer"
    line = []
    str=""
    can_work = False
    while True:
        for c in ser.read():
            str += c
            line.append(c)
            if c == '\n':
                print("Line: {0}".format(str ))
                #print line
                if can_work == True and str.find("m/s") > -1:
                    print str
                    os.system("fswebcam -r 640x480 --jpeg 85 -D 1 /root/pictures/web-cam-shot{0}.jpg".format(ctr))
                    file = open("/root/pictures/web-cam-shot{0}.jpg".format(ctr),'rb')      # file to send
                    session.storbinary("STOR web-cam-shot{0}.jpg".format(ctr), file)     # send the file
                    name_ok = "web-cam-shot{0}.jpg".format(ctr)
                    q1 = "http://192.168.0.47/test2.php?name={0}&data={1}".format(name_ok, str)
                    print q1
                    requests.get(q1)
                    file.close()
                    sleep(4)
                    ctr += 1
                if str.find(str2) > -1:
                    ser.write("\r\n\r\n\r\n")
                    sleep(1)
                    ser.write("test\r\n")
                    sleep(1)
                    #ser.write("help\r\n")
                    #sleep(1)
                    ser.write("airspeed\n")
                    #ser.write("compass\n")
                    can_work = True
                line = []
                str = ""
    ser.close()

def thread_f2():
    the_input = raw_input("Enter input: ")

    print "\r\n\r\n{0}\r\n\r\n".format(the_input)


if __name__ == "__main__":
    thread1 = Thread(target=thread_f1)
    thread1.start()
    thread2 = Thread(target=thread_f2)
    thread2.start()

    thread1.join()
    thread2.join()
    print "thread finished...exiting"


