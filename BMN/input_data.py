# capturing distance experiment

def getCapturingDistanceExperimentData():
    return [
        # (# R0 - Ksi
        #     {
        #         'key': 'R0',
        #         'values': [20, 50, 75, 100, 150, 200, 300, 500]
        #     },
        #     {
        #         'key': 'ksi',
        #         'values': [2,3,4,5,6,7]
        #     }
        # ),
        # (# r0 - Ksi
        #     {
        #         'key': 'r0',
        #         'values': [5, 10, 25, 50, 75, 100]
        #     },
        #     {
        #         'key': 'ksi',
        #         'values': [2,3,4,5,6,7]
        #     }
        # ),
        # (# Ksi - N
        #     {
        #         'key': 'ksi',
        #         'values': [2,3,4,5,6,7]
        #     },
        #     {
        #         'key': 'N',
        #         'values': [5,10,25,50]
        #     }
        # ),
        # (#r0 - N
        #     {
        #         'key': 'r0',
        #         'values': [5, 10, 25, 50, 75, 100]
        #     },
        #     {
        #         'key': 'N',
        #         'values': [5,10,25,50]
        #     }
        # ),
        (# R0 - N
            {
                'key': 'R0',
                'values': [20, 50, 75, 100, 150, 200, 300, 500]
            },
            {
                'key': 'N',
                'values': [1,2,3,4, 5, 10]
            }
        ),
        # (# Nu - R0
        #     {
        #         'key': 'R0',
        #         'values': [20, 50, 75, 100, 150, 200, 300, 500]
        #     },
        #     {
        #         'key': 'Nu',
        #         'values': [
        #             1.01 * 10 ** -2,
        #             1.01 * 10 ** -1,
        #             1.01
        #             ]
        #     }
        # )
    ]
