import re
import os
import sys
import codecs


def text_dictionary(path):
	dictionary = {}
	for name in os.listdir(path):
		text = codecs.open(path+"/"+name, "r", "utf-8")
		list = []
		for line in text:
			list.append(line.strip('\n'))
		dictionary[name] = list
	return dictionary

