"""

Generative Trainable Markov-model ver.1.0.0

Copyright (c) 2023 Tinashe Mashindi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import pickle
import random
from encoder import Encoder
from collections import defaultdict

"""
Re-arranging the dataset programmatically helps
improve the model's ability to establish relationships between words,
especially if the dataset does not have a natural or explicit sequential order.

iterations => number of times to mutate the dataset

more, may or may not always be better, so you just mess around with the count until
you get an optimal performance
"""
class ChainMutation:
    def __init__(self):
        pass

    # This function re-arranges the dataset, so may not be suitable for accurate dataset to output mapping
    # It excels in generative applications, where the goal is to generate new text
    def constructive(self, tokens, iterations, save):
        output = []
        sequenceA = [];
        sequenceB = [];
        sequenceC = [];

        # the dataset is split into 3 small datasets (sets)
        for i in range(len(tokens)):
            if i < len(tokens)//3 and i < len(tokens)//2:
                sequenceB.append(tokens[i])
            elif i > len(tokens)//3 and i < len(tokens)//2:
                sequenceA.append(tokens[i])
            elif i > len(tokens)//2 and i < len(tokens):
                sequenceC.append(tokens[i])

        # these small datasets are then rearranged:
        # set(1)->set(2)->set(3)->set(2)->set(3)->set(1)->set(2)->set(3)
        for x in range(iterations):
            output.append(sequenceA)
            output.append(sequenceB)
            output.append(sequenceC)
            output.append(sequenceB)
            output.append(sequenceC)
            output.append(sequenceA)
            output.append(sequenceB)
            output.append(sequenceC)
            print(f"\riterations: {x+1}",end='', flush=True)
        
        print('\n')
        if save:
            print('Saving Constructed Data')
            file = open('data/constructed_training_data.txt', 'w')
            file.write(output)

        new_set = []
        for array in output:
            for i in array:
                new_set.append(i)


        return new_set

encode = Encoder()
chain_mutation = ChainMutation();

# This is where the magic happens
class GTM:
    def __init__(self, order):
        self.order = order # number of tokens to consider when predicting
        self.chain = defaultdict(list) # this is where the transitions are stored
		# defaultdict is much faster than standard dict

    # training function
    def train(self, sequence, iterations):
        tokens = sequence.split(' ') # split sequence into tokens
        print('Encoding...')
        tokens = encode.words(tokens, tokens); # encode tokens
	    
        print('Training...')
        # generate key => value dictionary (chain)
        for i in range(len(tokens) - self.order):
            # generate key & value
            key = tuple(tokens[i:i+self.order])
            value = tokens[i+self.order]
            
            # if the key has been generated
            if key in self.chain:
                self.chain[key].append(value) # append the generated value
            else:
                # declare a new key => value pair using the generated key & value.
                self.chain[key] = [value]

    # save model
    def save(self, filename):
        with open(f"data/{filename}.gtm", 'wb') as file:
            pickle.dump(self.chain, file)

    # load model
    def load(self, filename):
        with open(f"data/{filename}.gtm", 'rb') as file:
            self.chain = pickle.load(file)

    # generate new sequence
    def generate_sequence(self, length, seed):
        # A robust function for infering from the model, regardless of its order
        def infer():
            possible_keys = []
            for key in self.chain.keys():
                # if key in chain contains all the words from the seed
                if all(char in key for char in seed):
                    # append key to possible states
                    possible_keys.append(key)

            return possible_keys;

        # if seed is provided
        if seed != None:
            possible_states = infer();
            # use its values to approximate a current_state
            seed = tuple(seed)
            current_state = random.choice(possible_states) # infer current state from dictionary
            #print('Current State:',current_state)
        else:
            # pick a state at random (returns a tuple)
            current_state = random.choice(list(self.chain.keys()));

        """The current state is where the 'Random Walk' starts. And the final sequence
           is a combination of the current state and all the tokens generated,
           during the random walk.
        """
        sequence = list(current_state) # convert to a mutable list

		# Do a random walk, while in the range of provided length
		# I'm subtracting the length of the seed from the generated tokens inorder to get an output of provided length
		# i.e. output_length = provided_length; since(provided_length = generated_sequence_length + seed_length)
        for i in range(length - len(sequence)):			
            if current_state in self.chain:
				# pick next token at random from the possible transitions of the current state
                next_token = random.choice(self.chain[current_state]);
				# and appended it to the sequence
                sequence.append(next_token)
				# then set the current state to be the first previous x tokens of the current sequence
				# where x = Markov Order (number)
                current_state = tuple(sequence[-self.order:])
            else:
                break
        
        return sequence

    # evaluate model (read number of parameters or transitions)
    def evaluate(self):
        modelSize = 0;
        for i in self.chain.values():
            modelSize += len(i)

        modelSize = modelSize/1000000 # 1 million
        modelSize = round(modelSize, 1);

        return f"Model Size: {modelSize}M"

