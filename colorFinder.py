import numpy
from cv2 import cv2

viewNoiseFilter = False
viewInput = True
viewRegions = False
viewFilter = True

ctrHSV = [0, 0, 0]
ctrBGR = [0, 0, 0]
ctrPos = (0, 0)
boundaries = ([0, 0, 0], [255, 255, 255])  # define the list of color HSV boundaries

pScr = 0
cScr = 0
blur = 1
trHigh = 255
trLow = 0
trVals = (255, 0, 1)
nVals = (5, 11, 1, 1)

cam = cv2.VideoCapture(0)


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
    global ctrPos, cScr
    y = int(len(cScr) / 2)
    x = int(len(cScr[0]) / 2)
    ctrPos = (x, y)
    bgr = numpy.uint8([[cScr[y][x]]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[0][0]
    bgr = bgr[0][0]
    print("BGR", bgr, "HSV", hsv)
    return hsv


def view(b, name, img):
    if b:
        cv2.imshow(name, img)
        cv2.waitKey(1)


def format(img):
    return numpy.array(img, dtype="uint8")


def searchColor(scr, lower, upper, thr, noise,show):
    c = 0

    # scr = cv2.resize(scr, (240, 160))
    #scr = cv2.fastNlMeansDenoisingColored(scr, None, noise[2], noise[3], noise[0], noise[1])
    #view(False, "Noise", scr)
    lower = format(lower)
    upper = format(upper)
    mask = cv2.inRange(scr, lower, upper)

    output = cv2.bitwise_and(scr, scr, mask=mask)

    output = cv2.blur(output, (thr[2], thr[2]))

    thresh = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(thresh, thr[1], thr[0], cv2.THRESH_BINARY)

    view(show, "Input", scr)
    view(show, "Thresh", thresh)

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
    view(viewRegions, "Regions", trans_blobs)
    return keypoints


def loop(params,show):
    global pScr, cScr
    pScr = cScr
    _, cScr = cam.read()
    cScr = format(cScr)
    scr = cv2.cvtColor(cScr, cv2.COLOR_BGR2HSV)

    for p in params:
        if len(p)==4:
            b = params.index(p) == show
            searchColor(scr, lower=p[0], upper=p[1], thr=p[2], noise=p[3], show=b)