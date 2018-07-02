'''

Find candidate entities for sending to neo4j as possible classes and operations

'''

# Dependencies
from flask import Flask
from flask import jsonify
from flask import request
import json
import spacy
from spacy.symbols import attr, nsubj, VERB, NOUN, PROPN
from spacy.matcher import Matcher
from svo import SVO


# Load the language model only one time in the life cycle
nlp = spacy.load('en')

app = Flask(__name__)

# set some global variables that will hold the matcher terms
class_list = []
operation_list = []
time_period = []
class_label = []



def on_match_class(matcher, doc, id, matches):
    
    global class_list

    match_id, start, end = matches[id]
    print(doc[start:end].text, match_id)
    class_list.append(doc[start:end].text)
    return True

def on_match_operation(matcher, doc, id, matches):
    
    global operation_list

    match_id, start, end = matches[id]
    print(doc[start:end].text, match_id)
    operation_list.append(doc[start:end].text)
    return True

def on_match_time(matcher, doc, id, matches):
    
    global time_period

    match_id, start, end = matches[id]
    print(doc[start:end].text, match_id)
    time_period.append(doc[start:end].text)
    return True


@app.route("/getentities/")
def get_entities():
    
    global class_list
    global operation_list
    global time_period

    # set some global variables that will hold the matcher terms
    class_list = []
    operation_list = []
    time_period = []
    class_label = []

    
    # define all the patterns for each of the four types 
    # of entities we are looking for. 

    dep_list = ['nsubj', 'pobj', 'dobj']
    oper_list = ['advmod', 'amod']
    timepd_list = ['pobj', 'npmadvmod']

    class_pattern = [[{'DEP': dep}] for dep in dep_list]
    operation_pattern = [[{'DEP': dep}] for dep in oper_list]
    time_period_pattern = [[{'DEP': dep}] for dep in timepd_list]

    
    # Loop through and form json response
    token_json = []
   
    doc = nlp(u'' + request.args.get('sentence'))

    matcher = Matcher(nlp.vocab)
    matcher.add('Operation', on_match_operation, *operation_pattern)
    matcher.add('Class', on_match_class, *class_pattern)
    matcher.add('Time', on_match_time, *time_period_pattern)
    #matcher.add('Class', on_match, [{'DEP': 'pobj'}, {'DEP': 'conj'}])
    
    matches = matcher(doc)

    token_json = {
        'class' : class_list,
        'operation' : operation_list,
        'time_period' : time_period
    }


    return json.dumps(token_json)






