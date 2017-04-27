
def manageParams(paramsLists):
    uniqueParamsLists = []

    for paramsList in paramsLists:
        paramKey = next(iter(paramsList))
        keyList = []
        for value in paramsList[paramKey]:
            keyList.append({paramKey: value})
        uniqueParamsLists.append(keyList)
    return uniqueParamsLists

def manageLists(listsOfParams):
    paramsLists = manageParams(listsOfParams)

    # [[{'key1': 1}, {'key1': 2}, {'key1': 3}], [{'key2': 1}, {'key2': 2}, {'key2': 3}]]
    finalList = []
    buffer = []
    for paramsList in paramsLists: # paramsList == [{'key1': 1}, {'key1': 2}, {'key1': 3}]
        # print(paramsList)
        # print(finalList)
        if len(finalList) == 0:
            # print(paramsList)
            finalList = paramsList.copy()
        else:
             for paramNew in paramsList:
                 for paramOld in finalList:
                    context = {}
                    context.update(paramOld)
                    context.update(paramNew)
                    buffer.append(context)
             finalList = buffer
             buffer = []
    return finalList
