#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 21:16:19 2023

@author: kweldon
"""
import os, importlib
import argparse

def run_shell_cmd(cmd):
    import subprocess as sub
    pipe = sub.Popen(cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE,close_fds=True)
    o,e = pipe.communicate()
    return 


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--.py summary", help="the .py")
#parser.add_argument("-c", "--config", help="the .json")
parser.add_argument("-a", "--all", action='store_true', help="run all dicoms?")

args = parser.parse_args()
if args.fileToParse:
    file = args.fileToParse
    cmd = 'cp %s anon.py'\
                %(file)
    print(cmd)
    run_shell_cmd(cmd)
else:
    print('I need a config file!!')

import anon; importlib.reload(anon)

dicomList = anon.dicomList()[0]
info = anon.dicomList()[1]
#%%


dFlag = os.path.join(info['studyDir'],info['dicomDir'])
pFlag = info['subID']
sFlag = info['sess']
cFlag = file[:-3] + '.json'
oFlag = info['bidsDir']
folder = 'sub-'+ pFlag + '_ses-' + sFlag
tmpDir = os.path.join(oFlag,'tmp_dcm2bids',folder)

#print(dFlag, pFlag, sFlag, cFlag, oFlag)

if args.all:
    cmd = 'dcm2bids -d %s -p %s -s %s -c %s -o %s --forceDcm2niix'\
                %(dFlag, pFlag, sFlag, cFlag, oFlag)
    print(cmd)
    run_shell_cmd(cmd)
else:
    for iD, dcm in enumerate(dicomList):
        if dcm['label']: 
            dcmName = os.path.join(dFlag,dcm['Name'])
            cmd = 'dcm2bids -d %s -p %s -s %s -c %s -o %s --forceDcm2niix'\
                %(dcmName, pFlag, sFlag, cFlag, oFlag)
            #print('running %s'%dcmName)
            print(cmd)
            run_shell_cmd(cmd)
            if not os.listdir(tmpDir):
                print('SUCCESS!!!')
