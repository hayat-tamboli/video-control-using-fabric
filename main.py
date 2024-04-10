#-----------------------------------------------------------------------------
#Step - 1  -Import Libraries and capture camera

#-----------------------------------------------------------------------------

import cv2 as cv
import numpy as np
import math
import serial
import serial.serialutil
import time
ser = None
try:
    ser = serial.Serial(port='COM7', baudrate=115200)
except serial.serialutil.SerialException as e:
    print("Could not open port: ", str(e))

# Open the video file
cap = cv.VideoCapture('myvideotoloop.mp4')
fps = cap.get(cv.CAP_PROP_FPS)
speedup_factor = 2.0
new_fps = fps * speedup_factor
frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' as the fourcc format for MP4 videos
# out = cv2.VideoWriter('output_video.mp4', fourcc, new_fps, (frame_width, frame_height))

# Read the first frame
ret, frame = cap.read()

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

allframes = []

# Loop through each frame in the video
while ret:
    frame = rescaleFrame(frame)
    # out.write(frame)
    # cv.imshow('Video', blur)
    allframes.append(frame)

    # Read the next frame
    ret, frame = cap.read()

i=0
try:
    while True:
        # Read line from serial port
        line = ser.readline().decode().strip()
        print("Received:", line)  # Print received data

        frametoShow = allframes[i]
        if line == "winking":
            frametoShow = cv.GaussianBlur(frametoShow, (7, 7), cv.BORDER_DEFAULT)
        cv.imshow('Video', frametoShow)
        if cv.waitKey(28) & 0xFF == ord('q'):
            break
        i += 1

except KeyboardInterrupt:
    # Close serial connection when script is interrupted
    ser.close()
    print("Serial connection closed.")

# Release the video capture object and close all windows
cap.release()
# out.release()
cv.destroyAllWindows()