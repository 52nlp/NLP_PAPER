import kokako
def build_cand_graph(self):
	for i in range(len(self.sentences)):
		words = self.sentences[i]
		for j in range(len(words)-1):
			if (words[j] != '') and (words[j+1] != ''):
				self.cand_graph.add_edge(words[j], words[j+1])


def make_candidate(self, node, cand, candidates, rank20):
	for n in self.cand_graph.neighbors(node):
		if n in rank20:
			cand.append(n)
			self.make_candidates(n, cand, candidates, rank20)
			cand = cand[:-1]
	candidates.append(cand)


def candidates(self):
	all_candidates = []
	for node in self.cand_graph:
		cand = []
		candidates = []
		cand.append(node)
		self.make_candidate(node, cand, candidates, rank20)
		all_candidates + candidates
	return all_candidates

def generate_candidates(self):
	candidates = self.candidates()
	for cand in candidates:
		self.keyphrase_candidates.add(' '.join(cand))


