#!/usr/bin/python 
'''Program to unpickle the sicura_8004_old.pkl file and then see its contents ''' 
import cPickle 
f = open('sicura_old_8004.pkl','rb')
[train,valid,test] = cPickle.load(f)

print train
print test
print valid 
