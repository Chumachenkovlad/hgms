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


def start():
    paramsLists = lm.manageLists(PARAMS_FOR_TRAEKTORY)
    # print('r0(nm)   R0(nm)  ksi(10^-)   N(pcls num) CatchingRadius(nm)')
    traectories = []
    for params in paramsLists:
        print(params)
        for R in range(5, 20):
            # resultString = getParamsString(params)
            chain.set_params(params)
            options = {
                'coors': (R, R, -20)
            }
            points = chain.get_traectory(options)
            traectories.append(chain.prepare_traectory_data(points))
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
                'R0': primary_value,
                'ksi': secondary_value
            }}
            chain.set_params(params)
            distance = chain.get_catching_distance_to_vesicule(params)
            plot['y'].append(distance)
            plot['x'].append(primary_value)
        plots.append(plot)    
    drawer.drawPlots(plots)
    
if __name__ == "__main__":
    distanceExperimentData = getCapturingDistanceExperimentData()
    for pair in distanceExperimentData:
        primary_params, secondary_params = pair
        try:
            plots_data(primary_params, secondary_params)
        except Exception:
            print(primary_params, secondary_params, 'dont work')
            pass

