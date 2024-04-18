# when you spin it hard the video speeds up

import random
import cv2
import serial
import serial.serialutil
import threading
import numpy as np
import time
import matplotlib.pyplot as plt

from datafromr4 import readDataFromR4, words_queue1
from datafromunor3 import readDataFromR3, words_queue2

# Start the timer
# start_time = time.time()

line1 = ""
line2 = ""
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
words = []
words1 = []
words2 = []
accel1orientation = "1-Z-down"
accel2orientation = "2-Z-down"
accel3orientation = "3-Z-down"
accel4orientation = "4-Z-down"
isStretching = False
isCompressing = False
isCrumbling = False
reverse = False


def receive_data_from_arduino():
    global words1
    global words2
    while True:
        # Check if there is data in the queue
        if not words_queue1.empty():
            words1 = words_queue1.get()
            # print("Received words:", words1)
        else:
            print("No data in the queue 1")
        
        if not words_queue2.empty():
            words2 = words_queue2.get()
            # print("Received words:", words2)
        else:
            print("No data in the queue 2")
        
        time.sleep(0.2)
    # readDataFromR4()
    # readDataFromR3()
    # ser1 = None
    # ser2 = None
    # try:
    #     ser1 = serial.Serial(port='COM8', baudrate=9600)
    # except serial.serialutil.SerialException as e:
    #     print("Could not open port: ", str(e))
    #     return
    # try:
    #     ser2 = serial.Serial(port='COM7', baudrate=9600)
    # except serial.serialutil.SerialException as e:
    #     print("Could not open port: ", str(e))
    #     return
    # while True:
    #     global line1
    #     global line2
    #     global slowDown
    #     global speedup
    #     global words
    #     global accel3orientation
    #     global accel4orientation
    #     global isStretching
    #     global isCompressing
    #     global isCrumbling
    #     global glitch
    #     global folded
    #     global flip
    #     global reverse
        # try:
        #     line1 = ser1.readline().decode('utf-8', errors='replace').strip()
        # except UnicodeDecodeError as e:
        #     print(f"UnicodeDecodeError: {e}")
        #     # Handle the error as needed, e.g., logging or continuing with a placeholder value
        #     line1 = "Error: Unable to decode"

        # try:
        #     line2 = ser2.readline().decode('utf-8', errors='replace').strip()
        # except UnicodeDecodeError as e:
        #     print(f"UnicodeDecodeError: {e}")
        #     # Handle the error as needed, e.g., logging or continuing with a placeholder value
        #     line2 = "Error: Unable to decode"
            
        # mainData = line2 + " " + line1
        # words = mainData.split()
        # print(words)
        # ignoreAccelerometer = False
        # if(len(words) > 6):
        #     accel1orientation = words[0]
        #     accel2orientation = words[1]
        #     accel3orientation = words[2]
        #     accel4orientation = words[3]
        #     isStretching = words[4]
        #     isCrumbling = words[5]
        #     isCompressing = words[6]
        
        
        # if(isCrumbling == "crumble"):
        #     glitch = True
        # else:
        #     glitch = False
        
        # glitch = False
        
        # if(isStretching == "stretching"):
        #     glitch = False
        #     slowDown = True
        # else:
        #     slowDown = False
        
        # if(isCompressing == "compress"):
        #     speedup = True
        #     ignoreAccelerometer = True
        #     slowDown = False
        # else:
        #     speedup = False
        # if(not ignoreAccelerometer):
        #     if(accel3orientation == "3-Z-up" and accel4orientation == "4-Z-up"):
        #         folded = False
        #         reverse = False
        #     else:
        #         if(isCrumbling == "crumble"):
        #             glitch = False
        #             reverse = True
        #         else:
        #             glitch = False
        #         folded = True
        #         glitch = False
        #         speedup = False
        #         slowDown = False
        #         if(accel3orientation == "3-Z-down" and accel4orientation == "4-Z-down"):
        #             flip = True
        #             folded = False
        #         else:
        #             flip = False
            
        # if(line1.find("play") == -1):
        #     folded = False
        # else:
        #     folded = True
        # global intenseSpin
        # if(line1.find("normalspeed") == -1):
        #     intenseSpin = False
        # else:
        #     intenseSpin = True

def analyzeData():
    global words
    global words1
    global words2
    global accel1orientation
    global accel2orientation
    global accel3orientation
    global accel4orientation
    global isStretching
    global isCompressing
    global isCrumbling
    global glitch
    global folded
    global flip
    global slowDown
    global speedup
    
    
    while True:
        words = words1 + words2
        print("Words: ", words)
        if(len(words) > 6):
            accel1orientation = words[0]
            accel2orientation = words[1]
            accel3orientation = words[2]
            accel4orientation = words[3]
            isStretching = words[4]
            isCrumbling = words[5]
            isCompressing = words[6]
            
        if(isCrumbling == "crumble"):
            if(accel1orientation == "1-Z-up" and accel2orientation == "2-Z-up" and accel3orientation == "3-Z-up" and accel4orientation == "4-Z-up"):
                pass
            else:
                glitch = True
        else:
            glitch = False
        
        if(isStretching == "stretching"):
            slowDown = True
            glitch = False
        else:
            slowDown = False
            
        if(isCompressing == "compress"):
            speedup = True
            glitch = False
        else:
            speedup = False
            
        if(accel1orientation == "1-Z-up" and accel2orientation == "2-Z-up" and accel3orientation == "3-Z-up" and accel4orientation == "4-Z-up"):
            folded = False
        else:
            # if()
            folded = True
        
        if(accel1orientation == "1-Z-down" and accel2orientation == "2-Z-down" and accel3orientation == "3-Z-down" and accel4orientation == "4-Z-down"):
            flip = False
        else:
            flip = True
            
        
        time.sleep(0.2)
    
def apply_glitch_effect(frame, translation_amount: int):
    # Duplicate the frame
    glitch_frame = frame.copy()

    # Apply translation to one of the copies
    rows, cols, _ = glitch_frame.shape
    M = np.float32([[1, 0, translation_amount], [0, 1, translation_amount]]) # type: ignore
    glitch_frame = cv2.warpAffine(glitch_frame, M, (cols, rows)) # type: ignore

    # Blend the original frame and glitched frame together
    alpha = 0.5  # Adjust blending level
    result = cv2.addWeighted(frame, alpha, glitch_frame, 1 - alpha, 0)

    return result

def flipVideo(frame):
    return cv2.flip(frame, 1)

def grayscaleVideo(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def pixelateVideo(frame):
    # Get input size
    height, width = frame.shape[:2]

    # Desired "pixelated" size
    w, h = (128, 128)

    # Resize input to "pixelated" size
    temp = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LINEAR)

    # Initialize output image
    frame = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

    return frame

def applySharpening(image, display=True):
    
    # Get the kernel required for the sharpening effect.
    sharpening_kernel = np.array([[-1, -1, -1],
                                  [-1, 9.2, -1],
                                  [-1, -1, -1]])
    
    # Apply the sharpening filter on the image.
    output_image = cv2.filter2D(src=image, ddepth=-1, 
                                kernel=sharpening_kernel)
    
    # Check if the original input image and the output image are specified to be displayed.
    if display:
        
        # Display the original input image and the output image.
        plt.figure(figsize=(15,15))
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Input Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
    # Otherwise.
    else:
    
        # Return the output image.
        return output_image

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

        # if flip:
        #     frame = flipVideo(frame)

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
        
        # Play pause functionality
        if(folded):
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)

        # Check if the 'X' key was pressed
        # if (key == ord('x')):
        #     reverse = not reverse
        if key == 27:  # If 'Esc' key was pressed
            break
        # if reverse:
            # cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 2)

    cap.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

# to run 2 loops at the same time
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