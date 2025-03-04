def analys(n = "", inc = 1):
    n = str(n.lower())
    lexOut = []
    pol = 0.0
    lex = {
        "angry": [
            "angry",
            "annoyed",
            "irritated",
            "vexed",
            "cross",
            "pissed",
            "enraged",
            "angered",
            "agitated",
            "miffed",
            "peeved",
            "fuming",
            "furious",
            "infuriated",
            "riled",
            "blood boil",
            "ticked off",
            "irked",
            "bothered",
            "outraged",
            "bugged",
            "mad",
            "frustrated",
            "stupid"
        ],
        "sad": [
            "disappointed",
            "depressed",
            "desperate",
            "dejected",
            "crushed",
            "upset",
            "sorrow",
            "mourn",
            "grief",
            "grieve",
            "weepy",
            "unhappy",
            "regret",
            "feeling down",
            "feels down",
            "downhearted",
            "despondent",
            "despair",
            "disconsolate",
            "inconsolable",
            "downcast",
            "miserable",
            "desolate",
            "glum",
            "gloomy",
            "wretched",
            "grim",
            "heartbroken",
            "broken-hearted",
            "broken hearted",
            "devastate",
            "melancholy",
            "woeful",
            "forlorn",
            "frown",
            "woebegone",
            "morose",
            "feeling blue",
            "feel blue",
            "feels blue",
            "crestfallen",
            "cheerless",
            "doleful",
            "dismal",
            "blighted",
            "horrible"
        ],
        "happy": [
            "happy",
            "amused",
            "delighted",
            "glad",
            "pleased",
            "joyful",
            "joyed",
            "overjoyed",
            "content",
            "jovial",
            "jolly",
            "gleeful",
            "smiling",
            "carefree",
            "cheery",
            "cheerful",
            "untroubled",
            "merry",
            "elated",
            "exuberant",
            "ecstatic",
            "euphoric",
            "on cloud nine",
            "over the moon",
            "walking on air",
            "tickled pink",
            "glad",
            "empowered",
            "renewed",
            "vibrant",
            "refreshed",
            "enjoy",
            "like"
        ],
        "jealous": [
            "jealous",
            "envi",
            "envy"
        ],
        "confused": [
            "uncertain",
            "indecisive",
            "perplexed",
            "confused",
            "lost",
            "unsure"
        ],
        "excited": [
            "excited",
            "thrilled",
            "exhilirated",
            "elevated",
            "enlivened",
            "electrify",
            "electrified",
            "enraptured",
            "high",
            "eager",
            "peppy",
            "aroused",
            "titillate",
            "impassion",
            "squirrelly",
            "rouse",
            "entice",
            "!"
        ],
        "indifferent": [
            "indifferent",
            "apathy",
            "apathetic",
            "impassive",
            "impassionate",
            "dispassionate",
            "emotionless",
            "unemotional",
            "unsympathetic",
            "unmoved",
            "unfeeling",
            "aloof",
            "cold",
            "distant",
            "detached",
            "unconcerned",
            "no interest in",
            "nonchalant"
        ],
        "afraid": [
            "afraid",
            "fear",
            "distress",
            "troubled",
            "worry",
            "worried",
            "dismay",
            "consternation",
            "anxious",
            "disquiet",
            "uneasy",
            "alarmed",
            "panic",
            "dread",
            "enthusiastic",
            "scared",
            "frightened",
            "terrified",
            "horror",
            "terror",
            "nervous",
            "frantic",
            "hysterical",
            "cower",
            "phobia",
            "fright",
            "creeps",
            "jitter",
            "trepidation",
            "twinge"
        ],
        "suprised": [
            "suprised",
            "startled",
            "flabbergasted",
            "speechless",
            "amazed",
            "dazed",
            "stupefied",
            "staggering",
            "dumbfounded",
            "taken aback",
            "astounded",
            "astonished",
            "shocked",
            "shudder",
            "nonplus",
            "stun",
            "bewildered",
            "flummoxed",
            "flinch"
        ]
    }
    polarity = {
        "positive": [
            "peaceful",
            "at peace",
            "loved",
            "loving",
            "like",
            "love",
            "liked",
            "enjoy",
            "favorite",
            "favourite",
            "fanci",
            "fancy",
            "fond",
            "soft spot for",
            "fondness for",
            "high regard",
            "in esteem",
            "attracted to",
            "prefer",
            "adore",
            "admire",
            "respect",
            "take to",
            "relish",
            "savor",
            "agreeable",
            "a thing for",
            "get off on",
            "secure",
            "powerful",
            "confident",
            "determined",
            "inspired",
            "healthy",
            "motivated",
            "strengthened",
            "invigorated",
            "moved by",
            "pleasant"
        ],
        "negative": [
            "displeased",
            "dissatisfied",
            "agravated",
            "disturbed",
            "upset",
            "offended",
            "dislike",
            "hate",
            "detest",
            "loathe",
            "oppose",
            "disrelish",
            "unbearable",
            "intolerable",
            "disapprove",
            "distaste",
            "disfavor",
            "abhor",
            "scorn",
            "aversion to",
            "repelled",
            "hesitant",
            "star-crossed",
            "star crossed",
            "ill-starred",
            "ill starred",
            "mediocre",
            "tired",
            "tiring",
            "wince",
            "pain",
            "ill-fated",
            "ill fated",
            "hurt"
        ]
    }
    polarity["negative"].extend(lex["angry"])
    polarity["negative"].extend(lex["sad"])
    polarity["negative"].extend(lex["jealous"])
    polarity["negative"].extend(lex["confused"])
    polarity["negative"].extend(lex["afraid"])
    polarity["positive"].extend(lex["happy"])
    polarity["positive"].extend(lex["excited"])

    for e in lex:
        for word in lex[e]:
            if word in n:
                lexOut.append(e)

    for i in polarity["positive"]:
        if i in n:
            pol += inc

    for i in polarity["negative"]:
        if i in n:
            pol -= inc

    # return lexOut, pol
    # return pol, list2Perc(lexOut), lexOut
    return pol, list2Perc(lexOut)

def list2Perc(n = []):
    n = list(n)
    d = {}
    for i in n:
        if i in d.keys():
            d[i] += 1/len(n)
        else:
            d[i] = 1/len(n)
    
    return d

if __name__ == '__main__':
    # t = list2Perc(["happy", "sad", "happy", "sad", "sad"])
    # print(t, sum(t.values()))

    # text = "That night was so horrible. He's so stupid!"
    text = "I really like apples!"

    t = analys(text)
    print(text, "\n", t)