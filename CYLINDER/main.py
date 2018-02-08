import model
import listManager as lm

PARAMS = [
    {'DeltaR': [1]},
    {'ZT': [1]},
    {'Zlim': [20]},
    {'Spow': [1]},
    {'T': [0.05]},
    {'A_RANGE': [[90]]},
    {'M2': [485]},
    {'M1': [1687.0]},
    {'H0': [3500, 7000]},
    {'r0': [i*0.01 for i in range(1,10)]},
    {'R0': [i*0.1 for i in range(1,10)]},
    {'Xu': [10 ** -i for i in range(1,8)]},
    {'Nu': [1.01 * 10 ** -2]},
    {'V0': [1.3]},
    {'b': [
        0.1 * 10 ** -4,
    ]},
    {'Z0': [-30]},
    {'showDetails': [False]}
]


def getParamsString(params):
    result = ''
    result += '{}\t'.format(params['r0'])
    result += '{}\t'.format(params['R0'])
    result += '{}\t'.format(params['Xu'])
    result += '{}\t'.format(params['H0'])
    result += '{}\t'.format(round(params['b'] * 10 ** 4, 2))
    return result


def start():
    paramsLists = lm.manageLists(PARAMS)


    """print('r0(um)\tR0(um)\tXu\tH0(Gs)\tb(um)\tCatchingRadius(um)')
    for params in paramsLists:
        resultString = getParamsString(params)
        resultString += '{}\t'.format(model.run(params))
        print(resultString)"""

    with open("results.txt", "w") as results_file:
        results_file.write('r0(um)\tR0(um)\tXu\tH0(Gs)\tb(um)\tCatchingRadius(um)\n')
        for params in paramsLists:
            resultString = getParamsString(params)
            resultString += '{}\t'.format(model.run(params))
            results_file.write(resultString + "\n")


if __name__ == "__main__":
    start()
