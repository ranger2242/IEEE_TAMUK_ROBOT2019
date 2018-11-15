import cv2
import argparse
import mss
import numpy
import imutils
from tkinter import *
from PIL import ImageTk
import png

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

window = Tk()
whiteScl = Scale(window, label="WHITE", from_="0", to="255", length="400", orient="horizontal")
stepScl = Scale(window, label="STEP", from_="3", to="31", resolution="2", length="400", orient="horizontal")
cnstScl = Scale(window, label="C", from_="-100", to="100", resolution=".05", length="400", orient="horizontal")

global thr
thr = cv2.THRESH_BINARY_INV
thrGroup = [
    Radiobutton(window, text="BINARY", padx=20, command=lambda: setThresh(0), value=0),
    Radiobutton(window, text="BINARY_INV", padx=20, command=lambda: setThresh(1), value=1),
#    Radiobutton(window, text="TRUNC", padx=20, command=lambda: setThresh(2), value=2),
#    Radiobutton(window, text="TOZERO", padx=20, command=lambda: setThresh(3), value=3),
#    Radiobutton(window, text="TOZERO_INV", padx=20, command=lambda: setThresh(4), value=4)

]

threshVals = [
    cv2.THRESH_BINARY,
    cv2.THRESH_BINARY_INV,
    cv2.THRESH_TRUNC,
    cv2.THRESH_TOZERO,
    cv2.THRESH_TOZERO_INV
]

def testContrast(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    # -----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)

    # -----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    #cv2.imshow('CLAHE output', cl)

    # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl, a, b))
    #cv2.imshow('limg', limg)

    # -----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    print(final)
    return final

def setThresh(ind):
    globals()["thr"] = threshVals[ind]
    print(thr)


def processLoop():
    frame = numpy.array(sct.grab(monitor))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Start timer
    timer = cv2.getTickCount()
    # Update tracker
    ok, bbox = tracker.update(gray)

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

    # ------------------------------- ---------------------------------------------------------
    # compute the absolute difference between the current frame and
    # first frame
    contFrame = testContrast(frame)
    gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray1 = cv2.cvtColor(contFrame, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (11, 11), 0)
    # if ff is None:
    #    ff = gray1
    frameDelta = cv2.absdiff(gray, gray1)

    thresh = cv2.adaptiveThreshold(frameDelta, whiteScl.get(), cv2.ADAPTIVE_THRESH_MEAN_C, thr, stepScl.get() + 1, cnstScl.get())
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # ----------------------------------------------------------------------------------------

    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        # Tracking failure
        cv2.putText(frame, "        Failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display FPS on frame
    #cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

    cv2.imshow("tr", frameDelta)

    cv2.imshow("-", frame)


def task():
    window.after(10, processLoop())  # reschedule event in 2 seconds

    window.after(10, task)  # reschedule event in 2 seconds


if __name__ == '__main__':

    # Set up tracker.
    # Instead of MIL, you can also use

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    args = vars(ap.parse_args())

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    with mss.mss() as sct:
        whiteScl.pack(side="top")
        stepScl.pack(side="top")
        cnstScl.pack(side="top")

        for btn in thrGroup:
            btn.pack(anchor=W)

        # Part of the screen to capture
        monitor = {"top": 40, "left": 0, "width": 800, "height": 640}
        frame = numpy.array(sct.grab(monitor))
        height, width, no_channels = frame.shape
        window.after(166, task())
        window.mainloop()
