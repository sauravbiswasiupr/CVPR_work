#!/usr/bin/python 
'''Function to demonstrate the basic usage of pickling in python 2 using the cPickle module '''
from cPickle import dump , HIGHEST_PROTOCOL 
from numpy import array 


a=[1,2,3,4]
b = array(a) 
dataset = 'pickling.pkl' 
try : 
    f  = open(dataset,'wb')
    dump(b,f,HIGHEST_PROTOCOL)

except Exception as e : 
    print "Gone with the wind "  


