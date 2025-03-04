import mathParse, nltk
from nltk import word_tokenize

def timExtr(inp = ""):
    timing = None
    timeWords = ["yesterday", "today", "tomorrow", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "next week", "this week", "weeks",  "hour", "hours", "minute", "minutes", "days", "second", "seconds", "am", "pm", "a.m", "p.m", "a.m.", "p.m."]
    words = word_tokenize(inp.lower())
    for i, word in enumerate(words):
        if word in timeWords:
            tag = nltk.pos_tag([words[i - 1]])[0][1]
            if tag == 'CD' or tag == 'DT':
                if words[i - 2] in ["at", "in"]:
                    # inp = inp.replace(" " + words[i - 2], "")
                    if words[i - 2] == "in":
                        timing = "+"#uses a plus to specify that this is an amount of time that must elapse before the request is fulfilled
                    else:
                        timing = "o"#uses an "o" to specify that this is a specific time at which the request is to be fulfilled
                elif "for" in words:
                    timing = "o"

                num = words[i - 1]
                # inp = inp.replace(" " + words[i - 1] + " " + word, "")
                if num in ["an", "a"]:
                    num = "1"  # uses 1 if the input uses "an" or "a"
                elif not num.isdigit():
                    # changes a number word into an actual number
                    num = str(mathParse.parser(num))

                timing += "_" + num + "_" + word  # combines the specified number and the "unit"
            else:
                if not timing:
                    timing = "o"
                timing += "_" + word
                # inp = inp.replace(" " + word, "")
        elif i < len(words) - 1:
            gWord = word + " " + words[i + 1]
            if gWord in timeWords:
                timing = "o_" + gWord
                # inp = inp.replace(" " + gWord, "")

    return timing