from math import atan, degrees, atan2

import imutils.convenience as imu
import numpy as np
from PIL import Image

import base
import cv2.cv2
import pytesseract

from geometry.point import Point
from geometry.rect import Rect


class DistanceTracker:

    def find_marker(self, gray, par):
        # convert the image to grayscale, blur it, and detect edges
        gray = cv2.GaussianBlur(gray, (par[0], par[0]), 0)
        edged = cv2.Canny(gray, 35, 125)
        base.view(False, "canny", edged)
        # find the contours in the edged image and keep the largest one;
        # we'll assume that this is our piece of paper in the image
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imu.grab_contours(cnts)
        if len(cnts) > 0:
            cnts = sorted(cnts, key=cv2.contourArea)
            cnts.reverse()
            # c = max(cnts, key=cv2.contourArea)

        # compute the bounding box of the of the paper region and return it
        boxes = []
        i = 0
        for c in cnts:
            if len(cnts) > i and i < 6:
                r = cv2.minAreaRect(c)
                boxes.append(r)
            i += 1
        rects = []
        rm = []
        for b in boxes:
            r1 = Rect(0,cv2.boxPoints(b))
            bo = True
            for b2 in rects:
                r2 = Rect(0,cv2.boxPoints(b2))
                if r1.isInscribed(r2) or r2.isInscribed(r1) or r1.dist(r2) < 10 or r1.hasSideLessThan(
                        15) or r1.squareness() < .9:
                    bo = False
            # scan for letter in  subimage

            if bo:
                rects.append(b)
        for r1 in rects:
            roi = base.getSubImg(gray,r1)
            if roi is not None:
                n = 5
                if roi.shape[0] >n and roi.shape[1] >n:
                    kernel = np.ones((n,n), np.uint8)
                    roi= cv2.blur(roi,(9,9))
                    roi = cv2.erode(roi, kernel, iterations=2)
                    ret, roi = cv2.threshold(roi, 20, 255, cv2.THRESH_BINARY_INV)

                    #roi = cv2.dilate(roi, kernel, iterations=1)


                    base.view(True, "roi", roi)
                    im_pil = Image.fromarray(roi)
                    try:
                        text = pytesseract.image_to_string(im_pil)
                        if len(text) > 0:
                            print(text)
                    except SystemError:
                        print("BOUNDS")

        return rects

    def distance_to_camera(self, knownWidth, focalLength, perWidth):
        # compute and return the distance from the maker to the camera
        if perWidth != 0:
            return (knownWidth * focalLength) / perWidth
        else:
            return 0

    def loop(self, thresh, par):
        # # loop over the images
        # load the furst image that contains an object that is KNOWN TO BE 2 feet
        # from our camera, then find the paper marker in the image, and initialize
        # the focal length
        image = thresh
        self.marker = self.find_marker(image, par)
        if self.marker is not None:
            self.focalLength = (96 * self.KNOWN_DISTANCE) / self.KNOWN_WIDTH

            # load the image, find the marker in the image, then compute the
            # distance to the marker from the camera

            marker = self.find_marker(image, par)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

            i = 0
            boxes = []
            for mark in marker:
                inches = self.distance_to_camera(self.KNOWN_WIDTH, self.focalLength, mark[1][0])
                self.dists[i].append(inches)
                self.dists[i].pop(0)
                avg = sum(self.dists[i]) / len(self.dists[i])
                # draw a bounding box around the image and display it
                box = cv2.boxPoints(mark)
                centroid = (int((box[0][0] + box[1][0] + box[2][0] + box[3][0]) / 4),
                            int((box[0][1] + box[1][1] + box[2][1] + box[3][1]) / 4))
                cCtr = (320, 240)
                angle = -degrees(atan2((centroid[1] - cCtr[1]), (centroid[0] - cCtr[0])))
                box = np.int0(box)
                boxes.append(box)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.line(image, cCtr, centroid, self.colors[i], thickness=2)
                cv2.circle(image, centroid, 4, self.colors[i])
                cv2.drawContours(image, [box], -1, self.colors[i], 2)
                cv2.putText(image, "%.2fft" % (avg / 12), (image.shape[1] - 200, 40 + (30 * i)), font, 1,
                            self.colors[i],
                            3)
                cv2.putText(image, "%.2f" % angle, (0, 40 + (30 * i)), font, 1, self.colors[i], 3)
                cv2.putText(image, str(i), (box[0][0], box[0][1]), font, 1, self.colors[i], 3)

                i += 1
            cv2.imshow("image", image)
            cv2.waitKey(1)
            return boxes

    def __init__(self):
        # initialize the known distance from the camera to the object, which
        # in this case is 24 inches
        self.KNOWN_DISTANCE = 12.0
        self.dists = []
        self.colors = [(0, 0, 255), (255, 0, 213), (255, 0, 0), (255, 175, 9), (0, 255, 0), (0, 255, 255)]
        for i in range(0, 6):
            self.dists.append(list(np.zeros((15,), dtype=int)))
        # initialize the known object width, which in this case, the piece of
        # paper is 12 inches wide
        self.KNOWN_WIDTH = 1.5
