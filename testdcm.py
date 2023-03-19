#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 09:50:24 2023

@author: kweldon
"""

import os, argparse
from pydicom import dcmread
#import nibabel.nicom.csareader as csareader

def run_shell_cmd(cmd):
    import subprocess as sub
    pipe = sub.Popen(cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE,close_fds=True)
    o,e = pipe.communicate()
    return 

#%%    
# parser = argparse.ArgumentParser()

# parser.add_argument("-f", "--file", help="Dicom file")
# args = parser.parse_args()
#file = args.file

cwd = '/home/znahas/shared/analysis/PCS/'
file = 'MR-ST006-SE013-0001.dcm'
path = os.path.join(cwd,file)
EchoNumbers = ''

#%%
print(file)
#lastDcm = os.path.split(subdir_contents[-1])[1]
ds = dcmread(path,force=True)

if 'XA' in ds.SoftwareVersions:
    print('XA system, checking echo number the hard way')
    a = ds
    # writing to file
    file1 = open('myfile.txt', 'w')
    file1.writelines(str(a))
    file1.close()
      
    # Using readlines()
    file1 = open('myfile.txt', 'r')
    lines = file1.readlines()
    for line in lines:
        if "0021, 1106" in line:
            mine = line
            #print(mine)
            break
    for item in mine:
        if item == 'X':
            index = mine.index(item)
            #print(index)
            nEch = mine[index+2]
else:
    nEch = ds.EchoNumbers


#ds = dcmread(path,force=True,specific_tags=[0x0021,1106])
#ds = dcmread(path,specific_tags=[(0x0021,1175)]


#DcmPath = subdir_contents[0]
#Dcm = os.path.split(subdir_contents[0])[1]
#dcm2niix will use 0021,1106 to deduce echo number

#%%AFNI
#tagToCheck = '0021,1106'
#tagToCheck = '0018,0086'
# cmd = 'dicom_hinfo -tag %s %s' \
#     %(tagToCheck, path)                            
# tag = run_shell_cmd(cmd)
#print(tag)
# if tag == None:
#     EchoNumbers = ''
# else:
#     EchoNumbers = ds.EchoNumber
#%%
print(ds.ImageType)
print(nEch) 

