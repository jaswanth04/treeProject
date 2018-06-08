'''
Created on May 5, 2015

@author: Jaswant.Jonnada
'''

import csv
import itertools
import json

def children(flows,turn,total):
    lessTurns = []
    moreTurns = []
    for item in flows:
        if len(item[0])<=turn:
            lessTurns.append(item)
        else:
            moreTurns.append(item)
            
    moreTurns.sort(key = lambda x:x[0][turn])
    gbc = itertools.groupby(moreTurns,lambda x:x[0][turn])
    
    resList = []
    
    for key,group in gbc:
        res = {}
        groupList = list(group)
        res['name'] = key
        calls = sum(map(lambda x:int(x[1]),groupList))
        res['size'] = calls
        res['perc'] = "%.2f" % (calls/float(total)*100)
        if max(map(lambda x:len(x[0]),groupList)) > (turn+1):
            res['children'] = children(groupList,turn+1,calls)
        resList.append(res)
    
       
    dropOff = sum(map(lambda x:int(x[1]),lessTurns))
    if dropOff != 0:
        resList.append({'name':'DropOff','size':dropOff,'perc':"%.2f" % ((dropOff/float(total))*100)})
    
    return resList

journeyFile = open('../upsJourneyCount.csv')
journeyFileReader = csv.reader(journeyFile)

lines = []
for line in journeyFileReader:
    lines.append([line[0].split(';'),line[1]])
    
journey = lines

#Grouping by firstNode
journey.sort(key = lambda x:x[0][0])
gb = itertools.groupby(journey,lambda x:x[0][0])

total = sum(map(lambda x:int(x[1]),journey))

resList = []

count = 0
for key,group in gb:
    res = {}
    groupList = list(group)
    res['name'] = key
    calls = sum(map(lambda x:int(x[1]),groupList))
    count = count + calls
    res['size'] = calls
    res['perc'] = "%.2f" % (calls/float(total)*100)
    if max(map(lambda x:len(x[0]),groupList)) > 1:
        res['children'] = children(groupList,1,calls)
    resList.append(res)
    
dropOff = total - count

if dropOff != 0:
    resList.append({'name':'DropOff','size':dropOff,'perc':"%.2f" % ((dropOff/float(total))*100)})
    
finalJson = {}
finalJson['name'] = 'Total'
finalJson['size'] = total
finalJson['children'] = resList


with open('D:\\d3js_projects\\flare_mm11.json','w') as jsonFile:
    json.dump(finalJson,jsonFile)
    print "successfully written"