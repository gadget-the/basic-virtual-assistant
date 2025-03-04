from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from nltk import word_tokenize, ne_chunk, pos_tag
from nltk.tree import Tree
import spacy
import re
import json
# import pprint
import smarthouse
import mathParse

training_inputs = []
training_labels = []
training_inputs2 = []
training_labels2 = []

with open('train.json', 'r') as fp:
    training_data = json.load(fp)  # load up the training data from the json file

# sort the data and labels for the main intent classifier
for intent in training_data["intent"]:
    training_inputs.extend(training_data["intent"][intent])
    training_labels.extend([intent] * len(training_data["intent"][intent]))

# sort the data and labels for the secondary intent classifier
for sub_intent in training_data["secondary-intent"]:
    training_inputs2.extend(training_data["secondary-intent"][sub_intent])
    training_labels2.extend([sub_intent] * len(training_data["secondary-intent"][sub_intent]))

training_inputs = [str(pos_tag(word_tokenize(i))) for i in training_inputs] # make the training data string versions of the part of speech tagged input
training_inputs2 = [str(pos_tag(word_tokenize(i))) for i in training_inputs2]
# print(training_inputs[30:35])

# convert text into a numerical representation through the use of the "bag of words" technique?
vectorizer = CountVectorizer()

training_vectors = vectorizer.fit_transform(training_inputs)
training_vectors2 = vectorizer.fit_transform(training_inputs2)

main_intent_classifier = LinearSVC()
# fit the main intent classifer to its training data
main_intent_classifier.fit(training_vectors, training_labels)

secondary_intent_classifier = LinearSVC()
# fit the secondary intent classifer to its training data
secondary_intent_classifier.fit(training_vectors2, training_labels2)

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

def get_location(text, lst = False):
    """ new attempt at making a function that extracts locations from the input """
    if not (text[-1] in ["?", ".", "!"]):
        text += "?"

    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    NER = spacy.load("en_core_web_sm")
    tagged = NER(text)

    named_entities = []

    # use spacy to check for 'GPE'-type named entities
    for word in tagged.ents:
        if str(word.label_) == 'GPE':
            named_entities.append(word.text)
    
    # use nltk to check for 'GPE'-type named entities
    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == 'GPE':
            named_entities.extend([t[0] for t in subtree.leaves()])

    # more in-depth way of removing duplicates, while preserving the order of the list
    named_entities.reverse()
    for i, x in enumerate(named_entities):
        m = list(named_entities)
        m.remove(x)
        if any(x.lower() in word_tokenize(y.lower()) for y in m):
            named_entities[i] = ""
    named_entities.reverse()
    named_entities = [i for i in named_entities if i]

    if named_entities:
        if lst:
            return named_entities
        else:
            return ", ".join(named_entities)
    else:
        return None

def remove_all(lst = [], to_remove = []):
    return [x for x in lst if not x in to_remove]

def get_time_info(input_string = ""):
    ''' outputs a dictionary of time related info based on the input '''
    # input_string = str(input_string).lower()
    input_string = mathParse.parser(input_string.lower())
    # print(input_string)
    words = word_tokenize(input_string)
    words = remove_all(words, ["st", "nd", "rd", "th"])
    # print(words)
    # time_of_day = ["am", "pm", "a.m.", "p.m.", "a.m", "p.m", "o'clock", "oclock"] # problems with the word "am"
    time_of_day = ["a.m.", "p.m.", "a.m", "p.m", "o'clock", "oclock"]
    day_words = ["yesterday", "today", "tomorrow", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "next week", "this week", "last week"]
    time_units = ["year", "month", "week", "day", "hour", "minute", "second"]
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    timing_is_set = False
    timing = {}

    # check for a time of the day(i.e. "8 a.m", "5 o'clock")
    for d in time_of_day:
        if d in input_string:
            for i, n in enumerate(words):
                if d == n:
                    # print(d)
                    timing_is_set = True
                    timing['elapsed'] = False # specify that it is a specific time at which to do the thing
                    if words[i - 1].replace(":", "").isdigit(): # 8:30 --> 830
                        timing['oClock'] = words[i - 1]
                        if not (d in ["o'clock", "oclock"]):
                            if "p" in d:
                                timing['timeOfDay'] = 'pm'
                            else:
                                timing['timeOfDay'] = 'am'
                        # if "p" in d: # convert to 24-hour clock
                        #     timing['oClock'] = int(words[i - 1]) + 12
                        # else:
                        #     timing['oClock'] = int(words[i - 1])
                    break

    if not ('oClock' in timing):
        for i in words:
            # if ":" in i:
            if len([x for x in i.split(":") if x]) == 2: # "8:30" = YES, "this:" == NO
                timing_is_set = True

                timing['elapsed'] = False
                timing['oClock'] = i
                timing['timeOfDay'] = None
                break

    # check for a day/day range?(i.e. "tomorrow", "today", "next week")
    # for t in day_words:
    #     if t in input_string:
    #         for i, n in enumerate(words):
    #             if t == n:
    #             # if t in n: # today --> todays
    #                 timing_is_set = True
    #                 timing['elapsed'] = False
    #                 timing['time'] = t
    #                 break

    for t in day_words:
        if t in input_string:
            timing_is_set = True
            timing['elapsed'] = False
            timing['time'] = t
            break

    # check for specified date
    # formatted dates like 12/27/2018 and 27/12/2018
    for word in words:
        # print(word, word.count("/"), word.replace('/', '').isdigit())
        if word.count("/") == 2 and word.replace('/', '').isdigit():
            timing_is_set = True

            date = {}
            date['formatted-date'] = word

            timing['date'] = date
            break

    # dates like 27 of December, 2018 and December 27th, 2018
    if not ('date' in timing):
        for month in months:
            if month in input_string:
                timing_is_set = True
                timing['elapsed'] = False

                date = {}
                date['month'] = month

                for i, word in enumerate(words):
                    # print(word)
                    if word.isdigit():
                    # if n.isdigit() or n.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").isdigit():
                        if i > 0:
                            if words[i - 1] == month:
                                if len(word) == 4:
                                    date['year'] = word
                                else:
                                    date['day'] = word
                            elif 'day' in date and words[i - 1] == date['day']:
                                if len(word) == 4:
                                    date['year'] = word
                            elif words[i + 1] == 'of' and words[i + 2] == month:
                                date['day'] = word

                timing['date'] = date
                break

    # if timing is still not set, check for a specific time to pass
    if not timing:
        timing['elapsed'] = True # specify that it is an amount of time that must elapse before the thing is to happen
        for unit in time_units:
            if unit in input_string:
                for i, word in enumerate(words):
                    if unit in word:
                        timing_is_set = True
                        if words[i - 1].isdigit():
                            timing[unit + "s"] = int(words[i - 1])
                        elif words[i - 1] == "an" or words[i - 1] == "a":
                            timing[unit + "s"] = 1
                        else:
                            timing[unit + "s"] = 0
            else:
                timing[unit + "s"] = 0
            
    # return timing
    return timing if timing_is_set else None # probably not a good way to do this

def intNEnt(input_string = "", last_classification = {}): # function that labels an input with its intent and sub-intent, as well as its specified "values"
    # input_string = mathParse.parser(input_string)
    input_POS_string = str(pos_tag(word_tokenize(input_string))) # use POS tagging

    # use the training data for each respective intent(main and sub) to fit the vectorizers and then transform the input
    # vectorizer.fit(training_inputs)
    # vectors = vectorizer.transform([input_string])
    # use POS tagging
    main_intent_vectors = vectorizer.fit(training_inputs).transform([input_POS_string])

    # predict the main intent label
    intent = main_intent_classifier.predict(main_intent_vectors)[0]

    # vectorizer.fit(training_inputs2)
    # secondary_intent_vectors = vectorizer.transform([input_string])
    # use POS tagging
    secondary_intent_vectors = vectorizer.fit(training_inputs2).transform([input_POS_string])

    # predict the secondary intent label
    sub_intent = secondary_intent_classifier.predict(secondary_intent_vectors)[0]

    # makes the "None" label an actual None
    sub_intent = None if sub_intent == 'None' else sub_intent

    classification = {"intent": intent, "secondary-intent": sub_intent}

    # input_string = mathParse.parser(input_string)

    timing = None

    if intent == "search":  # extract the search engine, if specified, and the searched term
        if sub_intent == "web-search":
            search_engine, search_term, _ = search_pattern_matching(input_string = input_string.lower())

            classification["engine"] = search_engine # use the extracted search engine(or none if one's not found)

            if search_term: # if a search (engine and) term is found, use them. else use the whole input as the search term
                classification["term"] = search_term
            else:
                classification["term"] = input_string.lower()
                
        elif sub_intent == "search-definition":
            # need to make a regex pattern for extracting the specified word(s)
            # "what is google"
            # "define feudalism"
            # "give me the definition of empathy"
            # "what does verbatim mean?"
            # "can you tell me what tantamount means?",
            # "what's the definition of the word kinetic?"
            # "what's a smarthouse"

            definition_pattern = r"(what's a )(.+)|(what's an )(.+)|(what is a )(.+)|(what is an )(.+)|(what's)(.+)|(what is )(.+)|(define )(.+)|(definition of )(.+)|(what does )(.+)( mean)|(what )(.+)( means)|(definition of the word )(.+)"
            definition_delimiters = [
                "what's a ",
                "what's an ",
                "what is a ",
                "what is an ",
                "what's",
                "what is ",
                "define ",
                "definition of ",
                "what does ",
                " mean",
                "what ",
                " means",
                "definition of the word "
            ]
            extraction = re.findall(definition_pattern, input_string.lower(), re.IGNORECASE)
            # print(extraction)

            if extraction:
                term = [i for i in extraction[0] if i and not (i in definition_delimiters)][0]
                # print(extracted_words)
            
            # classification["term"] = term if term else None
            classification["term"] = re.sub(r'[^\w\s]', '', term) if term else None
            
    elif intent == "funfact":
        fact_subject = None
        # words = word_tokenize(input_string.lower())
        words = word_tokenize(re.sub(r'[^\w\s]', '', input_string.lower())) # word level tokenized version of the input in lowercase with the punctuation stripped
        for i, word in enumerate(words):
            if "about" in words: # if the word "about" is in the words, check for it and take all the words that follow
                if word == "about":
                    fact_subject = " ".join(words[i + 1:])
                    break

            else:
                if (word in ["fact", "facts", "funfact", "funfacts"]) and (not (words[i - 1] in ["random", "fun", "a"])): # if "about" isn't in the input, take the words that precede other delimiter words
                    fact_subject = " ".join(words[:i])
                    break

        classification["subject"] = fact_subject
        
    elif intent == "random":
        rolls = 1

        word_to_digits = mathParse.parser(input_string, op=False)
        word_list = word_tokenize(word_to_digits)

        if sub_intent == "random-number":
            low = None
            high = None

            for i, word in enumerate(word_list):
                if word.isdigit() or word[0] == '-': # might want to do something different for checking negatives
                # if any(l.isdigit() for l in word):
                    if word_list[i - 1] == "between":
                        low = int(word)

                    elif word_list[i - 1] == "and":
                        high = int(word)

                    elif word_list[i + 1] == "random": # might want to do something different for this
                        rolls = int(word)

            classification['low'] = low
            classification['high'] = high

        elif sub_intent == "random-dice":
            sides = None

            for i, word in enumerate(word_list):
                if word.isdigit():
                    if word_list[i + 1] == "sided" or word_list[i + 1] == "side":
                        sides = int(word)
                        
                    elif word_list[i + 1] in ["dice", "die", "time", "times"]:
                        rolls = int(word)
                        
                elif word == "once":
                    rolls = 1
                    
                elif word == "twice":
                    rolls = 2

            classification['sides'] = sides

        elif sub_intent == "random-coin":
            for i, word in enumerate(word_list):
                if word.isdigit():
                    if word_list[i + 1] in ["coins", "coin", "time", "times"]:
                        rolls = int(word)
                        
                elif word == "once":
                    rolls = 1
                    
                elif word == "twice":
                    rolls = 2

        classification['rolls'] = rolls

    elif intent == "music":
        term = input_string
        if sub_intent == "music-play-song":
            for i in ["play some ", "put on some ", "play ", "put on "]: # check for and remove delimiters
                if i in input_string.lower():
                    # term = input_string.replace(i, "")
                    term = input_string[input_string.lower().index(i) + len(i):] # takes the rest of the string following the keyword
                    break

        elif sub_intent == "music-get-lyrics":
            for i in ["lyrics of ", "lyrics to ", "lyrics for ", "words of ", "lyrics to ", "words for "]: # another delimiter check
                if i in input_string.lower():
                    term = input_string[input_string.lower().index(i) + len(i):]
                    break

            if not term: # if term hasn't been set, try checking for and removing the possible 'end delimiter'
                if " lyrics" in input_string.lower():
                    term = input_string[:input_string.lower().index(" lyrics")]

        classification["term"] = term

    elif intent == "help": # use the classification of the last input "do that again"
        term = None
        input_string = input_string.lower()
        if input_string != "help": # if it's not a simple "help", look for a specified term that the user might be asking about
            # check for delimiters
            for i in ["how do I use the ", "how do I use ", "help with the ", "help me with the ", "help with ", "help me with ", "how does ", "what does the ", "what does "]:
                if i in input_string:
                    # term = input_string[input_string.index(i) + len(i):]
                    term = word_tokenize(input_string[input_string.index(i) + len(i):])[0]
                    break
            
            if not term:
                words = word_tokenize(input_string)
                for i, n in enumerate(words):
                    if n == "help":
                        term = words[i + 1]
                        break

                    elif n in ["command", "function", "ability", "skill"]:
                        term = words[i - 1]
                        break

        classification["term"] = term

    elif intent == "assistant-settings" and not (sub_intent in ["assistant-restart", "assistant-hard-restart", "assistant-shutdown"]):
        if sub_intent == "assistant-theme-change" or sub_intent == "assistant-add-wake-word" or sub_intent == "assistant-remove-wake-word":
            quotation_pattern = r"(\"|')(.*)(\"|')" # "<anything>" or '<anything>'(unintentionally "<anything>' and '<anything>")
            extraction = re.findall(quotation_pattern, input_string, re.IGNORECASE)
            # print(extraction)

            if extraction:
                term = [i for i in extraction[0] if i and i != "'" and i != '"'][0]
                # print(extracted_words)
            
            classification["term"] = term if term else None
        
        elif sub_intent == "assistant-volume-change":
            input_string = input_string.lower()
            sign = 1
            specified_value = 0
            change_by_value = False

            if "raise" in input_string or " up" in input_string or "increase" in input_string:
                change_by_value = True

            elif "lower" in input_string or " down" in input_string or "decrease" in input_string:
                change_by_value = True
                sign = -1

            if "full" in input_string or "max" in input_string:
                specified_value = 100

            elif "mute" in input_string:
                specified_value = 0

            elif "a bit" in input_string:
                specified_value = 10

            elif "a small bit" in input_string or "a little bit" in input_string:
                specified_value = 5

            else:
                percentage_pattern = r"(\d*(?= percent|%))" # "20%" or "49 percent"
                # extraction = re.findall(percentage_pattern, input_string.lower(), re.IGNORECASE)
                extraction = re.findall(percentage_pattern, mathParse.parser(input_string, op=False), re.IGNORECASE)

                if extraction:
                    # print([i for i in extraction if i])
                    specified_value = int([i for i in extraction if i][0])

            classification["specified-value"] = specified_value * sign
            classification["change-by-value"] = change_by_value

    elif intent == "simon-says":
        term = None
        # print(count_occurances(input_string, "'"))
        # print(count_occurances(input_string, "\""))

        # if ("\"" in input_string):
        # if ("\"" in input_string) or ("'" in input_string):
        if (count_occurances(input_string, "'") >= 2) or (count_occurances(input_string, "\"") >= 2):
            simon_pattern = r"(\")(.*)(\")|(')(.*)(')"

            extraction = re.findall(simon_pattern, input_string, re.IGNORECASE)
            # print(extraction)

            if extraction:
                term = [i for i in extraction[0] if i and i != "'" and i != '"'][0]
                # print(extracted_words)
        else:
            simon_pattern = r"(repeat after me )(.+)|(simon says )(.+)|(repeat after me, )(.+)|(say )(.+)|(tts )(.+)|(text-to-speech )(.+)|(text to speech )(.+)|(repeat: )(.+)|(repeat, )(.+)|(repeat )(.+)|(say, )(.+)|(.+)(using tts)|(.+)(using text to speech)|(.+)(using text-to-speech)"
            simon_delimiters = [
                "repeat after me ",
                "repeat after me, ",
                "simon says ",
                "say ",
                "say, ",
                "tts ",
                "text-to-speech ",
                "text to speech ",
                "repeat: ",
                "repeat, ",
                "repeat ",
                " using text-to-speech",
                " using text to speech",
                " using tts"
            ]

            extraction = re.findall(simon_pattern, input_string, re.IGNORECASE)
            # print(extraction)

            if extraction:
                term = [i for i in extraction[0] if i and not i in simon_delimiters][0]
                # print(extracted_words)

        classification["phrase"] = term if term else None

    # elif intent == "repeat":
    #     pass

    elif intent == "use-last-input": # use the classification of the last input "do that again"
        if last_classification:
            classification = last_classification

    else: # the user's input might have a time based request
        # extract timing requirements
        timing = get_time_info(input_string)

        if intent == "smarthouse":
            # extract the specified room, appliance, state and possibly value
            # if input_string[-1] == "?":
            #     input_string = input_string[:-1]

            room = ""
            appliance = ""
            state = ""
            value = None

            if sub_intent == "smarthouse-check-state":
                room, appliance, state = smarthouse.checkInput(input_string, True)

            elif sub_intent == "smarthouse-change-state":
                # print(smarthouse.checkInput(input_string, False))
                room, appliance, state, value = smarthouse.checkInput(input_string, False)

            classification["room"] = room
            classification["appliance"] = appliance
            classification["state"] = state
            classification["value"] = value
                
        elif intent == "run-program": # extract the program name
            common_name = None
            program_name = None

            for i in ["open ", "start up ", "start "]:
                if i in input_string.lower():
                    if timing:
                        if " at" in input_string:
                            common_name = input_string[input_string.lower().index(i) + len(i):input_string.lower().index(" at")]
                        
                        elif " in" in input_string:
                            common_name = input_string[input_string.lower().index(i) + len(i):input_string.lower().index(" in")]
                    
                    else:
                        common_name = input_string[input_string.lower().index(i) + len(i):]
                    
                    break

            program_name = lookUp(common_name)

            classification["common-name"] = common_name
            classification["program"] = program_name

        elif intent == "open_site":  # extract the specified url and browser
            site = None
            brow = None
            common_name = None

            brws = ["firefox", "chrome", "opera", "edge"]

            for i in brws: # check if one of the supported browsers has been mentioned. if so, set the browser to be used to that browser
                if i in input_string.lower():
                    brow = i
                    break
            
            for i in ["open ", "go to ", " opening "]:
                if i in input_string.lower():
                    if brow:
                        common_name = input_string[input_string.lower().index(i) + len(i):input_string.lower().index(" in")] # "open <url> in <browser>"
                    
                    else:
                        common_name = input_string[input_string.lower().index(i) + len(i):] # "would you mind opening <url>"
                    
                    break

            domain_list = [".com", ".net", ".gov", ".tv", ".org", ".xyz", ".ru", ".jp", ".eu"]
            
            website_pattern = fr'(https://?|http://?)(www.?)(\S*?)({"?|".join(domain_list) + "?"})(/\S*)'
            # website_pattern = r"(https://?|http://?)(www.?)(\S*?)(.com?|.net?|.org?|.gov?|.edu?)(/\S*)"
            contains_url = re.search(website_pattern, input_string, re.IGNORECASE)
            # contains_url = re.search(website_pattern, common_name, re.IGNORECASE)

            # if re.search(website_pattern, input_string, re.IGNORECASE):
            #     print("input contains a url")

            site = common_name if contains_url else lookUp(input_string.lower(), "site") # if there isn't a url in the input, use the look up table to see if the user mentioned any known websites "go to the youtube website"
            
            if not site: # if the look up table didn't return anything, just use the common name for the website
                site = common_name.replace("the ", "").replace(" website", "").replace(" site", "").replace(" webpage", "").lower().replace(" ", "")
                if site:
                    if not ("www" in site):
                        site = "www." + site

                    if not ("http" in site):
                        site = "https://" + site

                    # if not any(i in site for i in [".com", ".net", ".gov", ".tv", ".org", ".xyz", ".ru", ".jp", ".eu"]):
                    if not any(i in site for i in domain_list):
                        site += ".com/"

                else: # if we cannot use the common name for the website for whatever reason, just output example.com(to avoid breaking something)
                    site = "http://www.example.com/"
                
            classification["common-name"] = common_name
            classification["website"] = site
            classification["browser"] = brow

        elif intent == "weather": # extract the location for the weather request
            given_location = None
            given_location = get_location(input_string)

            classification["location"] = given_location

        elif intent == "time":
            possible_units = ["year", "month", "week", "day", "hour", "minute", "second"]

            if sub_intent == "timeTil" or sub_intent == "time-start-timer":
                given_units = []

                for i in possible_units:
                    if i in input_string.lower():
                        given_units.append(i + "s")

                if sub_intent == "timeTil":
                    given_units = given_units if given_units else ["seconds"]

                elif sub_intent == "time-start-timer":
                    timer_message = ""
                    given_units = given_units if given_units else ["seconds"]

                    timer_message = str(input_string)
                    words = word_tokenize(input_string)
                    for i, word in enumerate(words):
                        if word in possible_units or word[:-1] in possible_units:
                            timer_message = timer_message[timer_message.index(word) + len(word) + 1:]

                    classification['message'] = timer_message

                classification['units'] = given_units
                
            elif sub_intent == "time-get-date":
                possible_units.reverse() # a bit of a weird way to do this?
                given_units = []

                for i in possible_units:
                    # if i in input_string.lower():
                    # if i in word_tokenize(input_string.lower()):
                    if any(i == x or i + "s" == x for x in word_tokenize(input_string.lower())):
                        given_units.append(i)

                classification['units'] = given_units

            elif sub_intent == "time-check-timer" or sub_intent == "time-end-timer":
                timer_term = None
                timer_ID = None

                if any(n in input_string.lower() for n in ["all timers", "every timer", "each timer", "all of my timers", "all of the timers", "all the timers"]):
                    timer_ID = "all"

                else:
                    for w in word_tokenize(input_string): # check for a 'word' that contains both letters and numbers(like "ykt9epgd")
                        if any(x.isalpha() for x in w) and any(x.isdigit() for x in w):
                            timer_ID = w

                    if not timer_ID: # if we didn't find a 'word' for the timerID that meets the previous requirements, check for a "specified term"
                        input_string = input_string.lower()
                        words = word_tokenize(input_string)
                        if sub_intent == "time-end-timer":
                            for i, n in enumerate(words):
                                if n == "timer":
                                    if i < len(words) - 1 and words[i + 1] == "for":
                                        timer_term = input_string[input_string.index("for ") + 4:]

                                    else:
                                        for d in ["stop my ", "stop the ", "end the ", "end my ", "stop ", "end"]:
                                            if d in input_string:
                                                timer_term = input_string[input_string.index(d) + len(d):input_string.index(" timer")]
                                                break
                                            
                        elif sub_intent == "time-check-timer":
                            if "on my " in input_string:
                                timer_term = input_string[input_string.index("on my ") + 6:input_string.index(" timer")]
                            
                            elif "on the " in input_string:
                                timer_term = input_string[input_string.index("on the ") + 7:input_string.index(" timer")]
                        
                classification['IDTerm'] = timer_term
                classification['ID'] = timer_ID

    classification["timing"] = timing if not "timing" in classification else classification["timing"]

    return classification

def lookUp(name = "", lookup_type = "file"):
    with open('lookUp.json', 'r') as fp:
        reference_file = json.load(fp)

    for location in reference_file[lookup_type]:
        if location in name.lower():
            return location
        else:
            for common_name in reference_file[lookup_type][location]:
                if common_name in name.lower():
                    return location

    return None

def search_pattern_matching(input_string, search_engines = ["google", "bing", "yandex", "yahoo", "baidu"]):
    engine_term_pattern = fr'({"|".join(search_engines)}) search for (.+)|({"|".join(search_engines)}) search (.+)|search on ({"|".join(search_engines)}) (.+)|search ({"|".join(search_engines)}) for (.+)|search for (.+) on ({"|".join(search_engines)})|search (.+) on ({"|".join(search_engines)})|search for (.+)|search (.+)'
    extraction = re.findall(engine_term_pattern, input_string.lower(), re.IGNORECASE)
    # print(extraction)

    extracted_words = []
    extracted_engine = None
    extracted_term = None

    if extraction:
        extracted_words = [i for i in extraction[0] if i]
        [extracted_engine := i for i in extracted_words if i in search_engines]
        [extracted_term := i for i in extracted_words if not i in search_engines]
        # print(extracted_words, extracted_engine, extracted_term)

    return extracted_engine, extracted_term, extracted_words

def count_occurances(input_string, search_char):
    count = 0

    for i in range(len(input_string)):
        if input_string[i] == search_char:
            count += 1

    return count

def trainDataCont():
    for i in training_data["intent"]:
        print(i, len(training_data["intent"][i]))
    print("")
    for i in training_data["secondary-intent"]:
        print(i, len(training_data["secondary-intent"][i]))
    print("")

def showAccuracy(display_num = None):
    test_inputs_start = [
        "8 + 4",
        "turn on the heater in the living room",
        "what is the weather like in Redmond, Washington",
        "what are you up to",
        "open the garage",
        "ten squared",
        "what is the capital of Alaska",
        "two plus two",
        "what is 48 + 32",
        "where is timbuktu?",
        "how to change a tire",
        "please open the garage door",
        "weather in Palo Alto",
        "places with the best weather",
        "dim the lights in the living room",
        "open steam",
        "go to bing.com",
        "what time is it?",
        "is the light on in the garage",
        "weather forecast for the next week",
        "search for rash causes",
        "what is 100 - 60?",
        "twenty divided by 2",
        "weather in Timbuktu for the next week",
        "temperature in Palo Alto",
        "how can you help me?",
        "tell me a fact about the ocean",
        "play some Michael Jackson",
        "random number between fifty and one hundred",
        "again",
        "what is two plus two",
        "what is 2 + 2?",
        "search on yahoo facts about the brain",
        "roll a 100 sided die",
        "what are your functions?",
        "do you know any music facts?",
        "perform a full restart, please",
        "change to the theme \"Campfire\"",
        "please reenable text-to-speech",
        "simon says paranoia",
        "repeat after me \"it's a turnip\"",
        "say that again, please",
        "could you run that by me again?",
        "define empathy",
        "what is a cornucopia?",
        "I met this guy simon",
        "I told him to repeat what he said.",
    ]

    test_inputs = [str(pos_tag(word_tokenize(m))) for m in test_inputs_start]# use POS tagging
    test_labels = [
        "math",
        "smarthouse",
        "weather",
        "conversational",
        "smarthouse",
        "math",
        "search",
        "math",
        "math",
        "search",
        "search",
        "smarthouse",
        "weather",
        "search",
        "smarthouse",
        "run-program",
        "open_site",
        "time",
        "smarthouse",
        "weather",
        "search",
        "math",
        "math",
        "weather",
        "weather",
        "help",
        "funfact",
        "music",
        "random",
        "use-last-input",
        "math",
        "math",
        "search",
        "random",
        "help",
        "funfact",
        "assistant-settings",
        "assistant-settings",
        "assistant-settings",
        "simon-says",
        "simon-says",
        "repeat",
        "repeat",
        "search",
        "search",
        "conversational",
        "conversational",
    ]
    print(len(test_inputs_start), len(test_labels))

    # testing_vectors = vectorizer.transform(test_inputs)
    test_vectors = vectorizer.fit(training_inputs).transform(test_inputs)
    predictions = main_intent_classifier.predict(test_vectors)

    test_vectors = vectorizer.transform(test_inputs)

    test_vectors = vectorizer.fit(training_inputs2).transform(test_inputs)
    predictions2 = secondary_intent_classifier.predict(test_vectors)

    # find out the accuracy of the main intent classifier
    accuracy = accuracy_score(test_labels, predictions)

    if not display_num:
        display_num = len(predictions)

    # print information about the predictions and correct labels for the testing data(main intent)
    for pred, pred2, input_string, lbl in zip(predictions[:display_num], predictions2[:display_num], test_inputs_start[:display_num], test_labels[:display_num]):
        if pred != lbl:
            m = "X"
        else:
            m = "O"
        print(m, "-", input_string, "\n\tIntent:", pred, "<->", lbl, "\n\tSub-Intent:", pred2)

    # print out the accuracy of the main intent classifier
    print("{:.2%} Accuracy".format(accuracy))


if __name__ == "__main__":
    trainDataCont()

    showAccuracy(15)
    # showAccuracy()

    # print(lookUp("open mspaint", "file"))
    # print(lookUp("open the youtube site", "site"))

    # print(get_location("how's the weather in Atlanta, Georgia"))
    # print(get_location("how's the weather in Palo Alto"))
    # print(get_location("how's the weather in San Marino, California, USA"))
    # print(get_location("how's the weather in San Marino, California, United States"))
    # print(get_location("how's the weather in Fukuoka, Japan"))
    # print(get_location("how's the weather in atlanta, georgia"))
    # print(get_location("how's the weather in palo alto"))
    # print(get_location("how's the weather in san marino, california, united states"))
    # print(get_location("how's the weather in fukuoka, japan"))

    # test = "This is a test, my dude."
    # test = word_tokenize(test)
    # testBack = list(test)
    # testBack.reverse()
    # # print(testBack)
    # for f, b in zip(test, testBack):
    #     print(f, b)

    # print(get_time_info("how many days until 12/27/2018?"))
    # print(get_time_info("how many days until 27 of December, 2018?"))


    # print(search_pattern_matching("search on google pizza recipes"))
    # print(search_pattern_matching("search for pizza recipes"))

    # search_engines = ["google", "bing", "yandex", "yahoo", "baidu"]

    # engine_term_pattern = r'(\w+?) search for (.+)|(\w+?) search (.+)|search on (\w+?) (.+)|search (\w+?) for (.+)|search for (.+) on (\w+)|search (.+) on (\w+)'
    # engine_term_pattern = r'(google|yahoo|yandex) search for (.+)|(google|yahoo|yandex) search (.+)|search on (google|yahoo|yandex) (.+)|search (google|yahoo|yandex) for (.+)|search for (.+) on (google|yahoo|yandex)|search (.+) on (google|yahoo|yandex)'
    # engine_term_pattern = rf'({"|".join(search_engines)}) search for (.+)|({"|".join(search_engines)}) search (.+)|search on ({"|".join(search_engines)}) (.+)|search ({"|".join(search_engines)}) for (.+)|search for (.+) on ({"|".join(search_engines)})|search (.+) on ({"|".join(search_engines)})'
    # print(engine_term_pattern)
    # print(re.search(engine_term_pattern, "google search for pizza recipes", re.IGNORECASE).group())
    # # print(re.split(engine_term_pattern, "google search for pizza recipes", re.IGNORECASE))
    # print(re.findall(engine_term_pattern, "google search for pizza recipes", re.IGNORECASE))
    # # print(re.search(engine_term_pattern, "google search for pizza recipes", re.IGNORECASE).group(1))
    # # print(re.search(engine_term_pattern, "google search for pizza recipes", re.IGNORECASE).group(2))
    # print("\n")
    # print(re.search(engine_term_pattern, "google search pizza recipes", re.IGNORECASE).group())
    # # print(re.split(engine_term_pattern, "google search pizza recipes", re.IGNORECASE))
    # print(re.findall(engine_term_pattern, "google search pizza recipes", re.IGNORECASE))
    # # print(re.search(engine_term_pattern, "google search pizza recipes", re.IGNORECASE).group(3))
    # # print(re.search(engine_term_pattern, "google search pizza recipes", re.IGNORECASE).group(4))
    # print("\n")
    # print(re.search(engine_term_pattern, "search on google pizza recipes", re.IGNORECASE).group())
    # # print(re.split(engine_term_pattern, "search on google pizza recipes", re.IGNORECASE))
    # print(re.findall(engine_term_pattern, "search on google pizza recipes", re.IGNORECASE))
    # # print(re.search(engine_term_pattern, "search on google pizza recipes", re.IGNORECASE).group(5))
    # # print(re.search(engine_term_pattern, "search on google pizza recipes", re.IGNORECASE).group(6))
    # print("\n")
    # print(re.search(engine_term_pattern, "search google for pizza recipes", re.IGNORECASE).group())
    # # print(re.split(engine_term_pattern, "search google for pizza recipes", re.IGNORECASE))
    # print(re.findall(engine_term_pattern, "search google for pizza recipes", re.IGNORECASE))
    # # print(re.search(engine_term_pattern, "search google for pizza recipes", re.IGNORECASE).group(7))
    # # print(re.search(engine_term_pattern, "search google for pizza recipes", re.IGNORECASE).group(8))
    # print("\n")
    # print(re.search(engine_term_pattern, "search for pizza recipes on google", re.IGNORECASE).group())
    # # print(re.split(engine_term_pattern, "search for pizza recipes on google", re.IGNORECASE))
    # print(re.findall(engine_term_pattern, "search for pizza recipes on google", re.IGNORECASE))
    # # print(re.search(engine_term_pattern, "search for pizza recipes on google", re.IGNORECASE).group(9))
    # # print(re.search(engine_term_pattern, "search for pizza recipes on google", re.IGNORECASE).group(10))
    # print("\n")
    # print(re.search(engine_term_pattern, "search pizza recipes on google", re.IGNORECASE).group())
    # # print(re.split(engine_term_pattern, "search pizza recipes on google", re.IGNORECASE))
    # print(re.findall(engine_term_pattern, "search pizza recipes on google", re.IGNORECASE))
    # # print(re.search(engine_term_pattern, "search pizza recipes on google", re.IGNORECASE).group(11))
    # # print(re.search(engine_term_pattern, "search pizza recipes on google", re.IGNORECASE).group(12))
    # extracted_words = [i for i in re.findall(engine_term_pattern, "search pizza recipes on google", re.IGNORECASE)[0] if i]
    # extracted_engine = None
    # [extracted_engine := i for i in extracted_words if i in search_engines]
    # extracted_term = None
    # [extracted_term := i for i in extracted_words if not i in search_engines]
    # print(extracted_words, extracted_engine, extracted_term)

    # website_pattern = r"(https://?|http://?)(www.?)(\S*?)(.com?|.net?|.org?|.gov?|.edu?)(/\S*)"
    # website_pattern = "(https:\/\/?|http:\/\/?)(www\.*)(\S*?)(\.com?|\.net?|\.org?|\.gov?|\.edu?)(\/\S*)"

    # print(re.findall(website_pattern, "http://www.columbia.edu/~fdc/sample.html", re.IGNORECASE))
    # print(re.findall(website_pattern, "https://www.instagram.com/domtomato/", re.IGNORECASE))
    # print(re.findall(website_pattern, "https://www.minecraft.net/en-us", re.IGNORECASE))
    # print(re.findall(website_pattern, "https://www.amazon.com/", re.IGNORECASE))
    # print(re.findall(website_pattern, "https://www.google.com/", re.IGNORECASE))
    # print(re.findall(website_pattern, "https://www.google.com/search?client=firefox-b-1-d&q=pizza+places+near+me", re.IGNORECASE))
    # print(re.findall(website_pattern, "https://www.youtube.com/watch?v=l8iiC06coNE&list=TLPQMjYwNTIwMjIO3GLMpBtuoA&index=27", re.IGNORECASE))
    
    # print(re.search(website_pattern, "please open http://www.columbia.edu/~fdc/sample.html", re.IGNORECASE))
    # print(re.search(website_pattern, "go to https://www.instagram.com/domtomato/", re.IGNORECASE))
    # print(re.search(website_pattern, "open https://www.minecraft.net/en-us in google chrome", re.IGNORECASE))
    # print(re.search(website_pattern, "https://www.amazon.com/", re.IGNORECASE))
    # print(re.search(website_pattern, "please open https://www.google.com/ in edge", re.IGNORECASE))
    # print(re.search(website_pattern, "open the url https://www.google.com/search?client=firefox-b-1-d&q=pizza+places+near+me", re.IGNORECASE))
    # print(re.search(website_pattern, "please open the url https://www.youtube.com/watch?v=l8iiC06coNE&list=TLPQMjYwNTIwMjIO3GLMpBtuoA&index=27", re.IGNORECASE))
    # print(re.search(website_pattern, "open discord", re.IGNORECASE))
    # print(re.search(website_pattern, "open the youtube website", re.IGNORECASE))
    # print(re.search(website_pattern, "start up edge", re.IGNORECASE))

    # website_pattern = r"(https://?|http://?)(www.?)(\S*?)(.com?|.net?|.org?|.gov?|.edu?)(/\S*)"
    # print(re.search(website_pattern, "start up edge", re.IGNORECASE))

    
    # print(intNEnt("remind me to feed the cats in eight hours and five minutes"))
    while True:
        t = intNEnt(input("> "))
        print(t)
        # print(t, bool(t['timing']))
        # pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)
        # pp.pprint(intNEnt(input("> ")))