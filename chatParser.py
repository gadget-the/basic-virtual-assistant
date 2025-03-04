import json, random#, pyttsx3
from nltk import word_tokenize

def chatLogPars(filename = ''):
    statRespDict = {}
    with open('statResp.json', 'r') as fp:
        statRespDict = json.load(fp)#loads up the current statResp file
    with open(filename, 'r') as fp:
        fileCont = fp.read().split('\n')#loads up the contents of our input file
    # with open(filename, 'r') as fp:
    #     fileCont = [l.replace("\n", "") for l in fp.readlines()]#loads up the contents of our input file

    # print(fileCont)
    for i, item in enumerate(fileCont):
        if ": " in item:#checks if there is a colon in the line
            fileCont[i] = item[item.find(': ') + 2:]#removes the names of the person who is saying something on the current line
        else:#if there isn't a colon in the line it is left alone
            fileCont[i] = item

    for i, stat in enumerate(fileCont):
        if stat != "":#checks if the current item is just an empty string
            if not (stat in statRespDict):
                statRespDict[stat] = []#if the statement is already present in statResp, it doesn't add it(and the reverse is true)
            if i > 0 and fileCont[i - 1] in statRespDict:#checks if the previous statement is already in the dictionary
                if not (stat in statRespDict[fileCont[i - 1]]):#checks if the current statement is is the list of responses for the previous statement
                    statRespDict[fileCont[i - 1]].append(stat)#if the previous statement to which the current statement is in response to is present in statResp, it adds this statement as a response for the previous statement

    for key in statRespDict:#remove duplicates
        statRespDict[key] = list(dict.fromkeys(statRespDict[key]))

    #print(statRespDict)
    with open('statResp.json', 'w') as fp:
        json.dump(statRespDict, fp) # saves the dictionary as a json file
    print("Done!")
    return statRespDict

def respond(statement = '', debug = False, common = 0.75, refFile = 'statResp.json'):
    with open(refFile, 'r') as fp:
        statRespDict = json.load(fp) # loads up the current statResp file

    idkResp = [
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

    respSort = {}
    for key in statRespDict:
        a = list(set(statement.lower())&set(key.lower()))#https://www.sanfoundry.com/python-program-check-common-letters-string/
        if len(a) >= len(set(key.lower())) * common:
            respSort[key] = len(a)#only keeps the statements that have 3/4(the default) or more of their letters/characters in common with the inputed string

    respSort = {k: v for k, v in sorted(respSort.items(), key=lambda item: item[1], reverse=True)}#orders the dictionary by values(most shared letters to least)
    closestStat = ''
    if bool(respSort):#checks if the dictionary is empty
        closestStat = list(respSort.keys())[0]#takes the first statement in the list of ordered statements
  
    if closestStat != '':
        if len(statRespDict[closestStat]) > 0:
            # outputs a random response from the list for the closest statement(key) in the dictionary
            if debug: # if debug requested, also output the debug info
                return random.choice(statRespDict[closestStat]), list(respSort.keys())[:3], statRespDict[closestStat]
            else:
                return random.choice(statRespDict[closestStat])
        else:
            # if there are no responses in the list for the closest statement(key), it outputs an "idk" response
            if debug:
                return random.choice(idkResp), list(respSort.keys())[:3], statRespDict[closestStat]
            else:
                return random.choice(idkResp)
    else: # outputs an "idk" response if it can't find a close enough statement in statRespDict
        if debug:
            return random.choice(idkResp), None, None
        else:
            return random.choice(idkResp)

def respondWord(statement = '', debug = False, common = 0.75, refFile = 'statResp.json'):
    with open(refFile, 'r') as fp:
        statRespDict = json.load(fp)#loads up the current statResp file

    respSort = {}
    for key in statRespDict:
        a = list(set(word_tokenize(statement.lower()))&set(word_tokenize(key.lower())))#https://www.sanfoundry.com/python-program-check-common-letters-string/
        if len(a) >= len(set(word_tokenize(key))) * common:
            respSort[key] = len(a)#only keeps the statements that have 3/4(default) or more of their words in common with the inputed string

    respSort = {k: v for k, v in sorted(respSort.items(), key=lambda item: item[1], reverse=True)}#orders the dictionary by values(most shared words to least)
    closestStat = ''
    if bool(respSort):#checks if the dictionary is empty
        closestStat = list(respSort.keys())[0]#takes the first statement in the list of ordered statements

    if closestStat != '':
        if len(statRespDict[closestStat]) > 0:
            if debug:
                return random.choice(statRespDict[closestStat]), list(respSort.keys())[:3], statRespDict[closestStat]#if debug requested, output a random response and debug info
            else:
                return random.choice(statRespDict[closestStat])#if debug not requested, output a random response
        else:
            return respond(statement, debug, common, refFile)#if there are no responses for the closestStat, use the character based responder
    else:
        return respond(statement, debug, common, refFile)#if there is no closestStat, use the character based responder

if __name__ == '__main__':
    # chatLogPars('tests/testLogs/testLog12.txt')
    # with open('tests\\done.json', 'r') as fp:
    #     done = json.load(fp)

    # todo = [x for x in os.listdir("tests/logs/") if x not in done]
    # for f in todo:
    #     print(f)
    #     chatLogPars('tests/logs/' + f)
    #     done.append(f)
    #     mem = psutil.virtual_memory()[2]
    #     print('RAM memory % used:', mem)
    #     # print('% done:', len(done)/len(os.listdir("tests/logs/")), "Number done:", len(done), "Number left:", len(os.listdir("tests/logs/")) - len(done))
    #     if mem > 75.9:
    #         # print(done)
    #         # print(len(done), len(os.listdir("tests/logs/")) - len(done), len(done)/len(os.listdir("tests/logs/")))
    #         with open('tests\\done.json', 'w') as fp:
    #             json.dump(done, fp)
    #         break
    # print('DONE!')
    # only got through about 0.445 of the files for the Cornell Movie data, moved it to the 'tests\statResp-alt' folder

    # [os.remove('tests\\logs\\' + f) for f in done]
    # done = []
    # with open('tests\\done.json', 'w') as fp:
    #     json.dump(done, fp)

    # respond("Hi!")
    print(respond("Hi!"))
    # print(respondWord("Hi!", True))

    # engine = pyttsx3.init()

    # print('Your conversation starts here.\n')
    # while True:
    #     state = input("> ")
    #     # resp = respond(state, True)
    #     resp = respondWord(state, debug = False)
    #     print('Bot: ' + resp)
    #     # engine.say(resp)
    #     # engine.runAndWait()