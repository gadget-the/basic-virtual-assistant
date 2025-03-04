# from sklearn import tree
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics import accuracy_score
import random, string, json, spacy#, nltk#, re, os
from nltk import Tree, word_tokenize, pos_tag, ne_chunk
import name_extract as name_extract#, mathParse

training_inputs = []
training_labels = []
training_inputs2 = []
training_labels2 = []
training_inputs3 = []
training_labels3 = []

# print(os.listdir())

with open('tests\\NLP\\memory\\pTrain.json', 'r') as fp:
    trainData = json.load(fp)  # load up the training data from the json file

# sort the data and labels for the classifiers
for i in trainData["subject"]:
    training_inputs.extend(trainData["subject"][i])
    training_labels.extend([i] * len(trainData["subject"][i]))

for i in trainData["relation"]:
    training_inputs2.extend(trainData["relation"][i])
    training_labels2.extend([i] * len(trainData["relation"][i]))

for i in trainData["type"]:
    training_inputs3.extend(trainData["type"][i])
    training_labels3.extend([i] * len(trainData["type"][i]))

# test_inputs = []
# testing_labels = []

# converts the text into a numerical representation through the use of the "bag of words" technique
vectorizer = CountVectorizer()

training_vectors = vectorizer.fit_transform(training_inputs)
training_vectors2 = vectorizer.fit_transform(training_inputs2)
training_vectors3 = vectorizer.fit_transform(training_inputs3)

# testing_vectors = vectorizer.transform(test_inputs)

# fit the main classifer to its training data
classifier = LinearSVC()
classifier.fit(training_vectors, training_labels)

# fit the secondary classifer to its training data
classifier2 = LinearSVC()
classifier2.fit(training_vectors2, training_labels2)

# fit the tertiary classifer to its training data
classifier3 = LinearSVC()
# classifier3 = tree.DecisionTreeClassifier()
classifier3.fit(training_vectors3, training_labels3)

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

NER = spacy.load("en_core_web_sm")
    
def nameExtr(sent = "", lbl = "PERSON"):
    out = []

    tagged = NER(sent)

    for word in tagged.ents:
        if str(word.label_) == lbl:
            out.append(word.text)

    chunked = ne_chunk(pos_tag(word_tokenize(sent)))#put ner tags for each word, essentially

    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == "PERSON":
            for i in subtree.leaves():#grab each part of the name
                if not (i[0] in out):
                    out.append(i[0])
    
    return list(set(out))

def analys(n = ""):
    # predicts the main label
    vectorizer.fit(training_inputs)
    vectors = vectorizer.transform([n])
    subj = classifier.predict(vectors)[0]

    # predicts the main label
    vectorizer.fit(training_inputs2)
    vectors2 = vectorizer.transform([n])
    rel = classifier2.predict(vectors2)[0]

    # predict the tertiary label
    vectorizer.fit(training_inputs3)
    vectors3 = vectorizer.transform([n])
    ty = classifier3.predict(vectors3)[0]

    # makes the "None" label an actual None value
    rel = None if rel == 'None' else rel
    ty = None if ty == 'None' else ty

    n = n + "." if n[-1] != ["?", ".", "!"] else n

    c = {"subject": subj, "relation": rel, "type": ty}
    
    # if not c["type"]:
    #     return c
    # elif c["type"] == "name" or c["subject"] == "indicated":
    #     # names = nameExtr(n)
    #     names = nameExt.nameExt3(n)
    #     c["names"] = names

    if c["type"] == "name" or c["subject"] == "indicated":
        names = name_extract.name_extract(n)
        c["names"] = names

    familyWords = ["cousin", "brother", "sister", "aunt", "mom", "mother", "father", "dad", "son", "daughter", "child", "parent", "grandfather", "grandmother", "grandpa", "grandma", "uncle", "sibling", "baby", "stepfather", "stepmother", "step-father", "step-mother", "stepdad", "stepmom", "step-dad", "step-mom", "father-in-law", "mother-in-law", "sister-in-law", "brother-in-law", "grandparent", "nephew", "niece", "grandchild", "grandson", "granddaughter", "son-in-law", "daughter-in-law", "half-brother", "half-sister", "half-sibling"]
    romanceWords = ["partner", "spouse", "boyfriend", "girlfriend", "significant other", "wife", "husband", "lover", "babe", "companion", "mate", "date"]
    workWords = ["coworker", "boss", "manager", "intern", "employee", "supervisor", "owner", "ceo", "head", "colleague", "foreman", "superintendent", "administrator", "worker", "forewoman", "foreperson", "director", "employer"]
    petWords = ["puppy", "pet", "kitten", "dog", "cat", "gecko", "ferret", "lizard", "spider", "snake"]

    if c["relation"] == "family":
        for w in word_tokenize(n):
            if w.lower() in familyWords:
                c["relationship"] = w

    elif c["relation"] == "romance":
        for w in word_tokenize(n):
            if w.lower() in romanceWords:
                c["relationship"] = w

    elif c["relation"] == "work":
        for w in word_tokenize(n):
            if w.lower() in workWords:
                c["relationship"] = w

    elif c["relation"] == "pet":
        for w in word_tokenize(n):
            if w.lower() in petWords:
                c["relationship"] = w

    return c

def trainDataCont():
    for i in trainData["subject"]:
        print(i, len(trainData["subject"][i]))
    print("")
    for i in trainData["relation"]:
        print(i, len(trainData["relation"][i]))
    print("")
    for i in trainData["type"]:
        print(i, len(trainData["type"][i]))
    print("")

def UUID(length = 8):
    # out = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(length))
    out = ''.join(random.choices(string.ascii_letters + string.digits, k = length))
    
    return out

def store(n = ""):
    info = analys(n)
    with open('tests\\NLP\\memory\\memory.json', 'r') as fp:
        memory = json.load(fp)

    # pers = {
    #     "type": "PERSON",
    #     "names": [],
    #     "age": 0,
    #     "likes": [],
    #     "dislikes": [],
    #     "appearance": [],
    #     "qualities": [],
    #     "relationships": {
    #         "family": [],
    #         "friend": [],
    #         "romance": [],
    #         "work": [],
    #         "acquaintance": [],
    #         "pets": []
    #     },
    #     "events": []
    # }
    # pet = {
    #     "type": "PET",
    #     "names": [],
    #     "age": 0,
    #     "likes": [],
    #     "dislikes": [],
    #     "appearance": [],
    #     "qualities": [],
    #     "relationships": {
    #         "family": [],
    #         "friend": [],
    #         "romance": [],
    #         "acquaintance": [],
    #     },
    #     "events": []
    # }

    # for i in memory:
    #     print(i)

    if info["type"] == "remember":
        memory['remember'].append(n) # i could have it strip off delimiters(i.e. "don't forget about", "remind me that", or "remember that")
    elif info['subject'] == "indicated":
        # if info["type"] == "name" and len(info["names"]) == 1:
        if info["relation"] and info["relation"] != "unknown":#if using a relation
            if info["type"] == "name" and info["names"]:#name
                if info["relationship"]:
                    user = ""
                    for i in memory['type']:
                        if memory['type'][i] == "USER":
                            user = i

                    # print(user)
                    if user in memory['relations']:
                        t = ""
                        for i in memory['relations'][user]:
                            if info["names"][0] in i and info["relationship"] == i[1]:
                                t = i[0] # ("UUID", "RELATION")

                        if t:
                            if t in memory['names']:
                                if not (info["names"][0] in memory['names'][t]):
                                    memory['names'][t].append(info["names"][0])
                            else:
                                memory['names'][t] = []
                                memory['names'][t].append(info["names"][0])
                        else:
                            t = UUID()
                            memory['relations'][user].append((t, info["relationship"]))
                            memory['type'][t] = "PERSON"
                            memory["names"][t] = []
                            memory['names'][t].append(info["names"][0])
                    else:
                        memory['relations'][user] = []
                        t = UUID()
                        memory['relations'][user].append((t, info["relationship"]))
                        memory['type'][t] = "PERSON"
                        memory["names"][t] = []
                        memory['names'][t].append(info["names"][0])
        elif info["relation"] == "unknown":
            if info["names"]:
                t = ""
                for i in memory['names']:
                    # if info["names"][0] in memory['names'][i]:
                    if any(info["names"][0] in x for x in memory['names'][i]):
                        t = i
                
                if info["type"] == "age":
                    age = 0
                    for i in word_tokenize(n):
                        if i.isdigit():
                            if "years old" in n or "yo" in n:
                                age = int(i)
                            elif "months old" in n:
                                age = int(i)/12
                            elif "weeks old" in n:
                                age = int(i)/52 # 52.1429
                            else:
                                age = int(i)
                            break
                            

                    if t:
                        # if t in memory['age']:
                        #     memory['age'][t] = age
                        # else:
                        #     memory['age'][t] = age
                        if age:
                            memory['age'][t] = age

    with open('tests\\NLP\\memory\\memory.json', 'w') as fp:
        json.dump(memory, fp)

    return info, memory

if __name__ == "__main__":
    trainDataCont()

    print(UUID())

    # # print(analys(input("> ")))
    # print(analys("My sister's name is Julie.")) # {'subject': 'indicated', 'relation': 'family', 'type': 'name', 'names': ['Julie ..'], 'relationship': 'sister'}
    # print(analys("My brother's name is Erik.")) # {'subject': 'indicated', 'relation': 'family', 'type': 'name', 'names': ['Erik ..'], 'relationship': 'brother'}
    
    # print(analys("My friend Jon has a pet gecko he named Polly.")) # {'subject': 'indicated', 'relation': 'friend', 'type': 'name', 'names': ['Jon', 'Polly ..']}
    # print(analys("Jon has a pet gecko he named Polly.")) # {'subject': 'referenced', 'relation': 'unknown', 'type': 'appearance'}
    
    # print(analys("I have a pet gecko named Polly.")) # {'subject': 'indicated', 'relation': 'pet', 'type': None, 'names': ['Polly'], 'relationship': 'gecko'}
    
    # print(analys("I saw Dolly at the store the other day.")) # {'subject': 'speaker', 'relation': 'stranger', 'type': 'event'}
    
    # print(analys("I went to the store yesterday.")) # {'subject': 'speaker', 'relation': None, 'type': 'event'}
    print(analys("Dolly went to the store the other day.")) # {'subject': 'speaker', 'relation': None, 'type': 'event'} - {'subject': 'indicated', 'relation': None, 'type': 'event', 'names': []}

    # while True:
    #     t = analys(input("> "))
    #     print(t)

        # m = store("my sister's name is Julie")
        # m = store(input("> "))
        # print(m[0])