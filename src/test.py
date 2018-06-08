'''
Created on May 1, 2015

@author: Jaswant.Jonnada
'''

from itertools import groupby

data = [['c','a'],'a','b','c','d']


gb = groupby(data,key = lambda x:x[0])

for key,value in gb:
    print (key,list(value))