
from curves.all import *
class Curve():
    def __init__(self, name, curvetype, a, b, mod):
        self.help = ("Takes the arguments : type of curve, 2 curve parameters "
            "and a modulous to define the curve over the finite field Fq\n"
            "If Weistrass (W) : y^2 = x^3 + ax + b\n"
            "If Montgomery (M) : ay^2 = x^3 + bx^2 + x\n"
            "If Edward (E) : x^2 + y^2 = a^2 * (1 + bx^2 * y^2)\n")
        if str(curvetype).upper() not in ['W','E','M']:
            raise TypeError("That curve type is not currently supported please "
                            "pick Weistrass (W), Montgomery (M) and Edward (E)");
        self.type = str(curvetype).upper()
        self.name = name
        self.a = a
        self.b = b
        self.n = mod
    def copy(self):
        return curve(self.type, self.a, self.b, self.n, self.order);

def create_point(curve, order, x, y, z = 1):
    """
    INPUT   : Curve objects, order of the basepoint, x, y coordinates and optional
    z co-ordinate
    PROCESS : It is necessary to have a function to create the object so that it can
    inherit dynamically, as it needs to inherit one of the curve type specific
    objects.
    OUTPUT  : Point object with parameters put in
    """
    if curve.type == "W":
        parent = WeierstrassCurve
    elif curve.type == "M":
        parent = MontgomeryCurve
    elif curve.type == "E":
        parent = EdwardsCurve

    class Point(parent):
        def __init__(self, curve, x, y, z, order):
            self.help = ("Takes the arguments: curve (should be a curve object)"
                " that the point lies on and the x,y cartesian coordinates or "
                "X,Y,Z where x = X/Z; y = Y/Z")
            self.curve = curve
            self.x = x
            self.y = y
            self.z = z
            self.order = order
            parent.__init__(self)
        def basesub(self, p2):
            p2.negate()
            self.baseadd(p2)
            p2.negate()
        def sub(self,p2):
            self.basesub(p2)
            self.to_affine()
        def double(self):
            self.basedouble()
            self.to_affine()
        def add(self, p2):
            self.baseadd(p2)
            self.to_affine()
        def basemult(self, num):
            """
            INPUT   : An Integer
            PROCESS : Multiplies point by that integer by the double and add method
            OUPUT   : NONE
            """
            neg = 0
            if num<0:
                neg = 1
                num = -num
            working_point = self.copy()
            self.x,self.y,self.z = self.zero
            for i in reversed(bin(num)[2:]):
                if int(i):
                    self.baseadd(working_point)
                working_point.basedouble()
            if neg:
                self.negate()
        def mult(self,num):
            self.basemult(num)
            self.to_affine()
        def to_affine(self):
            """
            INPUT   : None
            PROCESS : Converts points from projective(X/Z, Y/Z) to affine form (x, y)
            OUPUT   : NONE
            """
            denominator = inv(self.z,self.curve.n)
            if isinstance(self.x,int):
                self.x = self.x*denominator%self.curve.n
            if isinstance(self.y,int):
                self.y = self.y*denominator%self.curve.n
            self.z = 1
        def find_y_squared(self):
            a = self.find_num_denom_y_squared()
            return a[0]*inv(a[1],self.curve.n)%self.curve.n;
        def find_y(self):
            """
            INPUT   : None
            PROCESS : Finds y coordinate given the x coordinate of the point
            OUPUT   : NONE
            """
            self.to_affine()
            a = self.find_y_squared()
            y_squared = a[0]*inv(a[1],self.curve.n)%self.curve.n
            self.y = tonelli_shanks(y_squared, self.curve.n)
        def copy(self):
            return create_point(self.curve, self.order, self.x, self.y, self.z);
    return Point(curve, x, y, z, order);

def inv(a, n):
    """
    INPUTS  : Number that multiplicative inverse needs to be found for, modulus
    PROCESS : Extended Euclidean algorithm
    Outputs : Multiplicative inverse
    """
    if a < 0: a%=n
    if n < 0: assert False, "Imposible, modulus can't be negative"
    r,t = [a,n],[1,0]
    while r[0]!=0:
        q = r[1]//r[0]
        r = [r[1] - q*r[0],r[0]]
        t = [t[1] - q*t[0],t[0]]
    return t[1]%n;

def has_root(a, p):
    return pow(a,(p-1)//2,p);

def tonelli_shanks(n, p):
    """
    INPUT   : Sqare, prime modulus
    PROCESS : Finds modular square root
    OUTPUT  : Square root of number over that modulus, or "Has no y" if no root
    """
    if has_root(n,p) != 1:
        return "Has no y";
    Q = p-1
    M = 0
    while Q%2 == 0:
        Q//=2
        M += 1
    z = 2
    while True:
        if has_root(z,p) != 1:
            break;
        z+=1
    c = pow(z,Q,p)
    t = pow(n,Q,p)
    R = pow(n,(Q+1)//2,p)
    if t == 0:
        return 0;
    while t != 1:
        for i in range(M):
            if pow(t,pow(2,i),p) == 1:
                b = pow(c, pow(2,M-i-1), p)
                M = i
                break;
        c = pow(b,2,p)
        t = t*c%p
        R = R*b%p
    return R;

def compatible(point, point2):
    try:
        point.curve.name != point2.curve.name
    except:
        return False;
    if point.curve.name != point2.curve.name:
        raise TypeError("Both points must be on the same curve")
    return True;

curves = {}
with open ("curves.txt","r") as curves_file:
    for line in curves_file:
        line = line.split(',')
        curves[line[0]] = line
base_points = {}
with open ("base_points.txt","r") as base_points_file:
    for line in base_points_file:
        line = line.split(',')
        base_points[line[0]] = line[1:]

def load_curve(curve_name):
    """
    INPUT   : Name of the curve
    PROCESS : Loads a curve if it is included in curves.txt and complies it into
                an objects
    OUTPUT  : Curve object
    """
    if curve_name in curves:
        curve_wanted = curves[curve_name]
    else:
        raise NameError("That curve is not in the included curves")
    return Curve(curve_wanted[0],curve_wanted[1],int(curve_wanted[2]),int(curve_wanted[3]),int(curve_wanted[4]));

def load_point(curve_name):
    """
    INPUT   : Name of the point
    PROCESS : Loads a base point if it is included in points.txt and complies it
                into an objects along with its curve
    OUTPUT  : Point object
    """
    if curve_name in base_points:
        point_wanted = base_points[curve_name]
    else:
        raise NameError("That base point is not in the included ones")
    return create_point(load_curve(curve_name),int(point_wanted[0]),
                            int(point_wanted[1]),int(point_wanted[2]));

list_of_curves = ['Anomalous', 'M221', 'E222', 'NIST_P224', 'Curve1174', 'Curve25519', 'BN',
'brainpoolP256t1', 'ANSSI_FRP256v1', 'NIST_P256', 'secp256k1', 'E382', 'M383', 'Curve383187',
'brainpoolP384t1', 'NIST_P384', 'Curve41417', 'Ed448_Goldilocks', 'M511', 'E521']

def show_base_parameters():
    """
    INPUT   : N one
    PROCESS :Shows all parameters for all curves and base points included in
                curves.txt and base_points.txt
    OUPUT   : Prints out all parameters, doesn't return anything
    """
    help = ""
    for key,value in curves:
        if value[0] == "W":
            equation = "y^2 = x^3 + {a}x + {b}".format(a = value[0], b = value[1])
            curvetype = "Weirestrass"
        elif value[0] == "M":
            equation = "{a}y^2 = x^3 + {b}x^2 + x".format(a = value[0], b = value[1])
            curvetype = "Montgomery"
        elif value[0] == "E":
            equation = "x^2 + y^2 = {a}^2 * (1 + {b}x^2 * y^2)".format(a = value[0], b = value[1])
            curvetype = "Edwards"
        point = base_points[key]
        help +="""
        Curve : {0}
        ===============================
        Curve Type     : {1}
        Curve Equation : {2}
        Finite Field   : {3}
        Order of Curve : {4}
        Base x         : {5}
        Base y         : {6}\n
        """.format(key, curvetype, equation, value[2], point[0], point[1], piont[2])
    print(help)
