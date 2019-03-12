import numpy
from cv2 import cv2


def format(img):
    return numpy.array(img, dtype="uint8")

def view(b, name, img):
    if b:
        cv2.imshow(name, img)
        cv2.waitKey(1)

