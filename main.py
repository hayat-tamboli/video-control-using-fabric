# when you spin it hard the video speeds up

import random
import cv2
import serial
import serial.serialutil
import threading
import numpy as np
import time
import matplotlib.pyplot as plt

# Start the timer
start_time = time.time()

line1 = ""
line2 = ""
folded = False # True make the video paused, False make the video play
intenseSpin = False # True makes the video Speed up, False makes the video play at normal speed
flip = False # True flips the video, False does not flip the video
grayscale = False # True makes the video grayscale, False makes the video colored
fabricCompressionOrCrumble = "";

animatedGlitch = False

def receive_data_from_arduino():
    ser1 = None
    ser2 = None
    try:
        ser1 = serial.Serial(port='COM8', baudrate=9600)
    except serial.serialutil.SerialException as e:
        print("Could not open port: ", str(e))
        return
    # try:
    #     ser2 = serial.Serial(port='COM9', baudrate=38400)
    # except serial.serialutil.SerialException as e:
    #     print("Could not open port: ", str(e))
    #     return
    while True:
        global line1
        # global line2
        line1 = str(ser1.readline().decode().strip())
        # line2 = str(ser2.readline().decode().strip())
        print(line1)
        global folded
        if(line1.find("play") == -1):
            folded = False
        else:
            folded = True
        global intenseSpin
        if(line1.find("normalspeed") == -1):
            intenseSpin = False
        else:
            intenseSpin = True
    
def apply_glitch_effect(frame, translation_amount):
    # Duplicate the frame
    glitch_frame = frame.copy()

    # Apply translation to one of the copies
    rows, cols, _ = glitch_frame.shape
    M = np.float32([[1, 0, translation_amount], [0, 1, translation_amount]])
    glitch_frame = cv2.warpAffine(glitch_frame, M, (cols, rows))

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
        plt.figure(figsize=[15,15])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Input Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
    # Otherwise.
    else:
    
        # Return the output image.
        return output_image

def run_video():
    video_path = 'videos/cinemagraph 1.mp4'
    cap = cv2.VideoCapture(video_path)

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
        # current_time = round((time.time() - start_time) * 1000)
        # print(current_time)

        # if(current_time> amimationStartTimer and current_time < animationStopTimer):
        #     # pls change this when in production
        #     animatedGlitch = true
        #     # cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)
        # else:
        #     if(current_time > amimationStartTimer):
        #         # cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + random.randint(1, 20))
        #         amimationStartTimer += 2000;
        #         animationStopTimer = amimationStartTimer + animation_timer
        #     animatedGlitch = False


        if line1 == "closed":
            frame = apply_glitch_effect(frame, random.randint(-20, 20))
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)

        if flip:
            frame = flipVideo(frame)

        if grayscale:
            frame = grayscaleVideo(frame)
        
        # frame = cv2.bilateralFilter(frame,15, 75, 75)


        if pixelateVideo:
            frame = pixelateVideo(frame)
        
        # Display the frame
        cv2.imshow('Video', frame)

        # defining the framerate
        delay = int(1000 / (fps * speed_up_factor))

        # Wait for key press
        key = cv2.waitKey(delay)

        # spped up functionlaity
        if (not intenseSpin):
            speed_up_factor = 8
        else:
            speed_up_factor = 1
        
        # Play pause functionality
        if(folded):
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)

        # Check if the 'X' key was pressed
        if (key == ord('x')):
            reverse = not reverse
        if key == 27:  # If 'Esc' key was pressed
            break
        if reverse:
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 2)

    cap.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

# to run 2 loops at the same time
arduino_thread = threading.Thread(target=receive_data_from_arduino)
video_thread = threading.Thread(target=run_video)

arduino_thread.start()
video_thread.start()

arduino_thread.join()
video_thread.join()