base = 10

class Formula:
    pass

class R:
    pass

class Formula:
    def __init__(self):
        pass
    def app(self, n: int, m: int) -> R:
        print("app ERROR")
    def __add__(self, other: Formula) -> Formula:
        return ADD(self,other)
    def __abs__(self) -> Formula:
        return ABS(self)
    def __neg__(self) -> Formula:
        return NEG(self)
    def __sub__(self, other: Formula) -> Formula:
        return SUB(self,other)
    def __mul__(self, other: Formula) -> Formula:
        return MUL(self, other)
    def __truediv__(self, other: Formula) -> Formula:
        return TRUEDIV(self,other)

class Digits:
    pass
class Digits:
    def __init__(self, n: int, isPositif: bool, tab: [int]):
        self.n = n
        self.isPositif = isPositif
        self.tab = tab
    def rshift(self, k: int):
        self.tab.insert(0,k)
        self.tab.pop()
    def __lt__(self, other: Digits) -> bool:
        if self.isPositif and other.isPositif:
            for i in range(0,self.n):
                if self.tab[i]<other.tab[i]:
                    return True
                elif other.tab[i]<self.tab[i]:
                    return False
            return False
        elif (not self.isPositif) and (not other.isPositif):
            for i in range(0,self.n):
                if self.tab[i]<other.tab[i]:
                    return False
                elif other.tab[i]<self.tab[i]:
                    return True
            return False
        elif self.isPositif and (not other.isPositif):
            return False
        else:
            return True
    def __gt__(self, other: Digits) -> bool:
        if self.isPositif and other.isPositif:
            for i in range(0,self.n):
                if self.tab[i]>other.tab[i]:
                    return True
                elif other.tab[i]>self.tab[i]:
                    return False
            return False
        elif (not self.isPositif) and (not other.isPositif):
            for i in range(0,self.n):
                if self.tab[i]>other.tab[i]:
                    return False
                elif other.tab[i]>self.tab[i]:
                    return True
            return False
        elif self.isPositif and (not other.isPositif):
            return True
        else:
            return False
    def __ge__(self, other: Digits) -> bool:
        return not (self<other)
    def __neg__(self) -> Digits:
        return Digits(self.n, not self.isPositif, self.tab)
    def __abs__(self) -> Digits:
        return Digits(self.n, True, self.tab)
    def __add__(self, other: Digits) -> (Digits, bool):
        if (self.isPositif == other.isPositif):
            z = Digits(self.n, self.isPositif, [0]*self.n)
            cpt = False
            for i in range(self.n-1,-1,-1):
                z.tab[i] = self.tab[i]+other.tab[i] \
                        + (1 if cpt else 0)
                if z.tab[i]>base-1:
                    z.tab[i]-=base
                    cpt = True
                else:
                    cpt = False
            return (z, cpt)
        else:
            if abs(self)>=abs(other):
                z = Digits(self.n, self.isPositif, [0]*self.n)
                cpt = False
                for i in range(self.n-1,-1,-1):
                    z.tab[i] = self.tab[i]-other.tab[i] \
                            - (1 if cpt else 0)
                    if z.tab[i]<0:
                        z.tab[i]+=base
                        cpt = True
                    else:
                        cpt = False
                return (z, False)
            else:
                z = Digits(self.n, other.isPositif, [0]*self.n)
                cpt = False
                for i in range(self.n-1,-1,-1):
                    z.tab[i] = other.tab[i]-self.tab[i] \
                            - (1 if cpt else 0)
                    if z.tab[i]<0:
                        z.tab[i]+=base
                        cpt = True
                    else:
                        cpt = False
                return (z, False)
    def __sub__(self, other: Digits) -> (Digits, bool):
        return self+Digits(other.n, not other.isPositif, other.tab)
    def __mul__(self, other: Digits) -> (Digits, int):
        z = Digits(self.n+other.n, self.isPositif==other.isPositif, [0]*(self.n+other.n))
        for i in range(self.n-1,-1,-1):
            a = Digits( \
                    self.n+other.n, \
                    self.isPositif==other.isPositif, \
                    [0]*(i+1) + other.tab + [0]*(self.n-i-1) \
                    )
            for j in range(0,self.tab[i]):
                (z, cpt) = z+a
        return (z, self.n+other.n)
    def __truediv__(self, other: Digits) -> Digits:
        r = Digits(self.n, True, self.tab)
        p = Digits(other.n, True, other.tab)
        z = Digits(self.n, self.isPositif==other.isPositif, [0]*self.n)
        for i in range(0,self.n):
            while r>=p:
                (r, cpt) = r-p
                z.tab[i] += 1
            p.rshift(0)
        return z

class Mantissa:
    pass
class Mantissa:
    def __init__(self, n: int, isPositif: bool, tab: [int]):
        self.digits = Digits(n, isPositif, tab)
    def copy(self) -> Mantissa:
        return Mantissa(self.digits.n, self.digits.isPositif, self.digits.tab.copy())
    def rshift(self, k: int):
        self.digits.rshift(k)
    def __gt__(self, other: Mantissa):
        return self.digits>other.digits

class Exponent:
    pass
class Exponent:
    def __init__(self, n: int, isPositif: bool, tab: [int]):
        self.digits = Digits(n, isPositif, tab)
    def copy(self) -> Exponent:
        return Exponent(self.digits.n, self.digits.isPositif, self.digits.tab.copy())
    def decrease(self):
        cpt = True
        if self.digits.tab==[0]*self.digits.n:
            self.digits.isPositif = False
            for i in range(self.digits.n-1,-1,-1):
                self.digits.tab[i] = self.digits.tab[i] + (1 if cpt else 0)
                if self.digits.tab[i]>base-1:
                    self.digits.tab[i]-=base
                    cpt = True
                else:
                    cpt = False
        elif self.digits.isPositif:
            for i in range(self.digits.n-1,-1,-1):
                self.digits.tab[i] = self.digits.tab[i] - (1 if cpt else 0)
                if self.digits.tab[i]<0:
                    self.digits.tab[i]+=base
                    cpt = True
                else:
                    cpt = False
            if self.digits.tab == [0]*self.digits.n:
                self.digits.isPositif = True
        else:
            for i in range(self.digits.n-1,-1,-1):
                self.digits.tab[i] = self.digits.tab[i] + (1 if cpt else 0)
                if self.digits.tab[i]>base-1:
                    self.digits.tab[i]-=base
                    cpt = True
                else:
                    cpt = False
    def increase(self):
        cpt = True
        if self.digits.isPositif:
            for i in range(self.digits.n-1,-1,-1):
                self.digits.tab[i] = self.digits.tab[i] + (1 if cpt else 0)
                if self.digits.tab[i]>base-1:
                    self.digits.tab[i]-=base
                    cpt = True
                else:
                    cpt = False
        else:
            for i in range(self.digits.n-1,-1,-1):
                self.digits.tab[i] = self.digits.tab[i] - (1 if cpt else 0)
                if self.digits.tab[i]<0:
                    self.digits.tab[i]+=base
                    cpt = True
                else:
                    cpt = False
            if self.digits.tab == [0]*self.digits.n:
                self.digits.isPositif = True
    def __lt__(self, other: Exponent) -> bool:
        return self.digits<other.digits

class R(Formula):
    def __init__(self, mantissa: Mantissa, exponent: Exponent):
        self.mantissa = mantissa
        self.exponent = exponent
    def copy(self) -> R:
        return R(self.mantissa.copy(), self.exponent.copy())
    def app(self, n: int, m: int) -> R:
        return self.copy()
    def __str__(self):
        return ("" if self.mantissa.digits.isPositif else "-") \
                + f"{self.mantissa.digits.tab[0]}" \
                + ("," if self.mantissa.digits.n>1 else "") \
                + str(self.mantissa.digits.tab[1:self.mantissa.digits.n])[1:-1].replace(", ","") \
                + " *10^ " \
                + ("" if self.exponent.digits.isPositif else "-") \
                + str(self.exponent.digits.tab)[1:-1].replace(", ","")
    def __gt__(self, other: R):
        (x, y) = normalize(self, other)
        return x.mantissa.digits>y.mantissa.digits
    def trim(self) -> R:
        while self.mantissa.digits.tab[0]==0 \
                and (not self.mantissa.digits.tab==[0]*self.mantissa.digits.n):
            self.mantissa.digits.tab.pop(0)
            self.mantissa.digits.tab.append(0)
            self.exponent.decrease()
        return self
    def cut(self, n: int) -> R:
        self.mantissa.digits.tab = self.mantissa.digits.tab[0:n] \
                + [0]*(n-self.mantissa.digits.n)
        self.mantissa.digits.n = n
        return self

def normalize(x: R, y: R) -> (R, R):
    while x.exponent < y.exponent:
        x.exponent.increase()
        x.mantissa.rshift(0)
    while y.exponent < x.exponent:
        y.exponent.increase()
        y.mantissa.rshift(0)
    return (x, y)

class ADD(Formula):
    def __init__(self, x: Formula, y: Formula):
        self.x = x
        self.y = y
    def app(self, n: int, m: int) -> R:
        x = self.x.app(n,m)
        y = self.y.app(n,m)
        (x, y) = normalize(x, y)
        (digits, cpt) = x.mantissa.digits+y.mantissa.digits
        mantissa = Mantissa(digits.n, digits.isPositif, digits.tab)
        exponent = x.exponent
        if cpt:
            mantissa.digits.rshift(1)
            exponent.increase()
        return R(mantissa, exponent).trim().cut(n)

class NEG(Formula):
    def __init__(self, x: Formula):
        self.x = x
    def app(self, n: int, m: int) -> R:
        x = self.x.app(n,m)
        mantissa = Mantissa(x.mantissa.digits.n, \
                not x.mantissa.digits.isPositif, \
                x.mantissa.digits.tab \
                )
        exponent = x.exponent
        return R(mantissa, exponent)

class SUB(Formula):
    def __init__(self, x: Formula, y: Formula):
        self.x = x
        self.y = y
    def app(self, n: int, m: int) -> R:
        return (self.x+(-self.y)).app(n,m)

class MUL(Formula):
    def __init__(self, x: Formula, y: Formula):
        self.x = x
        self.y = y
    def app(self, n: int, m: int) -> R:
        x = self.x.app(n,m)
        y = self.y.app(n,m)
        (digits, k) = x.mantissa.digits*y.mantissa.digits
        mantissa = Mantissa(digits.n, digits.isPositif, digits.tab)
        (digits, cpt) = x.exponent.digits+y.exponent.digits
        exponent = Exponent(digits.n, digits.isPositif, digits.tab)
#        for i in range(1,k):
#            exponent.increase()
        exponent.increase()
        return R(mantissa, exponent).trim().cut(n)

class TRUEDIV(Formula):
    def __init__(self, x: Formula, y: Formula):
        self.x = x
        self.y = y
    def app(self, n: int, m: int) -> R:
        x = self.x.app(n,m)
        y = self.y.app(n,m)
        digits = x.mantissa.digits/y.mantissa.digits
        mantissa = Mantissa(digits.n, digits.isPositif, digits.tab)
        (digits, cpt) = x.exponent.digits-y.exponent.digits
        exponent = Exponent(digits.n, digits.isPositif, digits.tab)
        return R(mantissa, exponent).trim().cut(n)

class ZERO(Formula):
    def app(self, n: int, m: int) -> R:
        return R(\
                Mantissa(n, True, [0]*n),\
                Exponent(m, True, [0]*m) \
                )

class ONE(Formula):
    def app(self, n: int, m: int) -> R:
        return R(\
                Mantissa(n, True, [(1 if i==0 else 0) for i in range(n)]),\
                Exponent(m, True, [0]*m)\
                )

class TWO(Formula):
    def app(self, n: int, m: int) -> R:
        return R(\
                Mantissa(n, True, [(2 if i==0 else 0) for i in range(n)]),\
                Exponent(m, True, [0]*m) \
                )

class THREE(Formula):
    def app(self, n: int, m: int) -> R:
        return R(\
                Mantissa(n, True, [(3 if i==0 else 0) for i in range(n)]),\
                Exponent(m, True, [0]*m) \
                )

class FOUR(Formula):
    def app(self, n: int, m: int) -> R:
        return R(\
                Mantissa(n, True, [(4 if i==0 else 0) for i in range(n)]),\
                Exponent(m, True, [0]*m) \
                )

class EPS(Formula):
    def app(self, n: int, m: int) -> R:
        return R(\
                Mantissa(n, True, [(0 if not i==n-1 else 1) for i in range(n)]),\
                Exponent(m, False, [base-1]*m) \
                )

class ABS(Formula):
    def __init__(self, x: Formula):
        self.x = x
    def app(self, n: int, m: int) -> R:
        y = self.x.app(n,m)
        y.mantissa.digits.isPositif = True
        return y


class SQRT(Formula):
    def __init__(self, x: Formula):
        self.x = x
    class y_n:
        def __init__(self, y_0: R):
            self.y_0 = y_0
        def lim(self, n: int, m: int) -> R:
            y_nm1 = self.y_0
            y_n = ((y_nm1 + (self.y_0/y_nm1)) / TWO()).app(n,m)
            while abs(y_n-y_nm1).app(n,m).mantissa>EPS().app(n,m).mantissa:
                y_nm1 = y_n
                y_n = ((y_nm1 + (self.y_0/y_nm1)) / TWO()).app(n,m)
            return y_n
    def app(self, n: int, m: int) -> R:
        return SQRT.y_n(self.x.app(n,m)).lim(n,m)

class PI(Formula):
    class p_n:
        def lim(self, n: int, m: int) -> R:
            P_n = (TWO()*FOUR()).app(n,m)
            p_n = (SQRT(TWO())*FOUR()).app(n,m)
            while abs(P_n-p_n).app(n,m).mantissa>EPS().app(n,m).mantissa:
                P_n = (TWO()*(P_n*p_n)/(P_n+p_n)).app(n,m)
                p_n = SQRT(p_n*P_n).app(n,m)
            return p_n
    def app(self, n: int, m: int) -> R:
        return (PI.p_n().lim(n,m)/TWO()).app(n,m)

n = 10
m = 1
print(n,m)
print((FOUR()*FOUR()).app(n,m))
print(SQRT(TWO()).app(n,m))
print(PI().app(n,m))
