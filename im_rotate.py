#!/usr/bin/python 
##script to read images and templates from the SICURA folder on the desktop \
## read the query_images/query folder and template folder and then rotate each
##template image or baggage image by 30 , 60 , 90 ,120 , 150 degrees 
# Author : Saurav 

import Image 
import time 
import os 

fs_image    =  "/home/saurav/Desktop/CVPR_work/rotated_images/"
fs_template =  "/home/saurav/Desktop/CVPR_work/rotated_templates/"

sample_images = "/home/saurav/Desktop/SICURA/query_images/query/"
template_images = "/home/saurav/Desktop/SICURA/temp/"


print "Rotating images...."
time.sleep(2)



im_list = os.listdir(sample_images) 
for im in im_list: 
    #rotate each image by 30 , 60 , 90 , 120 , 150 degrees and save in respective folders
    print im 
    img = Image.open(sample_images+im)
    
    im_30 = img.rotate(30)
    im_60 = img.rotate(60)
    im_90 = img.rotate(90)
    im_120 = img.rotate(120)
    im_150 = img.rotate(150)

    #now save in respective folders 
    im_30.save(fs_image+"rotated_30/"+im)
    im_60.save(fs_image+"rotated_60/"+im)
    im_90.save(fs_image+"rotated_90/"+im)
    im_120.save(fs_image+"rotated_120/"+im)
    im_150.save(fs_image+"rotated_150/"+im)

print "\Done"



