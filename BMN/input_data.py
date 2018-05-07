# capturing distance experiment

def getCapturingDistanceExperimentData():
    return [
        (# R0 - Ksi
            {
                'key': 'R0',
                'values': [50, 100, 250]
            },
            {
                'key': 'ksi',
                'values': [6,4,2]
            }
        ),
        # !!!!!!!!!!!!!!!!!!
        # (# r0 - Ksi
        #     {
        #         'key': 'r0',
        #         'values': [5, 10, 25, 50]
        #     },
        #     {
        #         'key': 'ksi',
        #         'values': [6,4,2]
        #     }
        # ),
        # (# Ksi - N
        #     {
        #         'key': 'ksi',
        #         'values': [7,6,5,4,3,2]
        #     },
        #     {
        #         'key': 'N',
        #         'values': [5,10,25,50]
        #     }
        # ),
        # !!!!!!!!!!!!!!!!!
        # (#r0 - N
        #     {
        #         'key': 'r0',
        #         'values': [5, 10, 25, 50]
        #     },
        #     {
        #         'key': 'R0',
        #         'values': [50, 100, 250]
        #     }
        # ),
        # (# R0 - N
        #     {
        #         'key': 'R0',
        #         'values': [20, 50, 75, 100, 150, 200, 300,400, 500]
        #     },
        #     {
        #         'key': 'N',
        #         'values': [5,10,25,50]
        #     }
        # ),
        # (# Nu - R0
        #     {
        #         'key': 'R0',
        #         'values': [20, 50, 75, 100, 150, 200, 300, 500]
        #     },
        #     {
        #         'key': 'Nu',
        #         'values': [ 1.01 * 10 ** i for i in [-2,-1.5,-1,-0.5, 1]]
        #     }
        # )
    ]
