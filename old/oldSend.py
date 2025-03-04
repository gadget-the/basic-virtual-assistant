import old.commandFilter as commandFilter, intEntFilter, weather_retrieval, smarthouse, chatParser, webSearch, threading, webbrowser, datetime, tkinter as tk, word2number as w2n
from nltk import word_tokenize

def send(self, test=None):
    if str(self.master.focus_get()) == ".!entry":  # checks if the input box has focus
        res = self.txtIn.get()  # sets res to the contents of the input box
        # clears the contents of the input box
        self.txtIn.delete(0, tk.END)
        self.lastIn = res

        # classif = eval("commandFilter." + self.drop.get() + "(res)")#bad, don't use eval
        classif = None
        if self.classifTyp.get():
            classifTyp = self.classifTyp.get()
            if self.classifSty:
                print(classifTyp)
                self.debugBox.insert(tk.INSERT, classifTyp + "\n")

            if classifTyp == "decTrClass":
                classif = commandFilter.decTrClass(res)#decision tree
            elif classifTyp == "knnClass":
                classif = commandFilter.knnClass(res)#nearest neighbor
            elif classifTyp == "lsvcClass":
                classif = commandFilter.lsvcClass(res)#linear support vector
            elif classifTyp == "forClass":
                classif = commandFilter.forClass(res)#random forest
            else:
                print("bad algo")
        else:
            classif = commandFilter.lsvcClass(res)
            # classif = commandFilter.decTrClass(res)#classifies the input['weather', 'smarthouse', 'math', 'search', 'conversational', 'etc.']
            # classif = commandFilter.knnClass(res)
            # classif = commandFilter.forClass(res)
        
        intEnt = intEntFilter.intNEnt(res)
        if intEnt["subInt"]:
            print(intEnt["subInt"])

        # adds the input to the log txt box
        self.txtBox.insert(tk.INSERT, "User: " + res + "\n")
        # saves the input and classification to a list
        self.log.append(("User", res, classif[0]))
        self.txtBox.see(tk.END)  # autoscroll

        if self.classifDeb:
            print(classif)# classif debug
            print(intEnt)
            self.debugBox.insert(tk.INSERT, classif[0] + "\n")
            self.debugBox.insert(tk.INSERT, str(intEnt) + "\n")

        out = None

        if classif == "weather":
            out = weather_retrieval.takeInput(res)
            # threading.Timer(5.0, weath.takeInput, [res]).start()
            # t = 5.0
            # threading.Timer(t, self.waitTime, [weath.takeInput, (res,)]).start()
        elif classif == "smarthouse":
            # out = ("smarthouse", res)
            out = smarthouse.checkInput(res)
        elif classif == "math":
            # out = ("math", res)
            try:
                out = "The answer is: " + str(w2n.word_to_num(" ".join(word_tokenize(res))))
            except Exception as e:
                print(e)
        elif classif == "conversation":
            # out = chatParser.respond(res, self.chatDeb)
            out = chatParser.respondWord(res, self.chatDeb)
        elif classif == "search":
            engines = ["google", "bing", "Google", "Bing"]
            engin = None
            [engin := e for e in engines if e in res]#finds the specified engine, if one is specified

            delim = ["google search", "search google", "search on google", "search bing", "search on bing", "search", "google"]
            # [res := res.replace(x, "") for x in delim if x in res]
            for d in delim:
                if d in res:
                    res = res.replace(d, "")
                    break

            if engin:
                out = "Searching on " + engin + ": " + res
                webSearch.search(res, engin)
            else:
                results = webSearch.ddgSrch(res)
                if results[0]:
                    self.address("Using DuckDuckGo's Instant Answer API:", self.speak)
                    out = results
                else:
                    out = "Searching on Google: " + res
                    webSearch.search(res)
        elif classif == "app":
            # out = ("app", res.replace("open ", ""))
            # app = res.replace("open ", "") + '.exe'
            # print(res.find("open "))
            app = res[res.find("open ") + 5:] + ".exe"
            out = "Attempting to open: " + app
            
            # self.findNOpen(app)
            findNOp = threading.Thread(target=self.findNOpen, args=(app,))
            findNOp.start()

        elif classif == "browser":
            # out = ("browser", res.replace("open ", "").replace("go to ", ""))
            site = res.replace("open ", "").replace("go to ", "")
            if "www" not in site:
                site = "www." + site
            if "http" not in site:
                site = "https://" + site
            out = "Opening: " + site
            webbrowser.open(site)

        elif classif == "time":
            # out = ("time", res)
            x = datetime.datetime.now()
            # + " and " + x.strftime("%S") + " seconds"
            out = "The time is: " + x.strftime("%I:%M")

        # self.address(out, self.speak)
        talk = threading.Thread(target=self.address, args=(out, self.speak,))
        talk.start()

    if self.logDeb:
        print(self.log)
        self.debugBox.insert(tk.INSERT, str(self.log) + "\n")