base = 10

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
            for i in range(self.n):
                if self.tab[i]<other.tab[i]:
                    return True
                elif other.tab[i]<self.tab[i]:
                    return False
            return False
        elif (not self.isPositif) and (not other.isPositif):
            for i in range(self.n):
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
            for i in range(self.n):
                if self.tab[i]>other.tab[i]:
                    return True
                elif other.tab[i]>self.tab[i]:
                    return False
            return False
        elif (not self.isPositif) and (not other.isPositif):
            for i in range(self.n):
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
                if z.tab == [0]*self.n:
                    z.isPositif = True
                return (z, cpt)
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
                if z.tab == [0]*self.n:
                    z.isPositif = True
                return (z, cpt)
    def __sub__(self, other: Digits) -> (Digits, bool):
        return self+(-other)
    def __mul__(self, other: Digits) -> (Digits, int):
        z = Digits(self.n+other.n, self.isPositif==other.isPositif, [0]*(self.n+other.n))
        for i in range(self.n-1,-1,-1):
            a = Digits( \
                    self.n+other.n, \
                    self.isPositif==other.isPositif, \
                    [0]*(i+1) + other.tab + [0]*(self.n-i-1) \
                    )
            for j in range(self.tab[i]):
                (z, cpt) = z+a
        return (z, self.n+other.n)
    def __truediv__(self, other: Digits) -> Digits:
        r = Digits(self.n, True, self.tab.copy())
        p = Digits(other.n, True, other.tab.copy())
        z = Digits(self.n, self.isPositif==other.isPositif, [0]*self.n)
        for i in range(self.n):
            while r>=p:
                (r, cpt) = r-p
                z.tab[i] += 1
            p.tab.insert(0,0)
            p.n+=1
            r.tab.append(0)
            r.n+=1
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

class Formula:
    pass
class R(Formula):
    pass

class Formula:
    def app(n: int,m: int) -> R:
        pass
    def __add__(self, other: Formula) -> Formula:
        return ADD(self,other)
    def __neg__(self) -> Formula:
        return NEG(self)
    def __sub__(self, other: Formula) -> Formula:
        return self+(-other)
    def __mul__(self, other: Formula) -> Formula:
        return MUL(self,other)
    def __truediv__(self, other: Formula) -> Formula:
        return TRUEDIV(self,other)
    def __abs__(self) -> Formula:
        return ABS(self)

class R(Formula):
    def __init__(self, mantissa: Mantissa, exponent: Exponent):
        self.mantissa = mantissa
        self.exponent = exponent
    def copy(self) -> R:
        return R(self.mantissa.copy(), self.exponent.copy())
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
    def app(self, n: int, m: int) -> R:
        return self

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
        return R(mantissa, exponent).trim().cut(mantissa.digits.n)

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
        exponent.increase()
        return R(mantissa, exponent).trim().cut(x.mantissa.digits.n)

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
        return R(mantissa, exponent).trim().cut(mantissa.digits.n)

class ABS(Formula):
    def __init__(self, x: Formula):
        self.x = x
    def app(self, n: int, m: int) -> R:
        x = self.x.app(n,m)
        mantissa = Mantissa(x.mantissa.digits.n, True, x.mantissa.digits.tab)
        return R(mantissa, x.exponent)


def normalize(self: R, other: R) -> (R, R):
    x = self.copy()
    y = other.copy()
    while x.exponent < y.exponent:
        x.exponent.increase()
        x.mantissa.rshift(0)
    while y.exponent < x.exponent:
        y.exponent.increase()
        y.mantissa.rshift(0)
    return (x, y)

class ZERO(Formula):
    def app(self, n: int, m: int) -> R:
        return R(Mantissa(n, True, [0]*n), Exponent(m, True, [0]*m))

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

def THREE(Formula):
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
                Exponent(m, True, [0]*m) \
                )

class SQRT(Formula):
    def __init__(self, y_0: Formula):
        self.y_0 = y_0
    def app(self, n: int, m: int) -> R:
        y_0 = self.y_0.app(n,m)
        y_nm1 = y_0
        y_n = ( (y_nm1 + y_0/y_nm1) / TWO() ).app(n,m)
        while abs(y_n-y_nm1).app(n,m)>EPS().app(n,m):
            y_nm1 = y_n
            y_n = ( (y_nm1 + y_0/y_nm1) / TWO() ).app(n,m)
        return y_n

class PI(Formula):
    def app(self, n: int,m: int) -> R:
        P_n = ( TWO()*FOUR() ).app(n,m)
        p_n = ( SQRT(TWO())*FOUR() ).app(n,m)
        while abs(P_n-p_n).app(n,m)>EPS().app(n,m):
            P_n = ( TWO()*(P_n*p_n)/(P_n+p_n) ).app(n,m)
            p_n = ( SQRT(p_n*P_n) ).app(n,m)
        return ( p_n/TWO() ).app(n,m)

n = 10
m = 2
print(n,m)
print(SQRT(TWO()).app(n,m))
print(PI().app(n,m))
