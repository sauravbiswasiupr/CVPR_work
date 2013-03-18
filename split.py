#!/usr/bin/python

#guns dataset i.e set4-train-test.txt contains all the 8004 images from the first Luebeck recording 
#split this dataset into guns and non guns and store as image_name and label ( 2 columns )  , gun or non-gun label is denoted by 0 or 1 

f = open('set4-train-test.txt','r')
f_split = open('dataset-labels.txt','w')


for line in f.readlines():
    words = line.split(" ")
    row = words[1]+".jpg"+" "+words[2]+"\n"
    f_split.write(row)

print "\n Done " 
    
