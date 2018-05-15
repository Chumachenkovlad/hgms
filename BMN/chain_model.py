from numba import jit
import math
import random
from random import randrange
import numpy
pi = math.pi
pi2 = math.pi ** 2

d_constants = dict()  # working constants
d_physical_const = dict()  # dict for physical parameters


def getRandomVector():
    v = [numpy.random.normal(0, 1) for i in range(0, 3)]
    inv_len = 1.0 / math.sqrt(sum(coord * coord for coord in v))
    return [coord * inv_len for coord in v]

@jit
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
    Ho = kw['Ho']

    r0 = kw['r0']
    R0 = kw['R0']
    ksi = kw['ksi']
    Nu = kw['Nu']
    N = kw['N']
    V0 = kw['V0']
    trueDelta = r0 / 2

    global d_constants

    CB = 4 * pi * ksi * r0 ** 2 * Mo ** 2 / \
        (27 * Nu * R0 * V0)  # 4*pi*ksi*r0^2*Mo^2/(27*nu*R0)
    Ex = 3 * pi * Ho / (2 * Mo)
    Ez = 3 * pi * Ho / (2 * Mo)
    Rm = (R0 / r0) ** 2
    delta = trueDelta / r0 + 2


    dt = d_working_const['dt']
    diffusion_exp = d_working_const['diffusion_exp']
    dimensions_count = d_working_const['dimensions_count']

    T = (dt * r0/ V0)

    # deffusion data
    R_BOLTSMANA = 1.3806488 * 10 ** -16
    TEMP = 273 + 37
    DEFFUSION_CONST = R_BOLTSMANA * TEMP / (3 * pi * Nu * R0)
    MSD_NORMAL_DISTRIBUTION_LIST = list(map(math.fabs, 
        numpy.random.normal(0, 
            2 * dimensions_count * DEFFUSION_CONST * T ** diffusion_exp, 1000))) #2dDt^a
    RANDOM_VECTORS = [getRandomVector() for i in range(1000)]
    constants = {
        'N': N,
        'CB': CB,
        'Ex': Ex,
        'Ez': Ez,
        'mR': Rm,
        'delta': delta,
        'D': R0 / r0,
        'DEFFUSION_CONST': DEFFUSION_CONST,
        'MSD_NORMAL_DISTRIBUTION_LIST': MSD_NORMAL_DISTRIBUTION_LIST,
        'RANDOM_VECTORS': RANDOM_VECTORS
    }

    d_constants = {**d_constants, **constants}

def getPointMSD():
    msd = random.choice(d_constants['MSD_NORMAL_DISTRIBUTION_LIST'])
    vector = random.choice(d_constants['RANDOM_VECTORS'])
    r0 = d_physical_const['r0']
    x_shift, y_shift, z_shift = [msd * projection / r0 for projection in vector]
    return x_shift, y_shift, z_shift

@jit
def f(X1, Y1, Z1, X, Y, Z):
    """
    this function get:
    1) coordinates of point into vesicule
    2) coordinates of center of vesicule
    and return fx, fy, fz summs of forces of each bmn of chain
    """
    Ex = d_constants['Ex']
    Ez = d_constants['Ez'] 
    delta = d_constants['delta'] 
    N = d_constants['N']

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


@jit
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
    limX1 = math.sqrt(mR)
    step = limX1 * 2 / 15  # d_working_const['step']  # math.sqrt(mR)/10
    step_volume = step ** 3
    """set a variation of X1,Y1,Z1 coors into vesicle"""
    for X1 in list(frange(-limX1, limX1, step)):
        limY1Y1 = mR - X1 ** 2
        if (limY1Y1 <= 0): continue
        limY1 = math.sqrt(limY1Y1)

        for Y1 in list(frange(-limY1, limY1, step)):
            limZ1Z1 = mR - X1 ** 2 - Y1 ** 2
            if (limZ1Z1 <= 0): continue
            limZ1 = math.sqrt(limZ1Z1)

            for Z1 in list(frange(-limZ1, limZ1, step)):
  
                dfx, dfy, dfz = f(X1, Y1, Z1, X, Y, Z)

                i_gradHX += dfx * step_volume
                i_gradHY += dfy * step_volume
                i_gradHZ += dfz * step_volume

    return i_gradHX, i_gradHY, i_gradHZ


@jit
def mover(X, Y, Z):
    """
    this function get old coordinates of center of vesicule
    return new coordinates
    """
    CB = d_constants['CB']  # 4pi*ksi*r0^2*Mo^2/(27*nu*R0)
    MSD_NORMAL_DISTRIBUTION_LIST = d_constants['MSD_NORMAL_DISTRIBUTION_LIST']
    RANDOM_VECTORS = d_constants['RANDOM_VECTORS']
    r0 = d_physical_const['r0']
    dt = d_working_const['dt']
    possible_direction = d_working_const['possible_direction']
    

    """
    calculate integral of gradient^2 by volume of vesicle
    """
    gradHX, gradHY, gradHZ = tpl_integral(X, Y, Z)

    """calculete speed for x y z directions"""
    VX = gradHX * CB  # We can add 1 with + or -
    VY = gradHY * CB  # to each  VX,VY,VZ
    VZ = gradHZ * CB + 1 # to chenge direction of movement of vesicule
    """calculete elementary time size"""

    deffusion_shift = random.choice(MSD_NORMAL_DISTRIBUTION_LIST)
    x_shift, y_shift, z_shift = getPointMSD()

    """calculate new coordinates of vesicle after moving DT time interval"""
    if 'x' in possible_direction:
        X += VX * dt + x_shift
    if 'y' in possible_direction:
        Y += VY * dt + y_shift
    if 'z' in possible_direction:
        Z += VZ * dt + z_shift

    if d_working_const['show_details']:
        print(math.sqrt(X ** 2 + Y ** 2), Z)
    return X, Y, Z


def stopper(X, Y, Z):
    """this function return false if vesicule will be
       captured by chain of bmn
    """
    D = d_constants['D']
    return math.sqrt(Y ** 2 + X ** 2) > 2 + D  # working only for movement of
    # vesicule in OZ axes direction movement


@jit
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
        oX, oY, oZ = X, Y, Z
        while stopper(X, Y, Z) and Z < 10:
            oX, oY, oZ = X, Y, Z
            X, Y, Z = mover(X, Y, Z)
        # print(R0, math.fabs(Z - oZ), math.fabs(X - oX), math.fabs(Y - oY))    
        if Z > 10  and math.fabs(Z - oZ) < 0.15 and  math.fabs(X - oX) < 0.15 and math.fabs(Y - oY) < 0.15:
            return R0, R_Yes
        else:
            R_Yes = R0
            R0 = R0 * 2


@jit
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
        # print(R0,R_No, R_Yes )
        X = R0 * cos_a
        Y = R0 * sin_a
        Z = Z0
        oX, oY, oZ = X, Y, Z
        while stopper(X, Y, Z) and Z < 10:
            # print(stopper(X, Y, Z), Z < N * delta * 1.2, X, Y, Z)
            oX, oY, oZ = X, Y, Z
            X, Y, Z = mover(X, Y, Z)
        # print(R0, math.fabs(Z - oZ)) 
        if Z > 10  and math.fabs(Z - oZ) < 0.15 and  math.fabs(X - oX) < 0.15 and math.fabs(Y - oY) < 0.15:
            R_No = R0 
        else:
            # print('R_Yes = R0')
            R_Yes = R0  

        if R_No - R_Yes < DeltaR:
            # print('X, Y, Z, R0')
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


def get_traectory(options):
    Zlim = d_working_const['Zlim']
    DeltaR = d_working_const['DeltaR']
    D = d_constants['D']
    N = d_constants['N']
    delta = d_constants['delta']
    cell_R = d_working_const['cell_R']
    over_step_count = 0
    points = []
    X, Y, Z = options['coors'];
    if (not options['limit']):
        while True:
            point = {};
            point['COORS'] = mover(X, Y, Z)
            X, Y, Z = point['COORS']
            # print(Z)
            if Z < 0:
                point['DISTANCE_TO_ZO_AXE'] = Z
                points.append(point)
            if Z > -1:
                break
    else:            
        for i in range(options['limit']):
            if over_step_count > 10 or Z > 5 * delta * 1.2:
                break
        # while stopper(X, Y, Z) and Z < N * delta * 1.2:
            point = {};
            point['COORS'] = mover(X, Y, Z)
            print(math.sqrt(  (point['COORS'][0] - X)**2 + (point['COORS'][1] - Y)**2 + (point['COORS'][2] - Z)**2   ))
            if(math.sqrt(sum(map(lambda c: c**2, point['COORS'])))) < D + 1.5:
                print('touch')
                break
            if (math.sqrt(  (point['COORS'][0] - X)**2 + (point['COORS'][1] - Y)**2 + (point['COORS'][2] - Z)**2   )) > 5:
                over_step_count+=1
                continue
            X, Y, Z = point['COORS'];
            point['DISTANCE_TO_ZO_AXE'] = X # math.sqrt(X ** 2 + Y**2)
            points.append(point)
    return points

def prepare_traectory_data(points):
    y = list(map(lambda p: float(p['COORS'][2]), points)) # Z
    x = list(map(lambda p: float(p['DISTANCE_TO_ZO_AXE']), points)) # R 
    return {'x': x, 'y': y}      

def set_params(params):
    globals()['A'] = params['A_RANGE']
    # globals()['Z'] = #params['Z0']
    global d_working_const
    d_working_const = {
        'chain': params['chain'],
        'dimensions_count': params['dimensions_count'],
        'dt': params['dt'],
        'cell_R': (params['cell_R'] / params['r0']) ,
        'diffusion_exp': params['diffusion_exp'],
        'DeltaR': params['DeltaR'],
        'ZT':     params['ZT'],
        'Zlim':   params['Zlim'],
        'Spow':   params['Spow'],
        'T':      params['T'],
        'V0': params['V0'],
        'step':   params['step'],
        'show_details': params['show_details'],
        'possible_direction': params['possible_direction'],
        'normalDistribution': numpy.random.normal(0, 1)
    }
    globals()['Z'] =params['Z0'] #  -d_working_const['cell_R']

    set_constants(
        Ho=-params['Ho'],
        r0=params['r0'] * 10 ** -7,
        R0=params['R0'] * 10 ** -7,
        ksi=10 ** (-1*params['ksi']),
        Nu=params['Nu'],
        N=params['N'],
        Mo=params['Mo'],
        V0=params['V0']
    )

def run(params):
    # Z,A are global params
    x, y, z, r = get_capture_area(Z, A)
    R, r = params['R0'], params['r0']
    catchR = sum(r) / len(r) - R / r
    distanceToVesicule = round(catchR, 2) * r
    return distanceToVesicule

def get_catching_distance_to_vesicule(params):
    x, y, z, r = get_capture_area(Z, A)
    R0, r0 = params['R0'], params['r0']
    catchR = sum(r) / len(r) - R0 / r0
    distanceToVesicule = round(catchR, 2) * r0
    # print(distanceToVesicule)
    return distanceToVesicule