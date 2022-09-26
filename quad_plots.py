# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 15:01:43 2022

@author: arock
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
from PIL import Image
from multiprocessing import Pool
import pandas as pd
import re

date_interest = '2022-09-20' #folder name with the plots we are interested in

cwd = os.getcwd().replace('//','/')+'/'
outdir = cwd + 'Output/'+date_interest+'/'
DRdir = outdir+'DRs/Close_View/'
Avgdir = outdir+'Avgs/Close_View/'
ATempsdir = outdir+'Avg_Temps/'

mapdir = cwd+'Images/'

plotdir = outdir+'Quad_Plots/'
if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

gauge_map = pd.read_csv(mapdir + 'images_map.csv')




    
for gauge in sorted(list(gauge_map['Gauge'].values)): #keep things sorted so we can make sure G1_1 isn't confused with LG1_1

    
    fnames = []
    names_map = {} #build dictionary to have key as gauge and value as file. then we can sort the keys and match, so the substring problem is gone for S2_10
    for dirs in [DRdir,Avgdir,ATempsdir]:
        for filename in sorted(list(os.listdir(dirs))): #keep sorted for the G1_1 substring as noted above
            temp1 = filename.split()
            for test in temp1:
                m = re.search('_.+_',test) #search for items that have _number_ which is the part of the filename with the gauge in it
                if m:
                    test = test.replace('(Manually Set)','') #for DRs, get rid of '(Manually Set)' to help with sorting
                    test = test.replace('.png','') #remove .png so we can subsequently remove teh last underscore
                    test = test[:-1] #remove last underscore for sorting 
                    names_map[test] = filename    #set the filename value to the trimmed gauge name key for sorting later
        for gauge_name in sorted(list(names_map.keys())): #sort on the keys of names map since they should
            
            if gauge in gauge_name: #if the gauge we're on is in the names map key (which pairs gauge name to filename)
                fnames.append(dirs+names_map[gauge_name]) #add the file name that each gauge is paired to into the list of filenames to put on the plot
                break
    
    site_img_file =  mapdir + gauge_map[(gauge_map['Gauge']==gauge)]['Image_Name'].values[0]
    fnames.append(site_img_file)
            
    fig, axs = plt.subplots(2,2,figsize=(42,26))
    
    axcoords = [[0,0],[0,1],[1,0],[1,1]]
    
    
    for i in range(len(fnames)):
        with Image.open(fnames[i]) as im:
            axs[axcoords[i][0],axcoords[i][1]].imshow(im)
    
    
    
    plt.tight_layout()
    axs[0,0].set_axis_off()
    axs[0,1].set_axis_off()
    axs[1,0].set_axis_off()
    axs[1,1].set_axis_off()
    
    
    fig.savefig(plotdir+gauge+'.png',dpi=100)
    plt.close('all')





