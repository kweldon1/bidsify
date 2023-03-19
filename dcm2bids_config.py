#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 19:47:48 2023

@author: kweldon
"""
import json, importlib
import argparse

def run_shell_cmd(cmd):
    import subprocess as sub
    pipe = sub.Popen(cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE,close_fds=True)
    o,e = pipe.communicate()
    return 

#%% here we changing the name of our .py file so we can import it as a module
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fileToParse", help="the .py file that you want to \
                    make a config file for")
args = parser.parse_args()
file = args.fileToParse
print(file)

cmd = 'cp %s anon.py'\
            %(file)
print(cmd)
run_shell_cmd(cmd)
import anon; importlib.reload(anon)
#import anon
#%%

dicomList = anon.dicomList()[0]
info = anon.dicomList()[1]

anatList = ['T1w', 'T2w', 'T1rho', 'T1map', 'T2map', 'T2star', 'FLAIR', 'FLASH']
fmapList = ['PErev', 'revPE', 'afi', 'fa', 'magnitude', 'phasediff', \
            'magnitude1', 'magnitude2', 'phase1', 'phase2']

newDict = []
for dcm in dicomList:
    if dcm['label']:
        #print(dcm)
        for echo in range(dcm['nEc']):
                echoN = echo +1
                dictionary = {
                      'dataType': '', 
                      'modalityLabel': '',
                      'customLabels': '',
                      'sidecarChanges': {
                          'ImageType': '',
                          },
                      'criteria': {
                           'SidecarFilename': '',
                           'SeriesDescription': '',
                           'ImageType': ''
                          }
                      }
                #decide on dataType
                #Data type - a functional group of different types of data. In BIDS we define six data types: 
                #func (task based and resting state functional MRI)
                #dwi (diffusion weighted imaging)
                #fmap (field inhomogeneity mapping data such as field maps)
                #anat (structural imaging such as T1, T2, etc.)
                #meg (magnetoencephalography)
                #beh (behavioral)        
                #add SeriesDescription to criteria

                add = ''
                if dcm['label'] in anatList:
                    dictionary['dataType'] = 'anat'
                    dictionary['modalityLabel'] = dcm['label']
                    
                elif dcm['label'] in fmapList or dcm['label'] == 'fmap':
                    dictionary['dataType'] = 'fmap'
                    dictionary['modalityLabel'] = 'fmap'
                    PEdir = 'dir-' + dcm['PEdir']
                    dictionary['customLabels'] = PEdir
                    
                elif dcm['label'] == 'dwi':
                    dictionary['dataType'] = 'dwi'
                    dictionary['modalityLabel'] = 'dwi'
                    
                else:
                    dictionary['dataType'] = 'func'
                    if 'SBRef' in dcm['Name']:
                        dictionary['modalityLabel'] = 'sbref'
                        taskType = 'task-' + dcm['label']
                        dictionary['customLabels'] = taskType +'ME_echo-%s'%echoN
                        ImageTypeChange = ["ORIGINAL","PRIMARY","FMRI","NONE"]
                        dictionary['sidecarChanges']['ImageType'] = ImageTypeChange

                        
                        #sbSidecar = '_phMag_magfixed'
                        #dictionary['criteria']['SidecarFilename'] = '*_e%s%s.json'%(echoN,sbSidecar)
                        add = '_e%s.json'%(echoN)
                                
                    else:
                        dictionary['modalityLabel'] = 'bold'
                        taskType = 'task-' + dcm['label']
                        if 'P' in dcm['ImageType']:
                             #dictionary['criteria']['SidecarFilename'] = '*e%s_ph.json'%echoN
                             add = 'e%s_ph.json'%echoN
                             dictionary['customLabels'] = taskType + 'MEph_echo-%s'%echoN
                        elif 'M' in dcm['ImageType']:
                             #dictionary['criteria']['SidecarFilename'] = '*_e%s.json'%echoN
                             add = '_e%s.json'%echoN
                             dictionary['customLabels'] = taskType +'ME_echo-%s'%echoN

                                            
                SeriesDes = dcm['Name'][9:]
                dictionary['criteria']['SidecarFilename'] = dcm['acqNum'] + add
                dictionary['criteria']['SeriesDescription'] = SeriesDes
                if not dictionary['modalityLabel'] == 'sbref':
                    dictionary['criteria']['ImageType'] = dcm['ImageType']
                for item in dictionary['criteria']['ImageType']:
                    if 'TE' in item:
                        dictionary['criteria']['EchoNumber'] = echoN
                
                if dictionary['customLabels'] == '':
                    del dictionary['customLabels']
                if dictionary['sidecarChanges']['ImageType'] == '':
                    del dictionary['sidecarChanges']
                if dictionary['dataType'] == 'func':
                    del dictionary['criteria']['ImageType']
                
                newDict.append(dictionary)

#%%write out that dictionary as a json file! use this config file to run dcm2bids

jsonString = json.dumps(newDict, indent=4)
fileName = file[:-3]
with open(fileName, "w") as outfile:
#with open("test_bids.json", "w") as outfile:
    outfile.write('{\n')
    outfile.write('\t"descriptions":\n')
    outfile.write('\t')
    outfile.write(jsonString)
    outfile.write('\n')
    outfile.write('}')
    
#%%rename the json until I get smart enought to do it on the fly

# cmd = 'mv test_bids.json %s.json'\
#             %(file[:-3]) #take off .py from filename
# print(cmd)
# run_shell_cmd(cmd)