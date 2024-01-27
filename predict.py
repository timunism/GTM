from model import GTM
from encoder import Encoder
import json

# filename
filename = "fiction-stories_122.7M_order-5"

# import generated notes
print('Generating...')

# setup
encoder = Encoder()

# Create an instance of the GTM class
markov_chain = GTM(order=5)

# Load the Markov chain from the file
markov_chain.load(filename)

output = [];
seed = 0;

generated_sequence = markov_chain.generate_sequence(length=150, seed=seed)

# retrieve individual words from the sequence and append them to the output
for encodedValue in generated_sequence:
    output.append(encodedValue)

# import encode map to use for decoding generate sequence
encodeMap = open('./data/map.json');
mapper = json.load(encodeMap);

# decode output
output = encoder.decode(output, mapper);

# clean output
output = output.split('.');
generatedText = "";

for sentence in output[1:]:
    generatedText += sentence + '.'

print(generatedText.strip())
print(markov_chain.evaluate())
