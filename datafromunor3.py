'''
Author: Hayat Tamboli
Date: 2024-04-14
Description: This file reads data from the serial port of the Arduino UNO R3 and stores it in a queue.
'''

import serial
import serial.serialutil
import queue

line = ""
words = []
words_queue2 = queue.Queue()

def readDataFromR3():
    global line
    global words
    global words_queue2
    ser = None
    try:
        ser = serial.Serial(port='COM8', baudrate=9600)
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
        words_queue2.put(words)

# readDataFromR3()