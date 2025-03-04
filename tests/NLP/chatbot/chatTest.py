from sklearn import tree
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
import json
# from nltk import pos_tag, word_tokenize

training_inputs = []
training_labels = []

# with open('tests\statResp-alt\dstcTrain.json', 'r') as fp:
# with open('tests\statResp-alt\ccpeTrain.json', 'r') as fp:
with open('statResp.json', 'r') as fp:
    trainData = json.load(fp)  # load up the training data from the json file

# sort the data for the classifiers
for i in trainData:
    # print(trainData[i])
    # print(i)
    for n in trainData[i]:
        training_inputs.extend([i] * len(trainData[i]))
        training_labels.extend(trainData[i])

# training_inputs = [str(pos_tag(word_tokenize(i))) for i in training_inputs]

# print(len(training_inputs))
# print(len(training_labels))

# convert the text into a numerical representation through the use of the "bag of words" technique
vectorizer = CountVectorizer()
training_vectors = vectorizer.fit_transform(training_inputs)

# fit the classifer to its training data
classifier = LinearSVC()
# classifier = tree.DecisionTreeClassifier()
classifier.fit(training_vectors, training_labels)

def respond(n = ""):
    vectorizer.fit(training_inputs)
    vectors = vectorizer.transform([n])
    # vectors = vectorizer.transform([str(pos_tag(word_tokenize(n)))])
    response = classifier.predict(vectors)[0]

    return response

if __name__ == "__main__":
    while True:
        t = respond(input("> "))
        print(t)