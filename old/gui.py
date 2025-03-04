import tkinter as tk
from tkinter import *
# from tkinter import scrolledtext
import commandFilter, chatParser, weather_retrieval, webSearch
import pyttsx3#, os

window = tk.Tk()
window.title('Basic Virtual Assistant')
window.geometry("400x585")
# width, height = 400, 600
# window.geometry(str(width) + "x" + str(height))

lb = 0
def address(txt = "", speak = True):
    global lb
    txt = str(txt)
    # print("Bot: " + txt)
    txtBox.insert(lb, "Bot: " + txt + "\n")
    txtBox.see(END)
    lb += 1
    if speak:
        engine.say(txt)
        engine.runAndWait()

engine = pyttsx3.init()

speak = True
def speakSw():
    global speak
    if speak:
        speak = False
    else:
        speak = True

def send(test = None):
    global lb
    # print(test)
    res = txtIn.get()
    txtIn.delete(0, END)
    # classif = commandFilter.decTrClass(res)
    # classif = commandFilter.knnClass(res)
    classif = commandFilter.lsvcClass(res)
    txtBox.insert(lb, "User: " + res + "\n")
    txtBox.see(END)
    lb += 1
    print(classif)
    out = None
    # speak = True
    if classif == "weather":
        out = weather_retrieval.takeInput(res)
    elif classif == "smarthouse":
        out = ("smarthouse", res)
    elif classif == "math":
        out = ("math", res)
    elif classif == "conversation":
        out = chatParser.respond(res)
    elif classif == "search":
        engines = ["google", "bing", "Google", "Bing"]
        engin = None
        for eng in engines:
            if eng in res:
                engin = eng
        # delim = ["google search", "search google", "search on google", "search bing", "search on bing", "search", "google"]
        # # if [term in x for term in delim]:
        # for term in delim:
        #     if term in x:
        #         x.replace(term, "")
        if engin:
            out = "Searching on " + engin + ": " + res
            webSearch.search(res, engin)
        else:
            results = webSearch.ddgSrch(res)
            if results[0]:
                address("Using DuckDuckGo's Instant Answer API:")
                out = results
            else:
                out = "Searching on Google: " + res
                webSearch.search(res)

    address(out, speak)

opening = tk.Label(text="Welcome, awaiting input:")
# opening.place(x=0, y=0)
opening.place(x=125, y=5)

txtBox = Listbox(window, width=62, height=30)
txtBox.place(x=10, y=30)

# scrollbar = Scrollbar()
# scrollbar.pack(side=RIGHT, fill=Y)
# txtBox.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=txtBox.yview)

txtIn = tk.Entry(window, width=40)
txtIn.place(x=52, y=523)

button1 = tk.Button(text="<send>", width=10, command=send)
button1.place(x=310, y=520)

button2 = tk.Button(text="<tts>", width=5, command=speakSw)
button2.place(x=325, y=550)

window.bind('<Return>', send)
window.bind('<Escape>', quit)
# window.bind('t', speakSw)

# address("Welcome, awaiting input")

txtIn.focus()
window.mainloop()