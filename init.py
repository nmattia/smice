import pyautogui
import time
import math
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Enables more logging and shows a window with the tracking
debug = False;

# When true, the cursor moves between two monitors (as opposed to between the
# left and right halves of a single monitor)
dualMonitor = True

# Current time since epoch, in seconds
def now_s():
    return int(round(time.time()))

# #IDONTKNOWPYTHON
# where we assume the user is looking, and whether or not it was forced.
# The side is "forced" when the user moves the mouse over to the other side.
looking = { 'where': "", 'forced': False }
where = "where"
forced = "forced"

# Returns "left" or "right" depending on where the user is looking
def articifial_intel():
    _, frame = webcam.read()

    gaze.refresh(frame)
    frame = gaze.annotated_frame()
    if debug:
        cv2.putText(frame, tracked, (90, 130), cv2.FONT_HERSHEY_DUPLEX, 2.0, (147, 58, 31), 1)
        cv2.imshow("Demo", frame)

    if gaze.is_blinking():
        if debug:
            print("BLINK182 (same)")
        return tracked
    elif gaze.is_right():
        if debug:
            print("RIGHT (right)")
        return "right"
    elif gaze.is_left():
        if debug:
            print("LEFT (left)")
        return "left"
    elif gaze.is_center():
        if debug:
            print("CENTER (RIGHT)")
        return "right"
    else:
        if debug:
            print("I GUESS NOT (same)")
        return tracked

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

screenWidth, screenHeight = pyautogui.size()
mid_x = screenWidth if dualMonitor else screenWidth / 2
quarter = screenWidth / 2 if dualMonitor else screenWidth / 4

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
    left[x] = currentMouseX if currentMouseX < mid_x else quarter
    left[y] = currentMouseY

    right[x] = mid_x + quarter
    right[y] = screenHeight / 2
else:
    tracked = "right"
    left[x] = quarter
    left[y] = screenHeight / 2

    right[x] = currentMouseX
    right[y] = currentMouseY

cursor = cursors[tracked]

global still_minus_1
still_minus_2 = cursor[x]
still_minus_1 = cursor[x]
still_minus_0 = cursor[x]

# returns true if the user has _not_ moved the cursor for 3 iterations in a
# row.
def still():

    global still_minus_0
    global still_minus_1
    global still_minus_2

    still_minus_2 = still_minus_1
    still_minus_1 = still_minus_0

    currentMouseX, _ = pyautogui.position()
    still_minus_0 = currentMouseX
    return still_minus_2 == still_minus_1 and still_minus_1 == still_minus_0

frames = 0
start_s = now_s()
last_s=0
while True:

    if cursors["left"][x] > mid_x:
        print("Left cursor is in the right pane, this should not happen")

    if cursors["right"][x] < mid_x:
        print("Right cursor is in the left pane, this should not happen")

    user_looking = user_looking_where()

    # poor man's debouncing; we only update this once a second.
    if now_s() - last_s > 1 and tracked != user_looking:
        tracked = user_looking
        cursor = cursors[tracked]
        pyautogui.moveTo(cursor[x], cursor[y])
        last_s = now_s()

    is_still = still()

    currentMouseX, currentMouseY = pyautogui.position()

    # when the user crosses over we force update the AI result
    if tracked == "left" and currentMouseX > mid_x or tracked == "right" and currentMouseX < mid_x:
        print("CROSS")
        tracked = other()
        tell_user_looking(tracked)

    # only save the cursor position if the user is somewhat still
    if is_still:
        cursors[tracked][x] = currentMouseX
        cursors[tracked][y] = currentMouseY

    if False:
        print('left  {}'.format(left))
        print('right {}'.format(right))
        print('tracked  {}'.format(tracked))
        print('looking {}'.format(looking))
        print('AI {}'.format(articifial_intel()))
        print('still {}'.format(is_still))

    frames+=1
    now = now_s()

    if debug:
        if frames%10 ==0:
            print(frames/(now-start_s))


        if cv2.waitKey(1) == 27:
            break

    time.sleep(0.1)
