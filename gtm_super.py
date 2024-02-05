# Import the mmap module
import mmap
import pickle
import random
from encoder import Encoder
from collections import defaultdict

class ChainMutation:
    def __init__(self):
        pass
    def constructive(self, tokens, iterations, save):
        # Create a memory-mapped file for output
        output_file = open('data/constructed_training_data.txt', 'wb')
        output_size = len(tokens) * iterations * 6 * 8 # Assuming 8 bytes per token
        output_file.truncate(output_size) # Extend the file to the desired size
        output = mmap.mmap(output_file.fileno(), output_size, access=mmap.ACCESS_WRITE)
        
        sequenceA = [];
        sequenceB = [];
        sequenceC = [];
        for i in range(len(tokens)):
            if i < len(tokens)//3 and i < len(tokens)//2:
                sequenceB.append(tokens[i])
            elif i > len(tokens)//3 and i < len(tokens)//2:
                sequenceA.append(tokens[i])
            elif i > len(tokens)//2 and i < len(tokens):
                sequenceC.append(tokens[i])
        offset = 0 # Keep track of the position in the output file
        for x in range(iterations):
            # Write the sequences to the output file as byte arrays
            output[offset:offset+len(sequenceA)*8] = bytearray(sequenceA)
            offset += len(sequenceA)*8
            output[offset:offset+len(sequenceB)*8] = bytearray(sequenceB)
            offset += len(sequenceB)*8
            output[offset:offset+len(sequenceC)*8] = bytearray(sequenceC)
            offset += len(sequenceC)*8
            output[offset:offset+len(sequenceB)*8] = bytearray(sequenceB)
            offset += len(sequenceB)*8
            output[offset:offset+len(sequenceC)*8] = bytearray(sequenceC)
            offset += len(sequenceC)*8
            output[offset:offset+len(sequenceA)*8] = bytearray(sequenceA)
            offset += len(sequenceA)*8
            output[offset:offset+len(sequenceB)*8] = bytearray(sequenceB)
            offset += len(sequenceB)*8
            output[offset:offset+len(sequenceC)*8] = bytearray(sequenceC)
            offset += len(sequenceC)*8
            print(f"\riterations: {x+1}",end='', flush=True)        
        print('\n')
        if save:
            print('Saving Constructed Data')
            # Flush the changes to the file
            output.flush()
        # Close the output file and the mmap object
        output.close()
        output_file.close()
        # Return the output file name
        return 'data/constructed_training_data.txt'
encode = Encoder()
chain_mutation = ChainMutation();
class GTM:
    def __init__(self, order):
        self.order = order
        self.chain = defaultdict(list)
    def train(self, sequence, iterations):
        tokens = sequence.split(' ')
        print('Encoding...')
        tokens = encode.words(tokens, tokens);
        print('Staging...')
        # Get the output file name from the constructive method
        output_file = chain_mutation.constructive(tokens=tokens, iterations=iterations, save=True)
        # Open the output file and create a memory-mapped file for reading
        output_file = open(output_file, 'rb')
        output_size = os.path.getsize(output_file.name)
        output = mmap.mmap(output_file.fileno(), output_size, access=mmap.ACCESS_READ)
        
        print('Training...')
        # Read the tokens from the output file as byte arrays
        tokens = [output[i:i+8] for i in range(0, output_size, 8)]
        for i in range(len(tokens) - self.order):
            key = tuple(tokens[i:i+self.order])
            value = tokens[i+self.order]
            if key in self.chain:
                self.chain[key].append(value)
            else:
                self.chain[key] = [value]
        # Close the output file and the mmap object
        output.close()
        output_file.close()
    def save(self, filename):
        with open(f"data/{filename}.gtm", 'wb') as file:
            pickle.dump(self.chain, file)
    def load(self, filename):
        with open(f"data/{filename}.gtm", 'rb') as file:
            self.chain = pickle.load(file)
    def generate_sequence(self, length, seed):
        def infer():
            possible_keys = []
            for key in self.chain.keys():
                if all(char in key for char in seed):
                    possible_keys.append(key)
            return possible_keys;
        if seed != None:
            possible_states = infer();
            seed = tuple(seed)
            current_state = random.choice(possible_states)
        else:
            current_state = random.choice(list(self.chain.keys()));
        sequence = list(current_state)
        for i in range(length - len(sequence)):         
            if current_state in self.chain:
                next_token = random.choice(self.chain[current_state]);
                sequence.append(next_token)
                current_state = tuple(sequence[-self.order:])
            else:
                break
        
        return sequence
    def evaluate(self):
        modelSize = 0;
        for i in self.chain.values():
            modelSize += len(i)

        modelSize = modelSize/1000000 # 1 million
        modelSize = round(modelSize, 1);

        return f"Model Size: {modelSize}M"
