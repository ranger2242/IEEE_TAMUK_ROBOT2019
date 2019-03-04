import time
import win32api
from datetime import datetime

import numpy
import pyautogui as aut
import keyboard
import threading
from cv2 import cv2
from mss import mss

cnt = 0

viewRegions = True
viewFilter = False
enableClicker = True
enableScreenshot = True
enableShop = False
selectMode = False
rectBounds = []
rect = []
prevScr = 0
currScr = 0
# define the list of boundaries
boundaries = [
    ([21, 62, 154], [29, 139, 231]),  # golden cookie
    ([19, 91, 106], [80, 240, 255])  # shop tab
]


def wait():
    global rectBounds, selectMode, rect
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    a = win32api.GetKeyState(0x01)
    if a != state_left:  # Button state changed
        pos = aut.position()
        if pos not in rectBounds:
            rectBounds.append(pos)

        print("CLICK", pos, rectBounds)
        if len(rectBounds) == 2:
            selectMode = False
            print(rectBounds)
            a = rectBounds[0]
            b = rectBounds[1]
            w = abs(a.x - b.x)
            h = abs(a.y - b.y)
            x = min(a.x, b.x)
            y = min(a.y, b.y)
            rect = [x, y, w, h]
            print("RECT", x, y, w, h)


def checkScreenRes():
    while selectMode:
        wait()


def clickShop(thresh):
    keypoints = findRegions(thresh, 30, 0)
    print()
    # global currScr, enableClicker
    # available = []
    # for i in range(0, 12):
    #    st = False
    #    x = 0
    #    y = 0
    #    for j in range(0, 10):
    #        for k in range(0, 10):
    #            x = rect[0] + rect[2] - 170 + j
    #            y = rect[1] + 353 + (i * 64) + k
    #            r, g, b = currScr.pixel(x, y)
    #            if 255 > g > 180:
    #                st = True
    #    if st:
    #        available.append((x, y))
    # if enableClicker:
    #    for i in reversed(available):
    #        x, y = i
    #        aut.click(x, y)
    #    if len(available) > 0:
    #        aut.moveTo(100, 450)


def searchColor(index, lt, ut, blur):
    global boundaries, currScr
    c = 0
    scr = numpy.array(currScr, dtype="uint8")
    scr = cv2.cvtColor(scr, cv2.COLOR_BGR2HSV)
    # for (lower, upper) in boundaries:
    (lower, upper) = boundaries[index]
    lower = numpy.array(lower, dtype="uint8")
    upper = numpy.array(upper, dtype="uint8")
    mask = cv2.inRange(scr, lower, upper)
    output = cv2.bitwise_and(scr, scr, mask=mask)

    output = cv2.blur(output, (blur, blur))
    thresh = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(thresh, lt, ut, cv2.THRESH_BINARY_INV)
    if viewFilter:
        cv2.imshow("-", thresh)
        cv2.moveWindow("-", 900, 0)
        cv2.waitKey(0)
    c += 1
    return thresh


def findRegions(thresh, area, circ):
    global viewRegions
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 3
    params.maxThreshold = 255
    params.filterByArea = True
    params.minArea = area
    params.filterByCircularity = True
    params.minCircularity = circ
    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(thresh)
    trans_blobs = cv2.drawKeypoints(thresh, \
                                    keypoints, numpy.array([]), (0, 0, 255),
                                    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    if viewRegions:
        cv2.imshow("-", trans_blobs)
        cv2.waitKey(0)
    return keypoints


def click(thresh):
    global cnt
    keypoints = findRegions(thresh, 3000, .5)
    #keypoints.sort(key=lambda x: x.pt[1], reverse=False)
    #if len(keypoints)>0:
    #    k = keypoints[len(keypoints)-1]
    #    if k.size > 35:
    #        x = int(k.pt[0])
    #        y = int(k.pt[1])
    #        if enableClicker:
    #            aut.click(x, y)
    #            aut.moveTo(100, 450)
    #            cnt += 1
    #            print(datetime.now(), "Clicked", x, y)
    #            print("Cou6nt: ", str(cnt))

cam =cv2.VideoCapture(0)
def checker():
    global rect, prevScr, currScr, flag, hold
    #threading.Timer(1.0 / 10.0, checker).start()
    prevScr = currScr
    _ , currScr = cam.read()
    click((searchColor(1, 1, 255, 1)))  #click shop and cookies

def mainl():
    global enableShop, enableClicker, cnt, currScr
    try:
        _ , currScr = cam.read()
        cv2.imshow("0", currScr)
        cv2.waitKey(0)
    except KeyboardInterrupt:
        print('\nDone.')
    except TypeError:
        print("typeError")

    # print(aut.position())


# ---------script
#aut.moveTo(100, 450)
if selectMode:
    checkScreenRes()
else:
    rect = (0, 0, 908, 1079)
checker()
while True:
    mainl()
