import nltk
from nltk.corpus import brown

def frequencies(trainData):
	fTags = {}; fword_tags = {}; ftag_tags = {}
	fTags['start'] = 0
	for i in range(len(trainData)):
		for j in range(len(trainData[i])):
			tp = (trainData[i][j][0].lower(),trainData[i][j][1])
			if tp[1] in fTags:
				fTags[tp[1]] += 1
			else:
				fTags[tp[1]] = 1
			if tp in fword_tags:
				fword_tags[tp] += 1
			else:
				fword_tags[tp] = 1
			if j == 0:
				fTags['start'] += 1
				x = ('start',tp[1])
			else:
				x = (trainData[i][j-1][1],tp[1])
			if x in ftag_tags:
				ftag_tags[x] += 1
			else:
				ftag_tags[x] = 1

	return (fTags, fword_tags, ftag_tags)

def findMax(word,fTags,fword_tags,ftag_tags,prevTag,prevProb):
	maximum = 0.0
	tag = ""
	for t in fTags:
		try:
			prob = prevProb*(ftag_tags[(prevTag,t)]*1.0/fTags[prevTag])*(fword_tags[(word.lower(),t)]*1.0/fTags[t])
		except:
			prob = 0.0
		if(prob == 0.0 and prob == maximum):
			tag = t
		if prob > maximum:
			maximum = prob
			tag = t
	return (tag,maximum)

def accuracy(expectedTags,tags):
	correct = 0
	wrong = 0
	for i in range(len(expectedTags)):
		for j in range(len(expectedTags[i])):
			if expectedTags[i][j] == tags[i][j]:
				correct += 1
			else:
				wrong += 1
	return (correct*100.0)/(correct+wrong)

def generateChunk():
	pass

if __name__ == '__main__':
	
	sent_tags = brown.tagged_sents(simplify_tags = True)
	# Shuffle sentences ?? (because every time test and train data is constant)
	size = 9*len(sent_tags)/10
	trainData = sent_tags[:size]
	testData = sent_tags[size:]

	(fTags,fword_tags,ftag_tags) = frequencies(trainData)

	tags=[]
	expectedTags = []
	for sent in testData:
		s = []
		for x in sent:
			s.append(x[1])
		expectedTags.append(s)
		tagSeq = []
		prevProb = 1
		prevTag = 'start'
		for index in range(len(sent)):
			word = sent[index][0]
			(tag,prevProb) = findMax(word,fTags,fword_tags,ftag_tags,prevTag,prevProb)
			tagSeq.append(tag)
		tags.append(tagSeq)

	print "Accuracy :- " + str(accuracy(expectedTags,tags))