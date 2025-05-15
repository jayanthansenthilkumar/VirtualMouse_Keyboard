# Hand Controller

A Python-based application that enables hands-free control of your computer using computer vision and hand gestures. The application uses your webcam to track hand movements and gestures, allowing you to control your mouse cursor and keyboard inputs through hand motions.

## Features

- **Mouse Control Mode**: Control your cursor with your index finger movements
- **Keyboard Control Mode**: Use hand position to trigger arrow key inputs
- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand landmark detection
- **Gesture Recognition**: Supports different gestures for various controls
- **Mode Switching**: Easy switching between mouse and keyboard modes
- **Live Feedback**: Displays current mode, FPS, and actions in the video feed

## Requirements

- Python
- OpenCV (cv2)
- MediaPipe
- PyAutoGUI

## How to Use

1. Run the application:
   ```
   python app.py
   ```

2. Control Gestures:
   - **Mouse Mode** (One finger extended):
     - Move your index finger to control the cursor
     - Pinch your thumb and index finger together to click
   
   - **Keyboard Mode** (Two fingers extended):
     - Move hand to left edge: LEFT arrow
     - Move hand to right edge: RIGHT arrow
     - Move hand to top edge: UP arrow
     - Move hand to bottom edge: DOWN arrow

3. Mode Switching:
   - Extend only index finger for Mouse Mode
   - Extend both index and middle fingers for Keyboard Mode

4. Press 'q' to quit the application

## Additional Information

- The application includes cursor movement smoothing for better control
- Real-time FPS counter is displayed
- Current mode (MOUSE/KEYBOARD) is shown on screen
- Fail-safe is disabled for PyAutoGUI to allow full screen movement
