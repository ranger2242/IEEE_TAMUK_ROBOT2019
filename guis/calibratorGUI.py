from tkinter import *
from trackers import colorFinder


class CalibratorGUI:

    def getLowB(self):
        return [self.hsvScl[0].get(), self.hsvScl[1].get(), self.hsvScl[2].get()]

    def getHighB(self):
        return [self.hsvScl[3].get(), self.hsvScl[4].get(), self.hsvScl[5].get()]

    def getThresh(self):
        return self.threshScl[0].get(), self.threshScl[1].get(), self.threshScl[2].get()

    def getNoise(self):
        return self.noiseScl[0].get() - 1, self.noiseScl[1].get() - 1, self.noiseScl[2].get(), self.noiseScl[3].get()

    def bnd(self, x, lb, hb):
        return max(lb, min(x, hb))

    def updateBoundVal(self):
        colorFinder.updateBnd((self.getLowB(), self.getHighB()))
        self.addToBounds()

    def updateThreshVal(self):
        colorFinder.updateThr(self.getThresh())
        self.addToBounds()

    def updateNoiseVal(self):
        colorFinder.updateNoise(self.getNoise())
        self.addToBounds()

    def addToBounds(self, n):  # -----------------------------------------------------------------
        ind = int(self.filterSelected.get())
        self.bounds[ind] = (self.getLowB(), self.getHighB(), self.getThresh(), self.getNoise())
        for x in self.bounds:
            print(x)
        print("-----------------------------------------------------------")

    def setLow(self):
        hsv = colorFinder.getCenterVal()
        for i in range(0, 3):
            self.hsvScl[i].set(hsv[i])

    def setHigh(self):
        hsv = colorFinder.getCenterVal()
        for i in range(3, 6):
            self.hsvScl[i].set(hsv[i-3])

    def printCtrHSVVal(self):
        print(colorFinder.getCenterVal())

    def getCtrHSVVal(self):
        hsv = colorFinder.getCenterVal()
        v = [
            self.bnd(hsv[0] - 5, 0, 255), self.bnd(hsv[1] - 80, 0, 255), 0,
            self.bnd(hsv[0] + 5, 0, 255), self.bnd(hsv[1] + 80, 0, 255), 255
        ]
        for i in range(0, 6):
            self.hsvScl[i].set(v[i])
    def swap(self,i):
        t= self.hsvScl[i].get()
        r = self.hsvScl[i+3].get()
        self.hsvScl[i].set(r)
        self.hsvScl[i+3].set(t)

    def setAllSliders(self):
        s = self.bounds[int(self.filterSelected.get())]
        low, high, thr, noise = s
        for i in range(0, 3):
            self.hsvScl[i].set(low[i])
        for i in range(3, 6):
            self.hsvScl[i].set(high[i - 3])
        for i in range(0, 3):
            self.threshScl[i].set(thr[i])
        for i in range(0, 4):
            self.noiseScl[i].set(noise[i])

    def makeScale(self, label, frame):
        return Scale(frame, label=label, from_=self.pa[0], to=self.pa[1], resolution=self.pa[2], length=self.pa[3],
                     orient=self.pa[4], command=self.addToBounds)

    def addToHSV(self, slide, side="top"):
        slide.pack(in_=self.hsvFrame, side=side)

    def addToThresh(self, button):
        button.pack(in_=self.threshFrame, side="top")

    def dumpAll(self):
        print("LOW_HSV", self.getLowB())
        print("HIGH_HSV", self.getHighB())
        print("THRESH", self.getThresh())
        print("NOISE", self.getNoise())

        with open('colorConfig.txt', 'w') as filehandle:
            for listitem in self.bounds:
                for list in listitem:
                    for x in list:
                        filehandle.write(str(x) + ' ')
                filehandle.write('\n')

    def buildHSVBoundTweaker(self):
        self.hsvScl = [
            self.makeScale("Low H", self.hsvFrame),
            self.makeScale("Low S", self.hsvFrame),
            self.makeScale("Low V", self.hsvFrame),
            self.makeScale("High H", self.hsvFrame),
            self.makeScale("High S", self.hsvFrame),
            self.makeScale("High V", self.hsvFrame)
        ]

        self.hsvScl[3].set(255)
        self.hsvScl[4].set(255)
        self.hsvScl[5].set(255)
        self.hsvFrame.pack(side="top", fill="both", expand=True)
        self.hsvSubFrame.pack(side="bottom")

        self.hSwap = Button(self.hsvSubFrame, text="Swap h", command=lambda: self.swap(0))
        self.sSwap = Button(self.hsvSubFrame, text="Swap s", command=lambda: self.swap(1))
        self.vSwap = Button(self.hsvSubFrame, text="Swap v", command=lambda: self.swap(2))

        self.vSwap.pack(anchor="w", side="right")
        self.sSwap.pack(anchor="w", side="right")
        self.hSwap.pack(anchor="w", side="right")

        for s in self.hsvScl:
            self.addToHSV(s)

    def buildThreshTweaker(self):
        self.threshScl = [
            self.makeScale("TR High", self.threshFrame),
            self.makeScale("TR Low", self.threshFrame),
            Scale(self.threshFrame, label="TR Blur", from_=1, to=30, resolution=self.pa[2], length=self.pa[3],
                  orient=self.pa[4], command=self.addToBounds)]
        self.threshScl[0].set(255)
        self.threshScl[1].set(0)
        self.threshScl[2].set(1)
        self.threshFrame.pack(side="top", fill="both", expand=True)

        for s in self.threshScl:
            self.addToThresh(s)

    def buildNoiseTweaker(self):
        self.noiseScl = [
            Scale(self.noiseFrame, label="templateWindowSize ", from_=0, to=71, resolution="2", length=self.pa[3],
                  orient=self.pa[4], command=self.addToBounds),
            Scale(self.noiseFrame, label="searchWindowSize ", from_=0, to=71, resolution="2", length=self.pa[3],
                  orient=self.pa[4], command=self.addToBounds),
            Scale(self.noiseFrame, label="h", from_=1, to=100, resolution="1", length=self.pa[3], orient=self.pa[4],
                  command=self.addToBounds),
            Scale(self.noiseFrame, label="hC", from_=1, to=100, resolution="1", length=self.pa[3], orient=self.pa[4],
                  command=self.addToBounds)

        ]
        self.noiseScl[0].set(5)
        self.noiseScl[1].set(11)
        self.noiseFrame.pack(side="top", fill="both", expand=True)

        for s in self.noiseScl:
            s.pack(in_=self.noiseFrame, side="top")

    def __init__(self):
        reset = ([0, 0, 0], [255, 255, 255], (255, 0, 1), (5, 1, 1, 1))
        self.bounds = []  # [d,d,d,d,d,d,d]

        self.hsvScl = []
        self.threshScl = []
        self.noiseScl = []
        self.pa = ("0", "255", "1", "400", "horizontal")
        self.window = Tk()
        self.window.title("COLOR FILTER TWEAKER")
        self.tweakerFrame = Frame(self.window)
        self.threshFrame = Frame(self.tweakerFrame)
        self.threshSubFrame = Frame(self.threshFrame)
        self.hsvFrame = Frame(self.tweakerFrame, borderwidth=2, relief="groove", padx=3, pady=3)
        self.hsvSubFrame = Frame(self.hsvFrame)
        self.noiseFrame = Frame(self.tweakerFrame, borderwidth=2, relief="groove")
        self.noiseSubFrame = Frame(self.noiseFrame)
        self.selectorFrame = Frame(self.window)

        self.tweakerFrame.pack(side="right")
        self.buildHSVBoundTweaker()
        self.buildThreshTweaker()
        self.buildNoiseTweaker()

        # build selector frame ================================
        self.filterSelected = StringVar()

        self.light = [
            Radiobutton(self.selectorFrame, text='Light0', variable=self.filterSelected, value=0,
                        command=self.setAllSliders),
            Radiobutton(self.selectorFrame, text='Light1', variable=self.filterSelected, value=1,
                        command=self.setAllSliders),
            Radiobutton(self.selectorFrame, text='Light2', variable=self.filterSelected, value=2,
                        command=self.setAllSliders),
            Radiobutton(self.selectorFrame, text='Light3', variable=self.filterSelected, value=3,
                        command=self.setAllSliders)
        ]
        self.block = Radiobutton(self.selectorFrame, text='Block', variable=self.filterSelected, value=4,
                                 command=self.setAllSliders)
        self.ship = Radiobutton(self.selectorFrame, text='Ship', variable=self.filterSelected, value=5,
                                command=self.setAllSliders)
        self.obstacle = Radiobutton(self.selectorFrame, text='Obstacle', variable=self.filterSelected, value=6,
                                    command=self.setAllSliders)

        self.selectorFrame.pack(side="left")

        self.light[0].pack(anchor="w")
        self.light[1].pack(anchor="w")
        self.light[2].pack(anchor="w")
        self.light[3].pack(anchor="w")
        self.block.pack(anchor="w")
        self.ship.pack(anchor="w")
        self.obstacle.pack(anchor="w")

        self.light[0].select()

        self.subFrame = Frame(self.selectorFrame)
        self.subFrame.pack(side="bottom")

        self.lowTarget = Button(self.subFrame, text="LOW", command=self.setLow)
        self.highTarget = Button(self.subFrame, text="HIGH", command=self.setHigh)
        self.dump = Button(self.subFrame, text="DUMP", command=self.dumpAll)
        self.ctr = Button(self.subFrame, text="PRINT CENTER", command=self.printCtrHSVVal)

        self.lowTarget.pack(anchor="w", side="right")
        self.highTarget.pack(anchor="w", side="right")
        self.ctr.pack(anchor="w", side="left")

        self.dump.pack(anchor="w", side="right")
        # =================================================================
        with open('colorConfig.txt', 'r') as filehandle:
            for line in filehandle:
                b = line[:-1]
                a = [int(x) for x in b.split()]
                d = ([a[0], a[1], a[2]], [a[3], a[4], a[5]], (a[6], a[7], a[8]), (a[9], a[10], a[11], a[12]))

                self.bounds.append(d)
            self.setAllSliders()

    def mainloop(self,scr):

        self.window.update()
        return colorFinder.loop(self.bounds, int(self.filterSelected.get()),scr)
