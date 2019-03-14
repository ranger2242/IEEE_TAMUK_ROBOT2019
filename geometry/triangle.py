import math

from geometry.line import Line
from geometry.point import Point


class Triangle:
    def area(self):
        sa = Line(self.a, self.b)
        sb = Line(self.c, self.b)
        sc = Line(self.a, self.c)
        s = (sa.length()+sb.length()+sc.length())/2
        return abs(s*(s-sa.length())*(s-sb.length())*(s-sc.length()))**.5

    def __init__(self, a, b, c):
        # a, b, c are points
        self.a = a
        self.b = b
        self.c = c
