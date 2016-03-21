import os
import pip
import nltk
from nltk.corpus import wordnet as wn
from collections import defaultdict

# Install googlesearch if not yet installed
if 'googlesearch' not in map(lambda x: x.project_name, pip.get_installed_distributions()):
  os.system('sudo pip install googlesearch')
from googlesearch import GoogleSearch as gs

googleResults = lambda key: gs('%s and' % key).top_results()
sentenceToWords = lambda sent: [w.lower() for w in\
    nltk.Text(nltk.wordpunct_tokenize(sent))\
    if w.isalpha() and len(w) > 1]

# Get the adjectives
adjs = [synset.lemma_names()[0] for synset in list(wn.all_synsets(wn.ADJ))]

'''
Get the words that follows key and
e.g. interesting as in weird and interesting with weird as key
'''
def similarWords(key):
  rtn = []
  query = '%s and ' % (key)
  search = gs(query).top_results()
  for result in search:
    content = sentenceToWords(result['content'])
    title = sentenceToWords(result['titleNoFormatting'])
    # Extract the word behind key and
    for i in range(len(content) - 2):
      if content[i] == key and content[i + 1] == 'and':
        rtn.append(content[i + 2])
    for i in range(len(title) - 2):
      if title[i] == key and title[i + 1] == 'and':
        rtn.append(title[i + 2])
  query = 'and %s' % (key)
  search = gs(query).top_results()
  for result in search:
    content = sentenceToWords(result['content'])
    title = sentenceToWords(result['titleNoFormatting'])
    # Extract the word before and key
    for i in range(2, len(content)):
      if content[i] == key and content[i - 1] == 'and':
        rtn.append(content[i - 2])
    for i in range(len(title) - 2):
      if title[i] == key and title[i - 1] == 'and':
        rtn.append(title[i - 2])
  return rtn


def dissimilarWords(key):
  rtn = []
  query = '%s but ' % (key)
  search = gs(query).top_results()
  for result in search:
    content = sentenceToWords(result['content'])
    title = sentenceToWords(result['titleNoFormatting'])
    # Extract the word behind key but
    for i in range(len(content) - 2):
      if content[i] == key and content[i + 1] == 'but':
        rtn.append(content[i + 2])
    for i in range(len(title) - 2):
      if title[i] == key and title[i + 1] == 'but':
        rtn.append(title[i + 2])
  query = 'but %s' % (key)
  search = gs(query).top_results()
  for result in search:
    content = sentenceToWords(result['content'])
    title = sentenceToWords(result['titleNoFormatting'])
    # Extract the word before but key
    for i in range(2, len(content)):
      if content[i] == key and content[i - 1] == 'but':
        rtn.append(content[i - 2])
    for i in range(len(title) - 2):
      if title[i] == key and title[i - 1] == 'but':
        rtn.append(title[i - 2])
  return rtn


# Construct the directed network: the link strength of two words is the number of cooccurence with and - cooccurence with but
# e.g.,
# network['interesting'] is the counter of similar(dissimilar) words of interesting
network = defaultdict(lambda: defaultdict(int))
for counter, key in enumerate(adjs):
  if counter % 100 == 0:
    print(counter)
  simWords = similarWords(key)
  disWords = dissimilarWords(key)
  for word in simWords:
    network[key][word] += 1
  for word in disWords:
    network[key][word] -= 1

# Build the manual labels
