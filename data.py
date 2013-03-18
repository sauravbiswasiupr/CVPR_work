#!/usr/bin/python 
'''the script reads in a list of image filenames from a text file and loads the corresponding images , if required normalizes them , and then stacks each image as a vector to make an ndarray of image arrays where each image , is resized to IMSIZE*IMSIZE and then unrolled into a 1D vector and stacked . We then prepare the train and test set and ultimately pickle it and gzip it so that it can be later unpickled and used by any classifier in the format required '''

from PIL import Image 
import numpy 
import pylab 
import os
from scipy.misc import imread 
IMSIZE = 256   #let it be 256 for now , we can later change this to a user argument 
from numpy import zeros,ones,hstack,vstack
import theano 
import theano.tensor as T
from pickle import dump

##imports done 

def create_im_list(filename):
   '''Function to read a filename and create a list of files contained in that file '''

   f = open(filename,'r')
   imlist=[]
   for line in f.readlines(): 
       words = line.rstrip('\n').split(" ")
       imlist.append((words[0],words[1])) 
       #note that each imlist entry is a tuple consisting of the image name and a label if it has a gun or not 
       print "Error "  
   return imlist 



def create_image_array(filename): 
    '''Function that takes a filename as parameter and stacks a numpy array of images rolled into 1D vector from that filename list '''
    imlist = create_im_list(filename) #note that a list of tuples is returned 
    imnbr = len(imlist) 
    
    #change to the directory where query images are present 
    folder = '/home/saurav/Desktop/SICURA/query_images/query/'
    images =[]
    labels=[] 
    for i  in range(imnbr):
        print "Image :" , imlist[i][0]  
        im = Image.open(folder+imlist[i][0])
        labels.append(int(imlist[i][1]))
        print im 
        im_resized = im.resize((256,256))
        im_resized = numpy.array(im_resized)
        #now flatten (unroll) the image into a 1D array and then append to the images[] list which will be later converted into a numpy array 
        images.append(im_resized.flatten())


    #now convert the image list into a numpy array along with the labels 
    immatrix = numpy.array(images,'f')
    labels = numpy.array(labels)
    return immatrix , labels 


def load_datafile(filename):
    
    
    immatrix,labels = create_image_array(filename)
    print "The first 4 entries of the entire image matrix : " , immatrix[:4][:]
    print "Labels : "  , labels[:4]
    print labels.shape

    #now time tom divide the data into the train , validation and test set , first 4000 included into training set , from 4000 to 6000 in validation set and the remaining are in 
    #
    train_x =  immatrix[:4000]
    train_y = labels[:4000]

    valid_x = immatrix[4000:6000]
    valid_y = labels[4000:6000] 

    test_x = immatrix[6000:]
    test_y = labels[6000:] 

    result =  [(train_x,train_y),(valid_x , valid_y) , (test_x,test_y)] 
    #now pickle the result and dump into a file 
    # dataset ='sicura_old_8004.pkl' 
    
    
    return result 


