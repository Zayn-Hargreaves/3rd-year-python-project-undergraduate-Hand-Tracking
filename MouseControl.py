import HandTrackingModule as htm
import cv2
from pynput.mouse import Button, Controller
from pynput import keyboard
import time
import numpy as np
import ctypes

mouse = Controller()
set = True
def on_press_key(key):
    global set
    if key == keyboard.Key.esc:
        set = False
        print(set)
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['1', '2', 'left', 'right']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        set = True
        print('Key pressed: ' + k)
        # return False  # stop listener; remove this if want more keys
    return True

def Control(x, y, x_4, x_3):
    mouse.position = (x, y)
    if x_4 > x_3:
        mouse.press(Button.left)
        print(x_4, x_3)
    else:
        mouse.release(Button.left)
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    # cap.set(3, 1280)
    # cap.set(4, 720)
    detector = htm.handDetector(maxHands=1)

    """
    For Window user
    """
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)  # 0 corresponds to screen width
    screen_height = user32.GetSystemMetrics(1)  # 1 corresponds to screen height
    """
    For Linux user 
    import (from Xlib import display)
    screen = display.Display().screen()
    screen_width = screen.width_in_pixels
    screen_height = screen.height_in_pixels
    """
    # Get frame
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    while cap.isOpened():
        success, img = cap.read()
        img = detector.findHands(img)
        img = cv2.flip(img, 1)
        lmList = detector.findPos(img, draw=False)
        h, w, c = img.shape
        if len(lmList) != 0:
            x_4, x_3 = lmList[4][1], lmList[3][1]
            x_point, y_point = w - lmList[9][1], lmList[9][2]
            x = np.interp(x_point, [0, frame_width], [0, screen_width])
            y = np.interp(y_point, [0, frame_height], [0, screen_height])
            listener = keyboard.Listener(on_press=on_press_key)
            listener.start()
            if set:
                Control(x, y, x_4, x_3)  # Controll Object

        # calculate fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        # add fps
        cv2.putText(img, "FPS: " + str(int(fps)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 158, 68), 3)
        # render video
        cv2.imshow('Hand Tracking', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()