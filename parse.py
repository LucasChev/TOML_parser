#!/usr/bin/python
import sys
sys.path.append("/Users/Lucas/anaconda3/lib/python3.6/site-packages")

import toml
import os
import csv
import collections

ROOT_DIR = '/Users/Lucas/dev/toml/'
OVERRIDE_KEY = '@Override'
DEST_ID = 'F1FTH'

def read_files(directory):
	with open(directory, 'r') as f:
		reader = csv.reader(f)
		params = list(reader)
		f.close()
	return params[0]

def build_csv(risk_parameters, DestId):
    ret = "DestId,Parameter,Value\n"
    for key,value in risk_parameters.items():
        ret += ("%s,%s,%s\n" % (DestId,key,value))
    return ret

def flatten(d, parent_key='', sep='_'):
	items = []
	for k, v in d.items():
	#         new_key = parent_key + k if parent_key else k
	    new_key = k
	    if isinstance(v, collections.MutableMapping):
	        items.extend(flatten(v, new_key, sep=sep).items())
	    else:
	        items.append((new_key, v))
	return dict(items)
ROOT_DIR + 'relevant_params.csv'
    
valid_parameter = read_files(ROOT_DIR + 'relevant_params.csv')

raw_files = os.listdir(ROOT_DIR)
files = []
for file in raw_files:
    if('.toml' in file):
        files.append(ROOT_DIR + file)

parsed_files = []
for file in files:
    parsed_files.append(flatten(toml.load(file)))

    risk_parameters = {}

for file in parsed_files:
    if(OVERRIDE_KEY in file):
        if(DEST_ID in file[OVERRIDE_KEY]):
            #Get all relevant parameters
            for param in valid_parameter:
                if(param in file):
                    print('%s=%s' % (param, file[param]))
                    risk_parameters[param] = file[param]

text_file = open(ROOT_DIR+"Output.csv", "w")
text_file.write(build_csv(risk_parameters, DEST_ID))
text_file.close()