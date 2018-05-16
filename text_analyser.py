'''

Utility file that generates pos and chunk data to be analysed for query patterns
Potentially extend this in future to convert it to query maps
'''

# Dependencies
import sys
import pandas as pd
from pandas import DataFrame
import json
import os
import wget
import urllib


if __name__ == "__main__":
    # Load the file that has the questions 
    fname='questions.txt'
    with open(fname) as f:
        content = f.readlines()

# remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

# For each line, send it to spacy_all for parsing
for con in content:
    url = 'http://localhost:5000/getall/?sentence='+urllib.parse.quote_plus(con)
    print(url)
    with urllib.request.urlopen(url) as u:
        jsonRes = json.loads(u.read().decode())

    # Obtain parsed output and stream it to 
    print(type(jsonRes))
    my_dic_data = jsonRes
    print("This is my dictionary", type(my_dic_data))

    dict_you_want ={}
    keys = []
    values = []
    for stuff in my_dic_data:
        print(stuff)
        keys = [item if item not in dict_you_want else (item+"_"+str(len(keys))) for item in stuff]
        values = stuff.values()
        dict_you_want.update(dict(zip(keys, values)))
    print("-----")


    print ("This is the dictionary of", dict_you_want)

    # Get the list items from the dictionary and add ‘list’ for Python 3.x

    # pd.DataFrame.from_dict(list(dict_you_want.items()), )
    #pd.DataFrame.from_dict(list(dict_you_want.items()), columns = [‘Term’,’Pos’])

    pd.DataFrame.from_dict(dict_you_want, orient = 'index')

    s = pd.Series(dict_you_want)

    #s.index.name = 'term'

    df = pd.DataFrame(s)

    print(df.transpose())


    # if file does not exist write header 
    if not os.path.isfile('results.csv'):
        df.T.to_csv('results.csv',header ='column_names')
    else: # else it exists so append without writing the header
        df.T.to_csv('results.csv',mode = 'a',header ='column_names')