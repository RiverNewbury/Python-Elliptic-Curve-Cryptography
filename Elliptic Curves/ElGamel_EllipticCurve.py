"""
E-521
Equation x^2 + y^2 = 1 - 376014x^2 * y^2
Mod Prime  :2^521 - 1
Base Point :(1571054894184995387535939749894317568645297350402905821437625181152304994381188529632591196067604100772673927915114267193389905003276673749012051148356041324,12)
"""
from directory.EllipticCurve import *
from directory.Prime import Rand_Prime


Message = 100 *  1267321589873549842319


Point = E521_Base.copy()
Point2 = E521_Base.copy()

if Message>Point.curve.n - 100:
    raise Error("The message once mapped to a value must be lower than the modulus")

MessagePoint = point(E521,Message,0)
# Point3 = point(E521,Base[0],Base[1])




# Server Side
A = Rand_Prime(pow(2,128),pow(2,256))
# This is the Server's Private Key
mult(Point,A)
print("public key",Point.x,Point.y)



# User Side
B = Rand_Prime(pow(2,128),pow(2,256))
# This is the Users random Number
mult(Point2,B)
Point3 = Point.copy()
mult(Point3,B)
for i in range (100):
    findycoordinate(MessagePoint)
    if MessagePoint.y != "Has no y":
        break;
    else:
        MessagePoint.x += 1
if MessagePoint.y == "Has no y":
    raise Error("Looks like this point can't be mapped onto the curve, sorry :(")
add(Point3,MessagePoint)
print("Sent back\t: ({0},{1}),({2},{3})".format(Point2.x,Point2.y,Point3.x,Point3.y))



# Server Side
mult(Point2,A)
sub(Point3,Point2)
print("Message Recieved\t:",Point3.x)
