import readfile
import kokako
import keyphrase_evaluation_inspec as ke
from evaluate import *

diction = readfile.text_dictionary("./cmi/data/inspec")
text1 = diction['1945.abstr.pre']

G = kokako.graph(text1, window = 5)
print G.graph.edge['oper']

tRank_score = G.undirected_TextRank()
ref = ke.read_file("/Users/fodrh/Documents/Hyungjin/NLP_CODE/NetworkX/kokako/cmi/data/references/inspec.ref")
ref1 = ref['352.abstr.pre']
print tRank_score
keys = diction.keys()

def datas(diction, ref, winsize):
	keys = diction.keys()
	data = {}
	for key in keys:
		text = diction[key]
		G = kokako.graph(text, window = winsize)
		tRank_score = G.undirected_TextRank()
		candidates = [word for score, word in tRank_score]
		data[key] = evaluate(candidates, ref[key])
	return data

data = datas(diction, ref, 2)
def average(data):
	average = { 'P5':0, 'R5':0, 'P10':0,'R10':0, 'R-MAX':0, 'MAP':0, 'F5':0, 'F10':0 }
	keys = data.keys()
	for key in keys:
		for measure in average.keys():
			average[measure] += data[key][measure]
	for measure in average.keys():
		average[measure] /= len(data)

	return average

average = average(data)
#print average
