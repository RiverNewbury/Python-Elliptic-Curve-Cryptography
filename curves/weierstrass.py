class WeierstrassCurve():# NOTE: CHECK ALL DOUBLE FUNCTIONS
    def __init__(self):
        self.help = ("This is the object which deals with a curve in the "
            "Weistrass form\n"
            "This should only be use if imported and assumes that any object "
            "it is imported into contains : \n"
            "Curve object containing all inforation about that curve (modulous "
            "and all variables\n"
            "x, y and z as points are defined in projective coordinates")
        self.zero = ("PAI",0,1)
    # def baseadd(self,p2):
    #     """
    #     Adds p2 to p1
    #     """
    #     n = self.curve.n
    #     b = self.curve.b
    #     a = self.curve.a
    #     if self.x == 'PAI':
    #         self.x = p2.x
    #         self.y = p2.y
    #         return;
    #     elif p2.x == 'PAI':
    #         return;
    #     if self.x == p2.x:
    #         if self.y != p2.y:
    #             self.x = 'PAI'
    #             return;
    #         grad = (3*self.x**2 + a)*inv(2*self.y,n)%n
    #     else:
    #         grad = (p2.y-self.y)*inv(p2.x-self.x,n)%n
    #
    #
    #     x = (grad**2-self.x-p2.x)%n
    #
    #     self.y = (grad*(self.x-x)-self.y)%n
    #     self.x = x
    def baseadd(self,p2):
        """
        INPUT   : Point to be added to this point
        PROCESS : Uses add-2002-bj algorithm
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
            self.basedouble()
            return;

        n = self.y*p2.z - p2.y*self.z
        d = self.x*p2.z - p2.x*self.z

        T = self.x*p2.z*d**2
        X = self.z*p2.z*n**2 - T - p2.x*self.z*d**2
        self.x = X*d%self.curve.n
        self.y = (-(self.y * d**3 * p2.z + n*(X - T)))%self.curve.n
        self.z = (d**3 *self.z*p2.z)%self.curve.n


        # U1 = self.x*p2.z
        # U2 = p2.x*self.z
        # S1 = self.y*p2.z
        # S2 = p2.y*self.z
        # ZZ = self.z*p2.z
        # T = U1+U2
        # TT = T**2
        # M = S1+S2
        # R = TT-U1*U2+self.curve.a*(ZZ**2)
        # F = ZZ*M
        # L = M*F
        # LL = L**2
        # G = (T+L)**2-TT-LL
        # W = 2*R**2-G
        # self.x = (2*F*W)%self.curve.n
        # self.y = (R*(G-2*W)-2*LL)%self.curve.n
        # self.z = (4*F*(F**2))%self.curve.n
        #print("AA",self.x,self.y,self.z)
        # u = p2.y*self.z - self.y*p2.z
        # v = p2.x*self.z - self.x*p2.z
        # A = u**2*self.z*p2.z-v**3-2*v**2*self.x*p2.z
        # self.x = (v*A)%self.curve.n
        # self.y = (u*(v**2*self.x*p2.z-A)-v**3*self.y*p2.z)%self.curve.n
        # self.z = (v**3*self.z*p2.z)%self.curve.n
    # def double(self):
    #     a = self.copy()
    #     self.add(a)
    def basedouble(self):
        """
        INPUT   : None
        PROCESS : Doubles, uses dbl-2007-bl algorithm
        """
        if self.x == 'PAI':
            return;
        n = 3*self.x**2 + self.curve.a*self.z**2
        d = 2*self.y*self.z

        T = self.x*self.z*d**2
        X = self.z*self.z*n**2 - 2*T
        self.x = X*d%self.curve.n
        self.y = (-(self.y * d**3 * self.z + n*(X - T)))%self.curve.n
        self.z = (d**3 *self.z*self.z)%self.curve.n
    def find_num_denom_y_squared(self):
        """
        INPUT   : None
        OUTPUT  : Returns numerator and denominator of y^2 using formula
        """
        return (self.x**3 + self.curve.a*self.x + self.curve.b,1);
    def negate(self):
        """
        INPUT   : None
        PROCESS : Negates this point
        """
        self.y = -self.y%self.curve.n
