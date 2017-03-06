#!python3

import time
import datetime
import serial
from pipeline import pipeSource, pipeMiddle, pipeSink
        
def pmDataReader(port='/dev/tty.wchusbserial1410', baudrate=115200, timeout=10):
    thePort = serial.Serial(port, baudrate, timeout=timeout)
    thePort.readline()

    def func():
        return thePort.readline().rstrip().decode()

    return func


def addTimeStamp(item):
    return "%s,%s,%s" % (datetime.datetime.now().strftime('%Y-%m-%d'),
                           datetime.datetime.now().strftime('%H:%M:%S'),
                           item)
    

def write2file(file='aqi.dat'):
    def func(item):
        with open(file, "a") as theFile:
            theFile.write(item + "\n")

    return func


if __name__ == '__main__':
    pipeSource(pmDataReader(), [pipeMiddle(addTimeStamp, [pipeSink(write2file()), pipeSink(print)])])
