import cv2
import numpy as np
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image


im =  cv2.imread('block2.jpg')
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

kernel = np.ones((5,5), np.uint8)


ret,thresh1 = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
img_erosion = cv2.erode(im, kernel, iterations=1)

cv2.imshow('38',img_erosion)
print(pytesseract.image_to_string(Image.open('block2.jpg')))
cv2.waitKey(0)
