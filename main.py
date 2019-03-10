from guis.calibratorGUI import CalibratorGUI
from guis.distanceGUI import DistanceGUI

colorGUI = CalibratorGUI()
distGUI = DistanceGUI()

while True:
    threshArr = colorGUI.mainloop()
    distGUI.mainLoop(threshArr)

