Basic Virtual Assistant
=======================

Language: _Python_
------------------

2019 - ~2023
------------

  

Project Summary
---------------

The aim of this project was to create a virtual assistant like Siri, Amazon Alexa, or Google Assistant but with the added goal of it being able to converse with its user coherently. By the time I stopped working on it, it had many features including: basic conversation, weather reporting, solving simple math inputs, web search, reporting the time/date, opening websites in a specified browser, opening other apps, funfacts, random number generation, simple alarms/timers, a customizable GUI, saving chatlogs, voice input, and Text-to-speech.

  

Full Features List(As of the Last version)
------------------------------------------

GUI

Using [tkinter](https://docs.python.org/3/library/tkinter.html), a GUI Toolkit for Python. I made changes and added to it over time. In the last version, I added dedicated pages for certain new features I was working on(like the alarm/timer features). When I started reworking the GUI for this version, I decided to use a side menu/tabs style(partly inspired by one of my sketches from the "planning phase" of the whole project). The debug menu/section is one thing that stayed throughout the versions.

  

Voice Input

Using Python's [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/) (Also based in part on example code found at: [https://github.com/Uberi/speech\_recognition/blob/master/examples/background\_listening.py](https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py)). I also added the ability for the user to not only use "Wake Words", but add new ones themselves.

  

Text to Speech

Using [pyttsx3](https://pypi.org/project/pyttsx3/), a Python Text to Speech library

  

Commands
*   Weather: Things like "How hot is it out there?" and "What's the temperature in Atlanta, Georgia"
*   Smarthouse: Was never actually connected to anything. Just a placeholder for such a system. "turn on the lights in the living room", "open the garage door", "dim the lights to 50%", "Is the garage door open?"
*   Math: "What's the square root of 49", "divide 52 by 8", "How many times does eight go into sixty-four evenly"
*   Web Search: The user also had the option to specify the site use for their search(Google, Bing, Yahoo, Yandex, Baidu, even sites like instagram, spotify, youtube, and amazon). "what is the capital of Russia", "google search what is a pangolin"
*   Define Words: "what does verbatim mean?", "can you tell me what tantamount means?"
*   Open Programs: I made a lookup table/file so the user didn't have to specify the full file location. "open firefox", ""
*   Open Websites: Lookup file is also used here for specific terms(though you can still specify the full url, if you wanted/needed to). The user also has the ability to specify the browser to open the site in.
*   Time Commands: "How many days are there until March 1st?", "What time is it?", "What's today's date?", "remind me in half an hour to water the plants outside", "stop that last timer", "how much time is left on the timer?"
*   Funfacts
*   Random Number Generators: random number, coin flip, dice(with amount of sides)
*   Music Commands: When asked to play a song, it would just open it in youtube. "play never gonna give you up by Rick Astley", "what are the lyrics for Kiss Me More by Doja Cat"
*   Help: Would respond with the help text, a list of its functions.
*   Conversational: It would try to "engage is conversation" when not given a command style input.
*   Repeat Command/Do That Again: ""
*   Assistant Settings: "", "", "", ""
*   "Repeat That"
*   "Simon Says"/"Repeat After Me"

  

Key Binds

*   Esc: Minimizes
*   Alt + x: Hard Shutdown
*   Ctrl + r: Soft Restart
*   Ctrl + Shift + r: Hard Restart


Links
-----

### Libraries/APIs/Websites I used

* [uselessfacts API for Funfacts](https://uselessfacts.jsph.pl/)
* [Free Dictionary API](https://dictionaryapi.dev/)
* [Wikipedia Python Library](https://pypi.org/project/wikipedia/)

### Smaller Tests from Along the Way

*   [Link](https://replit.com/@TheRicks2/BisqueEarlyDecagon)
*   [Link](https://replit.com/@TheRicks2/String-InterpolationFormatingConcatenation)
*   [Link](https://replit.com/@TheRicks2/chatLogParser-and-Basic-Response-Idea)
*   [Link](https://replit.com/@TheRicks2/chatterbot-fail)
*   [Link](https://replit.com/@TheRicks2/nerre)
*   [Link](https://replit.com/@TheRicks2/importance-filter-and-memory-thing)
*   [Link](https://replit.com/@TheRicks2/weather-gpe-extr-nltk)
*   [Link](https://replit.com/@TheRicks2/math-string-evaluator)

(Still need to add some things to this...)
