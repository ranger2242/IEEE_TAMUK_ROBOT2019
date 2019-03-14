import numpy
from cv2 import cv2

from geometry.rect import Rect


def format(img):
    return numpy.array(img, dtype="uint8")


def view(b, name, img):
    if b:
        cv2.imshow(name, img)
        cv2.waitKey(1)


def getSubImg2(img, r1):
    # r1 is geometry.rect Rect
    # img is gray
    x1 = min(int(r1.a.x), int(r1.c.x))
    x2 = max(int(r1.a.x), int(r1.c.x))
    y1 = min(int(r1.a.y), int(r1.c.y))
    y2 = max(int(r1.a.y), int(r1.c.y))
    if 0 <= x1 < img.shape[1] and 0 <= x2 < img.shape[1] and \
            0 <= y1 < img.shape[0] and 0 <= y2 < img.shape[0]:
        return img[y1:y2, x1:x2]  # the sub image
    else:
        return None


def getSubImg(img, r1):
    # r1 is a cv::RECT of shape [(x,y),ang)]
    # img is GRAY
    r1 = Rect(0, cv2.boxPoints(r1))
    ret = getSubImg2(img, r1)
    if ret is not None:
        return cv2.bitwise_not(ret)
    else:
        return None