"""
E-521
Equation x^2 + y^2 = 1 - 376014x^2 * y^2
Mod Prime  :2^521 - 1
Base Point :(1571054894184995387535939749894317568645297350402905821437625181152304994381188529632591196067604100772673927915114267193389905003276673749012051148356041324,12) 

This doesn't uses the curve M-511
Equation   :y^2 = x^3+530438x^2+x
Mod Prime  :2^511 - 187
Base Point :(5,2500410645565072423368981149139213252211568685173608590070979264248275228603899706950518127817176591878667784247582124505430745177116625808811349787373477)
"""
from directory.EllipticCurve import *
from directory.Prime import Rand_Prime

Point = E521_Base.copy()
Point2 = E521_Base.copy()

add(Point,Point2)
add(Point,Point2)
add(Point,Point2)

mult(Point2,4)
print(Point.x,Point.y)
print(Point2.x,Point2.y)
"""A = Rand_Prime(pow(2,128),pow(2,256))
B = Rand_Prime(pow(2,128),pow(2,256))
print(A,'\n',B)

mult(Point,A)
mult(Point2,B)
print("\n\n\n")
print(Point.x,Point.y,'\n')
print(Point2.x,Point2.y)

mult(Point,B)
mult(Point2,A)
print("\n\n\n")
print(Point.x,Point.y,'\n')
print(Point2.x,Point2.y)"""
