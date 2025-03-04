from sklearn.svm import LinearSVC
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics import accuracy_score
from nltk import word_tokenize, pos_tag#, Tree, ne_chunk
# import nltk
# import spacy
import json, random, string
import datetime, delorean
import re
# import numpy as np
from os.path import exists
from name_extract import name_extract


class intent_chatbot():
    def __init__(self, data_file = "tests\\NLP\\chatbot\\intent_chatbot-v2\\chat_memory.json", memory_training_file = "tests\\NLP\\chatbot\\intent_chatbot-v2\\memory_train.json", logs_folder = "tests\\NLP\\chatbot\\intent_chatbot-v2\\chatlogs"):
        self.memory_training_file = memory_training_file
        self.data_file = data_file
        self.logs_folder = logs_folder

        self.is_memory_trained = False
        
        # self.lost_responses = [
        #     {"text": "I'm unsure how to respond to that."},
        #     {"text": "I'm sorry, I don't know how to respond to that."},
        #     {"text": "I'm sorry, what?"},
        #     {"text": "Come again?"},
        #     {"text": "I don't know what that means."},
        #     {"text": "I'm afraid I don't understand what you've said."},
        #     {"text": "That sentence makes no sense to me."},
        #     {"text": "I'm sorry?"},
        #     {"text": "I'm lost?"},
        #     {"text": "I'm confused."},
        #     {"text": "Could you please clarify?"},
        #     {"text": "Would you mind restating that?"},
        #     {"text": "I'd be lying, if I said that I knew what that meant."}
        # ]
        self.lost_responses = [
            "I'm unsure how to respond to that.",
            "I'm sorry, I don't know how to respond to that.",
            "I'm sorry, what?",
            "Come again?",
            "I don't know what that means.",
            "I'm afraid I don't understand what you've said.",
            "That sentence makes no sense to me.",
            "I'm sorry?",
            "I'm lost?",
            "I'm confused.",
            "Could you please clarify?",
            "Would you mind restating that?",
            "I'd be lying, if I said that I knew what that meant."
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

    def train_from_chatlog(self, filename = '', chatlog_type = 0):
        print(f"Attempting to train from \"{filename}\"")
        learned_pairs = {}

        if exists(filename):
            with open(filename, 'r') as fp:
                input_chatlog = fp.read().split('\n')

            if chatlog_type == 0:
                for i, item in enumerate(input_chatlog):
                    if ": " in item: # checks if there is a colon in the line
                        input_chatlog[i] = item[item.find(': ') + 2:] # removes the names of the person who is saying something on the current line
                    else: # if there isn't a colon in the line it is left alone
                        input_chatlog[i] = item

                for i, stat in enumerate(input_chatlog):
                    if stat != "": # checks if the current item is just an empty string
                        if not (stat in learned_pairs):
                            learned_pairs[stat] = [] # if the statement is already present in statResp, it doesn't add it(and the reverse is true)
                        if i > 0 and input_chatlog[i - 1] in learned_pairs: # checks if the previous statement is already in the dictionary
                            if not (stat in learned_pairs[input_chatlog[i - 1]]): # checks if the current statement is is the list of responses for the previous statement
                                learned_pairs[input_chatlog[i - 1]].append(stat) # if the previous statement to which the current statement is in response to is present in statResp, it adds this statement as a response for the previous statement

            for key in learned_pairs: # remove duplicates
                learned_pairs[key] = list(dict.fromkeys(learned_pairs[key]))

            # add the pairs to the learned-pairs in the memory
            self.chatbot_info['learned-pairs'] = {**self.chatbot_info['learned-pairs'], **learned_pairs}

            # save the changes to the file
            with open(self.data_file, 'w') as fp:
                json.dump(self.chatbot_info, fp)

            print("Training complete.")
            return learned_pairs

        else:
            print("File not found.")
            return {}

    def train_from_chatlog_folder():
        pass

    def train_memory(self):
        with open(self.memory_training_file, 'r') as fp:
            self.memory_training_data = json.load(fp)

        if self.memory_training_data:
            print("Starting Training")

            self.memory_training_inputs = []
            self.type_training_labels = []

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

    def memory_parse(self, input_phrase = ""):
        package = {
            "text": input_phrase,
            "entry-type": [],
            "entities": []
        }

        if self.is_memory_trained:
            input_words = word_tokenize(input_phrase.lower())
            input_pos = pos_tag(input_words)
            # vectorizer.fit(memory_training_inputs)
            # input_vectors = vectorizer.transform([input_phrase])

            # use POS tagging string
            input_POS_string = str(input_pos)
            input_vectors = self.vectorizer.fit(self.memory_training_inputs).transform([input_POS_string])

            # predict the intent labels(using inverse_transform to turn it from the binary representation back to the original labels)
            package['entry-type'] = self.memory_binarizer.inverse_transform(self.entry_type_classifier.predict(input_vectors))[0]

            if ("I" in input_words) or ("my" in input_words):
                package['entities'].append("SPEAKER")

            if ("You" in input_words) or ("Your" in input_words):
                package['entities'].append("SELF")

            package['entities'].extend(name_extract(input_phrase))

            # return package

        else:
            print("Memory classifiers have not been trained.")
            # return {}

        return package

    def UUID(self, length = 8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k = length))

    def memory_save(self, package = {}):
        pass

    def respond(self, input_phrase = "", common_thres = 0.85, level = "word"):
        output_response = ""
        sorted_pairs = {}
        closest_statement = ''

        # hardcoded pairs(need special formating)
        for key in self.chatbot_info['hardcoded-pairs']:
            formatted_key = str(key)
            
            if "{SLOT" in formatted_key:
                [formatted_key := formatted_key.replace("{SLOT" + str(i + 1) + "}", "") for i in range(4)]
            
            if "|" in formatted_key:
                formatted_key = formatted_key.replace("|", " ")

            if level == "word":
                in_common = list(set(word_tokenize(input_phrase.lower()))&set(word_tokenize(formatted_key.lower())))
                check_length = len(set(word_tokenize(formatted_key))) * common_thres
            elif level == "char":
                in_common = list(set(input_phrase.lower())&set(formatted_key.lower()))
                check_length = len(set(formatted_key.lower())) * common_thres

            if len(in_common) >= check_length:
                sorted_pairs[key] = len(in_common)

        sorted_pairs = {k: v for k, v in sorted(sorted_pairs.items(), key=lambda item: item[1], reverse=True)}

        if bool(sorted_pairs): # if the dictionary isn't empty
            closest_statement = list(sorted_pairs.keys())[0]

        if closest_statement != '':
            given_terms = []
            slot1 = ""
            slot2 = ""
            slot3 = ""
            slot4 = ""

            if "{SLOT" in closest_statement:
                search_pattern = str(closest_statement)

                [search_pattern := search_pattern.replace("{SLOT" + str(i + 1) + "}", "(.*)") for i in range(4)]
                # print(search_pattern)

                extraction = re.findall(search_pattern, input_phrase, re.IGNORECASE)
                # print(extraction)

                if extraction:
                    if type(extraction[0]) == str:
                        given_terms = [i for i in extraction if i]
                    elif (type(extraction[0]) == tuple) or (type(extraction[0]) == list):
                        given_terms = [i for i in extraction[0] if i]
                    # print(given_terms)

                    if len(given_terms) >= 1:
                        slot1 = given_terms[0]

                    if len(given_terms) >= 2:
                        slot2 = given_terms[1]

                    if len(given_terms) >= 3:
                        slot3 = given_terms[2]

                    if len(given_terms) >= 4:
                        slot4 = given_terms[3]

            output_response = random.choice(self.chatbot_info['hardcoded-pairs'][closest_statement]).format(
                self_name = self.chatbot_info['personal-details']['name'],
                self_age = delorean.parse(self.chatbot_info['personal-details']['time-of-creation'], timezone='UTC').humanize()[:-4],
                SLOT1 = slot1,
                SLOT2 = slot2,
                SLOT3 = slot3,
                SLOT4 = slot4
            )

        # learned pairs, checked if it isn't a hardcoded
        if output_response == "":
            sorted_pairs = {}
            closest_statement = ''
            
            for key in self.chatbot_info['learned-pairs']:
                if level == "word":
                    in_common = list(set(word_tokenize(input_phrase.lower()))&set(word_tokenize(key.lower())))
                    check_length = len(set(word_tokenize(key))) * common_thres
                
                elif level == "char":
                    in_common = list(set(input_phrase.lower())&set(key.lower()))
                    check_length = len(set(key.lower())) * common_thres

                if len(in_common) >= check_length:
                    sorted_pairs[key] = len(in_common) # only keeps the statements that have 3/4(the default) or more of their letters/characters in common with the inputed string

            # orders the dictionary by most shared letters to least
            sorted_pairs = {k: v for k, v in sorted(sorted_pairs.items(), key=lambda item: item[1], reverse=True)}

            if bool(sorted_pairs): # if the dictionary isn't empty
                closest_statement = list(sorted_pairs.keys())[0] # take the first statement in the list of ordered pairs
        
            if closest_statement != '':
                if len(self.chatbot_info['learned-pairs'][closest_statement]) > 0:
                    # outputs a random response from the pair's list
                    output_response = random.choice(self.chatbot_info['learned-pairs'][closest_statement])
                
                else:
                    if level == "word":
                        output_response = self.respond(input_phrase, common_thres, level="char")
                    
                    elif level == "char":
                        output_response = random.choice(self.lost_responses)
            
            else:
                if level == "word":
                    output_response = self.respond(input_phrase, common_thres, level="char")
                
                elif level == "char":
                    output_response = random.choice(self.lost_responses)

        return output_response

    # def respond(self, input_phrase = "", common_thres = 0.85, level = "word"):
    #     output_response = ""
    #     closest_statement = ''
    #     sorted_pairs = {}
    #     check_pairs = {**self.chatbot_info['hardcoded-pairs'], **self.chatbot_info['learned-pairs']}

    #     for key in check_pairs:
    #         formatted_key = str(key)
            
    #         slot_num = 4
    #         if "{SLOT" in formatted_key:
    #             [formatted_key := formatted_key.replace("{SLOT" + str(i + 1) + "}", "") for i in range(slot_num)]
            
    #         if "|" in formatted_key:
    #             # formatted_key = formatted_key.split("|")
    #             formatted_key = formatted_key.replace("|", " ")

    #         if level == "word":
    #             in_common = list(set(word_tokenize(input_phrase.lower()))&set(word_tokenize(formatted_key.lower())))
    #             check_length = len(set(word_tokenize(formatted_key)))

    #         elif level == "char":
    #             in_common = list(set(input_phrase.lower())&set(formatted_key.lower()))
    #             check_length = len(set(formatted_key.lower()))

    #         if len(in_common) >= check_length * common_thres:
    #             sorted_pairs[key] = len(in_common)

    #     sorted_pairs = {k: v for k, v in sorted(sorted_pairs.items(), key=lambda item: item[1], reverse=True)}
    #     # print(input_phrase, sorted_pairs.keys(), sorted_pairs.values())

    #     if bool(sorted_pairs): # if the dictionary isn't empty
    #         closest_statement = list(sorted_pairs.keys())[0]

    #     if closest_statement != '':
    #         slot1 = ""
    #         slot2 = ""
    #         slot3 = ""
    #         slot4 = ""

    #         if ("{SLOT" in closest_statement):
    #             given_terms = []

    #             search_pattern = str(closest_statement)

    #             [search_pattern := search_pattern.replace("{SLOT" + str(i + 1) + "}", "(.*)") for i in range(slot_num)]
    #             # print(search_pattern)

    #             extraction = re.findall(search_pattern, input_phrase, re.IGNORECASE)
    #             # print(extraction)

    #             if extraction:
    #                 if type(extraction[0]) == str:
    #                     given_terms = [i for i in extraction if i]
    #                 elif (type(extraction[0]) == tuple) or (type(extraction[0]) == list):
    #                     given_terms = [i for i in extraction[0] if i]
    #                 # print(given_terms)

    #                 if len(given_terms) >= 1:
    #                     slot1 = given_terms[0]

    #                 if len(given_terms) >= 2:
    #                     slot2 = given_terms[1]

    #                 if len(given_terms) >= 3:
    #                     slot3 = given_terms[2]

    #                 if len(given_terms) >= 4:
    #                     slot4 = given_terms[3]

    #         if closest_statement in self.chatbot_info['hardcoded-pairs']:
    #             output_response = random.choice(self.chatbot_info['hardcoded-pairs'][closest_statement]).format(
    #                 self_name = self.chatbot_info['personal-details']['name'],
    #                 self_age = delorean.parse(self.chatbot_info['personal-details']['time-of-creation'], timezone='UTC').humanize()[:-4],
    #                 SLOT1 = slot1,
    #                 SLOT2 = slot2,
    #                 SLOT3 = slot3,
    #                 SLOT4 = slot4
    #             )
            
    #         elif closest_statement in self.chatbot_info['learned-pairs']:
    #             if len(self.chatbot_info['learned-pairs'][closest_statement]) > 0:
    #                 # outputs a random response from the pair's list
    #                 output_response = random.choice(self.chatbot_info['learned-pairs'][closest_statement])
    #         else:
    #             if level == "word":
    #                 output_response = self.respond(input_phrase, common_thres, level="char")
                
    #             elif level == "char":
    #                 output_response = random.choice(self.lost_responses)
        
    #     else:
    #         if level == "word":
    #             output_response = self.respond(input_phrase, common_thres, level="char")
            
    #         elif level == "char":
    #             output_response = random.choice(self.lost_responses)

    #     return output_response

    def start_conversation(self, quit_phrase = "bye"):
        chatlog = []
        continue_conversation = True
        quit_phrase = quit_phrase.lower()

        print('Your conversation starts here.\n')

        while continue_conversation:
            input_phrase = input("> ")
            
            if input_phrase.lower() == quit_phrase:
                continue_conversation = False

            input_significance = self.memory_parse(input_phrase)
            response = self.respond(input_phrase)

            print(input_significance)
            print('Bot: ' + response)

            # add timestamps?
            chatlog.append({"speaker": "USER", "text": input_phrase, "significance": input_significance})
            chatlog.append({"speaker": "BOT", "text": response})

        with open(self.logs_folder + "\\log-" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")), 'w') as fp: # 'logs/2022-01-22_23-37.json'
            json.dump(chatlog, fp)

        return chatlog


if __name__ == '__main__':
    bot = intent_chatbot()
    # bot.train_from_chatlog()
    bot.train_memory()

    # print(bot.respond("Hi there!"))
    # print(bot.respond("Hi! I'm doing great."))
    # print(bot.respond("Hello! How are you?"))
    # print(bot.respond("Hey! What are you up to?"))
    print(bot.respond("My name is Erik"))
    print(bot.respond("What's your name?"))
    print(bot.respond("How old are you?"))
    print(bot.respond("How are you?"))
    print(bot.respond("My birthday is today!"))

    # print(bot.respond_word("Hi there!"))
    # print(bot.respond_word("Hi! I'm doing great."))
    # print(bot.respond_word("Hello! How are you?"))
    # print(bot.respond_word("Hey! What are you up to?"))
    # print(bot.respond_word("My name is Erik"))
    # print(bot.respond_word("What's your name?"))
    # print(bot.respond_word("How old are you?"))
    # print(bot.respond_word("My birthday is today!"))

    # print(bot.respond(input("> ")))

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

    print(bot.start_conversation())

    # while True:
    #     # print(bot.memory_parse(input("> ")))
    #     # print(bot.respond(input("> ")))
    #     # print(bot.respond_word(input("> ")))

    #     user_input = input("> ")
    #     print(bot.memory_parse(user_input))
    #     print(bot.respond(user_input))
    #     # print(bot.respond_word(user_input))

    # print(bot.chatbot_info)