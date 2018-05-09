import spacy
from spacy.tokens import Doc
import pandas as pd
import json #for pretty printing
from print_utils import skip_and_print, print_table 


''' Overriding the default whitespace tokenisation with underscore 
tokenisation, since we know that csv headers are going to aleardy 
be independent entities.  '''

class UnderScoreTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab 
        
    def __call__(self, text):
        words = text.split('_')
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)



'''
load the data frame
we will make this dynamic, possibly expose via API or commandline
'''
df = pd.read_csv('./.data_sets/profit_cost.csv')
# print(df.head())

#create _ based string that will then be passed to spacy
titleString = '_'.join(list(df))

#print(titleString)

# Load a language model.
# ~~~~~~~~~~~~~~~~~~~~~~
nlp = spacy.load('en_core_web_sm')

# Understand your language model.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Language models may contain useful metadata, such as how it
# was created, or a contact email address.
skip_and_print('Data about the language model:')
print(json.dumps(nlp.meta, indent=4))

# Override the default tokenizer with our own tokenizer
nlp.tokenizer = UnderScoreTokenizer(nlp.vocab)
doc = nlp(titleString)

# Iterate over tokens of the document.
skip_and_print('List of tokens in doc:')
for token in doc:
    print(token)

# Enumerate all token attributes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Each token has many useful properties.
skip_and_print('List of attributes from a sample Token:')
print([attr for attr in dir(doc[0]) if '__' not in attr])
# Attributes include, e.g., .pos_, .text, and .vector.

# Mapping tokens to integers.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

# The `orth` attribute provides an integer id for every token:
skip_and_print('The .orth value for all tokens:')
print([token.orth for token in doc])  # A list of integers.

# Each token also comes with a normalized form. In English, this
# may simply be the lowercased word itself.

# Let's print a table of token texts, pos, ids, normalized forms, and
# the ids for the normalized forms:

skip_and_print('Printing all POS')
rows = [['Text', 'POS', 'Dep', 'Head', 'POS']]
for token in doc:
    rows.append([token.text,   # Token str w/o outer space.
                 token.pos_,   # pos tag of the token
                 token.dep_,   # Integer id for .text value.
                 token.head.text,  # Normalized str of .text value.
                 token.head.pos_])  # Integer id for .norm_ value.
print_table(rows)

skip_and_print('Printing all nodes')
nodeRows = [['Text']]
for token in doc:
    nodeText = token.text
    nodePos = token.pos_
    if (nodePos == 'PROPN'):
        if(nodeText not in nodeRows):
            nodeRows.append([token.text])
            
print_table(nodeRows)

'''

Not found relevent for csv parsing

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

'''