from sklearn.svm import LinearSVC
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics import accuracy_score
from nltk import word_tokenize, pos_tag#, Tree, ne_chunk
# import nltk
# import spacy
import json, random, string
import datetime
# import re
# import numpy as np
from os.path import exists


class intent_chatbot():
    def __init__(self, data_file = "tests\\NLP\\chatbot\\intent_chatbot-v1\\chatbot_info.json", memory_training_file = "tests\\NLP\\chatbot\\intent_chatbot-v1\\memory_train.json", logs_folder = "tests\\NLP\\chatbot\\logs"):
        self.memory_training_file = memory_training_file
        self.data_file = data_file
        self.logs_folder = logs_folder

        self.is_chat_trained = False
        self.is_memory_trained = False

        # self.possible_intents = [
        #     "greeting",
        #     "inquiry",
        #     "small-talk",
        #     "request",
        #     "goodbye",
        #     "inform",
        #     "apology",
        #     "comfort",
        #     "forgive",
        #     "condolences",
        #     "thanks",
        #     "accepting-thanks",
        #     "accusation",
        #     "yea",
        #     "nay",
        #     "dismiss",
        #     "explanation",
        #     "compliment",
        #     "insult"
        # ]

        # self.possible_topics = [
        #     "well-being",
        #     "mood",
        #     "activity",
        #     "personal-details",
        #     "story",
        #     "relationship",
        #     "unknown"
        # ]

        self.ruleset = { # statement intents - response intents
            "greeting": ["greeting"],
            "goodbye": ["goodbye"],
            "inquiry": ["inform", "yea", "nay"],
            "apology": ["forgive"],
            "thanks": ["accepting-thanks", "dismiss"],
            "accusation": ["apology", "nay", "dismiss"],
            "condolences": ["thanks"]
        }

        self.idk_responses = [
            {'text': "I'm unsure how to respond to that.", 'intent': ['inform']},
            {'text': "I'm sorry, I don't know how to respond to that.", 'intent': ['inform']},
            {'text': "I'm sorry, what?", 'intent': ['inform']},
            {'text': "Come again?", 'intent': ['request']},
            {'text': "I don't know what that means.", 'intent': ['inform']},
            {'text': "I'm afraid I don't understand what you've said.", 'intent': ['inform']},
            {'text': "That sentence makes no sense to me.", 'intent': ['inform']},
            {'text': "I'm sorry?", 'intent': ['inform']},
            {'text': "I'm lost?", 'intent': ['inform']},
            {'text': "I'm confused.", 'intent': ['inform']},
            {'text': "Could you please clarify?", 'intent': ['request']},
            {'text': "Would you mind restating that?", 'intent': ['request']},
            {'text': "I'd be lying, if I said that I knew what that meant.", 'intent': ['inform']}
        ]
        
        self.chatbot_info = {
            "personal-details": {
                "name": "",
                "time-of-creation": str(datetime.datetime.now()),
                "nicknames": []
            },
            "memory": {},
            "input-response-data": []
        }

        if exists(self.data_file):
            with open(self.data_file, 'r') as fp:
                self.chatbot_info = json.load(fp)
        else:
            with open(self.data_file, 'w') as fp:
                json.dump(self.chatbot_info, fp)


    def train_chat(self):
        with open(self.data_file, 'r') as fp:
            chatbot_data = json.load(fp)
            self.input_response_data = chatbot_data['input-response-data']

        if self.input_response_data:
            print("Starting Training")

            self.training_inputs = []
            self.intent_training_labels = []
            self.topic_training_labels = []
            self.inquiry_training_labels = []

            for statement in self.input_response_data:
                self.training_inputs.append(statement['text'])
                self.intent_training_labels.append(statement['intent'])
                self.topic_training_labels.append(statement['topic'])
                
                if "inquiry" in statement['intent']:
                    self.inquiry_training_labels.append(statement['inquiry-type'])
                else:
                    self.inquiry_training_labels.append("none")

                for response in statement['responses']:
                    self.training_inputs.append(response['text'])
                    self.intent_training_labels.append(response['intent'])
                    self.topic_training_labels.append(response['topic'])
                    
                    if "inquiry" in response['intent']:
                        self.inquiry_training_labels.append(response['inquiry-type'])
                    else:
                        self.inquiry_training_labels.append("none")

            # remove duplicates
            temp_lst1 = []
            temp_lst2 = []
            temp_lst3 = []
            temp_lst4 = []

            for i, item in enumerate(self.training_inputs):
                if not (item in self.training_inputs[:i]):
                    temp_lst1.append(self.training_inputs[i])
                    temp_lst2.append(self.intent_training_labels[i])
                    temp_lst3.append(self.topic_training_labels[i])
                    temp_lst4.append(self.inquiry_training_labels[i])

            self.training_inputs = temp_lst1
            self.intent_training_labels = temp_lst2
            self.topic_training_labels = temp_lst3
            self.inquiry_training_labels = temp_lst4

            # print(self.training_inputs, self.intent_training_labels)

            # use the MultiLabelBinarizer to convert the labels into a form that can be used for multilabel classification
            self.chat_binarizer = MultiLabelBinarizer()
            intent_training_labels_binarized = self.chat_binarizer.fit_transform(self.intent_training_labels)
            self.chat_binarizer2 = MultiLabelBinarizer()
            topic_training_labels_binarized = self.chat_binarizer2.fit_transform(self.topic_training_labels)

            # make the training data string versions of the part of speech tagged input
            self.training_inputs = [str(pos_tag(word_tokenize(i))) for i in self.training_inputs]

            # convert text into a numerical representation through the use of the "bag of words" technique
            self.vectorizer = CountVectorizer()
            training_vectors = self.vectorizer.fit_transform(self.training_inputs)

            # fit the intent classifer to its training data(use the binarized labels list)
            linear = LinearSVC()
            self.intent_classifier = MultiOutputClassifier(linear, n_jobs=2)
            self.intent_classifier.fit(training_vectors, intent_training_labels_binarized)

            # fit the topic classifer to its training data(use the binarized labels list)
            linear2 = LinearSVC()
            self.topic_classifier = MultiOutputClassifier(linear2, n_jobs=1)
            self.topic_classifier.fit(training_vectors, topic_training_labels_binarized)

            self.inquiry_classifier = LinearSVC()
            # print(training_vectors, "\n", len(self.intent_training_labels), len(self.topic_training_labels), len(self.training_inputs), len(self.inquiry_training_labels))
            self.inquiry_classifier.fit(training_vectors, self.inquiry_training_labels)

            self.is_chat_trained = True

            print("Done")

        else:
            self.is_chat_trained = False
            print("No Data Found")

    def train_memory(self):
        with open(self.memory_training_file, 'r') as fp:
            self.memory_training_data = json.load(fp)

        if self.memory_training_data:
            print("Starting Training")

            self.memory_training_inputs = []
            self.type_training_labels = []
            # self.topic_training_labels = []
            # self.inquiry_training_labels = []

            for item in self.memory_training_data:
                self.memory_training_inputs.append(item["text"])
                self.type_training_labels.append(item["entry-type"])

            # print(self.training_inputs)
            # print(self.type_training_labels)

            # use the MultiLabelBinarizer to convert the labels into a form that can be used for multilabel classification
            self.memory_binarizer = MultiLabelBinarizer()
            binarized_type_labels = self.memory_binarizer.fit_transform(self.type_training_labels)

            # make the training data string versions of the part of speech tagged input
            self.memory_training_inputs = [str(pos_tag(word_tokenize(i))) for i in self.memory_training_inputs]

            # convert text into a numerical representation through the use of the "bag of words" technique
            self.vectorizer = CountVectorizer()
            training_vectors = self.vectorizer.fit_transform(self.memory_training_inputs)

            # fit the intent classifer to its training data(use the binarized labels list)
            linear = LinearSVC()
            self.entry_type_classifier = MultiOutputClassifier(linear, n_jobs=2)
            self.entry_type_classifier.fit(training_vectors, binarized_type_labels)

            self.is_memory_trained = True
            
            print("Done")

        else:
            self.is_memory_trained = False

            print("No Data Found")

    def statement_parser(self, input_string = ""):
        intent_package = {
            "text": input_string,
            "intent": [],
            "topic": []
        }

        if self.is_chat_trained:
            # use POS tagging string
            input_POS_string = str(pos_tag(word_tokenize(input_string)))

            # vectorizer.fit(training_inputs)
            # input_vectors = vectorizer.transform([input_string])

            # use POS tagged string
            input_vectors = self.vectorizer.fit(self.training_inputs).transform([input_POS_string])

            # predict the intent labels(using inverse_transform to turn it from the binary representation back to the original labels)
            intent_package['intent'] = self.chat_binarizer.inverse_transform(self.intent_classifier.predict(input_vectors))[0]
            intent_package['topic'] = self.chat_binarizer2.inverse_transform(self.topic_classifier.predict(input_vectors))[0]

            if "inquiry" in intent_package['intent']:
                intent_package['inquiry-type'] = self.inquiry_classifier.predict(input_vectors)[0]
        
        else:
            print("Chat classifers have not been trained.")

        return intent_package

    def respond(self, input_phrase = "", previous_conversation = []):
        # if any(statement['text'] == input_phrase for statement in self.chatbot_info['input-response-data']):

        input_classification = self.statement_parser(input_phrase)
        
        known_statement = None
        response = random.choice(self.idk_responses)
        # response = {
        #     'text': random.choice(self.idk_responses),
        #     'intent': []
        # }

        for statement in self.chatbot_info['input-response-data']:
            if statement['text'] == input_phrase:
                known_statement = statement
        
        # print(known_statement)
        if known_statement:
            # print(known_statement['responses'])
            if known_statement['responses']:
                # response = {
                #     "text": random.choice(known_statement['responses'])
                # }
                response = random.choice(known_statement['responses'])

        return response

    def UUID(self, length = 8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k = length))

    def memory_parse(self, input_phrase = ""):
        package = {
            "text": input_phrase,
            "entry-type": [],
            "entities": []
        }

        if self.is_memory_trained:
            # use POS tagging string
            input_POS_string = str(pos_tag(word_tokenize(input_phrase)))

            # vectorizer.fit(memory_training_inputs)
            # input_vectors = vectorizer.transform([input_phrase])

            # use POS tagged string
            input_vectors = self.vectorizer.fit(self.memory_training_inputs).transform([input_POS_string])

            # predict the intent labels(using inverse_transform to turn it from the binary representation back to the original labels)
            package['entry-type'] = self.memory_binarizer.inverse_transform(self.entry_type_classifier.predict(input_vectors))[0]

            return package

        else:
            print("Memory classifiers have not been trained.")
            return {}


    def memory_save(self, package = {}):
        templates = {
            "EVENT": {
                "type": "EVENT",
                "time-of-occurrence": "",
                "event-duration": "",
                "involved": [],
                "quotations": []
            },
            "PERSON": {
                "type": "PERSON",
                "full-name": "",
                "nicknames": [],
                "age": 0,
                "date-of-birth": "",
                "likes": "",
                "dislikes": "",
                "appearance": [],
                "traits": [],
                "relationships": {},
                "quotations": []
            },
            "LOCATION": {
                "type": "LOCATION",
                "names": [],
                "position-information": {},
                "relations": {},
                "quotations": []
            },
            "ORGANIZATION": {
                "type": "ORGANIZATION",
                "names": [],
                "organization-type": "",
                "relations": {},
                "quotations": []
            },
            "OBJECT": {
                "type": "OBJECT",
                "names": [],
                "object-type": "",
                "relations": {},
                "properties": {},
                "quotations": []
            },
            "relation": {
                "ID": ["RELATION-TYPE"]
            }
        }

        relations = [
            "sister",
            "friend",
            "assistant",
            "boyfriend",
            "cousin",
            "owner",
            "boss",
            "pet",
            "like",
            "dislike"
        ]

        return None


if __name__ == '__main__':
    bot = intent_chatbot()
    bot.train_chat()
    bot.train_memory()

    print(bot.statement_parser("Hi there!"))
    # print(bot.statement_parser("Hi! I'm doing great."))
    # print(bot.statement_parser("Hello! How are you?"))
    # print(bot.statement_parser("Hey! What are you up to?"))

    # print(bot.respond("Hi there!"))
    # print(bot.respond("Hi! I'm doing great."))
    # print(bot.respond("Hello! How are you?"))
    # print(bot.respond("Hey! What are you up to?"))

    # print(bot.respond(input("> ")))
    # print(bot.statement_parser(input("> ")))

    # print(bot.memory_parse("I'm going to the dentist today."))
    # print(bot.memory_parse("I lost my pen two days ago."))
    # print(bot.memory_parse("I'm gonna go to Walmart later"))
    # print(bot.memory_parse("My name is Allie."))
    # print(bot.memory_parse("His sister's name is Katelyn."))
    # print(bot.memory_parse("We're going to the Grand Canyon."))
    # print(bot.memory_parse("It's kind of like the Grand Canyon."))
    # print(bot.memory_parse("We're going on a trip to Cairo."))
    # print(bot.memory_parse("John is her boyfriend"))
    # print(bot.memory_parse("Elvie just got a scooter."))
    # print(bot.memory_parse("He lost his job at Tesla"))
    # print(bot.memory_parse("I've always wanted to go to Tajikistan."))
    # print(bot.memory_parse("I don't like almonds."))
    # print(bot.memory_parse("Dave just graduated."))
    # print(bot.memory_parse("Edgar Allan Poe was a great poet."))
    # print(bot.memory_parse("Steve likes his steak rare."))
    # print(bot.memory_parse("Arnold Schwarzenegger was the governor of California"))
    # print(bot.memory_parse("You are my assistant."))
    # print(bot.memory_parse(""))

    # print(bot.UUID())

    while True:
        print(bot.statement_parser(input("> ")))
        # print(bot.respond(input("> ")))
        # print(bot.memory_parse(input("> ")))

    # print(bot.chatbot_info)
    # print(bot.chatbot_info['input-response-data'][0])