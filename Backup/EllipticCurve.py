class curve():
    def __init__(self,curvetype,a,b,mod):
        self.help = ("Takes the arguments : type of curve, 2 curve parameters as below and a modulous to define the curve over the finite field Fq\n"
                "If Weistrass (W) : y^2 = x^3 + ax + b\n"
                "If Montgomery (M) : ay^2 = x^3 + bx^2 + x\n"
                "If Edward (E) : x^2 + y^2 = a^2 * (1 + bx^2 * y^2)\n")
        if str(curvetype).upper() not in ['W','E','M']:
            raise TypeError("That curve type is not currently supported currently supported are Weistrass (W), Montgomery (M) and Edward (E)"); #possible wrong error type
        self.type = str(curvetype).upper()
        self.a = a
        self.b = b
        self.n = mod


class point():
    def __init__(self,curve,x,y):
        self.help = ("Takes the arguments : curve (should be a curve object) that the point lies on and the x,y coordinate of the point")
        self.curve = curve
        self.x = x
        self.y = y #pow((x*x*x+a*x+b),0.5)
    def copy(self):
        return point(self.curve,self.x,self.y);


class WeistrassCurve():
    def __init__(self):
        self.help = ("This is the object which deals with a curve in the Weistrass form")
        self.zero = ("PAI",0)
    def add(self,p1,p2):
        """
        Adds p2 to p1
        """
        n = p1.curve.n
        b = p1.curve.b
        if p1.x == 'PAI':
            p1.x = p2.x
            p1.y = p2.y
            return;
        elif p2.x == 'PAI':
            return;
        if p1.x == p2.x:
            if p1.y == p2.y:
                grad = (3*p1.x**2 + b)*inv(2*p1.y,n)%n
            else:
                p1.x = 'PAI'
                return;
        else:
            grad = (p2.y-p1.y)*inv(p2.x-p1.x,n)%n


        x = (grad**2-p1.x-p2.x)%n

        p1.y = (grad*(p1.x-x)-p1.y)%n
        p1.x = x
    def sub(self,p1,p2):
        """
        Subtracts p2 from p1
        """
        p2.y = -p2.y

        add(p1,p2)

        p2.y = -p2.y


class MontgomeryCurve():
    def __init__(self):
        self.help = ("This is the object which deals with a curve in the Montgomery form\n"
                     "NOT FINISHED")
        self.zero = ("PAI",0)
    def add(self,p1,p2):
        """
        Adds p2 to p1
        """
        #print("adding", p2.x,p2.y,'\n')
        #print("to",p1.x,p1.y,'\n')
        n = p1.curve.n
        a = p1.curve.a
        b = p1.curve.b
        if p1.x == 'PAI':
            p1.x = p2.x
            p1.y = p2.y
            return;
        elif p2.x == 'PAI':
            return;
        if p1.x == p2.x:
            if p1.y == p2.y:
                grad = (3*p1.x**2 + 2*b*p1.x + 1)*inv(2*a*p1.y,n)%n
            else:
                p1.x = 'PAI'
                return;
        else:
            grad = (p2.y-p1.y)*inv(p2.x-p1.x,n)%n


        x = (a*grad**2-p1.x-p2.x-b)%n

        p1.y = (grad*(p1.x-x)-p1.y)%n

        p1.x = x
        #print("resulting in",p1.x,p1.y,'\n')
    def sub(self,p1,p2):
        """
        Subtracts p2 from p1
        """
        p2.y = -p2.y

        add(p1,p2)

        p2.y = -p2.y

class EdwardsCurve():
    def __init__(self):
        self.help = ("This is the object which deals with a curve in the Edwards form")
        self.zero = (0,1)
    def add(self,p1,p2):
        """
        Adds p2 to p1
        """
        #print("adding", p2.x,p2.y)
        #print("to",p1.x,p1.y)
        if p1.x == p2.x and p1.y == p2.y:
            self.double(p1)
            return;
        n = p1.curve.n
        b = p1.curve.b

        x = ((p1.x*p2.y + p1.y*p2.x)*inv((1 + b*p1.x*p1.y*p2.x*p2.y),n))%n

        p1.y = ((p1.y*p2.y - p1.x*p2.x)*inv((1 - b*p1.x*p1.y*p2.x*p2.y),n))%n

        p1.x = x
    def sub(self,p1,p2):
        """
        Subtracts p2 from p1
        """
        p2.x = -p2.x
        add(p1,p2)
        p2.x = -p2.x
    def double(self,p1):
        #print("doubling",p1.x,p1.y)
        n = p1.curve.n
        x = p1.x

        p1.x = ((2*x*p1.y)*inv((1 + p1.curve.b*pow(x,2)*pow(p1.y,2)),p1.curve.n))%p1.curve.n

        p1.y = ((pow(p1.y,2)%n - pow(x,2)%n) * inv((1 - p1.curve.b * pow(x,2) * pow(p1.y,2)),p1.curve.n))%p1.curve.n

    def mult(self,final,num):
        working = final.copy()
        final.x = 0
        final.y = 1
        for i in reversed(bin(num)[2:]):
            if int(i):
                self.add(final,working)
            self.double(working)
        #print(final.x,final.y)

def inv(a,n):
    """
    r1 = Greatest common divisor
    t1 = Bezout Coefficient
    """
    if a < 0: a%=n
    if n < 0: assert False, "Imposible, modulus can't be negative"
    r,t = [a,n],[1,0]
    while r[0]!=0:
        q = r[1]//r[0]
        r = [r[1]-q*r[0],r[0]]
        t = [t[1]-q*t[0],t[0]]
    if t[1]<0: t[1]%=n
    return t[1];

def add(p1,p2):
    if p1.curve != p2.curve:
        raise AttributeError("a, b and n need to be the same on both eliptic curves to add them");
    if p1.curve.type == 'W':
        Weistrass.add(p1,p2)
    elif p1.curve.type == 'M':
        Montgomery.add(p1,p2)
    elif p1.curve.type == 'E':
        Edwards.add(p1,p2)

def sub(p1,p2):
    if p1.curve != p2.curve:
        raise AttributeError("a, b and n need to be the same on both eliptic curves to add them");
    if p1.curve.type == 'W':
        Weistrass.sub(p1,p2)
    elif p1.curve.type == 'M':
        Montgomery.sub(p1,p2)
    elif p1.curve.type == 'E':
        Edwards.sub(p1,p2)

def mult(FinalPoint,num):
    WorkingPoint = FinalPoint.copy()

    if FinalPoint.curve.type == 'W':
        FinalPoint.x,FinalPoint.y = Weistrass.zero
    elif FinalPoint.curve.type == 'M':
        FinalPoint.x,FinalPoint.y = Montgomery.zero
    elif FinalPoint.curve.type == 'E':
        FinalPoint.x,FinalPoint.y = Edwards.zero

    for i in reversed(bin(num)[2:]):
        if int(i):
            add(FinalPoint,WorkingPoint)
        add(WorkingPoint,WorkingPoint)

def lengendre(a,p):
    return pow(a,(p-1)//2,p);

def tonelli_shanks(n,p):
    if lengendre(n,p) != 1:
        return "Has no y";
    Q = p-1
    M = 0
    while Q%2 == 0:
        Q//=2
        M += 1
    z = 2
    while True:
        if lengendre(z,p) != 1:
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
                b = pow(c,pow(2,M-i-1),p)
                M = i
                break;
        c = pow(b,2,p)
        t = t*c%p
        R = R*b%p
    return R;

def findycoordinate(p1):
    #if FinalPoint.curve.type == 'W':
    #    ysquared =
    #elif FinalPoint.curve.type == 'M':
    #    FinalPoint.x,FinalPoint.y = Montgomery.zero
    if p1.curve.type == 'E':
        ysquared = ((p1.curve.a**2 - p1.x**2)*inv((1 - p1.curve.a**2 * p1.curve.b * (p1.x**2)),p1.curve.n))%p1.curve.n
    print(ysquared)
    p1.y = tonelli_shanks(ysquared,p1.curve.n)

Weistrass = WeistrassCurve()
Montgomery = MontgomeryCurve()
Edwards = EdwardsCurve()


M221 = curve('M',1,117050, 2**221 - 3)
M221_Base = point(M221,4,1630203008552496124843674615123983630541969261591546559209027208557)

E521 = curve("E",1,-376014,2**521 - 1)
E521_Base = point(E521,1571054894184995387535939749894317568645297350402905821437625181152304994381188529632591196067604100772673927915114267193389905003276673749012051148356041324,12)

M511 = curve("M",1,530438, 2**511 - 187)
M511_Base = point(M511,5,2500410645565072423368981149139213252211568685173608590070979264248275228603899706950518127817176591878667784247582124505430745177116625808811349787373477)
