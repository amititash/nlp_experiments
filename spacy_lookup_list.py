'''
Dependency parsing and other test stuff
'''

import spacy
from print_utils import skip_and_print, print_table
from spacy import displacy

nlp = spacy.load('en')

# Open the file and read line by line
with open('../questions.txt') as fp:  

    ## For each load the object as NLP doc and make it into a complete string
    document_string = ' '.join(fp)

# now create a doc object and pass it to nlp for further processing
skip_and_print('Working with string: "%s"' % document_string)

doc = nlp(document_string)

skip_and_print("Here are the noun chunks of the sentence")
print(list(doc.noun_chunks))

# Finding named entities.
# ~~~~~~~~~~~~~~~~~~~~~~~

rows = [['Name', 'Start', 'End', 'Label']]

# Each `ent` object is an instance of the `Span` class.
for ent in doc.ents:
    rows.append([
        ent.text,        # The str of the named entity phrase.
        ent.start_char,  # Source str index of the first char.
        ent.end_char,    # Source str index of the last+1 char.
        ent.label_       # A str label for the entity type.
    ])

skip_and_print('Named entities found:')
print_table(rows)

# Enumerate all token attributes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Each token has many useful properties.
skip_and_print('List of attributes from a sample Token:')
print([attr for attr in dir(doc[0]) if '__' not in attr])
# Attributes include, e.g., .pos_, .text, and .vector.

# Each token also comes with a normalized form. In English, this
# may simply be the lowercased word itself.

# Let's print a table of token texts, ids, normalized forms, and
# the ids for the normalized forms:

skip_and_print('Printing all POS')
rows = [['Text', 'Dep', 'Head', 'POS']]
for token in doc:
    rows.append([token.text,   # Token str w/o outer space.
                 token.dep_,   # Integer id for .text value.
                 token.head.text,  # Normalized str of .text value.
                 token.head.pos_])  # Integer id for .norm_ value.
print_table(rows)

'''
 Now that we know the sentence tokens and pos, we are interested
 in the syntactic dependecies to pick up the subject, object and root
 which can help us form the query

'''

# lets create a list first of items that are of interest
synt_dep_list = ['nsubj', 'ROOT', 'dobj', 'pobj', 'amod']
skip_and_print('Key Query Items')

rows = [['Text', 'Dep']]
for token in doc:
    if token.dep_ in synt_dep_list:
         rows.append([token.text,   
                 token.dep_,   
                 ])  
print_table(rows)

displacy.serve(doc, style='dep')