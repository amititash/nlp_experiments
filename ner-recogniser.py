import spacy
import pandas as pd
from print_utils import skip_and_print, print_table  #for printing nice table outputs


# Load a language model and parse a document.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nlp = spacy.load('en')

#document_string = "I like to visit Park Tea House in Berkeley."
'''
load the data frame
we will make this dynamic, possibly expose via API or commandline
'''
df = pd.read_csv('minigraph.csv')
# print(df.head())

#create _ based string that will then be passed to spacy
document_string = ' '.join(list(df))


skip_and_print('Working with string: "%s"' % document_string)
doc = nlp(document_string)


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

# Named entities found:
#
# Name           Start End Label
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


for ent in doc.ents:
    skip_and_print('Recovering "%s":' % ent)
    print(document_string)
    print(' ' * ent.start_char + '^' * len(ent.text))


