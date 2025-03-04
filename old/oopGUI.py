import tkinter as tk
import intEntFilter, mathParse, chatParser, weather_retrieval, webSearch, funfact, randGen, tube, timeStuff#, smarthouse
import os, subprocess, datetime, webbrowser, threading, random, json, time, pytz, string, pyttsx3, pyaudio, wave
from tzlocal.win32 import get_localzone_name
import speech_recognition as sr

class gui(tk.Frame):
    def __init__(self, master):
        with open('settings1.json', 'r') as fp:
            self.settings = json.load(fp)
        # print(settings)

        self.master = master
        self.engine = pyttsx3.init()
        self.timeZone = pytz.timezone(get_localzone_name())
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"))
        webbrowser.register('firefox', None, webbrowser.BackgroundBrowser("C:\\Program Files\\Mozilla Firefox\\firefox.exe"))

        self.ttsOn = True
        # self.chatDeb = False
        # self.classifDeb = False
        # self.logDeb = False
        # # self.classifSty = False
        self.sessionStartTime = datetime.datetime.now(tz = self.timeZone)
        self.log = {
            "sessionStartTime": "",
            "sessionEndTime": "",
            "sessionDuration": 0,
            "log": []
        }
        # self.lastIn = ""
        self.lastClass = {}
        self.timers = []
        # self.saveLog = False
        # self.helpText = """
        #     Hello!
        #     I am your Virtual Assistant.
        #     I have a number of functions.
        #         I can conversate(not well),
        #             "Hello!"
        #             "How are you?"
        #         I can tell you about the weather,
        #             "How's the weather?",
        #             "Is it humid in Dallas?",
        #             "How does the weather look for the next three days?"
        #         I can help you with things around the house(not actually),
        #             "Turn on the lights in the kitchen",
        #             "Set the oven temp to 450 in 5 minutes",
        #             "Turn off all the lights at 6:30"
        #         I can do math for you(like basic arithmetic, sometimes),
        #             "What is two plus two?",
        #             "eight divided by 4",
        #             "What is 350 times 29?"
        #         I can make a search on the web for you,
        #             "Search on Google cake recipes",
        #             "Search Yahoo for popular tech companies",
        #             "How many satelites are currently in orbit?"
        #         I can open apps on your computer,
        #             "Open Discord in seven minutes",
        #             "Open FireFox",
        #             "Please, start up settings"
        #         I can open websites for you,
        #             "Go to Youtube",
        #             "Open Google",
        #             "Go to https://www.wired.com/"
        #         I can tell you the time, set timers for you, and tell you long until a certain date,
        #             "How many days are there until January 19",
        #             "What time is it?",
        #             "Remind me in an hour to water the plants"
        #         I can tell you a funfact(currently just random, specified topics aren't used),
        #             "Tell me a funfact",
        #             "Do you know any cat facts?",
        #             "Tell me a fact about the ISS"
        #         I can generate random numbers,
        #             "Give me two random numbers between five and fifteen",
        #             "Roll a 20 sided die, please",
        #             "Flip a coin"
        #         And I can play music or grab lyrics from the web.
        #             "Play Blinding Lights by The Weeknd",
        #             "What are the lyrics to Woman by Doja Cat?",
        #             "Put on 505 by Arctic Monkeys"
        # """
        self.helpText = "Hello!\nI am your Virtual Assistant.\nI have a number of functions.\n\tI can conversate(not well),\n\t\t\"Hello!\"\n\t\t\"How are you?\"\n\tI can tell you about the weather,\n\t\t\"How's the weather?\",\n\t\t\"Is it humid in Dallas?\",\n\t\t\"How does the weather look for the next three days?\"\n\tI can help you with things around the house(not actually),\n\t\t\"Turn on the lights in the kitchen\",\n\t\t\"Set the oven temp to 450 in 5 minutes\",\n\t\t\"Turn off all the lights at 6:30\"\n\tI can do math for you(like basic arithmetic, sometimes),\n\t\t\"What is two plus two?\",\n\t\t\"eight divided by 4\",\n\t\t\"What is 350 times 29?\"\n\tI can make a search on the web for you,\n\t\t\"Search on Google cake recipes\",\n\t\t\"Search Yahoo for popular tech companies\",\n\t\t\"How many satelites are currently in orbit?\"\n\tI can open apps on your computer,\n\t\t\"Open Discord in seven minutes\",\n\t\t\"Open FireFox\",\n\t\t\"Please, start up settings\"\n\tI can open websites for you,\n\t\t\"Go to Youtube\",\n\t\t\"Open Google\",\n\t\t\"Go to https://www.wired.com/\"\n\tI can tell you the time, set timers for you, and tell you long until a certain date,\n\t\t\"How many days are there until January 19\",\n\t\t\"What time is it?\",\n\t\t\"Remind me in an hour to water the plants\"\n\tI can tell you a funfact(currently just random, specified topics aren't used),\n\t\t\"Tell me a funfact\",\n\t\t\"Do you know any cat facts?\",\n\t\t\"Tell me a fact about the ISS\"\n\tI can generate random numbers,\n\t\t\"Give me two random numbers between five and fifteen\",\n\t\t\"Roll a 20 sided die, please\",\n\t\t\"Flip a coin\"\n\tAnd I can play music or grab lyrics from the web.\n\t\t\"Play Blinding Lights by The Weeknd\",\n\t\t\"What are the lyrics to Woman by Doja Cat?\",\n\t\t\"Put on 505 by Arctic Monkeys\"\n"

        self.ttsOn = self.settings["spokenFeedback"]
        self.chatDeb = self.settings["printChatDebug"]
        self.classifDeb = self.settings["printClassification"]
        self.logDeb = self.settings["printLog"]
        # self.log = self.settings["log"]
        self.lastIn = self.settings["lastInput"]
        self.debugOpen = self.settings["debugOpen"]
        self.saveLog = self.settings["saveLog"]

        self.ttsCheck = tk.BooleanVar()
        self.var1 = tk.BooleanVar()# variables for check buttons
        self.var2 = tk.BooleanVar()
        self.var3 = tk.BooleanVar()
        self.var4 = tk.BooleanVar()

        # self.var4 = tk.IntVar()
        self.var1.set(self.logDeb)
        self.var2.set(self.classifDeb)
        self.var3.set(self.chatDeb)

        master.title('Basic Virtual Assistant')
        master.minsize(400, 585)
        # master.geometry("400x585")

        self.opening = tk.Label(text="Welcome, awaiting input:")
        # self.opening.place(x=125, y=5)
        self.opening.pack(pady=5)

        self.txtBox = tk.Text(master, wrap=tk.WORD)
        # self.txtBox.place(x=10, y=30)
        self.txtBox.pack(padx=10, expand=1, fill=tk.BOTH)
        # self.txtBox.config(state= tk.DISABLED)
        # self.txtBox.config(state='disabled')

        # self.scrollbar = tk.Scrollbar()
        # self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.txtBox.config(yscrollcommand=self.scrollbar.set)
        # self.scrollbar.config(command=self.txtBox.yview)

        self.txtIn = tk.Entry(master, width=40)# input field
        self.txtIn.pack(padx=50, pady=5, fill=tk.X)# makes the input field fill the x-axis, with a buffer

        self.button1 = tk.Button(text="<send>", width=10, command=self.send)# button to send input
        self.button1.pack(pady=5, padx=10, side=tk.RIGHT)# shifts the button to the right

        self.button1 = tk.Button(text="<speech>", width=10, command=self.speechThr)# button to start speech_rec capture
        self.button1.pack(pady=5, padx=10, side=tk.RIGHT)# shifts the button to the right

        self.check_button = tk.Checkbutton(text="<tts>", variable=self.ttsCheck, command=self.ttsToggle)# check button for turning tts on/off
        self.check_button.pack(pady=5, padx=5, side=tk.RIGHT)# shifts it to the right
        if self.ttsOn:
            self.check_button.select() # sets it to checked

        self.button1 = tk.Button(text="Debug", width=8, command=self.openDebug)
        self.button1.pack(pady=5, padx=10, side=tk.LEFT)

        master.bind('<Escape>', self.mainClose)  # sets a key to close the program
        # master.bind('t', ttsToggle)

        self.txtIn.bind('<Return>', self.send)  # sets a key to send input
        self.txtIn.bind('<Up>', self.reuse) # puts the last input back in the input field
        self.txtIn.bind('<Control-z>', self.reuse) # puts the last input back in the input field
        self.txtIn.bind('<Control-Z>', self.reuse) # puts the last input back in the input field
        self.txtIn.bind('<Down>', self.inputClear)  # clears the input field

        master.protocol("WM_DELETE_WINDOW", self.mainClose)

        self.txtIn.focus()  # gives the input field focus
        # threading.Thread(target=self.waitTime, args=(5, self.openDebug,)).start()
        # self.greet()
        # master.after(250, self.greet)
        if self.debugOpen:
            # self.openDebug()
            master.after(1, self.openDebug)

        # master.attributes('-fullscreen', True)
        # master.attributes('-alpha', 0.75)

    class timer(object):
        def __init__(self, outer, t = 0, message = "", method = None, args = ()):
            self.outer = outer
            self.timeLeft = t
            self.active = True
            self.method = method
            self.args = args
            self.message = message
            # self.timerID = ''.join(random.choices(string.ascii_letters + string.digits, k = 8))
            self.timerID = self.genID()
            self.stop = False

            threading.Thread(target = self.countdown).start()

        def genID(self): # ensure that the string that is generated contains at least one letter and at least one number
            s = ''.join(random.choices(string.ascii_letters + string.digits, k = 8))
            while not any(x.isalpha() for x in s) or not any(x.isdigit() for x in s):
                s = ''.join(random.choices(string.ascii_letters + string.digits, k = 8))

            return s

        def getTimeLeft(self):
            return self.timeLeft, divmod(self.timeLeft, 60)

        def countdown(self):
            while self.timeLeft > 0 and not self.stop:
                time.sleep(1)
                self.timeLeft -= 1

            if not self.stop:
                self.active = False
                if self.message:
                    self.outer.address(self.message, self.outer.ttsOn)

                if self.method:
                    try:
                        out = self.method(*self.args)
                        if out:
                            self.outer.address(out, self.outer.ttsOn)
                    except Exception as e:
                        print("Timer ID: '" + self.timerID + "' failed. Unable to fulfill request due to '" + str(e) + "' Error.")
                        self.outer.address("Timer ID: '" + self.timerID + "' failed. Unable to fulfill request due to '" + str(e) + "' Error.", self.outer.ttsOn)


        def stopTimer(self):
            self.active = False
            self.stop = True

        def addTime(self, moreTime):
            self.timeLeft += moreTime

    def greet(self):
        self.address("Welcome, awaiting input.", self.ttsOn)

    def openDebug(self):
        self.debugWin = tk.Toplevel(self.master)
        self.debugWin.title("Debug")
        self.debugWin.minsize(300,500)
        # self.debugWin.geometry("300x500")
        # self.debugWin.attributes('-topmost', 1)
        # print(self.debugWin.winfo_screenwidth(), self.debugWin.winfo_screenheight())

        # self.debSet()
        self.debugWin.bind('<Escape>', self.debClose)
        self.debugWin.protocol("WM_DELETE_WINDOW", self.debClose)

        self.debCheck1 = tk.Checkbutton(self.debugWin, text="Print Log", variable=self.var1, command=self.debSet)#checkbuttons for the debug settings
        self.debCheck1.pack()

        self.debCheck2 = tk.Checkbutton(self.debugWin, text="Classification", variable=self.var2, command=self.debSet)
        self.debCheck2.pack()

        self.debCheck3 = tk.Checkbutton(self.debugWin, text="Chatbot Debug", variable=self.var3, command=self.debSet)
        self.debCheck3.pack()

        self.debCheck4 = tk.Checkbutton(self.debugWin, text="Save Log for the Current Session", variable=self.var4, command=self.debSet)
        self.debCheck4.pack()

        if self.logDeb:
            self.debCheck1.select()

        if self.classifDeb:
            self.debCheck2.select()

        if self.chatDeb:
            self.debCheck3.select()

        if self.saveLog:
            self.debCheck4.select()

        self.debugBox = tk.Text(self.debugWin, wrap=tk.WORD)#text box for debug info
        self.debugBox.pack(padx=10, pady=10, expand=1, fill=tk.BOTH)

        self.debugOpen = True

    def debSet(self):
        self.logDeb = self.var1.get()
        self.classifDeb = self.var2.get()
        self.chatDeb = self.var3.get()
        self.saveLog = self.var4.get()
        # self.classifSty = bool(self.var4.get())
        # print("classifTyp:", self.drop.get(), self.classifTyp.get())
        # print(self.saveLog)

    def debClose(self, test = None):
        # self.logDeb = False
        # self.classifDeb = False
        # self.chatDeb = False
        # self.classifSty = False

        self.logDeb = self.var1.get()
        self.classifDeb = self.var2.get()
        self.chatDeb = self.var3.get()
        self.saveLog = self.var4.get()

        self.debugOpen = False

        self.debugWin.destroy()#close the debug window

    def mainClose(self, test = None):
        if self.timers:
            [x.stopTimer() for x in self.timers]
            # print([x for x in self.timers if x.active])

        sessionEndTime = datetime.datetime.now(tz = self.timeZone)
        duration = sessionEndTime - self.sessionStartTime
        self.log['sessionStartTime'] = str(self.sessionStartTime)
        self.log['sessionEndTime'] = str(sessionEndTime)
        self.log['sessionDuration'] = str(duration) + " / " + str(duration.total_seconds()) + " seconds"
        # if self.saveLog:
        if self.saveLog and self.log['log']:
            # fileName = 'log' + str(len([f for f in os.listdir("logs1/") if os.path.isfile(os.path.join("logs1/", f))])) # gets the amount of files in the folder
            fileName = str(self.sessionStartTime.strftime("%Y-%m-%d(%H.%M.%S)")) # time-based 'logs/2021-12-20(09.13.10).json'
            with open('logs1/' + fileName + '.json', 'w') as fp:
                json.dump(self.log, fp)

        self.settings["spokenFeedback"] = self.ttsOn
        self.settings["printChatDebug"] = self.chatDeb
        self.settings["printClassification"] = self.classifDeb
        self.settings["printLog"] = self.logDeb
        # self.settings["log"] = self.log
        self.settings["debugOpen"] = self.debugOpen
        self.settings["saveLog"] = self.saveLog
        self.settings["lastInput"] = self.lastIn

        with open('settings1.json', 'w') as fp:
            json.dump(self.settings, fp)#save settings to file

        self.master.destroy()#close the main window

    def address(self, txt="", speak=True):
        txt = str(txt)
        # self.txtBox.config(state='normal')
        self.txtBox.insert('end', "Bot: " + txt + "\n")#add text to textbox
        self.txtBox.see(tk.END)#scroll to bottom
        # self.txtBox.config(state='disabled')
        self.log['log'].append({'speaker': "ASSISTANT", 'text': txt, 'tts': self.ttsOn, 'time': str(datetime.datetime.now())})#add entry to the log
        if speak:
            # self.engine.say(txt)
            # self.engine.runAndWait()

            filename = 'speech.mp3'
            chunk = 1024
            self.engine.save_to_file(txt, filename)
            self.engine.runAndWait()

            # wf = wave.open(filename, 'rb')
            with wave.open(filename, 'rb') as wf:
                p = pyaudio.PyAudio()

                # Open a .Stream object to write the WAV file to
                stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True # indicates the sound will be played rather than recorded
                )

                # Read data in chunks
                data = wf.readframes(chunk)

                # Play the sound by writing the audio data to the stream
                while str(data) != "b''" and self.ttsOn:
                    stream.write(data)
                    data = wf.readframes(chunk)

                stream.close()
                p.terminate()

    def ttsToggle(self):
        self.ttsOn = self.ttsCheck.get()
        # if not self.ttsOn:
        #     self.engine.stop()

    def reuse(self, notImp=None):
        self.txtIn.delete(0, tk.END)
        self.txtIn.insert(tk.INSERT, self.lastIn)

    def inputClear(self, notImp=None):
        self.txtIn.delete(0, tk.END)

    def speechThr(self, test=None):
        ''' run the speech recogition stuff in a separate thread '''
        listen = threading.Thread(target=self.speechInput)
        listen.start()

    def speechInput(self):
        ''' obtain audio from the microphone using sphinx the speech_recognition library '''

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            self.address("Taking speech input...", False)
            audio = r.listen(source)
            # audio = r.listen(source, phrase_time_limit = 3)

        try:
            # sp = r.recognize_sphinx(audio)
            sp = r.recognize_google(audio, language ='en-US')

            self.txtIn.delete(0, tk.END)
            self.txtIn.insert(tk.INSERT, sp)
        except sr.UnknownValueError:
            self.address("Could not understand audio.", False)
            print("Could not understand audio.")
        except sr.RequestError as e:
            self.address("Sphinx error; {0}".format(e), False)
            print("Error; {0}".format(e))

    def findNOpen(self, app):
        '''find the specified executable file, if it exists'''
        loc = None

        if os.path.isfile(app):
            loc = os.path.abspath(app)

        if not loc:
            posLocs = []
            for root, dirs, files in os.walk(r'C:\\'):
                if app in files:
                    posLocs.append(os.path.abspath(os.path.join(root, app)))

            loc = sorted(posLocs, key=len)[0]

        try:
            subprocess.Popen(loc)
            self.address("Successfully opened: " + app, self.ttsOn)
        except Exception as e:
            print(e)
            self.address("Failed to open " + app + " due to " + str(e), " error.", self.ttsOn)

    def send(self, test = None):
        ''' processing the input from the text box '''
        inTxt = self.txtIn.get() # gets the contents of the input box
        self.txtIn.delete(0, tk.END) # clears the contents of the input box
        out = None

        try:
            intEnt = intEntFilter.intNEnt(inTxt, self.lastClass)
            if self.classifDeb:
                print(intEnt)
                if self.debugOpen:
                    self.debugBox.insert('end', str(intEnt) + "\n")
        except Exception as e:
            print(e)
            if self.classifDeb:
                intEnt = {"intent": None, "subInt": None, "timing": None}
                if self.debugOpen:
                    self.debugBox.insert('end', str(intEnt) + "\n")
            out = "Failed due to: " + str(e)

        # adds the input to the log txt box
        # self.txtBox.config(state='normal')
        self.txtBox.insert('end', "User: " + inTxt + "\n")
        self.txtBox.see(tk.END)  # autoscroll
        # self.txtBox.config(state='disabled')

        # saves the input and classification to the log list
        self.log['log'].append({'speaker': "USER", 'text': inTxt, 'intEnt': intEnt, 'time': str(datetime.datetime.now())})#save input to chatlog

        if intEnt:
            if intEnt['timing']:
                if intEnt['intent'] == 'weather':
                    timeSpan = intEnt['timing']['days'] if intEnt['timing']['elapsed'] else None
                    if not timeSpan:
                        timeSpan = intEnt['timing']['time'] if intEnt['timing']['time'] else timeSpan
                    out = "You wanted weather for " + str("Here" if not intEnt['location'] else intEnt['location']) + " for the next " + str(timeSpan) + " days."

                elif intEnt['intent'] == 'smarthouse':
                    if intEnt['subInt'] == 'change_state':
                        out = intEnt['room'] + " " + intEnt['appliance'] + " " + str(intEnt['state']) + " " + str(intEnt['value']) + " " + str(intEnt['timing'])
                        # smarthouse.changeState(intEnt['room'], intEnt['appliance'], intEnt['state'], intEnt['value'])
                    elif intEnt['subInt'] == 'check_state':
                        out = intEnt['room'] + " " + intEnt['appliance'] + " " + intEnt['state']
                        # out = smarthouse.recallState(intEnt['room'], intEnt['appliance'], intEnt['state'])

                elif intEnt['intent'] == 'time':
                    if intEnt['subInt'] == 'timeTil':
                        diff = timeStuff.fromNow(intEnt['timing']['date'], intEnt['units'][0])
                        if diff >= 0:
                            out = "There are " + str(abs(diff)) + " " + intEnt['units'][0] + " until " + intEnt['timing']['date'] + "."
                            # if round(random.random()) == 0:
                            #     out = intEnt['timing']['date'] + " is " + str(abs(diff)) + " " + intEnt['units'][0] + " from now."
                            # else:
                            #     out = "There are " + str(abs(diff)) + " " + intEnt['units'][0] + " until " + intEnt['timing']['date'] + "."
                        else:
                            out = intEnt['timing']['date'] + " was " + str(abs(diff)) + " " + intEnt['units'][0] + " ago."
                        
                    elif intEnt['subInt'] == 'startTimer':
                        sec = 0
                        for i in intEnt['timing']:
                            if i == "seconds":
                                sec += intEnt['timing'][i]
                            elif i == "minutes":
                                sec += intEnt['timing'][i] * 60
                            elif i == "hours":
                                sec += intEnt['timing'][i] * 3600

                        mess = intEnt['message'] if intEnt['message'] else "Time's up!"
                        t = self.timer(self, t = sec, message = mess)
                        if self.timers:
                            while any(i.timerID == t.timerID for i in self.timers):
                                del t
                                t = self.timer(self, t = sec, message = mess)

                        self.timers.append(t)

                        out = "Starting a timer for "
                        # l = intEnt['units'] if intEnt['units'] else ['seconds']
                        l = intEnt['units']
                        if len(l) > 1:
                            for i, x in enumerate(l):
                                if i < len(l) - 1:
                                    out += str(intEnt['timing'][x]) + " " + x + ", "
                                elif i == len(l) - 1:
                                    out += "and " + str(intEnt['timing'][x]) + " " + x + "."
                        else:
                            out += str(intEnt['timing'][l[0]]) + " " + l[0] + "."
                        out += " For a total of " + str(sec) + " seconds. The ID for it is " + t.timerID + "."

                    elif intEnt['subInt'] == 'date':
                        current = datetime.datetime.now()
                        if intEnt['units']:
                            if len(intEnt['units']) == 2:
                                # out = "You wanted the " + intEnt['units'][0] + " of the " + intEnt['units'][1] + "."
                                if intEnt['units'][0] == "day":
                                    if intEnt['units'][1] == "week":
                                        out = "Today is " + current.strftime("%A") + "."
                                    
                                    elif intEnt['units'][1] == "month":
                                        out = "Today is the " + current.strftime("%d") + "th day of the month."
                                    
                                    elif intEnt['units'][1] == "year":
                                        out = "Today is the " + current.strftime("%j") + "th day of the year."
                                
                                elif intEnt['units'][0] == "week":
                                    if intEnt['units'][1] == "year":
                                        out = "It is the " + current.strftime("%W") + "th week of the year."
                                else:
                                    out = "Umm..."
                            
                            elif len(intEnt['units']) == 1:
                                if intEnt['units'][0] == "day":
                                    out = "Today is " + current.strftime("%A") + ", " + current.strftime("%B") + " " + str(current.day) + ", " + str(current.year) + ", or " + current.strftime("%Y/%m/%d") + "."
                                
                                elif intEnt['units'][0] == "week":
                                    out = "It is " + str(current.year) + "."
                                
                                elif intEnt['units'][0] == "month":
                                    out = "It is the " + current.strftime("%W") + "th week of the year."
                                
                                elif intEnt['units'][0] == "year":
                                    out = "It is " + str(current.year) + "."
                            else:
                                out = "Man, I'm not gonna write code to do that."

                        elif intEnt['timing'] and 'time' in intEnt['timing']:
                            if intEnt['timing']['time'] == "today":
                                out = "Today is " + current.strftime("%A") + ", " + current.strftime("%B") + " " + str(current.day) + ", " + str(current.year) + ", or " + current.strftime("%Y/%m/%d") + "."

                            elif intEnt['timing']['time'] == "tomorrow":
                                current += datetime.timedelta(days=1)
                                out = "Tomorrow is " + current.strftime("%A") + ", " + current.strftime("%B") + " " + str(current.day) + ", " + str(current.year) + ", or " + current.strftime("%Y/%m/%d") + "."

                            elif intEnt['timing']['time'] == "yesterday":
                                current += datetime.timedelta(days=-1)
                                out = "Yesterday was " + current.strftime("%A") + ", " + current.strftime("%B") + " " + str(current.day) + ", " + str(current.year) + ", or " + current.strftime("%Y/%m/%d") + "."
                        else:
                            out = "Today is " + current.strftime("%A") + ", " + current.strftime("%B") + " " + str(current.day) + ", " + str(current.year) + ", or " + current.strftime("%Y/%m/%d") + "."

                elif intEnt['intent'] == 'open_app':
                    sec = 0
                    for i in intEnt['timing']:
                        if i == "seconds":
                            sec += intEnt['timing'][i]
                        elif i == "minutes":
                            sec += intEnt['timing'][i] * 60
                        elif i == "hours":
                            sec += intEnt['timing'][i] * 3600

                    out = "Attempting to open '" + intEnt['commonName'] + "' in "

                    # if 'years' in intEnt['timing'].keys():
                    if intEnt['timing']['elapsed']:
                        # print([x for x in intEnt['timing'].keys() if intEnt['timing'][x] and type(intEnt['timing'][x]) == int])
                        l = [x for x in intEnt['timing'].keys() if intEnt['timing'][x] and type(intEnt['timing'][x]) == int]
                        if len(l) > 1:
                            for i, x in enumerate(intEnt['timing']):
                                if type(intEnt['timing'][x]) == int and intEnt['timing'][x] > 0:
                                    if i < len(intEnt['timing'].keys()) - 1:
                                            out += str(intEnt['timing'][x]) + " " + x + ", "
                                    elif i == len(intEnt['timing'].keys()) - 1:
                                        out += "and " + str(intEnt['timing'][x]) + " " + x + "."
                        else:
                            out += str(intEnt['timing'][l[0]]) + " " + l[0] + "."

                        if intEnt['program']:
                            t = self.timer(self, t = sec, message="Now opening: '" + intEnt['commonName'] + "'.", method = subprocess.Popen, args = (intEnt['program'],))
                        else:
                            if ".exe" in intEnt['commonName']:
                                t = self.timer(self, t = sec, message="Now opening: '" + intEnt['commonName'] + "'.", method = self.findNOpen, args = (intEnt['commonName'],))
                            else:
                                t = self.timer(self, t = sec, message="Now opening: '" + intEnt['commonName'] + "'.", method = self.findNOpen, args = (intEnt['commonName'].replace(" ", "") + ".exe",))
                        
                        out += " The ID for this timer is '" + t.timerID + "'."
                        self.timers.append(t)

            else:
                if intEnt['intent'] == 'weather':
                    #should add something for the subintent: temperature, precipitation, and humidity
                    try:
                        w = weather_retrieval.weatherGrab2(intEnt['location'])
                        out = "It is " + str(w[0]) + " and " + str(w[1]) + ", with wind " + str(w[2]) + " and " + str(w[3]) + " humid in " + str(w[4]) + ".\nWeather information sourced from Weather.gov; Last Updated: " + str(w[5])
                    except Exception as e:
                        print(e)
                        out = "Failed to get weather due to '" + str(e) + "' Error."

                elif intEnt['intent'] == 'smarthouse':
                    if intEnt['subInt'] == 'change_state':
                        out = intEnt['room'] + " " + intEnt['appliance'] + " " + str(intEnt['state']) + " " + str(intEnt['value'])
                        # smarthouse.changeState(intEnt['room'], intEnt['appliance'], intEnt['state'], intEnt['value'])
                    elif intEnt['subInt'] == 'check_state':
                        out = intEnt['room'] + " " + intEnt['appliance'] + " " + intEnt['state']
                        #out = smarthouse.recallState(intEnt['room'], intEnt['appliance'], intEnt['state'])

                elif intEnt['intent'] == 'math':
                    try:
                        out = "The answer is: " + str(mathParse.parsEval(inTxt)) + "."
                    except Exception as e:
                        print(e)
                        out = "Failed due to: '" + str(e) + "' Error."

                elif intEnt['intent'] == 'conversation':#chatbot function
                    # out = chatParser.respond(inTxt)
                    if self.chatDeb:
                        self.chatDebDet = chatParser.respondWord(inTxt, self.chatDeb)
                        out = self.chatDebDet[0]
                    else:
                        out = chatParser.respondWord(inTxt)

                elif intEnt['intent'] == 'search':#search the specified term on a search engine(the user can specify an engine to use)
                    if intEnt['engine']:#if a search engine is specified, use that one(opens the page in browser)
                        out = "Searching on " + intEnt['engine'] + ": " + intEnt['term']
                        webSearch.search(intEnt['term'], intEnt['engine'])
                    else:
                        ddgRes = webSearch.ddgSrch(intEnt['term'])#if an engine is not, try duckduckgo instant answer api
                        if ddgRes[0]:
                            # self.address("Using DuckDuckGo's Instant Answer API:", self.ttsOn)
                            out = "Using DuckDuckGo's Instant Answer API:\n" + ddgRes[0] + " Sourced from " + ddgRes[1] + "."
                        else:#if ddg api doesn't return anything, just search on google(opens page in browser)
                            out = "Searching on Google: " + intEnt['term']
                            webSearch.search(intEnt['term'])

                elif intEnt['intent'] == 'open_app':
                    out = "Attempting to open: " + intEnt['commonName']

                    if intEnt['program']:
                        try:
                            # subprocess.call([intEnt['program']])
                            # subprocess.Popen(intEnt['program'])
                            subprocess.Popen(intEnt['program'], shell=True)
                            # subprocess.Popen(intEnt['program'], shell=True).wait()
                        except Exception as e:
                            print(e)
                            out = "Failed to open " + intEnt['commonName'] + " due to '" + str(e), "' Error."
                    else:
                        if ".exe" in intEnt['commonName']:
                            findNOp = threading.Thread(target=self.findNOpen, args=(intEnt['commonName'],)) # runs the function for locating a file's path in a separate thread
                        else:
                            findNOp = threading.Thread(target=self.findNOpen, args=(intEnt['commonName'].replace(" ", "") + ".exe",))

                        findNOp.start()

                elif intEnt['intent'] == 'open_site':
                    if intEnt['website']:
                        if intEnt['browser']: # if a browser is specified, attempt to use that one
                            try:
                                controller = webbrowser.get(intEnt['browser']) # make a controller for the specified browser
                                controller.open(intEnt['website']) # open page with controller
                                out = "Opening: " + intEnt['website'] + " in " + intEnt['browser'] + "."
                            except Exception as e:
                                print(e)
                                out = "Unable to open '" + intEnt['website'] + "' in '" + intEnt['browser'] + "' due to: '" + str(e) + "' Error. Opening in default browser."
                                webbrowser.open(intEnt['website']) # open page in default browser
                        else: # if no browser if specified, use default browser
                            webbrowser.open(intEnt['website']) # open page in default browser
                            out = "Opening: " + intEnt['website'] + " using default browser."
                    else:
                        out = "Please specify a website to open."

                elif intEnt['intent'] == 'time':
                    x = datetime.datetime.now() # get current time

                    if intEnt['subInt'] == 'currentTime':
                        out = "The time is: " + x.strftime("%I:%M %p") # use the time with 12 hour format
                    
                    elif intEnt['subInt'] == 'date':
                        out = "Today is " + x.strftime("%A") + ", " + x.strftime("%B") + " " + str(x.day) + ", " + str(x.year) + ", or " + x.strftime("%Y/%m/%d") + "."
                    
                    elif intEnt['subInt'] == 'checkTimer': # i should figure out a way to add a thing for checking how many active timers there are
                        # if self.timers and all(x.timeLeft > 0 for x in self.timers):
                        if self.timers:
                            if len(self.timers) == 1:
                                out = "There is only one active timer. The time left is " + str(self.timers[0].timeLeft) + " seconds."
                            elif len(self.timers) > 1:
                                checkedTimer = None
                                if intEnt['ID']:
                                    [checkedTimer := i for i in self.timers if i.timerID == intEnt['ID']]
                                    if checkedTimer:
                                        out = "The time left on the timer with the ID '" + intEnt['ID'] + "' is " + str(checkedTimer.timeLeft) + " seconds."
                                    else:
                                        out = "There is no timer with the ID '" + intEnt['ID'] + "'."
                                elif intEnt['IDTerm']:
                                    for i in self.timers:
                                        if intEnt['IDTerm'] in i.message:
                                            checkedTimer = i
                                            break
                                    
                                    if checkedTimer:
                                        out = "The time left on the timer related to '" + intEnt['IDTerm'] + "' is " + str(checkedTimer.timeLeft) + " seconds."
                                    else:
                                        out = "There are no timers with a message containing: '" + intEnt['IDTerm'] + "'."
                        else:
                            out = "There are no active timers."

                    elif intEnt['subInt'] == 'endTimer':
                        # if self.timers and all(x.timeLeft > 0 for x in self.timers):
                        if self.timers:
                            if len(self.timers) == 1:
                                out = "Ending the only one active timer."
                            elif len(self.timers) > 1:
                                timersIndex = None
                                if intEnt['ID']:
                                    if intEnt['ID'] == "all":
                                        [x.stopTimer() for x in self.timers]
                                        out = "Stopping all active timers."
                                    else:
                                        [timersIndex := i for i, n in enumerate(self.timers) if n.timerID == intEnt['ID']]
                                        if timersIndex:
                                            out = "Ending timer with ID '" + intEnt['ID'] + "'."
                                            self.timers[timersIndex].stopTimer()
                                            del self.timers[timersIndex]
                                        else:
                                            out = "There is no timer with the ID '" + intEnt['ID'] + "'."
                                elif intEnt['IDTerm']:
                                    for i, n in enumerate(self.timers):
                                        if intEnt['IDTerm'] in n.message:
                                            timersIndex = i
                                            break
                                    
                                    if timersIndex:
                                        self.timers[timersIndex].stopTimer()
                                        del self.timers[timersIndex]
                                        out = "Ending the timer related to '" + intEnt['IDTerm'] + "'."

                                    else:
                                        out = "There are no timers with a message containing: '" + intEnt['IDTerm'] + "'."
                        else:
                            out = "There are no active timers."
                    
                elif intEnt['intent'] == 'funfact':
                    if intEnt['subject']:
                        out = "You want a fact about " + intEnt['subject'] + "."
                    else:
                        try:
                            out = random.choice(funfact.randPrefixes) + funfact.randFac()
                        except Exception as e:
                            out = "Failed due to: '" + str(e) + "' Error."

                elif intEnt['intent'] == 'random':
                    if intEnt['subInt'] == 'randomNumber':
                        low = intEnt['low'] if intEnt['low'] else 1 # default should be between 1 and 10
                        high = intEnt['high'] if intEnt['high'] else 10
                        n = randGen.genRandNum(intEnt['rolls'], low, high)

                    elif intEnt['subInt'] == 'dice':
                        sides = intEnt['sides'] if intEnt['sides'] else 6
                        n = randGen.dice(intEnt['rolls'], sides)

                    elif intEnt['subInt'] == 'coinFlip':
                        n = randGen.coin(intEnt['rolls'])

                    if len(n) == 1:
                        out = "Here you go: " + str(n[0])
                    else:
                        out = "Here you go: " + str(n)
                        
                elif intEnt['intent'] == 'music':
                    if intEnt['subInt'] == 'playMusic':
                        link = tube.tube(intEnt['term'])[0]
                        out = "Attempting to play: " + intEnt['term'] + " at " + link

                        # apparently htmlsession isn't very threading friendly
                        # music = threading.Thread(target=tube.tube, args=(intEnt['term'],))
                        # music.start()
                        # out = "Attempting to play: " + intEnt['term']
                    elif intEnt['subInt'] == 'lyrics':
                        try:
                            lyr = tube.lyric(intEnt['term'])[0].replace("\n", "\n\t")
                            out = "Here are the lyrics for '" + intEnt['term'] + "':\n\t" + lyr
                        except Exception as e:
                            out = "Unable to get the lyrics for " + intEnt['term'] + " due to '" + str(e) + "' Error."

                elif intEnt['intent'] == 'help':
                    # out = "I can do a few things. I can tell you about the weather. I can change or check things around the house. I can do math. I can search something for you. I can have a conversation with you. I can open a program for you. I can open websites. I can tell you a fun fact and I can tell you the time."
                    
                    # with open('train.json', 'r') as fp:
                    #     trainData = json.load(fp)  # load up the training data from the json file
                    
                    # out = "I have the following functions:\n"
                    # for i in trainData["intent"]:
                    #     out += "\t" + i + "\n"

                    # out += "and subfunctions:\n"
                    # for i in trainData["subIntent"]:
                    #     out += "\t" + i + "\n"
                    out = self.helpText

        # self.log.append({'speaker': "Bot", 'text': out, 'tts': self.ttsOn})
        
        talk = threading.Thread(target=self.address, args=(out, self.ttsOn,)) # does the text to speech in a separate thread
        talk.start()
        self.lastIn = inTxt
        self.lastClass = intEnt
        # print(self.lastClass)
        
        if self.logDeb:
            print(self.log['log'])
            if self.debugOpen:
                self.debugBox.insert('end', str(self.log['log']) + "\n")

        if self.chatDeb and intEnt['intent'] == 'conversation':
            print("Possible Statements(top 3):", self.chatDebDet[1], "Possible Responses to the Most Likely Statement:", self.chatDebDet[2])
            if self.debugOpen:
                self.debugBox.insert('end', "Possible Statements(top 3): " + str(self.chatDebDet[1]) + "\nPossible Responses to the Most Likely Statement: " + str(self.chatDebDet[2]) + "\n")


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = gui(root)

    root.mainloop()

'''
I could add a "saveLogAfterSession" setting/button, that would reset each time it's opened
    it would save the log for the current session in a file(in a "logs" folder) when the program is closed
    this would allow me to save the log for the any given session, while not having to keep the logs for every session(or keep them together in one file)
        basically, it gives me a choice
    should probably be a checkButton on the debug menu
    DONE!
    I made it so that it saves the "sessionStartTime" and "sessionEndTime" as well as the log for the session
    I could try to add a "sessionLength" thing
        would require finding the difference between the "sessionStartTime" and the "sessionEndTime"
        not too sure about what unit I would use, probably minutes?
        DONE!
    
    The logs currently have the ["log0.json", "log1.json", "log2.json",...] naming convention
        I like this but, I think time-string-based names might work a bit better(at least for certain situations)
        this is because, if I want to find the log for a current date/time, I currently have to open each individual log and check the dates on them
        DONE!


I think the next iteration/version of this will be made more with background activity in mind?
    for example, this version is something that you have open when you need to do something and end up closing when you're done
    of course, you could leave it open the whole computer session and use it when you want, but I haven't done that nor do I think I'm likely to
    
    so for the next one, I want to have it able to run in the background more
    this would mean
        having a GUI for when it needs to be called to the foreground, but it would mostly just run in a largely unintrusive way
            I might add themes?
            add an audio visualiser, like I wanted?
            I'll almost definitely switch to a different GUI library
        having the speech-to-text set up in a better/different way
            have it listen for a "call word", so that you can call the assistant by name(or nickname) when you want to have it perform an action
            and maybe have it wait a period of time after a request is inputed in case there is a new request without the "wake word"/"call word"
        have the logs system set up differently
            for this version, I have it save the log from each session
            in the new proposed version, the program would be running the whole time the device was on(unless intentionally turned off)
            maybe the log could be saved when the device is turned off or the program is stopped
            or it could be saved periodically(or when something happens like an input)
            or both? cause, why not?
        perhaps there could be a notification system
            a notification tab? to cancel and dismiss notifications
            but also notifications that pop up on the screen while it's in the background
        a lot of these things will require multithreading(or parallel processing)

    technically it would be the 4th major version of the program(currently on something like 3.26.4)(https://stackoverflow.com/questions/65718/what-do-the-numbers-in-a-version-typically-represent-i-e-v1-9-0-1)
        i feel like at some point I'll probably switch languages(or maybe make a different version of the project in a different language)

    GUI Libraries?
        pass


help text?
    i could try making an actual text thing for the help command to output, instead of outputing the intents and sub-intents

    "I have the following functions:\n\tweather\n\tsmarthouse\n\tmath\n\tsearch\n\tconversation\n\topen_app\n\topen_site\n\ttime\n\thelp\n\tfunfact\n\trandom\n\tmusic\n\tuseLast\nand subfunctions:\n\tchange_state\n\tcheck_state\n\tforecast\n\ttemperature\n\tprecipitation\n\thumidity\n\trandomNumber\n\tdice\n\tcoinFlip\n\tplayMusic\n\tlyrics\n\tcurrentTime\n\tstartTimer\n\tcheckTimer\n\tendTimer\n\tdate\n\ttimeTil\n\tNone\n"

    help = """
        I am a Virtual Assistant.
        I have a number of functions.
            I can conversate(not well),
                "Hello!"
                "How are you?"
            I can tell you about the weather,
                "How's the weather?",
                "Is it humid in Dallas?",
                "How does the weather look for the next three days?"
            I can help you with things around the house(not actually),
                "Turn on the lights in the kitchen",
                "Set the oven temp to 450 in 5 minutes",
                "Turn off all the lights at 6:30"
            I can do math for you(like basic arithmetic, sometimes),
                "What is two plus two?",
                "eight divided by 4",
                "What is 350 times 29?"
            I can make a search on the web for you,
                "Search on Google cake recipes",
                "Search Yahoo for popular tech companies",
                "How many satelites are currently in orbit?"
            I can open apps on your computer,
                "Open Discord in seven minutes",
                "Open FireFox",
                "Please, start up settings"
            I can open websites for you,
                "Go to Youtube",
                "Open Google",
                "Go to https://www.wired.com/"
            I can tell you the time, set timers for you, and tell you long until a certain date,
                "How many days are there until January 19",
                "What time is it?",
                "Remind me in an hour to water the plants"
            I can tell you a funfact(currently just random, specified topics aren't used),
                "Tell me a funfact",
                "Do you know any cat facts?",
                "Tell me a fact about the ISS"
            I can generate random numbers,
                "Give me two random numbers between five and fifteen",
                "Roll a 20 sided die, please",
                "Flip a coin"
            And I can play music or grab lyrics from the web.
                "Play Blinding Lights by The Weeknd",
                "What are the lyrics to Woman by Doja Cat?",
                "Put on 505 by Arctic Monkeys"
    """
        or
    help = """
        I am a Virtual Assistant.\n
        I have a number of functions.\n
            \tI can conversate(not well),\n
                \t\t"Hello!",\n
                \t\t"How are you?"\n
            \tI can tell you about the weather,\n
                \t\t"How's the weather?",\n
                \t\t"Is it humid in Dallas?",\n
                \t\t"How does the weather look for the next three days?"\n
            \tI can help you with things around the house(not actually),\n
                \t\t"Turn on the lights in the kitchen",\n
                \t\t"Set the oven temp to 450 in 5 minutes",\n
                \t\t"Turn off all the lights at 6:30"\n
            \tI can do math for you(like basic arithmetic, sometimes),\n
                \t\t"What is two plus two?",\n
                \t\t"eight divided by 4",\n
                \t\t"What is 350 times 29?"\n
            \tI can make a search on the web for you,\n
                \t\t"Search on Google cake recipes",\n
                \t\t"Search Yahoo for popular tech companies",\n
                \t\t"How many satelites are currently in orbit?"\n
            \tI can open apps on your computer,\n
                \t\t"Open Discord in seven minutes",\n
                \t\t"Open FireFox",\n
                \t\t"Please, start up settings"\n
            \tI can open websites for you,\n
                \t\t"Go to Youtube",\n
                \t\t"Open Google",\n
                \t\t"Go to https://www.wired.com/"\n
            \tI can tell you the time, set timers for you, and tell you long until a certain date,\n
                \t\t"How many days are there until January 19",\n
                \t\t"What time is it?",\n
                \t\t"Remind me in an hour to water the plants"\n
            \tI can tell you a funfact(currently just random, specified topics aren't used),\n
                \t\t"Tell me a funfact",\n
                \t\t"Do you know any cat facts?",\n
                \t\t"Tell me a fact about the ISS"\n
            \tI can generate random numbers,\n
                \t\t"Give me two random numbers between five and fifteen",\n
                \t\t"Roll a 20 sided die, please",\n
                \t\t"Flip a coin"\n
            \tAnd I can play music or grab lyrics from the web.\n
                \t\t"Play Blinding Lights by The Weeknd",\n
                \t\t"What are the lyrics to Woman by Doja Cat?",\n
                \t\t"Put on 505 by Arctic Monkeys"\n
    """
    
    Boom! DONE!
    I made it a variable for the whole class/object
    This now means that when I add a new function I'll have to add text to the helpText string

    I could also make it so that the help command checks for a specified term?
        so that you could do "help music" or "help weather"
        it would have a corresponding help message for each, and could give examples(random examples from train.json)?
        this would require me writing custom help messages for each one


finally figured it out how to make the text-to-speech so that it can be interrupted
    I tried a number of things
        engine.stop() if the tts was turned off
        I added a speaking boolean and checked if the tts was active and being turned off
        I tried using the onWord, onStart, and onEnd function connect stuff

    what actually worked was saving the tts to a file and playing it using pyaudio
        it only plays audio if their is more audio to play *and* tts is set to on
        this means that if the ttsOn boolean is set to False while the tts audio is playing, it will stop


having troubles with the audio visualiser
    I think using Librosa to get the fft and spectrum analysis stuff is a good idea
    if I switch to pyqt for the gui, I could just use pyqtgraph for the visualization
    if not I could use the tkinter canvas, or matplotlib(though, there are some concerns with framerate)

    I wanted to try to make one that is circular, similar to the one I made with p5.js(https://openprocessing.org/sketch/1125924)
    function custCircSpec() {
        fill(100);
        //smooth();
        let angle = 360 / spectrum.slice(0, specSidNumb).length;
        //let level = amplitude.getLevel();
        let ciR = 75;
        let maxR = 100;
        beginShape();
        for (let i = 0; i < spectrum.slice(0, specSidNumb + 1).length; i++) {
            let x = cos(radians(i * angle)) * (map(spectrum[i], 0, 255, ciR + map(level, 0, 1, 0, 120), maxR + map(level, 0, 1, 0, 120)));
            let y = sin(radians(i * angle)) * (map(spectrum[i], 0, 255, ciR + map(level, 0, 1, 0, 120), maxR + map(level, 0, 1, 0, 120)));
            vertex(x + 250, y + 250);
        }
        //vertex(cos(radians(0)) * (map(spectrum[0], 0, 255, ciR + map(level, 0, 1, 0, 120), maxR + map(level, 0, 1, 0, 120))) + 250, sin(radians(0)) * (map(spectrum[0], 0, 255, ciR + map(level, 0, 1, 0, 120), maxR + map(level, 0, 1, 0, 120))) + 250);
        endShape(CLOSE);

        circle(250, 250, 125 + map(level, 0, 1, 0, 120));
    }

    an idea I has was to make it built into the tts function
        there could be settings or multiple presets(or the ability to save custom themes)
        it should be able to be turned on or off
            also there should be an idle animation or something for when it isn't active


revamp the math?
    considering making the math function better/what I wanted it to be

    I wanted it to be able to handle more complex stuff like area and circumfrence stuff


wake word?
    it should be have a constant voice rec stream(i.e. be listening) and check for the wake word
        something I still haven't figured out yet

    have a part of the settings menu in the new gui where you can edit wake words(add/remove/change)?
        have an option to have it listen for it's given name as a wake word?
            "Olive", "Hey Olive", "Excuse me, Olive?"

    have a function that allows the user to add a new wake word?
        "Hey Olive, add a new wake word"
        "What would you like the new wake word to be?"
        "<new wake word/phrase here>"


save the recent tts audio files?
    could be good like the logs
        though I don't think I'd want to save every single one
        I'd probably set it up to remove the older ones after a set amount of time

    it could save resources?
        if the user wants the assistant to repeat the last thing said(or what was said prior)
        it could just load up the last audio file instead of generating a completely new one
            "could you say that again",
            "say that again please",
            "repeat that"
'''