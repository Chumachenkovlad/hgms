DEFAULT_PARAMS = {
    'dimensions_count': 2,
    'dt': 0.1,
    'cell_R': 10000,
    'diffusion_exp': 0.8,
    'DeltaR': 0.01,
    'ZT': 0.1,
    'Zlim': 20,
    'Spow': 0.5,
    'T': 0.1,
    'A_RANGE': [60],
    'Ho': 7000,
    'r0': 50,
    'R0': 250,
    'ksi': 6,
    'Nu': 1.01 * 10 ** -2,
    'N': 5,
    'Mo': 477,
    'V0': 2 * 10 ** -4,
    'Z0': -20,
    'step': 1,
    'showDetails': False,
    'chain': True
    }

SERIES = [
    # Magnetic field - HIGH, vesicle sensitive - HIGH
    # {**DEFAULT_PARAMS,**{'Ho': 7000, 'ksi': 2}},
    # Magnetic field - HIGH, vesicle sensitive - LOW
    # {**DEFAULT_PARAMS,**{'Ho': 7000, 'ksi': 6}},
    # Magnetic field - LOW, vesicle sensitive - HIGH
    {**DEFAULT_PARAMS,**{'Ho': 50, 'ksi': 2}}
    # Magnetic field - LOW, vesicle sensitive - LOW
    # {**DEFAULT_PARAMS,**{'Ho': 50, 'ksi': 6}},
]    

PARAMS_META_DATA = {
    'Ho': {
        'description': 'OX part of external \nmagnetic field',
        'units': r'$ Gs$'
    },
    'r0': {
         'description': 'BMN particles radius',
         'units': r'$ nm$'
    },
    'R0': {
         'description': 'Vesicule radius',
         'units': r'$ nm$'
    },
    'ksi': {
         'description': 'Magnetic sensitiveness \nof vesicule',
         'units': r'$ -\log(\chi)$'
    },
    'Nu':{
         'description': 'Dynamic viscosity \nof medium',
         'units': r'$ \frac{g}{cm s}$'
    },
    'N': {
         'description': 'Count of bmn\nparticles',
         'units': r' pcs'
    },
    'Mo': {
         'description': 'BMN particles\nmagnetisation',
         'units': r''
    },
    'V0': {
         'description': r'Vesicule speed',
         'units': r'$ \frac{cm}{s}$'
    },
    'DISTANCE': {
        'description': r'Capturing distance',
        'units': r'$ nm$'
    }
} 
PARAMS_META_DATA_UA = {
    'Ho': {
        'description': 'Зовнішнє магнітне поле',
        'units': r'$ Гс$'
    },
    'r0': {
         'description': 'Радіус БМН',
         'units': r'$ нм$'
    },
    'R0': {
         'description': 'Радіус везикули',
         'units': r'$ нм$'
    },
    'ksi': {
         'description': 'Магнітна\nсприйнятливість\nвезикули',
         'units': r'$ -\log(\chi)$'
    },
    'Nu':{
         'description': 'Динамічна в\'язкість \nсередовища',
         'units': r'$ \frac{г}{см с}$'
    },
    'N': {
         'description': 'Кількість частинок\nу ланцюжку',
         'units': r' шт'
    },
    'Mo': {
         'description': 'Намагнічесність БМН',
         'units': r''
    },
    'V0': {
         'description': r'Швидкість везикули',
         'units': r'$ \frac{см}{с}$'
    },
    'DISTANCE': {
        'description': r'Розмір зони захоплення',
        'units': r'$ нм$'
    }
} 

def staticParamsDescription(exeptKeys):
    paramsKeys = list(PARAMS_META_DATA_UA.keys())
    paramsKeys = [key for key in paramsKeys if key not in exeptKeys]
    description = ""
    for key in paramsKeys:
        keyDescription = getDescription(key, DEFAULT_PARAMS[key])
        description = description + keyDescription+ '\n\n'
    return description    
        


def getDescription(key, value=''):
    return PARAMS_META_DATA_UA[key]['description']+', {} '.format(value)+PARAMS_META_DATA_UA[key]['units']