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

app = Flask(__name__)


# This route is for printing out eh dep tree for a sentence
# based on spacy
# required param - sentence

def get_nouns(doc, token_json):
    # noun_chunks = []
    # Parse for noun chunks
    for chunk in doc.noun_chunks:
        token_json.append(
        {"chunk": str(chunk),           # A Span object with the full phrase.
        "root": str(chunk.root),       # The key Token within this phrase.
        "dep": str(chunk.root.dep_),  # The grammatical role of this phrase.
        "roothead": str(chunk.root.head)   # The grammatical parent Token.
        })

    return True

# try getting the head word of a sentence via spacy
# the head word might be the key thing the user is talking about
def get_deps(doc, token_json):
    # dependencies = []
    for sent in doc.sents:
        for token in sent:
            token_json.append({token.dep_ : token.text})

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
    # pos_list = []
    for word, pos in blob.tags:
        print(word, pos)
        token_json.append({pos : word})
        
    return True

# Obtain SVOs for a sentence
# DEPRECATED
@app.route("/getall/")
def get_all():
    #parse nlp 
    doc = nlp(u'' + request.args.get('sentence'))
    # Loop through and form json response
    token_json = []

    get_nouns(doc, token_json)
   # token_json.append(nouns)

    deps = get_deps(doc, token_json)
   # token_json.append(deps)

    pos = get_pos(request.args.get('sentence'), token_json)
   # token_json.append(pos)

   # svos = get_svos(request.args.get('sentence'))
   # token_json.append({"svos" : svos})

    print(token_json)
    return json.dumps(token_json)



