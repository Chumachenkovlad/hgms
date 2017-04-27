import model
import listManager as lm


PARAMS = [
    {'DeltaR': [1]},
    {'ZT': [1]},
    {'Zlim': [20]},
    {'Spow': [1]},
    {'T': [0.05]},
    {'A_RANGE':[[90]]},
    {'M2': [485]},
    {'M1': [1687.0]},
    {'H0': [10000]},
    {'r0': [50,100,200]},
    {'R0': [50, 100,200,300]},
    {'Xu': [1.687 * 10 ** -5]},
    {'Nu': [1.01 * 10 ** -2]},
    {'V0': [1.3]},
    {'b': [4 * 10 ** -4]},
    {'Z0': [-20]},
    {'showDetails': [False]}
]


def getParamsString(params):
    result = ''
    result += '{}   '.format(params['r0'])
    result += '{}   '.format(params['R0'])
    result += '{}   '.format(params['Xu'])
    result += '{}   '.format(params['b'])
    return result


def start():
    paramsLists = lm.manageLists(PARAMS)
    print('r0(um)   R0(um)  Xu   b(um) CatchingRadius(um)')
    for params in paramsLists:
        resultString = getParamsString(params)
        resultString += '{}  '.format(model.run(params))
        print(resultString)

if __name__ == "__main__":
    start()