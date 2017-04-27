import math
pi = math.pi
pi2 = math.pi ** 2

d_constants = dict()  # working constants
d_physical_const = dict()  # dict for physical parameters

def frange(start, stop, step=1.0):
    """ Generator that build range with float values """
    x = start
    while x < stop:
        yield round(x, 3)
        x += step

def set_constants(**kw):
    """
    this function get parameters from dictionary kw, set them
    into global dict 'd_physical_const', calculete working constants and set them
    into global dict 'd_constants'
    """
    global d_physical_const
    d_physical_const = kw

    pi = math.pi
    Mo = kw['Mo']
    Hox = kw['Hox']
    Hoz = kw['Hoz']

    r0 = kw['r0']
    R0 = kw['R0']
    ksi = kw['ksi']
    Nu = kw['Nu']
    N = kw['N']
    V0 = kw['V0']
    trueDelta = r0 / 2

    global d_constants

    CB = 4 * pi * ksi * r0 ** 2 * Mo ** 2 / (27 * Nu * R0 * V0)  # 4*pi*ksi*r0^2*Mo^2/(27*nu*R0)
    Ex = 3 * pi * Hox / (2 * Mo)
    Ez = 3 * pi * Hoz / (2 * Mo)
    Rm = (R0 / r0) ** 2
    delta = trueDelta / r0 + 2

    d_constants['N'] = N
    d_constants['CB'] = CB
    d_constants['Ex'] = Ex
    d_constants['Ez'] = Ez
    d_constants['mR'] = Rm
    d_constants['delta'] = delta
    d_constants['D'] = R0 / r0


# @jit
def f(X1, Y1, Z1, X, Y, Z):
    """
    this function get:
    1) coordinates of point into vesicule
    2) coordinates of center of vesicule
    and return fx, fy, fz summs of forces of each bmn of chain
    """
    Ex = d_constants['Ex']  # 3*pi*HoX/(2*Mo)
    Ez = d_constants['Ez']  # 3*pi*HoZ/(2*Mo)
    delta = d_constants['delta']  # delta0+2
    N = d_constants['N']  # num of particles in chain

    """params independent from i(item of chein)"""
    X2plusY2 = (X + X1) ** 2 + (Y + Y1) ** 2
    ZZ1 = Z + Z1
    XX1 = X + X1
    YY1 = Y + Y1

    """initiate important variables involved in calculating of fx, fy, fz"""
    sumfx1 = 0
    sumfx2 = 0
    sumfx3 = 0
    sumfz1 = 0
    sumfz2 = 0
    sumfz3 = 0
    sum1 = 0
    sum2 = 0

    """calculete mambers of summs for item from N particles"""
    for i in range(1, N + 1):
        A = ZZ1 - (i - 1) * delta
        A2 = A ** 2
        B = X2plusY2 + A2
        B52 = B ** 2.5
        B72 = B ** 3.5
        C = B + A2

        """each summ append by i-mamber"""
        sumfx1 += (- 15 * X * XX1 * A / B72)
        sumfx2 += 15 * X * YY1 * A / B72
        sumfx3 += 3 * X / B52 - 15 * A2 / B72
        sumfz1 += (5 * XX1 * C / B72 - 2 * XX1 / B52)
        sumfz2 += (5 * YY1 * C / B72 - 2 * YY1 / B52)
        sumfz3 += 4 * A / B52 + 5 * A * B / B72
        sum1 += (3 * X * A / B52)
        sum2 += (3 * A2 - C) / B52

    """calculate f for x1,y1,z1 points in volume of vesicle"""
    fx = Ex * sumfx1 + Ez * sumfz1 + sum1 * sumfx1 + sum2 * sumfz1
    fy = Ex * sumfx2 + Ez * sumfz2 + sum1 * sumfx2 + sum2 * sumfz2
    fz = Ex * sumfx3 + Ez * sumfz3 + sum1 * sumfx3 + sum2 * sumfz3

    return fx, fy, fz


# @jit
def tpl_integral(X, Y, Z):
    """
    this function get coordinates of center of vesicule
    return i_gradHX, i_gradHY, i_gradHZ - whole parts of forces
    that act on vesicule.
    """
    i_gradHX = 0
    i_gradHY = 0
    i_gradHZ = 0
    mR = d_constants['mR']  # (R0/r0)^2
    limX1 = math.sqrt(mR) * 0.99
    step = d_working_const['step']  # math.sqrt(mR)/10

    """set a variation of X1,Y1,Z1 coors into vesicle"""
    for X1 in list(frange(-limX1, limX1, step)):
        limY1 = math.sqrt(mR - X1 ** 2) * 0.99
        # step = 2 * limY1 / 10

        for Y1 in list(frange(-limY1, limY1, step)):

            limZ1 = math.sqrt(mR - X1 ** 2 - Y1 ** 2) * 0.99
            # step = 2 * limZ1 / 10
            for Z1 in list(frange(-limZ1, limZ1, step)):
                # print (X1,Y1, Z1)
                """calculate fx,fz,fy for X1,Y1,Z1"""
                dfx, dfy, dfz = f(X1, Y1, Z1, X, Y, Z)

                i_gradHX += dfx
                i_gradHY += dfy
                i_gradHZ += dfz

    return i_gradHX, i_gradHY, i_gradHZ


# @jit
def mover(X, Y, Z):
    """
    this function get old coordinates of center of vesicule
    return new coordinates
    """
    ZT = d_working_const['ZT']
    Spow = d_working_const['Spow']
    T = d_working_const['T']
    CB = d_constants['CB']  # 4pi*ksi*r0^2*Mo^2/(27*nu*R0)

    """calculate integral of gradient^2 by volume of vesicle"""
    gradHX, gradHY, gradHZ = tpl_integral(X, Y, Z)

    """calculete speed for x y z directions"""
    VX = gradHX * CB  # We can add 1 with + or -
    VY = gradHY * CB  # to each  VX,VY,VZ
    VZ = gradHZ * CB + 1  # to chenge direction of movement of vesicule

    """calculete elementary time size"""
    DT = T / (ZT * (1 + (VX * VX + VY * VY + VZ * VZ) ** Spow))

    """calculate new coordinates of vesicle after moving DT time interval"""
    X += VX * DT
    Y += VY * DT
    Z += VZ * DT

    if d_working_const['showDetails']: 
        print(math.sqrt(X ** 2 + Y ** 2), Z)  # current info of vesicule movement
    return X, Y, Z


def stopper(X, Y, Z):
    """this function return false if vesicule will be
       captured by chain of bmn
    """
    D = d_constants['D']
    return math.sqrt(Y ** 2 + X ** 2) > 1 + D  # working only for movement of
    # vesicule in OZ axes direction movement


# @jit
def pre_roy(alpha, Z0, ry=0, rn=0):
    """
    this function get
    alpha - angle from OY in XOY squere
    Z0 - coordinates from witch vesicule starts ist moving
    """
    Zlim = d_working_const['Zlim']
    DeltaR = d_working_const['DeltaR']
    D = d_constants['D']
    N = d_constants['N']
    delta = d_constants['delta']

    R0 = 1
    R_Yes = R0

    """calculate `cos(alpha)` and `sin(alpha)` only once"""
    cos_a = math.cos(math.pi * alpha / 180)
    sin_a = math.sin(math.pi * alpha / 180)

    while True:

        X = R0 * cos_a
        Y = R0 * sin_a
        Z = Z0

        while stopper(X, Y, Z) and Z < N * delta * 1.2:
            X, Y, Z = mover(X, Y, Z)

        if Z > N * delta * 1.2:
            return R0, R_Yes

        else:
            R_Yes = R0
            R0 = R0 * 1.34


# @jit
def roy(alpha, Z0, ry=0, rn=0):
    Zlim = d_working_const['Zlim']
    DeltaR = d_working_const['DeltaR']
    D = d_constants['D']
    N = d_constants['N']
    delta = d_constants['delta']
    R_No, R_Yes = pre_roy(alpha, Z0)

    """calculate `cos(alpha)` and `sin(alpha)` only once"""
    cos_a = math.cos(math.pi * alpha / 180)
    sin_a = math.sin(math.pi * alpha / 180)

    while True:

        R0 = R_Yes + (R_No - R_Yes) / 2.0
        X = R0 * cos_a
        Y = R0 * sin_a
        Z = Z0
        
        while stopper(X, Y, Z) and Z < N * delta * 1.2: X, Y, Z = mover(X, Y, Z)

        if Z > N * delta * 1.2:
            R_No = R0
        else:
            R_Yes = R0

        if R_No - R_Yes < DeltaR:
            R0 = (R_No + R_Yes) / 2.0
            X = R0 * cos_a
            Y = R0 * sin_a
            Z = Z0
            return X, Y, Z, R0


def get_capture_area(Zi, A_RANGE):
    D = d_constants['D']
    x = []
    y = []
    z = []
    r = []
    for alpha in A_RANGE:
        X, Y, Z, R = roy(alpha, Zi)
        x = x + [X]
        y = y + [Y]
        z.append(Z)
        r.append(R)

    return x, y, z, r


def new_capar(Xi, Yi, Zi, n):
    x = []
    y = []
    z = []
    xy = []
    X = Xi
    Y = Yi
    Z = Zi

    for i in range(n):
        X, Y, Z = mover(X, Y, Z)

        xy = xy + [math.sqrt(X ** 2 + Y ** 2)]
        x = x + [X]
        y = y + [Y]
        z = z + [Z]

    return x, y, z, xy

def run(params):
    A = params['A_RANGE']
    Z = params['Z0']
    global d_working_const;
    d_working_const = {
        'DeltaR': params['DeltaR'],
        'ZT':     params['ZT'],
        'Zlim':   params['Zlim'],
        'Spow':   params['Spow'],
        'T':      params['T'],
        'step':   params['step'],
        'showDetails': params['showDetails']
    }

    set_constants(
        Hox=params['Hox'],
        Hoz=params['Hoz'],
        r0=params['r0'] * 10 ** -7,
        R0=params['R0'] * 10 ** -7,
        ksi=10 ** (-1*params['ksi']),
        Nu=params['Nu'],
        N=params['N'],
        Mo=params['Mo'],
        V0=params['V0']
    )

    x = []
    y = []
    z = []
    r = []
    
    x, y, z, r =  get_capture_area(Z, A)
    catchR = sum(r) / len(r)
    toV = round(float(catchR) - params['R0'] / params['r0'], 2) * params['r0']
    return toV



