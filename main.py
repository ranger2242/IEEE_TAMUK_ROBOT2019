from cv2 import cv2
import base
from guis.calibratorGUI import CalibratorGUI
from guis.denoiserGUI import DenoiserGUI
from guis.distanceGUI import DistanceGUI

colorGUI = CalibratorGUI()
distGUI = DistanceGUI()
noiseGUI = DenoiserGUI()
cam = cv2.VideoCapture(0)

pScr = 0
cScr = 0

while True:
    pScr = cScr
    _, cScr = cam.read()
    cScr = base.format(cScr)
    scr =cScr.copy()
    denoised = noiseGUI.mainLoop(scr)
    threshArr = colorGUI.mainloop(denoised)
    distGUI.mainLoop(threshArr)

