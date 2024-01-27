with open('fiction-stories.txt', 'r') as file:
	dataset = file.read()

corpus = dataset[:len(dataset)//2]

output = open('corpus.txt', 'w');
output.write(corpus)
output.close()