import sys
sys.path.append('..')
import chain_model as chain
import listManager as lm
import drawer as drawer

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


if __name__ == "__main__":
    start()
