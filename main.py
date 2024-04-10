# when you spin it hard the video speeds up

import cv2
import serial
import serial.serialutil
import threading

line = "0"

def receive_data_from_arduino():
    ser = None
    try:
        ser = serial.Serial(port='COM7', baudrate=9600)
    except serial.serialutil.SerialException as e:
        print("Could not open port: ", str(e))
        return
    while True:
        global line
        line = str(ser.readline().decode().strip())
        print(line)
    


def run_video():
    video_path = 'myvideo.mp4'
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
            break

        cv2.imshow('Video', frame)

        # defining the framerate
        delay = int(1000 / (fps * speed_up_factor))

        # Wait for key press
        key = cv2.waitKey(delay)

        # Check if the 'Z' key was pressed or if the line is "1"
        if ((key == ord('z'))|(line == "1")):
            speed_up_factor = 5 
        else:
            speed_up_factor = 1
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