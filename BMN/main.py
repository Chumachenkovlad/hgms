import sys
sys.path.append('..')
import chain_model as chain
import listManager as lm
import drawer as drawer
from params import *
from input_data import *
import math


def getParamsString(params):
    result = ''
    result += '{}   '.format(params['r0'])
    result += '{}   '.format(params['R0'])
    result += '{}   '.format(params['ksi'])
    result += '{}   '.format(params['N'])
    return result


def runTraectoryExperiment():
    START_Z = -40
    traectories = []
    for R in [0, 5, 10, 20]:
        # resultString = getParamsString(params)
        chain.set_params(DEFAULT_PARAMS)
        options = {
            'coors': (R, R, START_Z),
            'limit': 1000
        }
        dt = DEFAULT_PARAMS['dt']
        points = chain.get_traectory(options)
        pointToR = lambda p: math.sqrt(sum(map(lambda coor: coor**2, p['COORS']))) 
        valuesRange = list(map(pointToR, [points[i] for i in range(len(points))]))
        timesRange = [i*dt for i in range(len(points))]

        x = [points[i]['COORS'][0] for i in range(len(points))]
        y = [points[i]['COORS'][1] for i in range(len(points))]
        z = [points[i]['COORS'][2] for i in range(len(points))]

        traectories.append({'x': x, 'y': y, 'z': z, 'R': R, 'DEFAULT_PARAMS': DEFAULT_PARAMS})
    drawer.draw3DTraectory(traectories);    

def runWalkingToChainExperiment(default_params):
    traectories = []
    dt = default_params['dt']
    V0 = default_params['V0']
    r0 = default_params['r0']
    for N in [1 , 3, 5, 7]:
        chain.set_params({**default_params, **{
                    'ksi': N
                }})
        options = {
            'coors': (0, 0, -(default_params['cell_R'] / r0)),
            'limit': 0
        }
        points = chain.get_traectory(options)

        t = {
            'x': [i*dt*(V0/(r0*10**-7)) for i in range(len(points))],
            'y': [default_params['cell_R']+points[i]['COORS'][2]*r0 for i in range(len(points))],
            **{'R': N}
        }
        traectories.append(t)

        print(points.__len__() * dt, sep="\t")

    drawer.drawWalkingToChain(traectories)

def plots_data(primary_params, secondary_params):
    plots = []
    for secondary_value in secondary_params['values']:
        plot = {
            'secondaryParamValue': secondary_value,
            'secondaryParamKey': secondary_params['key'],
            'primaryParamKey': primary_params['key'],
            'x': [],
            'y': []
        }
        for primary_value in primary_params['values']:
            # extend default params by chosen
            params = {**DEFAULT_PARAMS, **{
                primary_params['key']: primary_value,
                secondary_params['key']: secondary_value
            }}    
            chain.set_params(params)
            distance = chain.get_catching_distance_to_vesicule(params)
            plot['y'].append(distance)
            plot['x'].append(primary_value)
            print(secondary_value, primary_value, distance, sep="\t")
        plots.append(plot)    
    drawer.drawPlots(plots)

def runDistanceExperiment():
    distanceExperimentData = getCapturingDistanceExperimentData()
    for pair in distanceExperimentData:
        primary_params, secondary_params = pair
        plots_data(primary_params, secondary_params) 
    
if __name__ == "__main__":
    # runDistanceExperiment()
    runTraectoryExperiment()
    # for params in SERIES:
    #     runWalkingToChainExperiment(params)
        

