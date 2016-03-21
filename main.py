import os
import pip
import nltk
from nltk.corpus import wordnet as wn

# Install googlesearch if not yet installed
if 'googlesearch' not in map(lambda x: x.project_name, pip.get_installed_distributions()):
  os.system('sudo pip install googlesearch')
from googlesearch import GoogleSearch as gs

googleResults = lambda key: gs('%s and' % key).top_results()
sentenceToWords = lambda sent: [w.lower() for w in\
    nltk.Text(nltk.wordpunct_tokenize(sent))\
    if w.isalpha()]

# Get the adjectives
adjs = [synset.lemma_names()[0] for synset in list(wn.all_synsets(wn.ADJ))]

'''
Get the words that follows key and
e.g. interesting as in weird and interesting with weird as key
'''
key = 'interesting'
rtn = []
query = '%s and ' % (key)
search = gs(query).top_results()
for result in search:
  content = sentenceToWords(result['content'])
  title = sentenceToWords(result['titleNoFormatting'])
  # Extract the word behind key and
  for i in range(len(content) - 2):
    if content[i] == 'interesting' and content[i + 1] == 'and':
      rtn.append(content[i + 2])
  for i in range(len(title) - 2):
    if title[i] == 'interesting' and title[i + 1] == 'and':
      rtn.append(title[i + 2])

