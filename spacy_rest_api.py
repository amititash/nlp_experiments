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


# Load the language model only one time in the life cycle
nlp = spacy.load('en')

app = Flask(__name__)


# This route is for printing out eh dep tree for a sentence
# based on spacy
# required param - sentence

@app.route("/parse/")
def parse_text():
    # Obtain the sentence from param
    sentence = request.args.get('sentence') 
    #parse nlp 
    doc = nlp(sentence)
    # Loop through and form json response
    token_json = []
    # Parse for noun chunks
    for chunk in doc.noun_chunks:
        token_json.append([
        str(chunk),            # A Span object with the full phrase.
        str(chunk.root),       # The key Token within this phrase.
        str(chunk.root.dep_),  # The grammatical role of this phrase.
        str(chunk.root.head)   # The grammatical parent Token.
        ])
    
    print(token_json)

    # Parse for verbs in the tree
    # based on spacy
    # Finding a verb with a subject from below — good
    verbs = set()
    for possible_subject in doc:
        if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
            verbs.add(possible_subject.head)
    
    token_json.append(str(verbs))

    return json.dumps(token_json)

# try getting the head word of a sentence via spacy
# the head word might be the key thing the user is talking about
@app.route("/headword/")
def head_word():
    head_word = "null"
    # Loop through and form json response
    token_json = []
    #question = "What films featured the character Popeye Doyle ?"
    doc = nlp(u'' + request.args.get('sentence'))
    for sent in doc.sents:
        for token in sent:
            token_json.append({token.text: token.dep_})
            if token.dep == nsubj and (token.pos == NOUN or token.pos == PROPN):
                head_word = token.text
            elif token.dep == attr and (token.pos == NOUN or token.pos == PROPN):
                head_word = token.text
        token_json.append({'head_word': head_word})

    return json.dumps(token_json)


# Obtain SVOs for a sentence
# DEPRECATED
@app.route("/oldgetsvos/")
def old_get_svos():
    svos = {}
    doc = nlp(u'' + request.args.get('sentence'))
    svos = findSVOs(doc)
    printDeps(doc)
    print(svos)
    return json.dumps(svos)

# Obtain SVOs for sentence based on stanford NLP 
@app.route("/getsvos/")
def get_svos():
    svo = SVO()
    sentences =  svo.sentence_split(request.args.get('sentence'))
    val = []
    print(sentences)
    for sent in sentences:
        root_tree = svo.get_parse_tree(sent)
        val.append(svo.process_parse_tree(next(root_tree)))

    print(val)
    return json.dumps(val)


# try getting the verb in past participle form of a sentence via spacy
# the verb might be the key to what the user wants to do 
@app.route("/getverb/")
def get_verb():
    verb_term = "null"
    # Loop through and form json response
    token_json = []
    #question = "What films featured the character Popeye Doyle ?"
    doc = nlp(u'' + request.args.get('sentence'))
    for sent in doc.sents:
        for token in sent:
            print(token.pos_)
            if token.tag_ == 'VBN' or token.tag_ == VERB:
                verb_term = token.text
        token_json.append({'verb_term': verb_term})

    return json.dumps(token_json)

