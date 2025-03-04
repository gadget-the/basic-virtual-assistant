from urllib.request import urlopen
import json, random

#https://uselessfacts.jsph.pl/
url = 'https://uselessfacts.jsph.pl/random.json?language=en'
randPrefixes = ["Did you know ", "Fun fact: ", "Fun fact! ", "Here's a fun fact: ", "Fun fact! Did you know that ", "Here's a fun fact, did you know ", "Did you know that ", "Here's a random fact: "]

def randFac():
    response = urlopen(url)
    data_json = json.loads(response.read())
    randomFact = data_json["text"]
    return randomFact

def day():
    todayFact = json.loads(urlopen('https://uselessfacts.jsph.pl/today.json?language=en').read())["text"]
    return todayFact

if __name__ == "__main__":
    randPre = random.choice(randPrefixes)
    print(randPre + randFac())
    print("Random fact of the day: " + day())