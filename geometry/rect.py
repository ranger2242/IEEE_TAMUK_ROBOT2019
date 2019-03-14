from math import floor

from geometry.line import Line
from geometry.point import Point
from geometry.triangle import Triangle


class Rect:
    def hasSideGreaterThan(self, i):
        for s in self.sidesLengths():
            if s > i:
                return True
        return False

    def hasSideLessThan(self, i):
        for s in self.sidesLengths():
            if s < i:
                return True
        return False

    def squareness(self):
        s = self.sidesLengths()
        a = min(s[0],s[1])
        b = max(s[0],s[1])
        if b != 0:
            return a/b
        else:
            return 0

    def area(self):
        lA = Line(self.a, self.b)
        lB = Line(self.a, self.d)
        return lA.length() * lB.length()

    def center(self):
        x = (self.a.x + self.b.x + self.c.x + self.d.x) / 4
        y = (self.a.y + self.b.y + self.c.y + self.d.y) / 4
        return Point(x, y)

    def dist(self, r2):
        return Line(self.center(), r2.center()).length()

    def points(self):
        return self.a, self.b, self.c, self.d

    def initType0(self,pointArr):
        self.a = Point(pointArr[0][0], pointArr[0][1])
        self.b = Point(pointArr[1][0], pointArr[1][1])
        self.c = Point(pointArr[2][0], pointArr[2][1])
        self.d = Point(pointArr[3][0], pointArr[3][1])

    def initType1(self,p,w,h):
        self.a = Point(p[0],p[1])
        self.b = Point(p[0]+w,p[1])
        self.c = Point(p[0]+w,p[1]+h)
        self.d = Point(p[0],p[1]+h)

    def __init__(self,type, pointArr=None,topLeft=None,width=0,height=0):
        #type
        # 0
        # pointArr->Explicit array of points [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
        #
        # 1
        # topLeft   -> top left corner of rectangle (x,y)
        # width     -> width of rectangle
        # height    -> height of rectangle

        if type==0:
            self.initType0(pointArr)
        elif type==1:
            self.initType1(topLeft,width,height)



    def isInscribed(self, r2):
        check = r2.points()
        for i in range(0, 4):
            t1 = Triangle(self.a, self.b, check[i])
            t2 = Triangle(self.c, self.b, check[i])
            t3 = Triangle(self.c, self.d, check[i])
            t4 = Triangle(self.d, self.a, check[i])
            a1 = floor(self.area())
            a2 = floor(t1.area() + t2.area() + t3.area() + t4.area())
            # print(a1,a2,"AREAS")
            if a2 > a1:
                return False
        return True

    def sidesLengths(self):
        return [Line(self.a, self.b).length(),
                Line(self.b, self.c).length(),
                Line(self.c, self.d).length(),
                Line(self.d, self.a).length()]
