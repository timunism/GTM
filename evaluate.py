import pickle
import argparse

parser = argparse.ArgumentParser(description="Learn the size of GTM models")
parser.add_argument("model_name", type=str, help="fullname of the model")
args = parser.parse_args()

model_name = args.model_name;

print('loading...')
with open(f'./data/{model_name}.gtm', 'rb') as file:
	model = pickle.load(file)

modelSize = 0;

for i in model.values():
	modelSize += len(i)

modelSize = modelSize/1000000 # 1 million

print(f"Model Size: {round(modelSize, 1)}M")