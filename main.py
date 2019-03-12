from guis.calibratorGUI import CalibratorGUI
from guis.distanceGUI import DistanceGUI
import trackers.cornerDetect as corner

colorGUI = CalibratorGUI()
distGUI = DistanceGUI()

while True:
    threshArr = colorGUI.mainloop()
    distGUI.mainLoop(threshArr)

