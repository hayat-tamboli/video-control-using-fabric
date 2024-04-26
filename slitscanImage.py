import cv2, sys
import numpy as np

mirror = False

video_capture = cv2.VideoCapture(0)

height = 1080
width = 1080
half = int(width/2)
if mirror:
    blank_image = np.zeros((height, width+width, 3), np.uint8)
else:
    blank_image = np.zeros((height, width+half, 3), np.uint8)


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    small = cv2.resize(frame, (width, height) )

    blank_image[:, half+1:width+half] = blank_image[:, half:width+half-1]
    blank_image[:, half] = small[:, half]
    blank_image[:, 0:half] = small[:, 0:half]

    cv2.imshow('Slitscan image', blank_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
