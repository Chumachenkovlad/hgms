import chain_model as chain
import listManager as lm


PARAMS = [
    {'DeltaR': [0.5]},
    {'ZT': [0.1]},
    {'Zlim': [40]},
    {'Spow': [0.5]},
    {'T': [0.5]},
    {'A_RANGE':[[60]]},
    {'Hox': [0]},
    {'Hoz': [0]},
    {'r0': [100,200]},
    {'R0': [200]},
    {'ksi': [2]},
    {'Nu': [1.01 * 10 ** -2]},
    {'N': [5]},
    {'Mo': [477]},
    {'V0': [2 * 10 ** -4]},
    {'Z0': [-20]},
    {'step': [0.5]},
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
    paramsLists = lm.manageLists(PARAMS)
    print('r0(nm)   R0(nm)  ksi(10^-)   N(pcls num) CatchingRadius(nm)')
    for params in paramsLists:
        resultString = getParamsString(params)
        resultString += '{}  '.format(chain.run(params))
        print(resultString)

if __name__ == "__main__":
    start()