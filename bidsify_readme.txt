#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 08:14:16 2023

@author: kweldon
"""

Step 1: newInit.py or initalize.py
    
    Look at a dicom directory and creat a summary .py file that can be
    marked up by a user to guide creating a dcm2bids config file.

    Inputs: 
        Required: -d: path to working dicomDir OR, if the folder is
                        in pwd (recommended), the name of the dicomDir

        Optional:
            -p: subID
            -s: sess
            -b: name or path to bids folder where these data should live
            --discardTRs: # NOT ACCURATE - DEFAULTS TO 0
                        #set TRs to trim off beginning and end of all func 
        
    Outputs:
        .py file in working directory

    Usage Example:
        python newInit.py -d /home/scat-raid4/share/BIDS_demos/cao/demo_dataset 
        python newInit.py -d demo_dataset --discardTRs '[0, 5]'

Step 2: mark up your .py file

Step 3: dcm2bids_config.py 

    Inputs: 
        Required: -f: the name of the summary file you want to make into a 
                        config file for dcm2bids

        Optional:
        
    Outputs:
        .json file in working directory

    Usage Example:
        python dcm2bids_config.py -f ION007_7T_anon.py

Step 4: batch_dcm2bids.py

    Inputs: 
        Required: -f: the name of the summary file you want to run dcm2bids on

        Optional:
            -a flag : if you want to run dcm2bids on the whole dicom directory
            instead of just the ones you marked up in the summary .py file
        
    Outputs:
        bids valid data?!?!

    Usage Example:
        python dcm2bids -f ION007_7T_anon.py
        python dcm2bids -f ION007_7T_anon.py -a
