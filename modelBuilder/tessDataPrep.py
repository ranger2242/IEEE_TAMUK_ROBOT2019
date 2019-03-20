from random import randint
from tkinter import *
from tkinter import filedialog
from os import listdir
from os.path import isfile, join

import numpy
from cv2 import cv2

# window = Tk()

# set up cropper
# next button
# iterate through data folder
# use roi selector to select bounding boxes
# crop images
# process images as if program ran
# display final
# save final to output folder
import base
from geometry.rect import Rect

folder = filedialog.askdirectory() + "/"
files = [f for f in listdir(folder) if isfile(join(folder, f))]

crops = []
imgIndex = 0


def loadImg(path):
    # path is full direct path to image
    print("Attempt load: ", path)
    img = cv2.imread(path)
    if img is not None:
        scl = .3
        x = int(img.shape[0] * scl)
        y = int(img.shape[1] * scl)
        img = cv2.resize(img, (x, y))
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # uncomment after extracting the process
        # img = processLikeRealGame(img)
    return img


def add(sub):
    global crops
    crops.append(sub)
    print('ADDED index', len(crops))


def roiTool(img):
    global imgIndex
    while True:
        # draw bounding boxes over objects
        # selectROI's default behaviour is to draw box starting from the center
        # when fromCenter is set to false, you can draw box starting from top left corner
        bbox = cv2.selectROI('ROI', img)
        if bbox[0] != 0 and bbox[1] != 0:
            print(bbox)
            rect = Rect(1, topLeft=(bbox[0], bbox[1]), width=bbox[2], height=bbox[3])
            sub = base.getSubImg2(img, rect)
            cv2.imshow("SUB", sub)

            k = cv2.waitKey(0) & 0xFF
            if k == ord('n'):  # save image and move on
                add(sub)
                imgIndex += 1
                print("NEXT IMG")
                break
            elif k == ord('r'):
                print("REDO")
            else:
                add(sub)


for f in files:
    print(f)
print("Loaded", len(files), "images")

run = True
save = False
while run:
    if imgIndex < len(files):
        img = loadImg(folder + files[imgIndex])
        if img is not None:
            roiTool(img)
    else:
        print("SAVING FILES")
        # write the files
        i = 0
        for c in crops:
            # path= "C:/Users/Chris/Google Drive/PYTHON/robot/modelBuilder/tesseractData/eng.stencil.exp"+str(i)+".png"
            path = "C:/Users/Chris/Google Drive/PYTHON/robot/" \
                   "modelBuilder/tesseractData/split/" + str(i) + ".png"
            print("WRITING FILE:", path)
            im = crops[i]
            height, width, channels = im.shape
            print(i, height, width, channels)
            # Create a black image
            x = height if height > width else width
            y = height if height > width else width
            square = numpy.zeros((x, y, 3), numpy.uint8)
            square = cv2.bitwise_not(square)
            #
            # This does the job
            #
            x1 = int((x - width) / 2)
            x2 = int(x - (x - width) / 2)
            y1 = int((y - height) / 2)
            y2 = int(y - (y - height) / 2)
            square[y1:y2, x1:x2] = im
            s =100/square.shape[1]
            square =cv2.resize(square,(int(s*square.shape[1]),int(s*square.shape[0])))
            cv2.imwrite(path, square)
            i += 1
        run = False
print("END PROGRAM")