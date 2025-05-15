import cv2
import mediapipe as mp
import pyautogui
import time

class HandController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.screen_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.screen_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.display_width, self.display_height = pyautogui.size()
        self.mode = "mouse"
        self.prev_x, self.prev_y = 0, 0
        self.smoothing = 0.5
        self.prev_frame_time = 0
        self.curr_frame_time = 0
        pyautogui.FAILSAFE = False

    def detect_gesture(self, hand_landmarks):
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        index_base = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        middle_base = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        index_extended = index_tip.y < index_base.y
        middle_extended = middle_tip.y < middle_base.y
        thumb_index_distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
        if thumb_index_distance < 0.05:
            return "click"
        elif index_extended and not middle_extended:
            return "mouse_mode"
        elif index_extended and middle_extended:
            return "keyboard_mode"
        return None

    def handle_mouse_control(self, index_finger_x, index_finger_y):
        screen_x = int(index_finger_x * self.display_width)
        screen_y = int(index_finger_y * self.display_height)
        smooth_x = int(self.prev_x + self.smoothing * (screen_x - self.prev_x))
        smooth_y = int(self.prev_y + self.smoothing * (screen_y - self.prev_y))
        pyautogui.moveTo(smooth_x, smooth_y)        
        self.prev_x, self.prev_y = smooth_x, smooth_y

    def handle_keyboard_control(self, x, y):
        if x < 0.3:
            pyautogui.press('left')
            return "LEFT"
        elif x > 0.7:
            pyautogui.press('right')
            return "RIGHT"
        elif y < 0.3:
            pyautogui.press('up')
            return "UP"
        elif y > 0.7:
            pyautogui.press('down')
            return "DOWN"
        return None
    
    def run(self):
        try:
            while self.cap.isOpened():
                success, frame = self.cap.read()
                if not success:
                    print("Failed to capture frame")
                    break
                frame = cv2.flip(frame, 1)
                self.curr_frame_time = time.time()
                fps = int(1 / (self.curr_frame_time - self.prev_frame_time)) if self.curr_frame_time != self.prev_frame_time else 0
                self.prev_frame_time = self.curr_frame_time
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                cv2.putText(frame, f"Mode: {self.mode.upper()}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, f"FPS: {fps}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(frame, hand_landmarks, 
                                                     self.mp_hands.HAND_CONNECTIONS)
                        index_finger = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        gesture = self.detect_gesture(hand_landmarks)
                        if gesture == "mouse_mode":
                            self.mode = "mouse"
                        elif gesture == "keyboard_mode":
                            self.mode = "keyboard"
                        if self.mode == "mouse":
                            self.handle_mouse_control(index_finger.x, index_finger.y)
                            if gesture == "click":
                                pyautogui.click()
                        else:
                            action = self.handle_keyboard_control(index_finger.x, index_finger.y)
                            if action:
                                cv2.putText(frame, f"Action: {action}", (10, 90),
                                          cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow('Hand Controller', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            self.hands.close()

if __name__ == "__main__":
    print("Starting Hand Controller...")
    print("Instructions:")
    print("- One finger: Mouse mode - Control cursor")
    print("- Two fingers: Keyboard mode - Arrow keys")
    print("- In mouse mode, pinch thumb and index finger to click")
    print("- In keyboard mode, move hand to edges for arrow keys")
    print("- Press 'q' to quit")
    
    controller = HandController()
    controller.run()