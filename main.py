# when you spin it hard the video speeds up

import cv2
import serial
import serial.serialutil
import threading

line = "0"

# Define a function to receive Arduino data
def receive_data_from_arduino():
    # Your Arduino data receiving logic goes here
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
    
    # Path to the prerecorded video
    video_path = 'myvideo.mp4'

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
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

        # Check if the frame was read successfully
        if not ret:
            break

        # Display the frame
        cv2.imshow('Video', frame)

        # Calculate delay based on speed-up factor
        delay = int(1000 / (fps * speed_up_factor))

        # Wait for key press
        key = cv2.waitKey(delay)

        # Check if the 'Z' key was pressed
        if ((key == ord('z'))|(line == "1")):
            speed_up_factor = 5 
        else:
            speed_up_factor = 1
        if (key == ord('x')):
            reverse = not reverse
        if key == 27:  # If 'Esc' key was pressed
            break
        if reverse:
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 2)

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

# Create two threads, one for each task
arduino_thread = threading.Thread(target=receive_data_from_arduino)
video_thread = threading.Thread(target=run_video)

# Start both threads
arduino_thread.start()
video_thread.start()


# Wait for both threads to finish
arduino_thread.join()
video_thread.join()