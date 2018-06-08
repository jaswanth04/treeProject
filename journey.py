@outputSchema("result:tuple(uuid:chararray,journey:chararray)")
def flow(input):
        journey = ''
        prev = '' 
	for event in input:
                if prev != str(event[2]):
			journey = journey+';'+str(event[2])
                uuid = str(event[0])
		prev = str(event[2])
        return tuple([uuid,journey[1:]])

@outputSchema("treeInfo:{(turn:int,uuid:chararray,sequence:int,node:chararray,outcome:chararray,resultMode:chararray,matchValue:chararray)}")
def insertTurnwoFlush(input):
        node = []
        prev = ''
        i = 0
        for event in input:
                if (prev != str(event[2])) and not('Flush' in str(event[2])):
                        i = i+1
                if not('Flush' in str(event[2])):
                        node.append(tuple([i]+list(event)))
	                prev = str(event[2])
        return node

@outputSchema("treeInfo:{()}")
def insertTurn(input):
        node = []
        prev = ''
        i = 0
        for event in input:
                if prev != str(event[2]):
                        i = i+1
                prev = str(event[2])
                node.append(tuple([i]+list(event)))
        return node


@outputSchema("treeInfo:{()}")
def insertTurnATT(input):
        node = []
        prev = ''
        i = 0
        for event in input:
                if prev != str(event[3]):
                        i = i+1
                prev = str(event[3])
                node.append(tuple([i]+list(event)))
        return node


@outputSchema("treeInfo:{(turn:int,uuid:chararray,sequence:int,node:chararray,outcome:chararray,resultMode:chararray,matchValue:chararray)}")
def insertTurnwolld(input):
        node = []
        prev = ''
        i = 0
        for event in input:
                if (prev != str(event[2])) and not('LogInLoadingPage' in str(event[2])):
                        i = i+1
                if not('LogInLoadingPage' in str(event[2])):
                        node.append(tuple([i]+list(event)))
                        prev = str(event[2])
        return node

