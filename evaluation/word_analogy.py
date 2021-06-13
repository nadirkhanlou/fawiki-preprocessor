import sys

import fasttext

from random import shuffle, seed

model_file = sys.argv[1]
test_file = sys.argv[2]
no_of_tests = 100 if len(sys.argv) < 4 else eval(sys.argv[3])

#-----------------------read evalate file and get words and humann judjments------------------

model = fasttext.load_model(model_file)
test_data = open(test_file).read()
lines = test_data.split('\n')
quadruples = []
for line in lines:
    if line == '':
        continue
    quadruples += [line.split()]
print("LOG: Number of quadruples:", len(quadruples))
if (no_of_tests > len(quadruples)):
    no_of_tests = len(quadruples)
counter = 0
i = 0
predictions = []

seed(70)
shuffle(quadruples)

print("LOG: Using", no_of_tests, "samples")
for q in quadruples[:no_of_tests]:
    i += 1
    # Top 5 results are chosen as predictions
    preds = [p[1] for p in model.get_analogies(q[0], q[1], q[2])[:5]]
    # if q[3] in preds:
    #     counter += 1
    #     print("Query: ", q[0], q[1], q[2], q[3])
    #     print("Predictions:", preds)
    predictions.append((q[3], preds))

print("LOG: Number of correct predictions:",
        counter, "out of", no_of_tests)
print("LOG: Accuracy:", counter/no_of_tests)

