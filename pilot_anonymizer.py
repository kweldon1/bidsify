#!/usr/bin/env python
"""

A simple program to anonymize all dicom files in the supplied folder.

Usage: 

Created: Ron Yang for HBCD Pilot data .

"""
import argparse
import datetime
import itertools
import json
import logging as log
import os
import subprocess
import shlex
import sys
import pydicom
import re

# CURRENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
# log.basicConfig(
#         filename=os.path.join(CURRENT_DIR,  os.path.basename(__file__) + ".log"),
#         format="%(asctime)s  %(levelname)10s  %(message)s",
#         level=log.INFO)

def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Anonymize the HBCD Pilot data with a folder.")

    parser.add_argument('--input','-i', required=True,
            help="Input directory name for original dicom files.")

    parser.add_argument('--patient-name', '-p', default=None, required=True,
            help="Anonymized Patient name")

    parser.add_argument('--patient-age', '-a',default=None,required=True,
            help='Anonymized Patient Age in Weeks.')

    # #validate age with pattern
    # pattern = re.compile("^[0-9]{3}[M,W]{1}")
    # if pattern.match(parser.parse_args().patient_age):
    #     print("Age format is ok")
    # else:
    #     print("Age format is bad")
    #     return 
    # #validate patient_name with tripple ID pattern PIARK0010_510042_V02
    # pattern = re.compile("^[0-9, A-Z]{9}[_][0-9]{6}[_][V][0-9]{2}")
    # if pattern.match(parser.parse_args().patient_name):
    #     print("Patient name  is ok")
    # else:
    #     print("Patient name is bad")
    #     return
    #check input name: No space and link should be [0-9,A-Z,a-z,-,_,.]
    pattern = re.compile("^[a-zA-Z0-9-_.]*$")
    if pattern.match(parser.parse_args().input):
        inFolder = parser.parse_args().input
        print('inFolder: ', inFolder)
        print("filaname format is ok")
    else:
        print("filename contains space")
        return
    return parser.parse_args()

def ensure_directory(parent,output):
    """
    Return valid directory path and, if it does not exist, create it
    """
    export_dir = os.path.join(parent, output)
    if not os.path.isdir(export_dir):  # makedirs -> OSError if leaf dir exists
        os.makedirs(export_dir)  # could still raise OSError for permissions
    return export_dir

CURRENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
log.basicConfig(
        filename=os.path.join(CURRENT_DIR,  os.path.basename(__file__) + ".log"),
        format="%(asctime)s  %(levelname)10s  %(message)s",
        level=log.INFO)

rawDir = '/home/faird/kweldon/scratch/template/data/raw'

if __name__ == "__main__":
    args = parse_arguments()
    if not args:
        print("please check the input parameters !")
        exit()
    # fix the output
    out_dir = args.input + '_anon'
    #out_dir = 'anonymizedOut'
    # Determine what the base directory is and create it if needed
    out_dir = ensure_directory(rawDir, out_dir)

    log.info('Started run with invocation: %s', sys.argv)

    if not out_dir:
        log.critical('Output Dir is not existed: %s', args.input)

    for x in os.listdir(args.input):
        #print(os.path.join(CURRENT_DIR,args.input, x), " target ", os.path.join(CURRENT_DIR, args.target_dir,  x))
        target_dir = ensure_directory(out_dir,  x)
        command = "dicom-anonymizer --keepPrivateTags " +  os.path.join(args.input, x) + " " +  target_dir 
        parameters = shlex.split(command)
        print(parameters)
        p = subprocess.run(parameters, shell=False)

        #loop each files
        for path in os.listdir(target_dir):
            # check if current path is a file
            if os.path.isfile(os.path.join(target_dir, path)):
                filename = os.path.join(target_dir, path)
                dataset = pydicom.dcmread(filename)
                if args.patient_name:

                    dataset.PatientName = args.patient_name
                    dataset.PatientID = args.patient_name
                #    dataset.PatientSex = sex
                if args.patient_age:
                    dataset.PatientAge = args.patient_age

                dataset.save_as(filename)
 
                
        log.info("Anonymize Patient Name, ID and Age for this folder: %s", x)

    log.info('Ended run with invocation: %s', sys.argv)

