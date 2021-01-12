class MontgomeryCurve():
    def __init__(self):
        self.help = ("This is the object which deals with a curve in the "
            "Mongomery form\n"
            "This should only be use if imported and assumes that any object "
            "it is imported into contains : \n"
            "Curve object containing all inforation about that curve (modulous "
            "and all variables\n"
            "x, y and z as points are defined in projective coordinates")
        self.zero = ("PAI",0,1)
    # def add(self,p1,p2):
    #     """
    #     Adds p2 to p1
    #     """
    #     #print("adding", p2.x,p2.y,'\n')
    #     #print("to",p1.x,p1.y,'\n')
    #     n = p1.curve.n
    #     a = p1.curve.a
    #     b = p1.curve.b
    #     if p1.x == 'PAI':
    #         p1.x = p2.x
    #         p1.y = p2.y
    #         return;
    #     elif p2.x == 'PAI':
    #         return;
    #     if p1.x == p2.x:
    #         if p1.y == p2.y:
    #             grad = (3*p1.x**2 + 2*b*p1.x + 1)*inv(2*a*p1.y,n)%n
    #         else:
    #             p1.x = 'PAI'
    #             return;
    #     else:
    #         grad = (p2.y-p1.y)*inv(p2.x-p1.x,n)%n
    #
    #
    #     x = (a*grad**2-p1.x-p2.x-b)%n
    #
    #     p1.y = (grad*(p1.x-x)-p1.y)%n
    #
    #     p1.x = x
    #     #print("resulting in",p1.x,p1.y,'\n')
    def baseadd(self,p2):
        """
        INPUT   : Other point to be added to the object
        PROCESS : Adds uses my algorithm
        """
        if self.x == 'PAI':
            self.x = p2.x
            self.y = p2.y
            self.z = p2.z
            return;
        elif p2.x == 'PAI':
            return;
        if self.x*p2.z%self.curve.n == p2.x*self.z%self.curve.n:
            if self.y*p2.z%self.curve.n != p2.y*self.z%self.curve.n:
                self.x, self.y, self.z = self.zero
                return;
            self.double()
            return;
        B = self.curve.a
        A = self.curve.b
        n = self.y*p2.z - p2.y*self.z
        d = self.x*p2.z - p2.x*self.z
        U1 = self.x*p2.z
        U2 = p2.x*self.z
        ZZ = self.z*p2.z
        X = B*n**2*ZZ - (A*ZZ + (U1 + U2))*d**2
        self.x = (d*X)%self.curve.n
        self.y = (-(self.y*p2.z*d**3 + n*(X - U1*d**2)))%self.curve.n
        self.z = (d**3*ZZ)%self.curve.n

    def basedouble(self):
        """
        INPUT   : None
        PROCESS : Doubles using my algorithm
        """
        if self.x == 'PAI':
            return;
        B = self.curve.a
        A = self.curve.b
        n = 3*self.x**2 + 2*self.curve.b*self.z*self.x + self.z**2
        d = 2*self.curve.a*self.z*self.y
        U1 = self.x*self.z
        ZZ = self.z*self.z
        X = B*n**2*ZZ - (A*ZZ + (2*U1))*d**2
        self.x = (d*X)%self.curve.n
        self.y = (-(self.y*self.z*d**3 + n*(X - U1*d**2)))%self.curve.n
        self.z = (d**3*ZZ)%self.curve.n
    # def algorithm(self,A,B):
    #     AA = A**2
    #     BB = B**2
    #     Zs = self.z*p2.z
    #     Xs = self.x*p2.x
    #     C = Zs*self.curve.b + p2.z*self.x + self.z*p2.x
    #     D = p2.z*BB
    #     E = (Zs*self.curve.a*AA - C*BB)
    #
    #     self.y = (A*(D*self.x - E) - self.y*D*B)%self.curve.n
    #     self.x = (B*E)%self.curve.n
    #     self.z = (Zs*BB*B)%self.curve.n
    def find_num_denom_y_squared(self):
        """
        INPUT   : None
        OUTPUT  : Returns numerator and denominator of y^2 using formula
        """
        numerator = (self.x**3 + self.curve.b*self.x**2 + self.x)
        denominator = self.curve.a
        return (numerator,denominator);
    def negate(self):
        """
        INPUT   : None
        PROCESS : Negates this point
        """
        self.y = -self.y%self.curve.n
