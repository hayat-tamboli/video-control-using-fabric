'''
Author: Hayat Tamboli
Date: 2024-05-04
Description: This file contains functions to apply various effects to a video
'''

import cv2
import numpy as np

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

# TODO: Debug this function
# TODO: allows changes in axis and direction of slitscan
def slitscanVideo(frame, height, width):
    half = int(width/2)
    blank_image = np.zeros((height, width+half, 3), np.uint8)
    small = cv2.resize(frame, (width, height) )
    blank_image[:, half+1:width+half] = blank_image[:, half:width+half-1]
    blank_image[:, half] = small[:, half]
    blank_image[:, 0:half] = small[:, 0:half]
    return blank_image
