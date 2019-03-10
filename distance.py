import imutils.convenience as imu
import numpy as np
import basic
import cv2.cv2


class DistanceTracker:

    def find_marker(self, gray,par):
        # convert the image to grayscale, blur it, and detect edges
        gray = cv2.GaussianBlur(gray, (par[0], par[0]), 0)
        edged = cv2.Canny(gray, 35, 125)
        basic.view(True,"canny",edged)
        # find the contours in the edged image and keep the largest one;
        # we'll assume that this is our piece of paper in the image
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imu.grab_contours(cnts)
        if len(cnts)>0:
            c = max(cnts, key=cv2.contourArea)

        # compute the bounding box of the of the paper region and return it
            return cv2.minAreaRect(c)
        else:
            return None

    def distance_to_camera(self, knownWidth, focalLength, perWidth):
        # compute and return the distance from the maker to the camera
        return (knownWidth * focalLength) / perWidth

    def loop(self, thresh,par):
        # # loop over the images
        # load the furst image that contains an object that is KNOWN TO BE 2 feet
        # from our camera, then find the paper marker in the image, and initialize
        # the focal length
        image = thresh
        self.marker = self.find_marker(image,par)
        if self.marker is not None:
            self.focalLength = (96 * self.KNOWN_DISTANCE) / self.KNOWN_WIDTH

            # load the image, find the marker in the image, then compute the
            # distance to the marker from the camera

            marker = self.find_marker(image,par)
            inches = self.distance_to_camera(self.KNOWN_WIDTH, self.focalLength, self.marker[1][0])
            image=cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
            # draw a bounding box around the image and display it
            box = cv2.boxPoints(marker)
            box = np.int0(box)
            cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
            cv2.putText(image, "%.2fft" % (inches / 12),
                        (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                        2.0, (0, 255, 0), 3)
            cv2.imshow("image", image)
            cv2.waitKey(1)

    def __init__(self):
        # initialize the known distance from the camera to the object, which
        # in this case is 24 inches
        self.KNOWN_DISTANCE = 12.0

        # initialize the known object width, which in this case, the piece of
        # paper is 12 inches wide
        self.KNOWN_WIDTH = 1.5
