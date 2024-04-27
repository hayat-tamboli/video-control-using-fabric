'''
Author: Hayat Tamboli
Date: 2024-04-14
Description: This file reads data from the serial port of the Arduino UNO R4 and stores it in a queue.
'''

import serial
import serial.serialutil
import queue

line = ""
words = []
words_queue1 = queue.Queue()

def readDataFromR4():
    global line
    global words
    ser = None
    try:
        ser = serial.Serial(port='COM7', baudrate=9600)
    except serial.serialutil.SerialException as e:
        print("Could not open port: ", str(e))
        return
    
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='replace').strip()
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")
            line = "Error: Unable to decode"
        
        words = line.split()
        # print(words)
        words_queue1.put(words)
        
# readDataFromR4()