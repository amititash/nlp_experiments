'''
Dependency parsing of noun chunks in a sentence
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

# Find noun chunks
# ~~~~~~~~~~~~~~~~

skip_and_print('All the found noun chunks & some properties:')

rows = [['Chunk', '.root', 'root.dep_', '.root.head']]
for chunk in doc.noun_chunks:
    rows.append([
        chunk,            # A Span object with the full phrase.
        chunk.root,       # The key Token within this phrase.
        chunk.root.dep_,  # The grammatical role of this phrase.
        chunk.root.head   # The grammatical parent Token.
    ])
print_table(rows, padding=4)

