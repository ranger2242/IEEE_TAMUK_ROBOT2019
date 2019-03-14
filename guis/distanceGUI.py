from tkinter import *
from trackers.distance import DistanceTracker


class DistanceGUI:

    def update(self,n):
        self.par = [int(self.blur.get()-1)]

    def mainLoop(self, threshArr):
        # make this return (distance, angle)
        boxArr = []
        for i in range(0, len(threshArr)):
            if i == 0:
                boxArr.append(self.distTr.loop(threshArr[i], self.par))
        return boxArr

    def __init__(self):
        self.distTr = DistanceTracker()
        self.pa = ("0", "255", "1", "400", "horizontal")
        self.par=[5]
        self.window = Tk()
        self.window.title("DISTANCE TWEAKER")
        self.blur = Scale(self.window, label="Dist Blur", from_=2, to=30, resolution=2,
                          length=self.pa[3],
                          orient=self.pa[4], command=self.update)
        self.blur.set(5)
        self.blur.pack()
