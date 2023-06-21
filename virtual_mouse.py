import hand_tracking as ht
import cv2
import numpy as np
import time
import pyautogui

cam_width, cam_height = 640, 480

# Get the screen size
screen_width, screen_height = pyautogui.size()

# Get the frame reduction to create a box where the hand control is limited
frame_reduction = 75

smooth = 2
x_prev, y_prev = 0, 0
current_x, current_y = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

prev_time = 0
detector = ht.Hand_Detector(max_hands=1)


while True:
    # Initialize
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Find hand landmarks
    frame = detector.DetectHands(frame)
    landmarkList, bounding_box = detector.Landmarks_Position(frame)

    # Get the tip of the index and middle finger
    if len(landmarkList) != 0:
        x1, y1 = landmarkList[8][1:] # 8 is the tip of index finger
        x2, y2 = landmarkList[12][1:] # 12 is the tip of middle finger

        # Check which finger are up
        fingers = detector.Find_Finger()
        cv2.rectangle(frame, (frame_reduction, frame_reduction), (cam_width - frame_reduction, cam_height - frame_reduction)\
            , (255, 0, 255), 2)

        # If there is only the index finger => moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            # Convert coordinate
            x3 = np.interp(x1, (frame_reduction, cam_width - frame_reduction), (0, screen_width))
            y3 = np.interp(y1, (frame_reduction, cam_height - frame_reduction), (0, screen_height))

            current_x = x_prev + (x3 - x_prev) / smooth
            current_y = y_prev + (y3 - y_prev) / smooth

            # Move mouse
            pyautogui.moveTo(current_x, current_y)
            cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            x_prev, y_prev = current_x, current_y

        # If both index and middle finger are up => clicking mode
        if fingers[1] == 1 and fingers[2] == 1:

            # Calculate the distance between two finger
            length, frame, click_point = detector.Find_Distance(8, 12, frame)

            # If the distance < certain value then click
            if length < 30:
                cv2.circle(frame, (click_point[4], click_point[5]), 10, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

    # Frame rate
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Display the fps to the screen
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), thickness=3)

    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break