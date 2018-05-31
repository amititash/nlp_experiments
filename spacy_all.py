'''
Simple homegrown service to parse a sentence and output dependency tree and POS

'''

# Dependencies
from flask import Flask
from flask import jsonify
from flask import request
import json
import spacy
from spacy.symbols import attr, nsubj, VERB, NOUN, PROPN
from subject_object_extraction import findSVOs, printDeps
from svo import SVO
from textblob import TextBlob


# Load the language model only one time in the life cycle
nlp = spacy.load('en')

merge_entities = nlp.create_pipe('merge_noun_chunks')
nlp.add_pipe(merge_entities, after='ner')

app = Flask(__name__)


# This route is for printing out eh dep tree for a sentence
# based on spacy
# required param - sentence

def get_nouns(doc, token_json):
    noun_chunks = ""
    # Parse for noun chunks
    for chunk in doc.noun_chunks:
        # Create a arrow separated string that can be appended into the 
        # json object. this maintains the structure and is easy to analyse
        noun_chunks = str(chunk) + "->" + str(chunk.root) + "->" + str(chunk.root.dep_) + "->" + str(chunk.root.head)
        token_json.append({"nounChunk" : noun_chunks})

    return True

# try getting the head word of a sentence via spacy
# the head word might be the key thing the user is talking about
def get_deps(doc, token_json):
    # dependencies = []
    for sent in doc.sents:
        dep_tree = ""
        for token in sent:
            dep_tree = dep_tree + "->"+ token.dep_
        token_json.append({"depTree" : dep_tree})

    return True

# Obtain SVOs for sentence based on stanford NLP 
def get_svos(sentence):
    svo = SVO()
    sentences =  svo.sentence_split(sentence)
    svo_list = []
    for sent in sentences:
        root_tree = svo.get_parse_tree(sent)
        svo_list.append(svo.process_parse_tree(next(root_tree)))

    return svo_list


# Use textblob for POS - easier functionality
def get_pos(sentence, token_json):
    blob = TextBlob(sentence)
    pos_list = ""

    # since htis is a tuple we will have to first join
    # then split and then get the 1st element
    Separator = '-'
    for pos in blob.tags:
        posWord = Separator.join(pos).split('-')[1]
        pos_list = pos_list + "->" + posWord
    #collect all the strings and push them in the JSON array
    token_json.append({"posList" : pos_list})
        
    return True


@app.route("/getall/")
def get_all():
    #parse nlp 
    doc = nlp(u'' + request.args.get('sentence'))
    # Loop through and form json response
    token_json = []

    # get noun chunks
    get_nouns(doc, token_json)
   

    # get dependency tree
    get_deps(doc, token_json)
   # token_json.append(deps)

    # get part of speech
    get_pos(request.args.get('sentence'), token_json)
   


    print(token_json)
    return json.dumps(token_json)



