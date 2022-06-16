from math import sqrt

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Cercle():
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
        self.centre = Point(x,y)

class Rectangle():
    def __init__(self,x,y,l,h):
        self.x = x
        self.y = y
        self.l = l
        self.h = h


def collision_rectangle_rectangle(r1,r2):
    if( (r2.x >= r1.x + r1.l) or (r2.x + r2.l <= r1.x) or(r2.y >= r1.y + r1.h) or (r2.y + r2.h <= r1.y) ):
        return False
    else:
        return True

def distance(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return sqrt(dx*dx+dy*dy)

def collision_cercle_rectangle(cercle,rect):
    rectangle_cercle = Rectangle(cercle.x-cercle.r,cercle.y-cercle.r,cercle.r*2,cercle.r*2)
    if not collision_rectangle_rectangle(rectangle_cercle,rect):
        return False
    if distance(cercle.centre, Point(rect.x, rect.y)) <= cercle.r or distance(cercle.centre, Point(rect.x, rect.y + rect.h)) <= cercle.r or distance(cercle.centre, Point(rect.x + rect.l, rect.y)) <= cercle.r or distance(cercle.centre, Point(rect.x + rect.l, rect.y + rect.h)) <= cercle.r:
        return True
    
    test_v = abs(cercle.y-(rect.y+rect.h))<= cercle.r or abs(cercle.y-rect.y)<= cercle.r
    test_h = abs(cercle.x-(rect.x+rect.l))<= cercle.r or abs(cercle.x-rect.x)<= cercle.r
    if test_v or test_h:
        return True
    else:
        return False
