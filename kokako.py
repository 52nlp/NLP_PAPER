import re
import math
import bisect
import nltk
import networkx as nx
from compiler.ast import flatten

stemmer = nltk.stem.snowball.EnglishStemmer()

class graph:

	def __init__(	self,
					sentences,
					window = 2,
					tags = ['JJ', 'NNP', 'NNS', 'NN', 'jj', 'nnp', 'nns', 'nn'],
					tag_delim = '/',
					use_tags = True	):

		self.graph = nx.Graph()
		self.cand_graph = nx.DiGraph()
		self.sentences = list(sentences)
		self.window = window
		self.tags = set(tags)
		self.tag_delim = tag_delim
		self.use_tags = use_tags
		self.rank20 = []
		self.keyphrase_candidates = set([])
		
		self.build_graph()
		self.undirected_TextRank()
		self.generate_candidates()
	

	def build_graph(self):

		for i in range(len(self.sentences)):
			words = self.sentences[i].split(' ')
			for j in range(len(words)):
				word, POS = self.wordpos_to_tuple(words[j], self.tag_delim)
				if POS in self.tags:
					words[j] = stemmer.stem(word)
					if not self.graph.has_node(words[j]):
						self.graph.add_node(words[j])
				else:
					words[j] = ''

			for j in range(len(words)):
				word1 = words[j]

				if word1 == '':
					continue

				for k in range(j+1, min(len(words), j+self.window)):
					word2 = words[k]

					if word2 == '':
						continue

					if not self.graph.has_edge(word1, word2):
						self.graph.add_edge(word1, word2, weight = 0)
					self.graph[word1][word2]['weight'] += 1
			self.sentences[i] = words
	
	
	def wordpos_to_tuple(self, word, delim='/'):
		m = re.match("^(.+)"+delim+"(.+)$", word)
		token, POS = m.group(1), m.group(2)
		return (token.lower(), POS)


	def tuple_to_wordpos(self, wordpos_tuple, delim='/'):
		return wordpos_tuple[0] + delim + wordpos_tuple[1]


	def remove_pos(self, candidate):

		words = []
		for wordpos in candidate.split(' '):
			words.append(wordpos[0:wordpos.rfind("/")])
		return ' '.join(words)

	def make_candidate(self, words):
		candidate = []
		for i in range(len(words)):
			if (words[i] != '' and words[i] in self.rank20):
				candidate.append(words[i])
			else:
				if len(candidate) > 0:
					return candidate
		return candidate


	def generate_candidates(self):
		for i in range(len(self.sentences)):
			words = self.sentences[i]
			for j in range(len(words)):
				candidate = self.make_candidate(words[j:])
				if len(candidate) > 0:
					self.keyphrase_candidates.add(' '.join(candidate))
	
	def score_candidates(self, scores):
		scored_candidates = []
		for keyphrase in self.keyphrase_candidates:
			score = 0
			for word in keyphrase.split(' '):
				score += scores[word]
			score /= ( len(keyphrase.split(' ')) + 1.0 )
			
#			if self.use_tags:
#				keyphrase = self.remove_pos(keyphrase)
			bisect.insort(scored_candidates, (score, keyphrase))
		scored_candidates.reverse()
		return scored_candidates

	def undirected_TextRank(self, d=0.85, f_conv=0.0001, max_iter=100):
		max_node_difference = f_conv
		node_scores = {}
		for node in self.graph.nodes():
			node_scores[node] = 1.0

		iter_number = 0
		while (max_node_difference >= f_conv and iter_number < max_iter):
			current_node_scores = node_scores.copy()
			score_difference = 0
			for node_i in self.graph.nodes():
				sum_Vj = 0
				neighbor_len = 0
				for node_j in self.graph.neighbors_iter(node_i):
					sum_Vj += current_node_scores[node_j]
					neighbor_len += 1
				
				if neighbor_len != 0:
					node_scores[node_i] = (1 - d) + (d * sum_Vj) / neighbor_len
				score_difference =  max(score_difference, \
						math.fabs(node_scores[node_i] - current_node_scores[node_i]))

				iter_number += 1
		#self.rank20 = filter(lambda x: x != '',flatten(self.sentences))
		self.rank20 = sorted(node_scores, key=lambda x:node_scores[x], reverse=True)
		return self.score_candidates(node_scores)
