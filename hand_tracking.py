import cv2
import mediapipe as mp
import time
import math

class Hand_Detector():
    def __init__(self, mode = False, max_hands = 2):
        # Initialization
        self.mode = mode
        self.max_hands = max_hands

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands)
        self.mp_draw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def DetectHands(self, frame, draw=True):
        if frame is None or frame.size == 0:
            return frame
        # Convert the frame to RGB for Mediapipe Hands
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.result = self.hands.process(frame_rgb)

        if self.result.multi_hand_landmarks:
            for hand_landmarks in self.result.multi_hand_landmarks:
                if draw:
                    # Draw finger landmarks
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return frame

    def Landmarks_Position(self, frame, handNo=0, draw=True):
        self.landmarkList = []
        xlist = []
        ylist = []
        bounding_box = [] # Create a boundary box around the hand

        if self.result.multi_hand_landmarks:
            hand = self.result.multi_hand_landmarks[handNo]
            # Draw palm landmarks and get the index number of the finger
            for idx, landmark in enumerate(hand.landmark):
                height, width, _ = frame.shape

                # Calculate the position
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                xlist.append(cx)
                ylist.append(cy)

                self.landmarkList.append([idx, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            x_min, x_max = min(xlist), max(xlist)
            y_min, y_max = min(ylist), max(ylist)
            bounding_box = x_min, y_min, x_max, y_max

            if draw:
                cv2.rectangle(frame, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), (0, 0, 255), 3)

        return self.landmarkList, bounding_box

    def Find_Distance(self, p1, p2, frame, draw=True, r=15, t=3):
        x1, y1 = self.landmarkList[p1][1:]
        x2, y2 = self.landmarkList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(frame, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), r, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, frame, [x1, y1, x2, y2, cx, cy]

    def Find_Finger(self):
        fingers = []
        if self.landmarkList[self.tipIds[0]][1] > self.landmarkList[self.tipIds[0] - 1][1]: # Check for the cx-coordinates
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.landmarkList[self.tipIds[id]][2] < self.landmarkList[self.tipIds[id] - 2][2]: # Check for the cy-coordinates
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

