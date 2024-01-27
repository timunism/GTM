"""
Most Books have the statement Chapter X: Title, which denote the start
of a new chapter and its title. The following is a simple script
to remove that statement from as many sentences as possible. The
targets are the words that are mostly likely to come after the Title,
those we'll be the starting point for the newly generated sentence
"""

# import the dataset
print('importing dataset...')

with open('fiction-stories.txt', 'r') as file:
	corpus = file.read();

# running the process as a function results in ridiculous peformance gain
# Double spaces may cause some data to slip through processing
def sortSentences(corpus):
	# target word to start the sentence from
	targets = [
			'As', 'In', 'At', 'After', 'While', 
			'When', 'Now', 'With', 'Years', 'Filled',
			'Later', 'Looking', 'Despite', 'And', 'It',
			'To', 'Though', 'During', 'Realizing', 'Over'
			'Many', 'Once', 'Finally', 'What', 'Determined', 'Dr', 'Jack'
			'Sarah', 'Thomas', 'Lyla', ' As', ' To', ' In', 'James', 'Charles',
			'However']

	targetToRemove = 'Chapter'
	sentences = '';
	count = 0;
	# convert dataset to array of sentences
	for sentence in corpus.split('.'):
		if sentence.strip().startswith(targetToRemove):
			checked = False
			# retrieve target sentences
			snippet = sentence[:60]
			snippet = snippet.split(' ');
			# if target word exists remove the words associated with it
			for word in snippet:
				for target in targets:
					if target in word:
						try:
							end=sentence.index(target)
							sentence = sentence.split(sentence[:end])
							# return the clean sentence
							sentence = sentence[1]
							count += 1
							checked = True
							break
						except Exception as e:
							pass

				if checked == False and 'The' in word:
					try:
						new_sentence = sentence.split(': The')
						end=new_sentence[1].index('The')
						sentence = sentence.split(sentence[:end])
						# return the clean sentence
						sentence = sentence[1]
						count += 1
					except Exception as e:
						pass
			if checked == False:
				new_snippet = snippet[6:]
				if new_snippet[0][0].isupper():
					sentence = ''
					for i in new_snippet:
						sentence += i + ' ';

					#print(f" {sentence}")
					checked = True
					count += 1
				else:
					new_snippet = snippet[5:]
					if new_snippet[0][0].isupper():
						sentence = ''
						for i in new_snippet:
							sentence += i + ' ';

						#print(f" {sentence}")
						checked = True
						count += 1
					else:
						pass
				
			print(f'\rCleaned: {count}', end='', flush=True)

		sentences += sentence + '.'
	return sentences

print('Sorting Sentences...')
cleanSentences = sortSentences(corpus);

cleanCorpus = open('clean_corpus.txt', 'w');
cleanCorpus.write(cleanSentences);
cleanCorpus.close()
