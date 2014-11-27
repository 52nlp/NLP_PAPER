import re
import os
import sys
import nltk
import codecs

stemmer = nltk.stem.snowball.EnglishStemmer()


def keyphrase_to_stems(text):
	words = text.split(' ')
	for i in range(len(words)):
		words[i] = stemmer.stem(words[i])
	return ' '.join(words)

	
def read_file(path):
	dictionary = {}
	for line in codecs.open(path, "r", "utf-8"):
		line = line.strip()
		if line != '':
			document_id, text = line.split('\t')
			keyphrases = text.lower().split(';')
			for i in range(len(keyphrases)):
				keyphrases[i] = re.sub(' +', ' ', keyphrases[i])
				keyphrases[i] = keyphrase_to_stems(keyphrases[i].strip())
			dictionary[document_id + '.pre'] = keyphrases
	return dictionary


