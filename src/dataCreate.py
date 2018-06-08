'''
Created on May 1, 2015

@author: Jaswant.Jonnada
'''

import csv
import itertools
import json

global lines

def childNodes(turn,uuidSet,totalCalls):
    uuidList = filter(lambda x: x[1] in uuidSet ,lines[1:])
    turnNodeList = filter(lambda x: int(x[0])==turn ,uuidList)
    
    turnNodeList.sort(key = lambda x:x[3])
    group_by_node = itertools.groupby(turnNodeList,lambda x:str(x[3]))
    
    resList = []
    count = 0
    for key,group in group_by_node:
        res = {}
        uuid = set(map(lambda x:x[1],group))
        res['name'] = key
        res['size'] = len(uuid)
        res['perc'] = "%.2f" % (len(uuid)/float(totalCalls)*100)
        count = count + len(uuid)
        if len(filter(lambda x: ((x[1] in uuid) and (int(x[0])==turn+1)),uuidList)) != 0:
            res['children'] = childNodes(turn+1, uuid, len(uuid))
            print "turn is:"+str(turn)+";node:"+key 
        resList.append(res)
    
    hangupCount = totalCalls-count
    if hangupCount != 0:
        hangup = {'name':'hangup','size':hangupCount,'perc':"%.2f" % ((hangupCount/float(totalCalls))*100)}
        resList.append(hangup)
    
    return resList


treeFile = open('../upsTreeData.csv')
treeFileReader = csv.reader(treeFile)

lines = []
for line in treeFileReader:
    lines.append(line)

#Listing the first nodes    
firstNodeList = filter(lambda x: int(x[0])==1 ,lines[1:])

#Grouping by firstNode
firstNodeList.sort(key = lambda x:x[3])
gb = itertools.groupby(firstNodeList,lambda x:str(x[3]))

resList = []
totalCalls = len(set(map(lambda x:x[1],lines[1:])))
count = 0

for key,group in gb:
    res = {}
    uuid = set(map(lambda x:x[1],group))
    res['name'] = key
    res['size'] = len(uuid)
    res['perc'] = "%.2f" % (len(uuid)/float(totalCalls)*100)
    count = count + len(uuid)
    if len(filter(lambda x: ((x[1] in uuid) and (int(x[0])==2)),lines[1:])) != 0:
        res['children'] = childNodes(2, uuid, len(uuid))
    resList.append(res)
    print count
    
hangupCount = totalCalls-count
if hangupCount != 0:
    hangup = {'name':'hangup','size':hangupCount,'perc':"%.2f" % ((hangupCount/float(totalCalls))*100)}
    resList.append(hangup)
print resList
 
finalJson = {}
finalJson['name'] = 'Total'
finalJson['size'] = totalCalls
finalJson['children'] = resList
 
with open('D:\\d3js_projects\\flare_mm.json','w') as jsonFile:
    json.dump(finalJson,jsonFile)
    print "successfully written"



