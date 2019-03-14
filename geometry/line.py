import math


class Line:
    def length(self):
        dx= abs(self.a.x-self.b.x)
        dy=abs(self.a.y-self.b.y)
        return math.sqrt(dx*dx+dy*dy)

    def __init__(self,a,b):
        self.a=a
        self.b=b