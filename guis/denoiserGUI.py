from tkinter import *
import cv2

class DenoiserGUI:

    def update(self,n):
        i = 0
        for s in self.noiseScl:
            self.vals[i]=s.get()
            i+=1

    def nlDenoising(self,img,params):
        #image in BGR
        return cv2.fastNlMeansDenoisingColored(img, None, params[2], params[3], params[0],params[1])

    def bilateralDenoising(self,img):
        #image must be grayscale
        return cv2.bilateralFilter(img, self.vals[0], self.vals[1], self.vals[2])


    def mainLoop(self,scr):
        return self.bilateralDenoising(scr,)

    def __init__(self):
        self.window = Tk()
        self.bilateralFrame = Frame(self.window)
        l = 400
        orient = 'horizontal'
        self.vals =[9,75,75]
        self.noiseScl = [
            Scale(self.bilateralFrame, label="d",
                  from_=1, to=255, resolution="1", length=l, orient=orient, command=self.update),
            Scale(self.bilateralFrame, label="sigmaColor ",
                  from_=0, to=255, resolution="1", length=l, orient=orient, command=self.update),
            Scale(self.bilateralFrame, label="sigmaSpace",
                  from_=0, to=255, resolution="1", length=l, orient=orient, command=self.update)
        ]
        self.bilateralFrame.pack(side="top", fill="both", expand=True)

        i = 0
        for s in self.noiseScl:
            s.set(self.vals[i])
            i+=1

        for s in self.noiseScl:
            s.pack(in_=self.bilateralFrame, side="top")
