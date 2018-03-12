PARAMS = [
    {'DeltaR': [0.2]},
    {'ZT': [0.1]},
    {'Zlim': [20]},
    {'Spow': [0.5]},
    {'T': [0.1]},
    {'A_RANGE': [[60]]},
    {'Hox': [50]},
    {'Hoz': [50]},
    {'r0': [20]},
    {'R0': [i * 20 for i in range(1, 20)]},
    {'ksi': [4]},
    {'Nu': [1.01 * 10 ** -2]},
    {'N': [20]},
    {'Mo': [477]},
    {'V0': [2 * 10 ** -4]},
    {'Z0': [-20]},
    {'step': [1]},
    {'showDetails': [False]}
]

PARAMS_FOR_TRAEKTORY = [
    {'DeltaR': [0.2]},
    {'ZT': [0.1]},
    {'Zlim': [20]},
    {'Spow': [0.5]},
    {'T': [0.5]},
    {'A_RANGE': [[60]]},
    {'Hox': [0]},
    {'Hoz': [0]},
    {'r0': [50]},
    {'R0': [200]},
    {'ksi': [2]},
    {'Nu': [1.01 * 10 ** -2]},
    {'N': [20]},
    {'Mo': [477]},
    {'V0': [2 * 10 ** -4]},
    {'Z0': [-20]},
    {'step': [1]},
    {'showDetails': [False]}
]

DEFAULT_PARAMS = {
    'DeltaR': 0.2,
    'ZT': 0.1,
    'Zlim': 20,
    'Spow': 0.5,
    'T': 0.5,
    'A_RANGE': [60],
    'Hox': 0,
    'Hoz': 0,
    'r0': 100,
    'R0': 200,
    'ksi': 2,
    'Nu': 1.01 * 10 ** -2,
    'N': 5,
    'Mo': 477,
    'V0': 2 * 10 ** -4,
    'Z0': -20,
    'step': 1,
    'showDetails': False
    }

PARAMS_META_DATA = {
    'Hox': {
        'description': 'OX part of external \n magnetic field',
        'units': r'$ Gs$'
    },
    'Hoz': {
        'description': 'OZ part of external \n magnetic field',
        'units': r'$ Gs$'
    },
    'r0': {
         'description': 'bmn particles radius',
         'units': r'$ nm$'
    },
    'R0': {
         'description': 'vesicule radius',
         'units': r'$ nm$'
    },
    'ksi': {
         'description': 'magnetic sensitiveness \n of vesicule',
         'units': r'$ -\log(\chi)$'
    },
    'Nu':{
         'description': 'dynamic viscosity \n of medium',
         'units': r'$ \frac{g}{cm s}$'
    },
    'N': {
         'description': 'count of bmn particles',
         'units': r' pcs'
    },
    'Mo': {
         'description': 'Bmn particles magnetisation',
         'units': r''
    },
    'V0': {
         'description': r'vesicule speed',
         'units': r'$ \frac{cm}{s}$'
    },
    'DISTANCE': {
        'description': r'capturing distance',
        'units': r'$ nm$'
    }
} 

def staticParamsDescription(exeptKeys):
    paramsKeys = list(PARAMS_META_DATA.keys())
    paramsKeys = [key for key in paramsKeys if key not in exeptKeys]
    description = ""
    for key in paramsKeys:
        keyDescription = getDescription(key, DEFAULT_PARAMS[key])
        description = description + keyDescription+ '\n'
    return description    
        


def getDescription(key, value=''):
    return PARAMS_META_DATA[key]['description']+', {}'.format(value)+PARAMS_META_DATA[key]['units']