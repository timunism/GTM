from model import GTM

# filename
filename = "story-teller" # dont add extension
trainingset_name = 'story-teller.txt' # add extension

# Create an instance of the GTM class
orderValue = 5
markov_chain = GTM(order=orderValue)

# Train the Markov chain on a sequence
def import_file(filename):
    with open(f"./data/{filename}", 'r', encoding="utf-8") as file:
        file_contents = file.read()
    return file_contents

# Example usage
sequence = import_file(trainingset_name);
markov_chain.train(sequence)

# Save the Markov chain to a file

print('saving...')
# Count the number of values in the generated chain
modelSize = 0;
for i in markov_chain.chain.values():
    modelSize += len(i)

modelSize = modelSize/1000000 # 1 million
modelSize = round(modelSize, 1);

# save the model
markov_chain.save(f"{filename}_{modelSize}M_order-{orderValue}")
print('done')
