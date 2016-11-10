import nltk
from nltk.corpus import conll2000

def frequencies_Tags(trainData):
	fTags = {}; fword_tags = {}; ftag_tags = {}
	fTags['start'] = 0
	for tree in trainData:
		prevTag = 'start'
		x = nltk.chunk.util.tree2conlltags(tree)
		for i in range(len(x)):
			tp = (x[i][0].lower(),x[i][1],x[i][2])
			if tp[1] in fTags:
				fTags[tp[1]] += 1
			else:
				fTags[tp[1]] = 1
			if tp[:2] in fword_tags:
				fword_tags[tp[:2]] += 1
			else:
				fword_tags[tp[:2]] = 1

			if i == 0:
				fTags['start'] += 1
			tagTuple = (prevTag,tp[1])
			prevTag = tp[1]
			if tagTuple in ftag_tags:
				ftag_tags[tagTuple] += 1
			else:
				ftag_tags[tagTuple] = 1

	return (fTags, fword_tags, ftag_tags)

def frequencies_Chunks(trainData):
	fChTags =  {}; fwords_chTags = {}; ftags_chTags = {}

	fChTags['start'] = 0
	for tree in trainData:
		x = nltk.chunk.util.tree2conlltags(tree)
		prevTag = 'start'
		for i in range(len(x)):
			tp = (x[i][0].lower(),x[i][1],x[i][2])
			if tp[2] in fChTags:
				fChTags[tp[2]] += 1
			else:
				fChTags[tp[2]] = 1
			if i == 0:
				fChTags['start'] += 1
			wordTuple = (tp[1],tp[2]) #here word is pos tag
			if wordTuple in fwords_chTags:
				fwords_chTags[wordTuple] += 1
			else:
				fwords_chTags[wordTuple] = 1
			tagTuple = (prevTag,tp[2])
			prevTag = tp[2]
			if tagTuple in ftags_chTags:
				ftags_chTags[tagTuple] += 1
			else:
				ftags_chTags[tagTuple] = 1
	return (fChTags,fwords_chTags, ftags_chTags)

def findMaxPOS(word,fChTags,fwords_chTags,ftags_chTags,prevTag,prevProb):

	maximum = 0.0
	tag = ""
	for t in fChTags:
		try:
			prob = prevProb*(ftags_chTags[(prevTag,t)]*1.0/fChTags[prevTag])*(fwords_chTags[(word.lower(),t)]*1.0/fChTags[t])
		except:
			prob = 0.0
		if prob == 0.0 and prob == maximum:
			tag = t
		if prob > maximum:
			maximum = prob
			tag = t
	return(tag,maximum)

def findMaxChunk(word,fChTags,fwords_chTags,ftags_chTags,prevTag,prevProb):

	maximum = 0.0
	tag = ""
	for t in fChTags:
		try:
			prob = prevProb*(ftags_chTags[(prevTag,t)]*1.0/fChTags[prevTag])*(fwords_chTags[(word,t)]*1.0/fChTags[t])
		except:
			prob = 0.0
		if prob == 0.0 and prob == maximum:
			tag = t
		if prob > maximum:
			maximum = prob
			tag = t
	return(tag,maximum)

def Calculate(testData,fChTags,fwords_chTags,ftags_chTags):

	expTags = []; calTags = []
	for tree in testData:
		sent = nltk.chunk.util.tree2conlltags(tree)

		sentExpTags = []
		tagSeq = []
		prevTag = 'start'
		prevChunkTag = 'start'
		prevProb = 1
		prevChunkProb = 1

		for i in range(len(sent)):
			word = sent[i][0]
			(tag,prevProb) = findMaxPOS(word,fTags,fword_tags,ftag_tags,prevTag,prevProb)
			prevTag = tag
			(tag,prevChunkProb) = findMaxChunk(tag,fChTags,fwords_chTags,ftags_chTags,prevChunkTag,prevChunkProb)
			prevChunkTag = tag
			sentExpTags.append(sent[i][2])
			tagSeq.append(tag)
		expTags.append(sentExpTags)
		calTags.append(tagSeq)

	return (expTags,calTags)

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

if __name__ == '__main__':
	
	data = conll2000.chunked_sents()
	size = 9*len(data)/10
	trainData = data[:size]
	testData = data[size:]

	(fTags,fword_tags,ftag_tags) = frequencies_Tags(trainData)
	(fChTags,fwords_chTags, ftags_chTags) = frequencies_Chunks(trainData)

	(expTags,calTags) = Calculate(testData,fChTags,fwords_chTags,ftags_chTags)

	print "Accuracy :- " + str(accuracy(expTags,calTags))