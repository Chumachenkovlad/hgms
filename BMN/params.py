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
    'r0': 50,
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
        'desctiption': lambda v: r'OX part of external magnetic field,{}$ Gs$'.format(v)
    },
    'Hoz': {
        'desctiption': lambda v: r'OZ part of external magnetic field,{}$ Gs$'.format(v)
    },
    'r0': {
         'desctiption': lambda v: r'bmn particles radius,{}$ nm$'.format(v)
    },
    'R0': {
         'desctiption': lambda v: r'vesicule radius,{}$ nm$'.format(v)
    },
    'ksi': {
         'desctiption': lambda v: r'magnetic sensitiveness of vesicule, {}$ -\log(\chi)$'.format(v)
    },
    'Nu':{
         'desctiption': lambda v: r'dynamic viscosity of medium, {}$ Gs$'.format(v)
    },
    'N': {
         'desctiption': lambda v: r'OX part of external magnetic field, {}$ Gs$'.format(v)
    },
    'Mo': {
         'desctiption': lambda v: r'OX part of external magnetic field, {}$ Gs$'.format(v)
    },
    'V0': {
         'desctiption': lambda v: r'OX part of external magnetic field, {}$ Gs$'.format(v)
    },
}    

print(PARAMS_META_DATA['Hox']['desctiption'](5))