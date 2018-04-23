import sys
sys.path.append('..')
import chain_model as chain
import listManager as lm
import drawer as drawer
from params import *
from input_data import *


def getParamsString(params):
    result = ''
    result += '{}   '.format(params['r0'])
    result += '{}   '.format(params['R0'])
    result += '{}   '.format(params['ksi'])
    result += '{}   '.format(params['N'])
    return result


def runTraectoryExperiment():
    paramsLists = lm.manageLists(PARAMS_FOR_TRAEKTORY)
    # print('r0(nm)   R0(nm)  ksi(10^-)   N(pcls num) CatchingRadius(nm)')
    traectories = []
    for R in [0]: #chain.frange(0,20,4):
        # resultString = getParamsString(params)
        chain.set_params(DEFAULT_PARAMS)
        options = {
            'coors': (R, R, -10),
            'limit': True
        }
        points = chain.get_traectory(options)
        traectories.append({**chain.prepare_traectory_data(points), **{'R': R}})
    drawer.drawTraectories(traectories)
        # chain.run(params)
        # resultString += '{}  '.format(chain.run(params))
        # print(resultString)

def runWalkingToChainExperiment():
    paramsLists = lm.manageLists(PARAMS_FOR_TRAEKTORY)
    # print('r0(nm)   R0(nm)  ksi(10^-)   N(pcls num) CatchingRadius(nm)')
    traectories = []
    dt = DEFAULT_PARAMS['dt']
    for N in [0,1, 3, 7, 25]:
        chain.set_params({**DEFAULT_PARAMS, **{
                    'N': N
                }})
        options = {
            'coors': (0, 0, -(DEFAULT_PARAMS['cell_R'] / DEFAULT_PARAMS['r0'])),
            'limit': True
        }
        points = chain.get_traectory(options)
        t = {
            'x': [i*dt for i in range(len(points))],
            'y': [points[i]['COORS'][2] for i in range(len(points))],
            **{'R': N}
        }
        traectories.append(t)
        # print(t)
        print(points.__len__() * dt, sep="\t")

    drawer.drawTraectories(traectories)
        # chain.run(params)
        # resultString += '{}  '.format(chain.run(params))
        # print(resultString)

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
        plots.append(plot)    
    drawer.drawPlots(plots)

def runDistanceExperiment():
    distanceExperimentData = getCapturingDistanceExperimentData()
    for pair in distanceExperimentData:
        primary_params, secondary_params = pair
        plots_data(primary_params, secondary_params) 
    
if __name__ == "__main__":
    # runDistanceExperiment()
    # runTraectoryExperiment()
    runWalkingToChainExperiment()

