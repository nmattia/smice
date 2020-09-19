import pyautogui
import time
import math
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

def now_s():
    return int(round(time.time()))

looking = { 'where': "", 'forced': False }

where = "where"
forced = "forced"

def articifial_intel():
    _, frame = webcam.read()

    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    if gaze.is_blinking():
        return tracked
    elif gaze.is_right():
        return "right"
    elif gaze.is_left():
        return "left"
    elif gaze.is_center():
        return "left"
    else:
        return "right"

def user_looking_where():
    now_looking = articifial_intel()
    if now_looking == looking[where]:
        looking[forced] = False
        return now_looking
    else:
        if not looking[forced]:
            looking[where] = now_looking
        return looking[where]

def tell_user_looking(whr):
    looking[where] = whr
    looking[forced] = True

start_s = now_s()

screenWidth, screenHeight = pyautogui.size()
mid_x = screenWidth / 2

currentMouseX, currentMouseY = pyautogui.position()

tracked = "left"

left = { 'x': 0, 'y' : 0 }
right = { 'x': 0, 'y' : 0 }

x = 'x'
y = 'y'

cursors = { 'left' : left, 'right' : right }

def other():
    global tracked
    return "left" if tracked == "right" else "right"

def crossed():
    global tracked
    global cursors
    if tracked == "left":
        return cursors[tracked][x] > mid_x
    else:
        return cursors[tracked][x] < mid_x

if currentMouseX < mid_x:
    tracked = "left"
    left[x] = currentMouseX if currentMouseX < mid_x else screenWidth / 4
    left[y] = currentMouseY

    right[x] = mid_x + screenWidth / 4
    right[y] = screenHeight / 2
else:
    tracked = "right"
    left[x] = screenWidth / 4
    left[y] = screenHeight / 2

    right[x] = currentMouseX
    right[y] = currentMouseY

cursor = cursors[tracked]

global still_minus_1
still_minus_2 = cursor[x]
still_minus_1 = cursor[x]
still_minus_0 = cursor[x]

print(still_minus_1)

def still():

    global still_minus_0
    global still_minus_1
    global still_minus_2

    still_minus_2 = still_minus_1
    still_minus_1 = still_minus_0

    currentMouseX, _ = pyautogui.position()
    still_minus_0 = currentMouseX
    return still_minus_2 == still_minus_1 and still_minus_1 == still_minus_0

while now_s() - start_s < 60:
    # for _ in range(1,100):
        # print("")

    if cursors["left"][x] > mid_x:
        print("EERRROOOR LEFT")

    if cursors["right"][x] < mid_x:
        print("EERRROOOR RIGHT")
    user_looking = user_looking_where()

    if tracked != user_looking:
        tracked = user_looking
        cursor = cursors[tracked]
        pyautogui.moveTo(cursor[x], cursor[y])

    is_still = still()

    currentMouseX, currentMouseY = pyautogui.position()

    if tracked == "left" and currentMouseX > mid_x or tracked == "right" and currentMouseX < mid_x:
        print("CROSS")
        tracked = other()
        tell_user_looking(tracked)
    else:
        print("")

    if is_still:
        cursors[tracked][x] = currentMouseX
        cursors[tracked][y] = currentMouseY

    print('left  {}'.format(left))
    print('right {}'.format(right))
    print('tracked  {}'.format(tracked))
    print('looking {}'.format(looking))
    print('AI {}'.format(articifial_intel()))
    print('still {}'.format(is_still))
    time.sleep(0.1)

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"
