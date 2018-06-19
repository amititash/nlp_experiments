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
import itertools, nltk, string



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

    # using nltk to extract key phrases. 
    # not really needed in this function and can 
    # be called directly but for now hooking it up here
    key_phrase_list = extract_candidate_chunks(sentence)


    # since htis is a tuple we will have to first join
    # then split and then get the 1st element
    Separator = '-'
    for pos in blob.tags:
        posWord = Separator.join(pos).split('-')[1]
        pos_list = pos_list + "->" + posWord
    #collect all the strings and push them in the JSON array
    # token_json.append({"posList" : pos_list})
    token_json.append(key_phrase_list)

        
    return True

# if we want to separately call this API just to get the dependency try and not the entire thing
@app.route("/getdeps/")
def get_deps_api():
    
    # do everything similar to get all
    # just call one func

     #parse nlp 
    doc = nlp(u'' + request.args.get('sentence'))
    # Loop through and form json response
    token_json = []

    # get dependency tree
    get_deps(doc, token_json)

    return json.dumps(token_json)

# if we want to separately call this API just to get the pos and not the entire thing
@app.route("/getpos/")
def get_pos_api():
    
    # do everything similar to get all
    # just call one func. Loop through and form json response
    token_json = []

    # get dependency tree
    get_pos(request.args.get('sentence'), token_json)

    return json.dumps(token_json)


def extract_candidate_chunks(text, grammar=r'KT: {<JJ> | (<JJ>* <NN.*>+)? <JJ>* <NN.*>+}'):
        
    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize, POS-tag, and chunk using regular expressions
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent)) for tagged_sent in tagged_sents))

    # join constituent chunk words into a single chunked phrase
    candidates = [' '.join(word for word, pos, chunk in group).lower() for key, group in itertools.groupby(all_chunks, lambda word__pos__chunk: word__pos__chunk[2] != 'O') if key]

    return [cand for cand in candidates if cand not in stop_words and not all(char in punct for char in cand)]

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

if __name__ == "__main__":
    app.run(port=2001)

