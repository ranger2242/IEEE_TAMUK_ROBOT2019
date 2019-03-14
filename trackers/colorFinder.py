import numpy
from cv2 import cv2
import base
import trackers.obj3dTracker as dec
import trackers.cornerDetect as corner

viewNoiseFilter = False
viewInput = True
viewRegions = False
viewFilter = True

ctrHSV = [0, 0, 0]
ctrBGR = [0, 0, 0]
ctrPos = (0, 0)
boundaries = ([0, 0, 0], [255, 255, 255])  # define the list of color HSV boundaries


blur = 1
trHigh = 255
trLow = 0
trVals = (255, 0, 1)
nVals = (5, 11, 1, 1)

cScr=0

def updateBnd(vals):
    global boundaries
    boundaries = (vals[0], vals[1])


def updateThr(vals):
    global trVals
    print(vals)
    trVals = vals


def updateNoise(vals):
    global nVals
    print(vals)
    nVals = vals


def adder(l, h):
    global boundaries
    boundaries.insert(0, (l, h))


def getCenterVal():  # ===============================
    global ctrPos,cScr
    y = int(len(cScr) / 2)
    x = int(len(cScr[0]) / 2)
    ctrPos = (x, y)
    bgr = numpy.uint8([[cScr[y][x]]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[0][0]
    bgr = bgr[0][0]
    print("BGR", bgr, "HSV", hsv)
    return hsv


def searchColor(scr, lower, upper, thr, show):
    c = 0
    img = scr.copy()
    img = cv2.circle(img, (320, 240), 10, (0, 0, 255))

    # scr = cv2.resize(scr, (240, 160))
    base.view(show, "Input", img)

    lower = base.format(lower)
    upper = base.format(upper)

    mask = cv2.inRange(scr, lower, upper)

    output = cv2.bitwise_and(scr, scr, mask=mask)

    thresh = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(thresh, thr[1], thr[0], cv2.THRESH_BINARY)

    base.view(False, "Thresh", thresh)

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
    base.view(viewRegions, "Regions", trans_blobs)
    return keypoints


def loop(params, show,scr):
    global cScr
    cScr=scr
    scr = cv2.blur(scr, (params[0][2][2], params[0][2][2]))
    scr = cv2.cvtColor(scr, cv2.COLOR_BGR2HSV)
    threshes = []
    for p in params:
        if len(p) == 4:
            b = params.index(p) == show
            threshes.append(searchColor(scr, lower=p[0], upper=p[1], thr=p[2], show=b))
    #dec.track3d(threshes[0])
    #corner.harrisCorners(threshes[0])
    return threshes
