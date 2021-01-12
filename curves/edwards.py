class EdwardsCurve():
    def __init__(self):
        self.help = ("This is the object which deals with a curve in the "
            "Edwards form\n"
            "This should only be use if imported and assumes that any object "
            "it is imported into contains : \n"
            "Curve object containing all inforation about that curve (modulous "
            "and all variables\n"
            "x, y and z are the co-ordinates of the point as defined in projective co-ordinates")
        self.zero = (0,1,1)
    # def add(self,p1,p2):
    #     """
    #     Adds p2 to p1
    #     """
    #     if p1.x == p2.x and p1.y == p2.y: # If it is the same point redirect to point doubling
    #         self.double(p1)
    #         return;
    #     n = p1.curve.n
    #     b = p1.curve.b
    #
    #     x = ((p1.x*p2.y + p1.y*p2.x)*inv((1 + b*p1.x*p1.y*p2.x*p2.y),n))%n
    #
    #     p1.y = ((p1.y*p2.y - p1.x*p2.x)*inv((1 - b*p1.x*p1.y*p2.x*p2.y),n))%n
    #
    #     p1.x = x
    def baseadd(self,p2):
        """
        INPUT   : Other point
        PROCESS : Adds using the add-2007-bl algorithm
        """
        A = self.z*p2.z
        B = A**2
        C = self.x*p2.x
        D = self.y*p2.y
        E = self.curve.b*C*D
        F = B - E
        G = B + E

        self.x = (A*F*((self.x + self.y)*(p2.x + p2.y) - C - D))%self.curve.n
        self.y = (A*G*(D - C))%self.curve.n
        self.z = (self.curve.a*F*G)%self.curve.n
    def basedouble(self):
        """
        INPUT   : None
        PROCESS : Doubles using the dbl-2007-bl algorithm
        """
        B = (self.x+self.y)**2
        C = self.x**2
        D = self.y**2
        E = C+D
        H = (self.curve.a*self.z)**2
        J = E-2*H

        self.x = (self.curve.a*(B-E)*J)%self.curve.n
        self.y = (self.curve.a*E*(C-D))%self.curve.n
        self.z = (E*J)%self.curve.n
    def find_num_denom_y_squared(self):
        """
        INPUT   : None
        OUTPUT  : Returns numerator and denominator of y^2 using the formula
        """
        numerator = (self.curve.a**2 - self.x**2)
        denominator =1 - self.curve.b*(self.curve.a*self.x)**2
        return (numerator,denominator);
    def negate(self):
        """
        INPUT   : None
        PROCESS : Negates the point
        """
        self.x = -self.x%self.curve.n
