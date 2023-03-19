#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 13:36:57 2022

@author: kweldon
"""

"""
Look at a dicom directory and creat a summary .py file that can be
marked up by a user to guide creating a dcm2bids config file.

Inputs: 
    Required: -d: path to working dicomDir OR, if the folder is
                    in pwd, the name of the dicomDir

    Optional:
        -d: path to working directory
        --discardTRs: set # TRs to trim off beginning and end of all func
    
Outputs:
    .py file in working directory

Usage Example:
    python newInit.py -d /home/scat-raid4/share/BIDS_demos/cao/demo_dataset 
    python newInit.py -d demo_dataset --discardTRs '[0, 5]'



"""
#import os, datetime, getpass, glob, sys, json
#import numpy as np

#import pydicom
import os, datetime, glob, getpass, argparse
from pydicom import dcmread

def run_shell_cmd(cmd):
    import subprocess as sub
    pipe = sub.Popen(cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE,close_fds=True)
    o,e = pipe.communicate()
    return 
#%%       
#mainDir = '/home/faird/kweldon/scratch/template/data/'
#FOR TESTING
mainDir = '/home/znahas/shared/analysis/PCS/'
dicoms = 'PCS_HR6945_001'
dicomPath = os.path.join(mainDir,dicoms)
#%%
# parser = argparse.ArgumentParser()

# parser.add_argument("-d", "--dicomDir", help="Dicom directory path")
# parser.add_argument("-p", "--participantID", help="subID")
# parser.add_argument("-s", "--sess", help="sess")
# parser.add_argument("-b", "--bids", help="bids output directory")
# parser.add_argument("-n", "--discardTRs", help="how many TRs to discard (e.g. 3 for 3 noise scans")

# args = parser.parse_args()
    
# if args.participantID:
#     subID = args.participantID
# else:
#     subID = ''
# if args.participantID:
#     sess = args.sess
# else:
#     sess = ''
# if args.bids:
#     bids = args.bids
# else:
#     bids = 'bids' 
# if args.discardTRs:
#     discard = int(args.discardTRs)
# else:
#     discard = 0     
#dicomPath = args.dicomDir
    
subID = ''
sess = ''
bids = 'bids'
discard = ''
mainDir = os.getcwd()
sessName = os.path.split(dicomPath)[1] + '.py'

#%%
print('Reading from dicom dir: ', dicomPath)
print('Creating (or overwriting) ', sessName, ' summary in ', mainDir)

filename = os.path.join(mainDir, sessName)
fid = open(filename, 'w')
fid.write('# Date analysis initialized '+str(datetime.datetime.now()).split('.')[0]+' by ' +getpass.getuser()+'\n')
  
fid.write('def dicomList():\n')
fid.write('\tinfo = {}\n')
fid.write("\tinfo['studyDir'] = '%s' \n"%mainDir) 
fid.write("\tinfo['dicomDir'] = '%s' \n" %dicomPath)
fid.write("\tinfo['subID'] = %s  \n"%subID)
fid.write("\tinfo['sess'] = %s # session number in str \n"%sess)
fid.write("\tinfo['bidsDir'] = %s \n"%bids)
 
#%%
fid.write('\n# Labels that will not be treated as functional scans:\n')
fid.write('#   anat: [T1w, T2w, T1rho, T1map, T2map, T2star, FLAIR, FLASH,\n')
fid.write('#          PD, PDmap, PDT2, inplaneT1, inplaneT2, angio]\n')    
fid.write('#   fmap: [PErev, revPE, afi, fa, magnitude, phasediff, \n')
fid.write('#          magnitude1, magnitude2, phase1, phase2]\n')
fid.write('#   t1-epi: [t1_epi, t1epi, t1w_epi, t1wepi]\n')
fid.write('#   dwi: dwi\n')    
fid.write('#   afi: afi\n')    
fid.write('# \n')    
fid.write('# Notes:  \n\n')   
fid.close()  
    
#%% Figure out which datasets we're working on
try:
    dicom_dir = dicomPath
except:
    print("where is your dicom directory??")
dcmList = []
if os.path.exists(dicom_dir):
    #print('Raw data dir: ', dicom_dir)
    files = os.listdir(dicom_dir)
    files.sort()
    # first, get a list of directories that actually have dicom files
    for iF in range(len(files)):
        subdir = os.path.join(dicom_dir, files[iF])
        if os.path.isdir(subdir) and os.path.split(subdir)[1].startswith('MR'):
            #print(subdir)
            subdir_contents = glob.glob(os.path.join(subdir, 'MR*.dcm'))
            subdir_contents.sort()
            print(subdir_contents)
            lastDcmPath = subdir_contents[-1]
            print(lastDcmPath)
            lastDcm = os.path.split(subdir_contents[-1])[1]
            ds = dcmread(lastDcmPath)
            #DcmPath = subdir_contents[0]
            #Dcm = os.path.split(subdir_contents[0])[1]
            #ds = dcmread(DcmPath)
            
#%%
            name = files[iF]
            label = ''
            nTRs = len(subdir_contents)
            acqNum = name[5:8] + '*'
            nEc = ''
#%%ImageType            
            #turns out some images don't have ImageType
            if 'XA' in ds.SoftwareVersions:
                print('XA system, checking ImageType the hard way')
                a = ds
                # writing to file
                file1 = open('checkIT.txt', 'w')
                file1.writelines(str(a))
                file1.close()
                  
                # Using readlines()
                file1 = open('checkIT.txt', 'r')
                lines = file1.readlines()
                for line in lines:
                    if "0021, 1175" in line:
                        mine = line
                        print(mine)
                        break
                for item in mine:
                    if item == '[':
                        startIndex = mine.index(item)
                    if item == ']':
                        endIndex = mine.index(item) + 1
                #print(startIndex, endIndex)
                ImageType = mine[startIndex:endIndex]
                #delete the stupid file
                cmd = 'rm %s' %'checkIT.txt'
                run_shell_cmd(cmd)
            else:
                ImageType = ds.ImageType
            

#%%EchoNumbers            
            
            #turns out some images don't have EchoNumbers, use afni's dicom_hinfo to help
            if 'XA' in ds.SoftwareVersions:
                print('XA system, checking echo number the hard way')
                a = ds
                # writing to file
                file1 = open('checkEN.txt', 'w')
                file1.writelines(str(a))
                file1.close()
                  
                # Using readlines()
                file1 = open('checkEN.txt', 'r')
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
                        nEc = mine[index+2]
                #delete the stupid file
                cmd = 'rm %s' %'checkEN.txt'
                run_shell_cmd(cmd)
            else:
                nEc = ds.EchoNumbers
            

            # tagToCheck = '0018,0086' #EchoNumbers tag
            # cmd = 'dicom_hinfo -tag %s %s' \
            #     %(tagToCheck, lastDcmPath)                            
            #     #print('*******', cond)
            # tag = run_shell_cmd(cmd)
            # #print(tag)
            # if tag == None:
            #     nEc = ''
            # else:
            #     EchoNumbers = ds.EchoNumber
            #     nEc = ds.EchoNumbers   
                
            #print(name, label, ImageType, nEc)    
            if subdir_contents:
                dcmList.append({'Name': name,
                                'acqNum': acqNum,
                                'label': label,
                                'nTRs': nTRs,
                                'ImageType': ImageType,
                                'nEc': nEc,
                                'discardTRs': discard,
                                })
            
print(dcmList)
#%%
# now that we've collected all of our information ... write it down
fid = open(sessName, 'a') 
fid.write('\t# Raw data DETAILS\n')
fid.write('\tdcm = []\n')
#%%
for dcm in dcmList:
    fid.write("\tdcm.append({'Name': '%s',\n" %dcm['Name'])
    fid.write("\t            'label': '%s',\n" %dcm['label'])
    fid.write("\t            'acqNum': '%s',\n" %dcm['acqNum'])
    fid.write("\t            'nTRs': %d,\n" %dcm['nTRs'])
    fid.write("\t            'ImageType': %s,\n" %dcm['ImageType'])
    fid.write("\t            'nEc': %s,\n" %dcm['nEc'])
    if 'discardTRs' in dcm:
        fid.write("\t            'discardTRs': %s, #[from_start, from_end],\n" %dcm['discardTRs'])
    fid.write("\t            'PEdir': '', #(PA, AP, LR, or RL) \n")
    #fid.write("\t            'intendedFor': '',\n")
    fid.write("\t            })\n")
    
fid.write("\treturn dcm,info\n")
fid.write("if __name__ == '__main__':\n")
fid.write("\tdicomList()\n")
fid.close()

print('''
  Now you need to edit that .py file!
  Instructions:  

  Mark which scans should be analyzed by entering a label:
      the top of .py lists labels that are reserved for
        marking t1-epi, anat, dwi, afi, and fieldmap (revPE) data
      anything else gets interpreted as functional data

  Optionally use the discardTRs field to indicate how many volumes
      should be trimmed off of start or end of scan (to accommodate
      steady-state or noise scans)
 
      ''')
