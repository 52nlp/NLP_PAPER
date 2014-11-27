import re
import math
import bisect
import nltk
import networkx as nx

class graph:

	def __init__(	self,
					sentences,
					strategy
					):

		self.graph = nx.DiGraph()
		self.sentences = sentences
		self.strategy = strategy
		self.candidates = []
		self.keyphrase_candidates = set([])

		self.build_graph()
		self.generate_candidates()



	def build_graph(self):
		for i in range(len(self.sentences)):
			sentence = self.sentences[i]
			for word in sentence:
				if word != '':
					if not self.cand_graph.has_node(word):
						self.cand_graph.add_node(word)
			for j in range(len(sentence)-1):
				
