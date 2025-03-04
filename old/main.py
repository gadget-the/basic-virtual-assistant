import os, pyttsx3, commandFilter, chatParser, weather_retrieval, webSearch

def address(txt = "", speak = True):
    txt = str(txt)
    print("Bot: " + txt)
    if speak:
        engine.say(txt)
        engine.runAndWait()

if __name__ == '__main__':
    engine = pyttsx3.init()
    greet = "Welcome, awaiting input:"
    address(greet)
    while True:
        x = input("> ")
        # classif = commandFilter.decTrClass(x)
        # classif = commandFilter.knnClaswhats(x)
        classif = commandFilter.lsvcClass(x)
        print(classif)
        out = None
        # speak = True
        speak = False
        if classif == "weather":
            out = weather_retrieval.takeInput(x)
        elif classif == "smarthouse":
            out = ("smarthouse", x)
        elif classif == "math":
            out = ("math", x)
        elif classif == "conversation":
            out = chatParser.respond(x)
        elif classif == "search":
            engines = ["google", "bing", "Google", "Bing"]
            engin = None
            for eng in engines:
                if eng in x:
                    engin = eng
            # delim = ["google search", "search google", "search on google", "search bing", "search on bing", "search", "google"]
            # # if [term in x for term in delim]:
            # for term in delim:
            #     if term in x:
            #         x.replace(term, "")
            if engin:
                address("Searching on " + engin + ":")
                out = webSearch.search(x, engin)
                speak = False
            else:
                results = webSearch.ddgSrch(x)
                if results[0]:
                    address("Using DuckDuckGo's Instant Answer API:")
                    out = results
                else:
                    address("Searching on Google:")
                    out = webSearch.search(x)
                    speak = False

        address(out, speak)