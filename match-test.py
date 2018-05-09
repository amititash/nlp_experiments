'''
based on code from
https://stackoverflow.com/questions/47638877/using-phrasematcher-in-spacy-to-find-multiple-match-types?rq=1&utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

'''

import spacy
import pandas as pd
from spacy.matcher import PhraseMatcher
from print_utils import skip_and_print, print_table


# Load a language model.
# ~~~~~~~~~~~~~~~~~~~~~~
nlp = spacy.load('en_core_web_sm')


#  create lists of entities that we need to detect in the csv
sales_terms = [nlp(text) for text in ('ship date','ship mode','client size', 'customer name', 'deal size', 'supplies subgroup', 'supplies group')]


# Then load the doc and run throgh the sentences
matcher = PhraseMatcher(nlp.vocab)
matcher.add('SALES', None, *sales_terms)


# capture the tuples in this list and identify pos
'''
load the data frame
we will make this dynamic, possibly expose via API or commandline
'''
df = pd.read_csv('minigraph.csv')
# print(df.head())

#create _ based string that will then be passed to spacy
document_string = ' '.join(list(df))

# making the string lower case to pass it through the table of matching terms
lower_string = document_string.lower()


skip_and_print('Working with string: "%s"' % document_string)
doc = nlp(lower_string)

rows = [[]]

matches = matcher(doc)
for match_id, start, end in matches:
    rule_id = nlp.vocab.strings[match_id]  # get the rule id from the list
    span = doc[start : end]  # get the matched slice of the doc
    #rows.append([rule_id, span.text])  # Integer id for .norm_ value.
    print(rule_id, span.text)
#print_table(rows)

