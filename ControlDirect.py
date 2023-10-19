import HandTrackingModule as htm
import cv2
from pynput import keyboard
import time
import numpy as np
import pydirectinput

set = True
def ControlDirectInput(lmList):
    if lmList[8][2] < lmList[5][2] and lmList[17][2] > lmList[20][2]:
        pydirectinput.keyDown("down")
        pydirectinput.keyUp("down")
        print("Down")
    elif lmList[8][2] < lmList[5][2]:
        pydirectinput.keyDown("left")
        pydirectinput.keyUp("left")
        print("Turn Left")
    elif lmList[17][2] > lmList[20][2]:
        pydirectinput.keyDown("right")
        pydirectinput.keyUp("right")
        print("Turn Right")
    elif lmList[12][2] < lmList[9][2]:
        pydirectinput.keyDown("up")
        pydirectinput.keyUp("up")
        print("Up") 

# def on_press_key(key):
#     global set
#     if key == keyboard.Key.esc:
#         set = False
#         print(set)
#         return False  # stop listener
#     try:
#         k = key.char  # single-char keys
#     except:
#         k = key.name  # other keys
#     if k in ['1', '2', 'left', 'right']:  # keys of interest
#         # self.keys.append(k)  # store it in global-like variable
#         set = True
#         print('Key pressed: ' + k)
#         # return False  # stop listener; remove this if want more keys
#     return True

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    # cap.set(3, 1280)
    # cap.set(4, 720)
    detector = htm.handDetector(maxHands=1)
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
            # listener = keyboard.Listener(on_press=on_press_key)
            # listener.start()
            if set:
                ControlDirectInput(lmList)  # Control Object

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