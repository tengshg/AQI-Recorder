#!python3
# -*- coding: utf-8 -*-

####
# 2017-03-05 Teng, shgteng@live.com 
####

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


def extractData(typeToExtract='AQI'):
    """
    Extract the specific data such as 'AQI' from the raw data. 
    The raw data read from the PM meter is in the format:
    "AQI,AQIU,HCHO,TEMP,HUMI,CF1.0,AT1.0,CF2.5,AT2.5,CF10,AT10,PM0.3,PM0.5,PM1.0,PM2.5,PM5.0,PM10"
    for instnce:
    "8,73,0.00,0.00,0.00,26,23,27,27,27,27,14190,1677,14,4,0,0"
    """
    keys = ['AQI','AQIU','HCHO','TEMP','HUMI','CF1.0','AT1.0','CF2.5','AT2.5','CF10','AT10','PM0.3','PM0.5','PM1.0','PM2.5','PM5.0','PM10']

    def func(item):
        if item:
            results = item.split(',')
            if len(results) == 17: 
                data = dict((zip(keys, results)))
                return data.get(typeToExtract, None)
        return None

    return func


def addTimeStamp(item):
    return "%s\t%s\t%s" % (datetime.datetime.now().strftime('%Y-%m-%d'),
                           datetime.datetime.now().strftime('%H:%M:%S'),
                           item)
    

def filter(threshold = 30):
    preValue = 0

    def getCurrentValue(item):
        parts = item.split("\t")
        if len(parts) != 3:
            return 0

        try:
            return int(parts[2])
        except ValueError:
            return None

    def func(item):
        nonlocal preValue
        curValue = getCurrentValue(item)

        if not curValue:
            return None

        theLimit = preValue + threshold
        preValue = preValue * 0.1 + curValue * 0.9
        if curValue > theLimit:
            return None

        return item

    return func

def write2file(file='aqi.dat'):
    def func(item):
        with open(file, "a") as theFile:
            theFile.write(item + "\n")

    return func


if __name__ == '__main__':
    pipeSource(pmDataReader(), 
               [pipeMiddle(extractData(), 
                           [pipeMiddle(addTimeStamp, 
                                       [pipeSink(write2file()), 
                                        pipeSink(print)
                                       ])
                           ])
               ])
