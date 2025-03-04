from sklearn.svm import LinearSVC
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics import accuracy_score
from nltk import word_tokenize, pos_tag#, Tree, ne_chunk
# import nltk
# import spacy
import json, random, string
# import re
import numpy as np

with open('tests\\NLP\\chatbot\\chatbot_info.json', 'r') as fp:
    chatbot_info = json.load(fp)  # load up the training data from the json file

possible_intents = [
    "greeting",
    "inquiry",
    "small-talk",
    "request",
    "goodbye",
    "inform",
    "apology",
    "comfort",
    "forgive",
    "condolences",
    "thanks",
    "accepting-thanks",
    "accusation",
    "yea",
    "nay",
    "dismiss",
    "explanation",
    "compliment",
    "insult"
]

ruleset = { # statement intents - response intents
    "greeting": ["greeting"],
    "goodbye": ["goodbye"],
    "inquiry": ["inform", "yea", "nay"],
    "apology": ["forgive"],
    "thanks": ["accepting-thanks", "dismiss"],
    "accusation": ["apology", "nay", "dismiss"],
    "condolences": ["thanks"]
}

training_inputs = []
intent_training_labels = []

for statement in chatbot_info['input-response-data']:
    training_inputs.append(statement['text'])
    intent_training_labels.append(statement['intent'])

    for response in statement['responses']:
        training_inputs.append(response['text'])
        intent_training_labels.append(response['intent'])

# for statement in chatbot_info['input-response-data']:
#     for intent in statement['intent']:
#         training_inputs.append(statement['text'])
#         intent_training_labels.append(intent)

#     for response in statement['responses']:
#         for intent in response['intent']:
#             training_inputs.append(response['text'])
#             intent_training_labels.append(intent)

# remove duplicates
temp_lst1 = []
temp_lst2 = []
temp_lst3 = []

for i, item in enumerate(training_inputs):
    if not (item in training_inputs[:i]):
        temp_lst1.append(training_inputs[i])
        temp_lst2.append(intent_training_labels[i])

training_inputs = temp_lst1
intent_training_labels = temp_lst2

# print(training_inputs, intent_training_labels)

# use the MultiLabelBinarizer to convert the labels into a form that can be used with for multilabel classification
binarizer = MultiLabelBinarizer()
intent_training_labels_binarized = binarizer.fit_transform(intent_training_labels)

# make the training data string versions of the part of speech tagged input
training_inputs = [str(pos_tag(word_tokenize(i))) for i in training_inputs]

# convert text into a numerical representation through the use of the "bag of words" technique
vectorizer = CountVectorizer()
training_vectors = vectorizer.fit_transform(training_inputs)

# fit the intent classifer to its training data(use the binarized labels list)
linear = LinearSVC()
intent_classifier = MultiOutputClassifier(linear, n_jobs=2)
intent_classifier.fit(training_vectors, intent_training_labels_binarized)


def statement_parser(input_string = ""):
    # use POS tagging string
    input_POS_string = str(pos_tag(word_tokenize(input_string)))

    # vectorizer.fit(training_inputs)
    # input_vectors = vectorizer.transform([input_string])

    # use POS tagged string
    input_vectors = vectorizer.fit(training_inputs).transform([input_POS_string])

    # predict the intent labels(using inverse_transform to turn it from the binary representation back to the original labels)
    intent = binarizer.inverse_transform(intent_classifier.predict(input_vectors))

    return intent

def UUID(length = 8):
    # out = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(length))
    out = ''.join(random.choices(string.ascii_letters + string.digits, k = length))
    
    return out


if __name__ == '__main__':
    # print(chatbot_info)

    print(statement_parser("Hi there!"))
    print(statement_parser("Hi! I'm doing great."))
    print(statement_parser("Hello! How are you?"))

    # print(statement_parser(input("> ")))

    while True:
        print(statement_parser(input("> ")))

    # print(chatbot_info['input-response-data'][0])