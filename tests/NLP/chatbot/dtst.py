import json, nltk, os, pprint
# from chatParser import respond
from datasets import load_dataset
from nltk.corpus import nps_chat
from nltk.tokenize.treebank import TreebankWordDetokenizer

def grabLogs(num = 500):
    dataset = load_dataset('re_dial')
    for f, item in enumerate(dataset['train']['messages'][:num]):
        with open('tests\\logs\\log' + str(f) + '.txt', 'w') as f:
            # print(len(item))
            for i, tem in enumerate(item):
                #print(str(tem['senderWorkerId']) + ": " + tem['text'])
                #print(tem)
                #print(i, len(item))
                if i < (len(item) - 1) and item[i + 1]['senderWorkerId'] == tem['senderWorkerId']:
                    f.write(str(tem['senderWorkerId']) + ": " + tem['text'] + " " + item[i + 1]['text'] + '\n')
                    del item[i + 1]
                else:
                    f.write(str(tem['senderWorkerId']) + ": " + tem['text'] + '\n')
        # f.close()

def grabLogs2():
    nltk.download('nps_chat')

    # chatroom = nps_chat.posts('10-19-20s_706posts.xml')
    chatroom = nps_chat.posts('11-06-adults_706posts.xml')
    # print(chatroom[120:123])
    for i in chatroom[0:15]:
        print(TreebankWordDetokenizer().detokenize(i))
    # print(TreebankWordDetokenizer().detokenize(chatroom[123]))

def grabLogs3(num = 25):
    with open('tests\\datasets\\ccpe-conversational-dataset.json', 'r') as fp:
        ccpe = json.load(fp)

    # print(len(ccpe[:num]))
    for i, item in enumerate(ccpe[:num]):
        print(item["conversationId"])
        with open('tests\\logs\\log' + str(i) + '.txt', 'w') as f:
            for j, m in enumerate(item["utterances"]):
                # line = m["speaker"] + ": " + m["text"]
                if j < (len(item["utterances"]) - 1) and item["utterances"][j + 1]["speaker"] == m["speaker"]:
                    line = m["speaker"] + ": " + m['text'] + " " + item["utterances"][j + 1]['text']
                    del item["utterances"][j + 1]
                else:
                    line = m["speaker"] + ": " + m["text"]
                f.write(line + "\n")

                # if j < (len(item["utterances"]) - 1):
                #     print(line, m["speaker"], item["utterances"][j + 1]["speaker"])
                # print(line)
        # f.close()

    # print(ccpe)

def grabLogs4(num = 25):
    with open('tests\\datasets\\dstc-dialogue-dataset.json', 'r') as fp:
        dstc = json.load(fp)
    
    for i, d in enumerate(dstc[:num]):
        print(d["dialogue_id"])
        with open('tests\\logs\\log-' + d["dialogue_id"] + '.txt', 'w') as f:
            for t in d["turns"]:
                line = t["speaker"] + ": " + t["utterance"]
                # print(t["speaker"])
                # print(line)
                f.write(line + "\n")

    # print(dstc)

def grabLogs5Part1():
    with open('tests\\datasets\\movie_lines.txt', 'r') as f:
        lines = f.readlines()
    with open('tests\\datasets\\movie_conversations.txt', 'r') as f:
        conversations = f.readlines()
    formatted_lines = {}
    formatted_conversations = {}

    for line in lines:
        # print(line)
        lineLst = line.split(" +++$+++ ")

        lineID = lineLst[0]
        characterID = lineLst[1]
        movieID = lineLst[2]
        characterName = lineLst[3]
        utterance = lineLst[4]

        # print(convID, speaker, utterance)
        formatted_lines[lineID] = {
            "characterID": characterID,
            "movieID": movieID,
            "characterName": characterName,
            "utterance": utterance
        }
    
    for c in conversations:
        convLst = c.split(" +++$+++ ")
        # characterID1 = convLst[0]
        # characterID2 = convLst[1]
        # movieID = convLst[2]
        convUtterances = convLst[3].replace("['", "").replace("']\n", "").split("', '")
        # print(characterID1, characterID2, movieID, convUtterances)
        convID = "conversation" + str(len(formatted_conversations.keys()))
        formatted_conversations[convID] = []
        for i in convUtterances:
            if i in formatted_lines:
                # formatted_conversations[convID].append(formatted_lines[i]["characterName"] + ": " + formatted_lines[i]["utterance"])
                formatted_conversations[convID].append((formatted_lines[i]["characterName"], formatted_lines[i]["utterance"]))

    # with open('tests\\datasets\\processedLines.json', 'w') as fp:
    #     json.dump(formatted_lines, fp)
    with open('tests\\datasets\\processedCMDC.json', 'w') as fp:
        json.dump(formatted_conversations, fp)
    print('DONE!')

def grabLogs5Part2(num = None):
    with open('tests\\datasets\\processedCMDC.json', 'r') as fp:
        data = json.load(fp)

    for conv in list(data.keys())[:num] if num else data:
        print(conv)
        with open('tests\\logs\\log-' + conv + '.txt', 'w') as f:
            for t in data[conv]:
                line = t[0] + ": " + t[1].replace("\t", "").replace("\n", "")
                f.write(line + "\n")

    print('DONE!')

if __name__ == "__main__":
    # grabLogs()
    # grabLogs2()
    # grabLogs3(500)
    # grabLogs4(500)
    # grabLogs5Part1()
    # grabLogs5Part2(num=5)
    grabLogs5Part2()