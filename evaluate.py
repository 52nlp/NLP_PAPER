def evaluate(candidates, reference_set):
	ranks = []
	scores = {}

	average_precision = 0.0
	for i in range(len(candidates)):
		if candidates[i] in reference_set:
			ranks.append(i+1)
			average_precision += len(ranks) / float(i+1)

	keys_at_5 = 0
	for i in range(len(ranks)):
		if ranks[i] <= 5:
			keys_at_5 += 1
		else:
			break

	scores['P5'] = keys_at_5 / 5.0
	scores['R5'] = keys_at_5 / float(len(reference_set))
	if (scores['P5'] + scores['R5']) > 0:
		scores['F5'] = 2.0 * (scores['P5']*scores['R5']) / (scores['P5']+scores['R5'])
	else:
		scores['F5'] = 0.0

	keys_at_10 = 0
	for i in range(len(ranks)):
		if ranks[i] <= 10:
			keys_at_10 += 1
		else :
			break

	scores['P10'] = keys_at_10 / 10.0
	scores['R10'] = keys_at_10 / float(len(reference_set))
	if (scores['P10'] + scores['R10']) > 0:
		scores['F10'] = 2.0 * (scores['P10']*scores['R10']) / (scores['P10']+scores['R10'])
	else:
		scores['F10'] = 0.0

	scores['R-MAX'] = len(ranks) / float(len(reference_set))
	scores['MAP'] = average_precision / len(reference_set)

	return scores

