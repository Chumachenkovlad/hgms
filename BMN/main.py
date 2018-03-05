import sys
sys.path.append('..')
import chain_model as chain
import listManager as lm
import drawer as drawer
from params import *



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

def plots_data():
    primary_params = {
        'R0': [50, 100, 200, 300, 500, 750]
    }
    secondary_params = {
        'ksi': [2,3,4,5,6,7]
    }
    plots = {}
    for secondary_value in secondary_params['ksi']:
        plots[secondary_value] = {
            'x': [],
            'y': []
        }
        for primary_value in primary_params['R0']:
            params = {**DEFAULT_PARAMS, **{
                'R0': primary_value,
                'ksi': secondary_value
            }}
            chain.set_params(params)
            distance = chain.get_catching_distance_to_vesicule(params)
            plots[secondary_value]['y'].append(distance)
            plots[secondary_value]['x'].append(primary_value)
    print(plots)
    drawer.drawPlots(plots)
    
if __name__ == "__main__":
    # start()
    plots_data()
