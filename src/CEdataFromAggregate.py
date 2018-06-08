import csv
import itertools
import json

def children(flows,turn,total,outcome,completed):
    lessTurns = []
    moreTurns = []
    for item in flows:
        if len(item[0])<=turn:
            lessTurns.append(item)
        else:
            moreTurns.append(item)

    moreTurns.sort(key = lambda x:x[0][turn]['dialogName'])
    gbc = itertools.groupby(moreTurns,lambda x:x[0][turn]['dialogName'])

    resList = []

    for key,group in gbc:
    #if key == 'GetCountry':
        res = {}
        groupList = list(group)
        groupList.sort(key=lambda x:(x[0][turn]['outcome'],x[0][turn]['completed']))
        outcomeMoreGroup = itertools.groupby(groupList,lambda x:(x[0][turn]['outcome'],x[0][turn]['completed']))
        # for group in groupList:
        #     print group[0][turn]
        res['name'] = key
        calls = sum(map(lambda x:int(x[1]),groupList))
        res['size'] = calls
        res['perc'] = "%.2f" % (calls/float(total)*100)
        res['outcome'] = outcome
        res['completed'] = completed
        moreChildrenList = []
        for (outcomeMore,completedMore), outcomeMoreDialogGroup in outcomeMoreGroup:
            # print 'In turn' + str(turn)
            # print (key,outcomeMore,completedMore)
            outcomeMoreDialogList = list(outcomeMoreDialogGroup)
            max_turn_present = max(map(lambda x:len(x[0]),outcomeMoreDialogList))
            # print max_turn_present
            if max_turn_present >= (turn+1):
                moreChildrenList.append(children(outcomeMoreDialogList,turn+1,calls,outcomeMore,completedMore))
        res['children'] = [item for sublist in moreChildrenList for item in sublist]
        resList.append(res)

    lessTurnList = []

#The below code is working fine
    for item in lessTurns:
        lessDict = {}
        lessDict['name'] = 'DropOff'
        lessDict['outcome'] = outcome
        lessDict['completed'] = completed
        lessDict['size'] = float(item[1])
        lessDict['perc'] = float(item[1])/total * 100
        lessTurnList.append(lessDict)

    resList.extend(lessTurnList)
    #print lessTurns
    return resList

with open('../data/avis_dialogJourney_count_feb.tsv') as journeyTsv:
    journeyData = csv.reader(journeyTsv, delimiter='\t')

    journeyDictList = []
    for journey in journeyData:
        dialogJourney = []
        dialogList = journey[0].split(';;')
        dialogNewList = []
        for dialog in dialogList:
            dialogDict = {}
            dialogInfo = dialog.split('/')
            dialogDict['dialogName'] = dialogInfo[0]
            dialogDict['outcome'] = dialogInfo[1]
            dialogDict['completed'] = dialogInfo[2]
            dialogNewList.append(dialogDict)
        journeyDictList.append([dialogNewList,journey[1]])



journeyDictList.sort(key=lambda x:x[0][0]['dialogName'])
turnGroup = itertools.groupby(journeyDictList,lambda x:x[0][0]['dialogName'])

total = sum(map(lambda x:int(x[1]),journeyDictList))
jsonList = []
finalJson = {}

for turnDialog,turnDialogGroup in turnGroup:
    # if turnDialog == 'CarOrTruck':
    jsonElement = {}
    turnDialogList = list(turnDialogGroup)
    jsonElement['name'] = turnDialog
    turnDialogCallCount = sum(map(lambda x:int(x[1]),turnDialogList))
    jsonElement['size'] = turnDialogCallCount
    jsonElement['perc'] = turnDialogCallCount/float(total) * 100
    childrenList = []
    turnDialogList.sort(key=lambda x:(x[0][0]['outcome'],x[0][0]['completed']))
    outcomeGroup = itertools.groupby(turnDialogList,lambda x:(x[0][0]['outcome'],x[0][0]['completed']))
    for (outcome,completed), outcomeDialogGroup in outcomeGroup:
        outcomeDialogList = list(outcomeDialogGroup)
        if max(map(lambda x:len(x[0]),outcomeDialogList)) >= 1:
            childrenList.append(children(outcomeDialogList,1,turnDialogCallCount,outcome,completed))
    jsonElement['children'] = [item for sublist in childrenList for item in sublist]
    jsonList.append(jsonElement)

finalJson['name'] = 'Total'
finalJson['size'] = total
finalJson['children'] = jsonList

print finalJson

with open('D:/VegaVis/flare_mm11.json','w') as jsonFile:
    json.dump(finalJson,jsonFile)
    print "successfully written"


