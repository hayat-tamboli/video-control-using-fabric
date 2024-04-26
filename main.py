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
crumbleCount = 0


def receive_data_from_arduino():
    global words1
    global words2
    while True:
        # Check if there is data in the queue
        if not words_queue1.empty():
            words1 = words_queue1.get()
            # print("Received words:", words1)
        else:
            words1 = words1
        
        if not words_queue2.empty():
            words2 = words_queue2.get()
            # print("Received words:", words2)
        else:
            words2 = words2
        
        time.sleep(0.05)

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
    global reverse
    
    
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
            if((accel1orientation == "1-Z-up" and accel2orientation == "2-Z-up" and accel3orientation == "3-Z-up" and accel4orientation == "4-Z-up") or folded):
                glitch = False
            else:
                crumbleCount = crumbleCount + 1
                if(crumbleCount > 5):
                    glitch = True
        else:
            glitch = False
            crumbleCount = 0
        
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
            
        
        if((accel1orientation == "1-Z-down" and accel2orientation == "2-Z-down" and accel3orientation == "3-Z-down" or accel4orientation == "4-Z-down") or (accel1orientation == "1-Z-down" and accel2orientation == "2-Z-down" or accel3orientation == "3-Z-down" and accel4orientation == "4-Z-down") or (accel1orientation == "1-Z-down" or accel2orientation == "2-Z-down" and accel3orientation == "3-Z-down" and accel4orientation == "4-Z-down")):
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

def slitscanVideo(frame, height, width):
    half = int(width/2)
    blank_image = np.zeros((height, width+half, 3), np.uint8)
    small = cv2.resize(frame, (width, height) )
    blank_image[:, half+1:width+half] = blank_image[:, half:width+half-1]
    blank_image[:, half] = small[:, half]
    blank_image[:, 0:half] = small[:, 0:half]
    return blank_image

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