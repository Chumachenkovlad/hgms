import sys
sys.path.append('..')
import math

pi = math.pi
pi2 = math.pi ** 2
i = 0
d_constants = dict()
d_physical_const = dict()


def set_constants(**kw):
    global d_physical_const
    d_physical_const = kw

    M1 = float(kw['M1'])  # for cylinder
    M2 = float(kw['M2'])  # for elements
    H0 = float(kw['H0'])  # external magentic field
    r0 = float(kw['r0'])  # radius of element that lain on cylinder
    R0 = float(kw['R0'])  # radius of cylinder (equals to element radius)
    b = float(kw['b'])  # (3-7)*10**-6
    Nu = float(kw['Nu'])  # 1.01*10**-3 viscosity
    V0 = float(kw['V0'])  # speed of liquid
    Xu = float(kw['Xu'])  # X parameter

    global d_constants

    CB = b ** 2 * M1 ** 2 * Xu / (9 * Nu * V0 * R0)
    Gamma = r0 / R0
    Ksi = M2 / M1
    H0B = H0 / M1

    d_constants['CB'] = CB
    d_constants['Gamma'] = Gamma
    d_constants['Ksi'] = Ksi
    d_constants['H0B'] = H0B

    global d_working_const

    d_constants['DeltaR'] = d_working_const['DeltaR']
    d_constants['ZT'] = d_working_const['ZT']
    d_constants['Zlim'] = d_working_const['Zlim']
    d_constants['Spow'] = d_working_const['Spow']
    d_constants['T'] = d_working_const['T']


def mover(X, Y, Z):
    CB = d_constants['CB']
    H0B = d_constants['H0B']
    Ksi = d_constants['Ksi']
    Gamma = d_constants['Gamma']
    ZT = d_constants['ZT']
    Spow = d_constants['Spow']
    T = d_constants['T']

    X2, Y2, Z2 = X ** 2, Y ** 2, Z ** 2
    Y2minusZ2 = (Y2 - Z2)
    Y2plusZ2 = (Y2 + Z2)
    Zshift = Z + 1 + Gamma
    Zshift2 = Zshift ** 2

    Gamma3 = Gamma ** 3

    U = Zshift2 + X2 + Y2
    U5, U6, U52, U72 = U ** 5, U ** 6, U ** 2.5, U ** 3.5

    piGammaKsi = pi * Gamma3 * Ksi
    piGammaKsi2 = piGammaKsi ** 2
    pi2GammaKsipi = pi * piGammaKsi
    G = (X2 - 2 * Zshift2 + Y2)

    A0 = 32 * pi2 * (2 * Z * Y2minusZ2 - Y2 * Z) / Y2plusZ2 ** 4
    A1 = 64 * piGammaKsi2 * G / (9 * U5)
    A2 = 16 * piGammaKsi * H0B / (3 * U52)
    A3 = 32 * piGammaKsi2 * Zshift2 / U5
    A4 = 160 * piGammaKsi2 * G ** 2 / (9 * U6)
    A5 = 40 * piGammaKsi * H0B * G / (3 * U72)
    A6 = 80 * pi2GammaKsipi * \
        (Y2minusZ2 * G + 6 * Y2 * Z * Zshift) / (3 * Y2plusZ2 ** 2 * U72)
    A7 = 160 * piGammaKsi2 * Y2plusZ2 * Zshift2 / U6
    A8 = 32 * pi2GammaKsipi * Y2minusZ2 / (3 * Y2plusZ2 ** 2 * U52)

    # print(A0, A1, A2, A3, A4, A5, A6, A7, A8)
    # print()
    B0 = 32 * pi2 * (2 * Y * Y2minusZ2 + Y * Z2) / Y2plusZ2 ** 4
    B1 = 8 * pi * H0B / (Y2 + Z2) ** 2
    B2 = 128 * pi2 * (Y2minusZ2 ** 2 + Y2 * Z2) / Y2plusZ2 ** 5
    B3 = 16 * pi * H0B * Y2minusZ2 / (Y2 + Z2) ** 3
    B4 = 64 * pi2GammaKsipi * Ksi * \
        ((Y2 - Z2) * G + 6 * Y2 * Z * Zshift) / (3 * Y2plusZ2 ** 3 * U52)
    B5 = 32 * pi2GammaKsipi / (3 * Y2plusZ2 ** 2 * U52)

    # print(B0, B1, B2, B3, B4, B5)
    # print()
    D1 = Y * Y2minusZ2 + Y * G + 6 * Y * Z * Zshift
    D2 = 2 * Zshift * Y2minusZ2 - 3 * Y2 * Zshift - 3 * Y2 * Z + Z * G

    gradHX = A1 * X - A2 * X + A3 * X - A4 * X + A8 * X + A5 * X - A7 * X - A6 * X
    gradHY = B0 - B1 * Y - B2 * Y + B3 * Y + B5 * D1 + A1 * Y - \
        A2 * Y + A3 * Y - A4 * Y + A5 * Y - B4 * Y - A6 * Y - A7 * Y
    gradHZ = B1 * Z - A0 - B2 * Z + B3 * Z - A4 * Zshift - B5 * D2 + A3 * (
        X2 + Y2) / Zshift - 2 * A1 * Zshift + 2 * A2 * Zshift + A5 * Zshift - A6 * Zshift - A7 * Zshift - B4 * Z

    VX = gradHX * CB
    VY = gradHY * CB
    VZ = gradHZ * CB + 1

    DT = (T / (ZT * (1 + (VX * VX + VY * VY + VZ * VZ)) ** Spow))

    X = X + VX * DT
    Y = Y + VY * DT
    Z = Z + VZ * DT

    if d_working_const['showDetails']:
        print(math.sqrt(X ** 2 + Y ** 2), Z, sep="\t")

    return X, Y, Z


def stopper(X, Y, Z):
    Gamma = d_constants['Gamma']

    result = (math.sqrt(Y ** 2) > 1) and (math.sqrt(X **
                                                    2 + Y ** 2 + (Z - Gamma - 1) ** 2) > Gamma)

    return result


# @jit
def pre_roy(alpha, Z0, ry=0, rn=0):
    """
    this function get
    alpha - angle from OY in XOY squere
    Z0 - coordinates from witch vesicule starts ist moving
    """
    Zlim = d_working_const['Zlim']
    DeltaR = d_working_const['DeltaR']

    R0 = 1
    R_Yes = R0

    """calculate `cos(alpha)` and `sin(alpha)` only once"""
    cos_a = math.cos(math.pi * alpha / 180)
    sin_a = math.sin(math.pi * alpha / 180)

    while True:

        X = R0 * cos_a
        Y = R0 * sin_a
        Z = Z0

        while stopper(X, Y, Z) and Z < Zlim:
            X, Y, Z = mover(X, Y, Z)

        if Z >= Zlim:
            return R0, R_Yes

        else:
            R_Yes = R0
            R0 = R0 * 1.34


# @jit
def roy(alpha, Z0, ry=0, rn=0):
    Zlim = d_working_const['Zlim']
    DeltaR = d_working_const['DeltaR']
    R_No, R_Yes = pre_roy(alpha, Z0)

    """calculate `cos(alpha)` and `sin(alpha)` only once"""
    cos_a = math.cos(math.pi * alpha / 180)
    sin_a = math.sin(math.pi * alpha / 180)

    while True:

        R0 = R_Yes + (R_No - R_Yes) / 2.0
        X = R0 * cos_a
        Y = R0 * sin_a
        Z = Z0

        while stopper(X, Y, Z) and Z < Zlim:
            X, Y, Z = mover(X, Y, Z)

        if Z >= Zlim:
            R_No = R0
        else:
            R_Yes = R0

        if R_No - R_Yes < DeltaR:
            R0 = (R_No + R_Yes) / 2.0
            X = R0 * cos_a
            Y = R0 * sin_a
            Z = Z0
            return X, Y, Z, R0


def get_capture_area(Zi, anglesRange):
    x = []
    y = []
    z = []
    r = []

    for alpha in anglesRange:
        X, Y, Z, R = roy(alpha, Zi)
        x.append(X)
        y.append(Y)
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

    # print Z

    return x, y, z, xy


def run(params):
    x = []
    y = []
    z = []
    xy = []
    anglesRange = params['A_RANGE']
    Z = params['Z0']
    global d_working_const
    d_working_const = {
        'DeltaR': params['DeltaR'],
        'ZT': params['ZT'],
        'Zlim': params['Zlim'],
        'Spow': params['Spow'],
        'T': params['T'],
        'showDetails': params['showDetails']
    }

    set_constants(
        M1=params['M1'],  # for cylinder
        M2=params['M2'],  # for elements
        H0=params['H0'],  # external magentic field
        r0=params['r0'] * 10 ** -4,  # radius of element that lain on cylinder
        R0=params['R0'] * 10 ** -4,  # radius of cylinder
        b=params['b'],  # (3-7)*10**-6
        Nu=params['Nu'],  # 1.01*10**-3 viscosity
        V0=params['V0'],  # speed of liquid
        Xu=params['Xu'],  # X parameter
    )

    x = []
    y = []
    z = []
    r = []

    x, y, z, r = get_capture_area(Z, anglesRange)
    catchR = sum(r) / len(r)
    toV = round(catchR, 2) * params['R0']
    return toV
