'''
This loops through a sf csv export and tries to list out all nodes and relationships
version 1.0
'''

# dependencies
import os
import pandas as pd
import re
import spacy
from print_utils import skip_and_print, print_table 



# utility function to check for camel case
def camel(s):
    return (s != s.lower() and s != s.upper())

# utility function to convert from camel to sentence case
# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower()

# Assumes a folder that has all sf files exported as csv
# loop through the folder to list all files
directory = os.fsencode("../sf_focus/")

# This is where we will store all the files we have iterated
file_list = []

for file in os.listdir(directory):
    file_name = os.fsdecode(file)
    if file_name.endswith(".csv"): 
        file_list.append(file_name)
        continue
    else:
        continue



#loop through this csv and read the headers
# store the headers in dictionary
# Use list comprehension in camel case to normal case conversion of the list - @todo
file_dict = dict()
for file in file_list:
    each_file = str(directory, 'utf-8')+file 
    df = pd.read_csv(each_file)
    #create _ based string that will then be passed to spacy
    titleString = ','.join(list(df))
    #create the index without the csv
    file_idx = file.split(".")
    normalised_idx  = convert(file_idx[0])
    file_dict[normalised_idx] = convert(titleString)

print(file_dict)



