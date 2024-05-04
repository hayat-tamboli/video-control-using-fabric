'''
Author: Hayat Tamboli
Date: 2024-04-14
Description: This file takes data from the serial ports of the Arduino UNO R3 and R4 and processes it to control the video playback
'''

import random
import cv2
import serial
import serial.serialutil
import threading
import time

from datafromr4 import readDataFromR4, words_queue1
from datafromunor3 import readDataFromR3, words_queue2
from videoeffects import apply_glitch_effect, grayscaleVideo, pixelateVideo

folded = False # True make the video paused, False make the video play
speedup = False # True makes the video Speed up, False makes the video play at normal speed
flip = False # True flips the video, False does not flip the video
grayscale = False # True makes the video grayscale, False makes the video colored
glitch = False # True makes the video glitch, False does not make the video glitch
fabricCompressionOrCrumbleorStretch = "" # "fabricCompression" makes the video fabric compression, "crumble" makes the video crumble
wasGlitching = False
slowDown = False # True makes the video slow down, False makes the video play at normal speed
pixelate = False # True makes the video pixelated, False makes the video not pixelated
count = 0
combinedSensorData = []
r4SensorData = []
r3SensorData = []
accel1orientation = "1-Z-down"
accel2orientation = "2-Z-down"
accel3orientation = "3-Z-down"
accel4orientation = "4-Z-down"
isStretching = False
isCompressing = False
isCrumbling = False
reverse = False
crumbleCount = 0

# Function to read data from the Arduino UNO R4 and R3 and save it in global variables
def receive_data_from_arduino():
    global r4SensorData
    global r3SensorData
    while True:
        # Check if there is data in the queue
        if not words_queue1.empty():
            r4SensorData = words_queue1.get()
            # print("Received words:", words1)
        else:
            r4SensorData = r4SensorData
        
        if not words_queue2.empty():
            r3SensorData = words_queue2.get()
            # print("Received words:", words2)
        else:
            r3SensorData = r3SensorData
        
        time.sleep(0.05)

# Function to analyze the data from the Arduino UNO R4 and R3 and control the video playback
def analyzeData():
    global r4SensorData
    global r3SensorData
    global glitch
    global folded
    global flip
    global slowDown
    global speedup
    global reverse
    
    
    while True:
        CombiningAndDistributingDataFromSensors()
        clothFaceDown, clothFaceUp = FlatClothDirection()
        glitch = isClothGettingCompressed(clothFaceUp)
        
        if(isStretching == "stretching"):
            slowDown = True
            glitch = False
        else:
            slowDown = False
            
        if(isCompressing == "compress"):
            speedup = True
            glitch = False
            slowDown = False
        else:
            speedup = False
        
        if clothFaceDown:
            reverse = True
            folded = False
            glitch = False
        else:
            reverse = False
            
        if(accel1orientation == "1-Z-up" and accel2orientation == "2-Z-up" and accel3orientation == "3-Z-down" and accel4orientation == "4-Z-down"):
            folded = True
            reverse = False
        
        if(accel1orientation == "1-Z-down" and accel2orientation == "2-Z-up" and accel3orientation == "3-Z-up" and accel4orientation == "4-Z-down"):
            folded = True
            reverse = False
        else:
            folded = False
        
        time.sleep(0.05)

def isClothGettingCompressed(clothFaceUp):
    global crumbleCount
    global isCrumbling
    if(isCrumbling == "crumble"):
        if(clothFaceUp or folded):
            return False
        else:
            crumbleCount = crumbleCount + 1
            # added to remove unnecessary glitching
            if(crumbleCount > 5):
                return True
    else:
        crumbleCount = 0
        return False

def FlatClothDirection():
    global accel1orientation
    global accel2orientation
    global accel3orientation
    global accel4orientation
    clothFaceDown = ((accel1orientation == "1-Z-down" and accel2orientation == "2-Z-down" and accel3orientation == "3-Z-down" or accel4orientation == "4-Z-down") or (accel1orientation == "1-Z-down" and accel2orientation == "2-Z-down" or accel3orientation == "3-Z-down" and accel4orientation == "4-Z-down") or (accel1orientation == "1-Z-down" or accel2orientation == "2-Z-down" and accel3orientation == "3-Z-down" and accel4orientation == "4-Z-down"))
    clothFaceUp = (accel1orientation == "1-Z-up" and accel2orientation == "2-Z-up" and accel3orientation == "3-Z-up" and accel4orientation == "4-Z-up")
    return clothFaceDown,clothFaceUp

def CombiningAndDistributingDataFromSensors():
    global accel1orientation
    global accel2orientation
    global accel3orientation
    global accel4orientation
    global isStretching
    global isCompressing
    global isCrumbling
    global combinedSensorData
    # combine the data from the two sensors
    combinedSensorData = r4SensorData + r3SensorData
    # data would look like this: ['1-Z-up', '2-Z-up', '3-Z-up', '4-Z-up', 'stretching', 'crumble', 'compress']
    print("Data from Sensors: ", combinedSensorData)
    if(len(combinedSensorData) > 6):
        accel1orientation = combinedSensorData[0]
        accel2orientation = combinedSensorData[1]
        accel3orientation = combinedSensorData[2]
        accel4orientation = combinedSensorData[3]
        isStretching = combinedSensorData[4]
        isCrumbling = combinedSensorData[5]
        isCompressing = combinedSensorData[6]


# Function to run the video !!!!!!!!!!!!!!!!!!!!
def run_video():
    global wasGlitching
    global glitch
    global folded
    global flip
    global reverse
    
    video_path1 = 'videos/walking.mp4'
    video_path2 = 'videos/umbrella.mp4'
    video_path3 = 'videos/briefcase.mp4'
    
    cap = cv2.VideoCapture(video_path2)

    if not cap.isOpened():
        print("Error: Unable to open video file")
        return

    # Get the video properties
    fps = cap.get(cv2.CAP_PROP_FPS)

    speed_up_factor = 1
    reverse = False
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840*2)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160*2)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        if glitch:
            frame = apply_glitch_effect(frame, random.randint(-20, 20))
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)
            wasGlitching = True
            
        if(glitch and wasGlitching):
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + random.randint(1, 20))
            wasGlitching = False;

        if grayscale:
            frame = grayscaleVideo(frame)

        if pixelate:
            frame = pixelateVideo(frame)
        
        # Display the frame
        cv2.imshow('Video', frame)

        # defining the framerate
        delay = int(1000 / (fps * speed_up_factor))

        # Wait for key press
        key = cv2.waitKey(delay)

        # spped up functionlaity
        if (speedup):
            speed_up_factor = 8
        else:
            speed_up_factor = 1
            
            
        if (slowDown):
            speed_up_factor = 0.3
        
        # frame = slitscanVideo(frame, cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Play pause functionality
        if(folded):
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)

        # Check if the 'X' key was pressed
        # if (key == ord('x')):
        #     reverse = not reverse
        if key == 27:  # If 'Esc' key was pressed
            break
        if reverse:
            speed_up_factor = 10
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 2)
            if(cap.get(cv2.CAP_PROP_POS_FRAMES) == 0):
                cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT)-1)

    cap.release()
    cv2.destroyAllWindows()

# to run 5 loops/threads at the same time
arduino_thread = threading.Thread(target=receive_data_from_arduino)
data_analysis_thread = threading.Thread(target=analyzeData)
arduino_thread1 = threading.Thread(target=readDataFromR4)
arduino_thread2 = threading.Thread(target=readDataFromR3)
video_thread = threading.Thread(target=run_video)

arduino_thread.start()
arduino_thread1.start()
arduino_thread2.start()
data_analysis_thread.start()
video_thread.start()

arduino_thread.join()
arduino_thread1.join()
arduino_thread2.join()
data_analysis_thread.join()
video_thread.join()