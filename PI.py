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
            for j in range(0,self.tab[i]):
                (z, cpt) = z+a
        return (z, self.n+other.n)
    def __truediv__(self, other: Digits) -> Digits:
        r = Digits(self.n, True, self.tab.copy())
        p = Digits(other.n, True, other.tab.copy())
        z = Digits(self.n, self.isPositif==other.isPositif, [0]*self.n)
        for i in range(0,self.n):
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

class R:
    pass
class R:
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
    def __add__(self, other: R) -> R:
        (x, y) = normalize(self, other)
        (digits, cpt) = x.mantissa.digits+y.mantissa.digits
        mantissa = Mantissa(digits.n, digits.isPositif, digits.tab)
        exponent = x.exponent
        if cpt:
            mantissa.digits.rshift(1)
            exponent.increase()
        return R(mantissa, exponent).trim().cut(mantissa.digits.n)
    def __neg__(self) -> R:
        x = self
        mantissa = Mantissa(x.mantissa.digits.n, \
                not x.mantissa.digits.isPositif, \
                x.mantissa.digits.tab \
                )
        exponent = x.exponent
        return R(mantissa, exponent)
    def __sub__(self, other: R) -> R:
        return self+(-other)
    def __mul__(self, other: R) -> R:
        x = self
        y = other
        (digits, k) = x.mantissa.digits*y.mantissa.digits
        mantissa = Mantissa(digits.n, digits.isPositif, digits.tab)
        (digits, cpt) = x.exponent.digits+y.exponent.digits
        exponent = Exponent(digits.n, digits.isPositif, digits.tab)
        exponent.increase()
        return R(mantissa, exponent).trim().cut(x.mantissa.digits.n)
    def __truediv__(self, other: R) -> R:
        x = self
        y = other
        digits = x.mantissa.digits/y.mantissa.digits
        mantissa = Mantissa(digits.n, digits.isPositif, digits.tab)
        (digits, cpt) = x.exponent.digits-y.exponent.digits
        exponent = Exponent(digits.n, digits.isPositif, digits.tab)
        return R(mantissa, exponent).trim().cut(mantissa.digits.n)
    def __abs__(self) -> R:
        x = self
        x.mantissa.digits.isPositif = True
        return x
    def SQRT(self) -> R:
        def lim() -> R:
            n = self.mantissa.digits.n
            m = self.exponent.digits.n
            y_nm1 = self
            y_n = (y_nm1 + (self/y_nm1)) / TWO(n,m)
            while abs(y_n-y_nm1)>EPS(n,m):
                y_nm1 = y_n
                y_n = (y_nm1 + (self/y_nm1)) / TWO(n,m)
            return y_n
        return lim()

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

def ZERO(n: int, m: int) -> R:
    return R(Mantissa(n, True, [0]*n), Exponent(m, True, [0]*m))

def ONE(n: int, m: int) -> R:
    return R(\
            Mantissa(n, True, [(1 if i==0 else 0) for i in range(n)]),\
            Exponent(m, True, [0]*m)\
            )

def TWO(n: int, m: int) -> R:
    return R(\
            Mantissa(n, True, [(2 if i==0 else 0) for i in range(n)]),\
            Exponent(m, True, [0]*m) \
            )

def THREE(n: int, m: int) -> R:
    return R(\
            Mantissa(n, True, [(3 if i==0 else 0) for i in range(n)]),\
            Exponent(m, True, [0]*m) \
            )

def FOUR(n: int, m: int) -> R:
    return R(\
            Mantissa(n, True, [(4 if i==0 else 0) for i in range(n)]),\
            Exponent(m, True, [0]*m) \
            )

def EPS(n: int, m: int) -> R:
    return R(\
            Mantissa(n, True, [(0 if not i==n-1 else 1) for i in range(n)]),\
            Exponent(m, True, [0]*m) \
            )

def PI(n: int,m: int) -> R:
    def lim() -> R:
        P_n = TWO(n,m)*FOUR(n,m)
        p_n = TWO(n,m).SQRT()*FOUR(n,m)
        while abs(P_n-p_n)>EPS(n,m):
            P_n = TWO(n,m)*(P_n*p_n)/(P_n+p_n)
            p_n = (p_n*P_n).SQRT()
        return p_n
    return lim()/TWO(n,m)

n = 100
m = 2
print(n,m)
print(TWO(n,m).SQRT())
print(PI(n,m))
