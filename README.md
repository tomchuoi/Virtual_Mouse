# Virtual Mouse Control with Hand Tracking

This project demonstrates a virtual mouse control system using hand tracking with OpenCV and PyAutoGUI. The program uses a webcam to track hand movements and translates them into mouse cursor movements and clicks on the screen.

## Features

- Tracks the user's hand using the webcam.
- Moves the mouse cursor based on the user's index finger position.
- Performs left-click when the user's index and middle fingers are raised and close together.
- Supports real-time display of the webcam feed with visual feedback.

## Requirements

- Python 3.x
- OpenCV
- Mediapipe
- PyAutoGUI

## How to use:
- To move the mouse cursor, raise your index finger in front of your webcam. The program will automatically track your index finger's movement and reflect it as cursor movement on the screen.
- To click the mouse, raise both your middle and index fingers and make them touch each other, that's all.

