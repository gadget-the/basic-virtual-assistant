import datetime
import json
import os
import random
import re
import string
import subprocess
import sys
import threading
import time
import wave
import webbrowser
import tkinter as tk
from tkinter import colorchooser as cc

import numpy as np
import pyaudio
import pyttsx3
import pytz
import speech_recognition as sr
from tzlocal.win32 import get_localzone_name

import chatParser
import funfact
import intEntFilter
# import smarthouse
import mathParse
import randGen
import timeStuff
import tube
import weather_retrieval
import webSearch


class gui(tk.Frame):
    def __init__(self, master):
        self.master = master

        master.title('Virtual Assistant')
        master.attributes('-fullscreen', True)
        master.protocol("WM_DELETE_WINDOW", self.main_close) # run the closing procedure when the main window is closed by the user
        # master.bind('<Escape>', self.main_close) # change it to alt-x? make it a bit harder to fully shut it down, also have escape minimize the window
        master.bind('<Escape>', lambda event: master.wm_state('iconic')) # minimize main window
        master.bind('<FocusIn>', self.close_pop_out) # i could make a function that checks if extraneous things(pop out, settings, alarms/timers menu) are open and closes each of them
        # keyboard shortcuts
        master.bind('<Alt-x>', self.main_close) # I should make a force stop shortcut that just stops the main window and bypasses the closing procedure
        master.bind('<Control-r>', self.restart)
        master.bind('<Control-R>', lambda event: self.restart(hard_restart=True))

        self.tts_engine = pyttsx3.init() # initialize the tts engine(?)
        self.time_zone = pytz.timezone(get_localzone_name()) # get the timezone of the user

        self.speech_rec_stream = self.speech_recognition_stream(outer_gui=self)
        # self.help_output_text = "Hello!\nI am your Virtual Assistant.\nI have a number of functions.\n\tI can conversate(not well),\n\t\t\"Hello!\"\n\t\t\"How are you?\"\n\tI can tell you about the weather,\n\t\t\"How's the weather?\",\n\t\t\"Is it humid in Dallas?\",\n\t\t\"How does the weather look for the next three days?\"\n\tI can help you with things around the house(not actually),\n\t\t\"Turn on the lights in the kitchen\",\n\t\t\"Set the oven temp to 450 in 5 minutes\",\n\t\t\"Turn off all the lights at 6:30\"\n\tI can do math for you(like basic arithmetic, sometimes),\n\t\t\"What is two plus two?\",\n\t\t\"eight divided by 4\",\n\t\t\"What is 350 times 29?\"\n\tI can make a search on the web for you,\n\t\t\"Search on Google cake recipes\",\n\t\t\"Search Yahoo for popular tech companies\",\n\t\t\"How many satelites are currently in orbit?\"\n\tI can open apps on your computer,\n\t\t\"Open Discord in seven minutes\",\n\t\t\"Open FireFox\",\n\t\t\"Please, start up settings\"\n\tI can open websites for you,\n\t\t\"Go to Youtube\",\n\t\t\"Open Google\",\n\t\t\"Go to https://www.wired.com/\"\n\tI can tell you the time, set timers for you, and tell you long until a certain date,\n\t\t\"How many days are there until January 19\",\n\t\t\"What time is it?\",\n\t\t\"Remind me in an hour to water the plants\"\n\tI can tell you a funfact(currently just random, specified topics aren't used),\n\t\t\"Tell me a funfact\",\n\t\t\"Do you know any cat facts?\",\n\t\t\"Tell me a fact about the ISS\"\n\tI can generate random numbers,\n\t\t\"Give me two random numbers between five and fifteen\",\n\t\t\"Roll a 20 sided die, please\",\n\t\t\"Flip a coin\"\n\tAnd I can play music or grab lyrics from the web.\n\t\t\"Play Blinding Lights by The Weeknd\",\n\t\t\"What are the lyrics to Woman by Doja Cat?\",\n\t\t\"Put on 505 by Arctic Monkeys\"\n"

        with open('settings.json', 'r') as fp:
            self.settings = json.load(fp)

        with open('output-phrases.json', 'r') as fp: # load up the possible output phrase options
            self.output_phrases = json.load(fp)

        # assign settings values to the actual variables
        self.ui_theme = self.settings['visual-style']
        self.color_scheme_presets = self.settings['theme-presets']
        self.tts_on = self.settings['text-to-speech']
        self.volume = self.settings['output-volume']
        self.listen_wake_word = self.settings['listen-for-wake-word']
        self.wake_words = self.settings['wake-phrases']
        self.last_input = self.settings['last-input']
        self.last_output = self.settings['last-output']

        # register browsers
        self.browser_paths = self.settings['browser-paths']
        [webbrowser.register(browser_name, None, webbrowser.BackgroundBrowser(self.browser_paths[browser_name])) for browser_name in self.browser_paths]

        # assign color variables from the saved/loaded color scheme
        self.text_color = self.ui_theme['color-scheme'][0]
        self.primary_background_color = self.ui_theme['color-scheme'][1]
        self.secondary_background_color = self.ui_theme['color-scheme'][2]
        self.tertiary_background_color = self.ui_theme['color-scheme'][3]
        self.quaternary_background_color = self.ui_theme['color-scheme'][4]

        master.config(bg=self.primary_background_color)

        self.timers = []

        # stuff for if it saves the session log
        self.session_start_time = datetime.datetime.now(tz = self.time_zone)
        self.log = {
            "session-start-time": "",
            "session-end-time": "",
            "session-duration": 0,
            "session-log": []
        }

        # default values for certain settings, always the same at start
        self.save_log = True
        self.log_output = False
        self.classification_output = False
        self.chatbot_info_output = False
        
        # assign the tkinter variables from the regular bool variables
        self.listen_wake_word_var = tk.BooleanVar(value=self.listen_wake_word)
        self.log_output_var = tk.BooleanVar(value=self.log_output)
        self.classification_output_var = tk.BooleanVar(value=self.classification_output)
        self.chatbot_info_output_var = tk.BooleanVar(value=self.chatbot_info_output)
        self.save_log_var = tk.BooleanVar(value=self.save_log)
        self.tts_on_var = tk.BooleanVar(value=self.tts_on)

        # custom menu side bar
        # self.menu_bar = tk.Frame(master, bg='red')
        self.menu_bar = tk.Frame(master, bg=self.tertiary_background_color)
        self.menu_bar.pack(side='right', fill='y')
        self.menu_bar.columnconfigure(1, weight=1)
        [self.menu_bar.rowconfigure(x, weight=1) for x in range(7)]

        # menu buttons
        # settings menu button
        self.settings_menu_open = False
        tk.Button(self.menu_bar, text="Settings", command=self.open_settings_menu, justify='center', wraplength=45, foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3).grid(column=1, row=0, padx=5, pady=5, sticky='nsew')

        # text input button
        tk.Button(self.menu_bar, text="Text Input", justify='center', command=self.text_input_toggle, wraplength=45, foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3).grid(column=1, row=1, padx=5, pady=5, sticky='nsew')
        
        # pop out button
        self.pop_out_is_open = False
        tk.Button(self.menu_bar, text="Pop Out Mode", command=self.pop_out_mode, justify='center', wraplength=45, foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3).grid(column=1, row=2, padx=5, pady=5, sticky='nsew')
        
        # debug menu button, toggle debug menu
        tk.Button(self.menu_bar, text="Debug", command=self.debug_toggle, justify='center', wraplength=45, foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3).grid(column=1, row=3, padx=5, pady=5, sticky='nsew')

        # volume button, toggle volume menu
        tk.Button(self.menu_bar, text="Volume", command=self.volume_toggle, justify='center', wraplength=45, foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3).grid(column=1, row=4, padx=5, pady=5, sticky='nsew')

        # alarms and timer menu
        self.timer_alarm_menu_open = False
        tk.Button(self.menu_bar, text="Alarms and Timers", command=self.open_timer_alarm_menu, justify='center', wraplength=45, foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3).grid(column=1, row=5, padx=5, pady=5, sticky='nsew')
        
        tk.Button(self.menu_bar, text="Restart", command=self.restart, justify='center', wraplength=45, foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3).grid(column=1, row=6, padx=5, pady=5, sticky='nsew')
        # tk.Button(self.menu_bar, text="Close", command=self.main_close, justify='center', wraplength=45, foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3).grid(column=1, row=7, padx=5, pady=5, sticky='nsew')

        # volume menu
        self.volume_toggle_var = False
        self.volume_frame = tk.Frame(self.menu_bar, bg=self.secondary_background_color)

        # volume slider
        self.volume_slider = tk.Scale(self.volume_frame, from_=100, to=0, orient='vertical', background=self.quaternary_background_color, foreground=self.text_color, highlightbackground=self.quaternary_background_color, highlightcolor=self.tertiary_background_color, command=self.volume_change)
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(fill='both', expand=1, padx=5, pady=5)

        # volume mute button
        tk.Button(self.volume_frame, text="Mute", justify='center', foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3, command=lambda: self.volume_change(value = 0)).pack(fill='both', side='bottom', padx=5, pady=5)

        # debug menu
        self.debug_toggle_var = False
        self.debug_frame = tk.Frame(self.menu_bar, bg=self.secondary_background_color)

        self.save_log_check = tk.Checkbutton(self.debug_frame, text="Save Log for the Current Session", offvalue=False, onvalue=True, variable=self.save_log_var, command=self.debug_check_update, background=self.secondary_background_color, fg=self.text_color, selectcolor=self.quaternary_background_color)
        self.save_log_check.grid(column=0, row=0, padx=5, pady=5)
        if self.save_log:
            self.save_log_check.select()

        # show the session log
        self.log_output_check = tk.Checkbutton(self.debug_frame, text="Show Log", offvalue=False, onvalue=True, variable=self.log_output_var, command=self.debug_check_update, background=self.secondary_background_color, fg=self.text_color, selectcolor=self.quaternary_background_color)
        self.log_output_check.grid(column=0, row=1, padx=5, pady=5)
        # if self.log_output:
        #     self.log_output_check.select()

        self.log_output_box = tk.Text(self.debug_frame, wrap='word', background=self.quaternary_background_color, foreground=self.text_color, width=40, state='disabled')#text box for debug info
        # self.log_output_box.grid(column=0, row=2, padx=5, pady=5, sticky='nsew')

        # show the "intEnt" classification of the input
        self.classification_output_check = tk.Checkbutton(self.debug_frame, text="Classification", offvalue=False, onvalue=True, variable=self.classification_output_var, command=self.debug_check_update, background=self.secondary_background_color, fg=self.text_color, selectcolor=self.quaternary_background_color)
        self.classification_output_check.grid(column=0, row=3, padx=5, pady=5)
        # if self.classification_output:
        #     self.classification_output_check.select()

        self.classification_output_box = tk.Text(self.debug_frame, wrap='word', background=self.quaternary_background_color, foreground=self.text_color, width=40, state='disabled') # text box for debug info
        # self.classification_output_box.grid(column=0, row=4, padx=5, pady=5, sticky='nsew')

        # show chatbot information for the input; alternate statement classifications and the list of possible responses for the input statement
        self.chatbot_info_output_check = tk.Checkbutton(self.debug_frame, text="Chatbot Debug", offvalue=False, onvalue=True, variable=self.chatbot_info_output_var, command=self.debug_check_update, background=self.secondary_background_color, fg=self.text_color, selectcolor=self.quaternary_background_color)
        self.chatbot_info_output_check.grid(column=0, row=5, padx=5, pady=5)
        # if self.chatbot_info_output:
        #     self.chatbot_info_output_check.select()

        self.chatbot_info_output_box = tk.Text(self.debug_frame, wrap='word', background=self.quaternary_background_color, foreground=self.text_color, width=40, state='disabled')#text box for debug info
        # self.chatbot_info_output_box.grid(column=0, row=6, padx=5, pady=5, sticky='nsew')
        
        # display the last user input and classification
        self.last_input_label = tk.Label(self.debug_frame, text="Last User Input", justify='center', background=self.secondary_background_color, foreground=self.text_color)
        self.last_input_label.grid(column=0, row=7, padx=5, pady=5, sticky='nsew')

        self.last_input_box = tk.Text(self.debug_frame, wrap='word', background=self.quaternary_background_color, foreground=self.text_color, width=40, height=10, state='disabled') # text box for debug info
        self.last_input_box.grid(column=0, row=8, padx=5, pady=5, sticky='nsew')

        # text input area
        self.text_input_toggle_var = False
        self.text_input_frame = tk.Frame(self.menu_bar, bg=self.secondary_background_color)

        self.text_input = tk.Entry(self.text_input_frame, foreground=self.text_color, background=self.quaternary_background_color, width=50)
        self.text_input.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        self.text_input.bind('<Return>', self.take_user_input)
        self.text_input.bind('<Up>', self.grab_last_input)

        self.text_send_button = tk.Button(self.text_input_frame, text="Send", command=self.take_user_input, justify='center', foreground=self.text_color, background=self.quaternary_background_color, width=6, height=3)
        self.text_send_button.grid(column=1, row=0, padx=5, pady=5, sticky='nsew')

        # audio visualizer area
        self.audio_visualizer = tk.Frame(master, bg=self.primary_background_color)
        self.audio_visualizer.pack(side='top', fill='both', expand=1)

        # text output area
        self.text_display_area = tk.Frame(master, bg=self.primary_background_color)
        self.text_display_area.pack(side='bottom')

        # split things into smaller frames to make it easier to format it the way I want
        self.text_box_area = tk.Frame(self.text_display_area, bg=self.tertiary_background_color)
        self.text_box_area.pack(side='top')

        scroll_bar = tk.Scrollbar(self.text_box_area, background=self.quaternary_background_color, troughcolor=self.secondary_background_color)
        scroll_bar.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky='nse')

        # textbox for outputs
        self.textbox_toggle_var = True
        self.textbox_expand_var = False
        self.textbox = tk.Text(self.text_box_area, wrap='word', background=self.quaternary_background_color, foreground=self.text_color, width=50, height=8)
        scroll_bar.config(command = self.textbox.yview)
        # self.textbox.insert('end', "Welcome! Awaiting Input:\n")
        self.textbox.config(state='disabled', yscrollcommand = scroll_bar.set)
        # self.textbox.config(yscrollcommand = scroll_bar.set)
        self.textbox.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        
        # minimize/hide the output textbox
        self.textbox_toggle_button = tk.Button(self.text_display_area, text="hide", foreground=self.text_color, background=self.quaternary_background_color, command=self.textbox_toggle, width=7)
        self.textbox_toggle_button.pack(pady=5, padx=5, side='bottom')
        
        # expand the output textbox
        self.textbox_expand_button = tk.Button(self.text_display_area, text="expand", foreground=self.text_color, background=self.quaternary_background_color, command=self.textbox_expand_toggle, width=8)
        self.textbox_expand_button.pack(pady=5, padx=5, side='bottom')
        
        # start the speech recognition stream if the setting is turned on
        if self.listen_wake_word:
            self.speech_rec_stream.start()

        # master.lift()
        master.attributes('-topmost', 1)
        master.attributes('-topmost', 0)
        # self.output_to_user(text = "Welcome! Awaiting Input:")

        # self.play_sound('assets\\sounds\\notification1.wav') # "wave.Error: unknown format: 65534" bad wave type? apparently need to convert wave_format_extensible to wave_format_pcm
        # self.play_sound(filename = "assets\\sounds\\alarm1.mp3") # "wave.Error: file does not start with RIFF id"?


    class speech_recognition_stream(object):
        ''' based in part on example code found at: https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py '''
        def __init__(self, outer_gui = None, recognizer_type = 0):
            self.outer_gui = outer_gui
            self.recognizer_type = recognizer_type
            self.stop_listening = None

        def get_user_speech_input(self, wake_phrase_used, time_limit = 6):
            ''' take the user's input after they use a wake work '''
            rec = sr.Recognizer()
            with sr.Microphone() as source:
                rec.adjust_for_ambient_noise(source)

                # if the pop out is not open and the main window is minimized, turn on pop out mode
                # print(self.outer_gui.master.state(), self.outer_gui.master.focus_get()) # hmm
                if not self.outer_gui.pop_out_is_open and (self.outer_gui.master.state() == "iconic" or not self.outer_gui.master.focus_get()):
                    self.outer_gui.pop_out_mode()
                    
                # start and stop("flip flop"/toggle) the tts in order to stop any currently playing speech
                if self.outer_gui.tts_on:
                    self.outer_gui.tts_on = False
                    self.outer_gui.tts_on = True

                # notify the user that we heard the wake word and ask them to make their request
                # print("Heard wake word! What do you want to say!")
                self.outer_gui.output_to_user(text = random.choice(self.outer_gui.output_phrases['wake-phrase-used']).format(wake_phrase = None))

                # audio = rec.listen(source)
                # audio = rec.listen(source, phrase_time_limit=3)
                # audio = rec.listen(source, phrase_time_limit=6)
                audio = rec.listen(source, phrase_time_limit=time_limit)

            try:
                if self.recognizer_type == 0: # online and offline recog types
                    user_input = rec.recognize_google(audio, language ='en-US')
                elif self.recognizer_type == 1:
                    user_input = rec.recognize_sphinx(audio)
                self.outer_gui.take_user_input(input_text = user_input, speech_based_input = True)
            except sr.UnknownValueError: # if the user's input is not recognized, tell them the request wasn't understood
                # print("I'm sorry, I didn't understand that.")
                # self.outer_gui.output_to_user(text = "I'm sorry, I didn't understand that.")
                self.outer_gui.output_to_user(text = random.choice(self.outer_gui.output_phrases['unclear-request']))
            except sr.RequestError as e:
                print(f"\"Speech Recognition Stream\": Encountered an error while parsing your input; \"{e}\"")
                self.outer_gui.output_to_user(text = f"\"Speech Recognition Stream\": Encountered an error while parsing your input; \"{e}\"")

        def check_audio_stream(self, recognizer, audio):
            ''' check for wake phrases being used '''
            try:
                if self.recognizer_type == 0: # online and offline speech rec options
                    speech_string = recognizer.recognize_google(audio, language ='en-US')
                elif self.recognizer_type == 1:
                    speech_string = recognizer.recognize_sphinx(audio)

                # print(speech_string)

                # check if the user used a wake phrase, if so take their input
                for phrase in self.wake_words:
                    if phrase.lower() in speech_string.lower():
                        self.get_user_speech_input(wake_phrase_used = phrase)
                        break

            except sr.UnknownValueError:
                # print("Could not understand audio")
                pass
            except sr.RequestError as e:
                print(f"\"Speech Recognition Stream\": Encountered an error while parsing your input; \"{e}\"")
                self.outer_gui.output_to_user(text = f"\"Speech Recognition Stream\": Encountered an error while parsing your input; \"{e}\"")

        def start(self):
            print("Starting Speech Recognition Stream.")
            self.outer_gui.output_to_user(text = "Starting Speech Recognition Stream.", save_to_log = False)
            # threading.Thread(target=self.outer_gui.output_to_user, args=("Starting Speech Recognition Stream.",)).start() # this one causes problems for some reason
            
            try:
                self.wake_words = self.outer_gui.wake_words
                rec = sr.Recognizer()
                mic = sr.Microphone()

                with mic as source:
                    rec.adjust_for_ambient_noise(source)

                # self.stop_listening = rec.listen_in_background(mic, self.check_audio_stream)
                self.stop_listening = rec.listen_in_background(mic, self.check_audio_stream, phrase_time_limit=5)

                print("Speech Recognition Stream Started.")
                threading.Thread(target=self.outer_gui.output_to_user, args=("Speech Recognition Stream Started.", False)).start()
            except Exception as e: # i know i should catch a specific error, but I'll leave this for now
                print(f"Failed to start Speech Recognition Stream due to \"{e}\" Error")
                threading.Thread(target=self.outer_gui.output_to_user, args=(f"Failed to start Speech Recognition Stream due to \"{e}\" Error", False)).start()

        def stop(self):
            ''' if the speech recognition stream is currently active, stop it and notifiy the user it has been stopped '''
            if self.stop_listening:
                self.stop_listening(wait_for_stop=False)

                print("Speech Recognition Stream Stopped.")
                self.outer_gui.output_to_user(text = "Speech Recognition Stream Stopped.", save_to_log = False)
                # threading.Thread(target=self.outer_gui.output_to_user, args=("Speech Recognition Stream Stopped.", False,)).start()

    class timer(object):
        def __init__(self, outer_gui, time = 0, message = "", method = None, args = (), notification_sound = "assets\\sounds\\notification1.wav"):
            self.outer_gui = outer_gui
            self.time_left = time
            self.method = method
            self.args = args
            self.message = message
            self.timer_ID = self.generate_ID()
            self.stopped = False
            self.notification_sound = notification_sound

            threading.Thread(target = self.countdown).start() # start the countdown for the timer in a separate thread

        def generate_ID(self):
            ''' generate an ID for the timer; the string that is generated contains at least one letter and at least one number '''
            s = "".join(random.choices(string.ascii_letters + string.digits, k = 8))
            while not any(x.isalpha() for x in s) or not any(x.isdigit() for x in s):
                s = "".join(random.choices(string.ascii_letters + string.digits, k = 8))

            return s

        def get_time_left(self):
            ''' return the time left on a timer; as the total seconds and formatted as a string '''
            mins, secs = divmod(self.time_left, 60)

            if mins >= 60:
                hours, mins = divmod(mins, 60)
                time_left_string = "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
            else:
                time_left_string = "{:02d}:{:02d}".format(mins, secs)

            return self.time_left, time_left_string

        def countdown(self):
            while self.time_left > 0 and not self.stopped:
                time.sleep(1)
                self.time_left -= 1

            if not self.stopped: # if the user didn't ask for the timer to be stopped
                if self.message: # if the timer has a message
                    self.outer_gui.output_to_user(text = self.message)

                if self.method: # if timer has a method attached to it
                    try: # attempt to run the method
                        out = self.method(*self.args)
                        if out:
                            self.outer_gui.output_to_user(text = out)
                    except Exception as e: # notify the user of failure
                        print(f"Timer ID: \"{self.timer_ID}\" failed. Unable to fulfill request due to \"{e}\" Error.")
                        self.outer_gui.output_to_user(text = f"Timer ID: \"{self.timer_ID}\" failed. Unable to fulfill request due to \"{e}\" Error.")

                # play the sound to notify the user
                self.outer_gui.play_sound(filename = self.notification_sound)
                
            # remove the timer from the list of active timers
            self.outer_gui.timers.remove(self)
            # print(self.outer_gui.timers)

        def stop(self):
            ''' stop and active timer '''
            self.stopped = True

        def add_time(self, amount):
            ''' add time to an active timer; amount is in seconds '''
            self.time_left += amount

    def grab_last_input(self, event = None):
        ''' put the last input as current text in the text input box '''
        if self.pop_out_is_open:
            self.pop_out_text_input.delete(0, tk.END)
            self.pop_out_text_input.insert(tk.INSERT, self.last_input['text'])
        else:
            self.text_input.delete(0, tk.END)
            self.text_input.insert(tk.INSERT, self.last_input['text'])

    def main_close(self, event = None):
        ''' do things before actually shutting down the whole thing(closing the settings, closing the timer/alarm menu, stopping all active timers, ending the speech rec stream, saving the session log, saving the settings) '''
        if self.settings_menu_open:
            self.close_settings_menu()

        if self.timer_alarm_menu_open:
            self.close_timer_alarm_menu()

        if self.pop_out_is_open:
            self.close_pop_out()

        if self.timers:
            [timer.stop() for timer in self.timers]

        self.speech_rec_stream.stop()

        if self.save_log and self.log['session-log']: # if the user wants to save the log and there is a log to save
            session_end_time = datetime.datetime.now(tz = self.time_zone)
            duration = session_end_time - self.session_start_time
            self.log['session-start-time'] = str(self.session_start_time)
            self.log['session-end-time'] = str(session_end_time)
            self.log['session-duration'] = str(duration) + " / " + str(duration.total_seconds()) + " seconds"
            
            filename = self.session_start_time.strftime("%Y-%m-%d_%H-%M") # 'logs/2022-01-22_23-37.json'

            with open('logs/' + filename + '.json', 'w') as fp:
                json.dump(self.log, fp)

        # assign and save the values to the settings from the actual variables
        self.settings['visual-style'] = self.ui_theme
        self.settings['theme-presets'] = self.color_scheme_presets
        self.settings['text-to-speech'] = self.tts_on
        self.settings['output-volume'] = self.volume
        self.settings['listen-for-wake-word'] = self.listen_wake_word
        self.settings['wake-phrases'] = self.wake_words
        self.settings['browser-paths'] = self.browser_paths
        self.settings['last-input'] = self.last_input
        self.settings['last-output'] = self.last_output

        with open('settings.json', 'w') as fp:
            json.dump(self.settings, fp)

        # and finally, close the main window
        self.master.destroy()

    def textbox_toggle(self):
        ''' toggle showing the main output textbox '''
        if self.textbox_toggle_var: # if it's being shown, hide it
            self.textbox_toggle_var = False

            self.text_box_area.pack_forget()
            self.textbox_expand_button.pack_forget()
            self.textbox_toggle_button.config(text="open")
        else: # if it's hidden, show it
            self.textbox_toggle_var = True

            if self.textbox_expand_var:
                self.textbox_expand_toggle()

            self.text_box_area.pack(side='top')
            self.textbox_expand_button.pack(pady=5, padx=5, side='bottom')
            self.textbox_toggle_button.config(text="hide")

        # print(self.textbox_toggle_var)

    def textbox_expand_toggle(self):
        ''' expanding the main output textbox '''
        self.audio_visualizer.pack_forget()
        self.text_display_area.pack_forget()
        self.text_box_area.pack_forget()

        if self.textbox_expand_var: # if the textbox is expanded, make it normal size again
            self.textbox_expand_var = False

            self.audio_visualizer.pack(side='top', fill='both', expand=1)
            self.text_display_area.pack(side='bottom')
            self.text_box_area.pack(side='top')
        else: # if it's not expanded, expanded it
            self.textbox_expand_var = True

            if not (self.textbox_toggle_var):
                self.textbox_toggle()

            self.audio_visualizer.pack(side='top') # for expand
            self.text_display_area.pack(side='bottom', fill='both', expand=1) # for expand
            self.text_box_area.pack(side='top', fill='both', expand=1) # for expand
            self.text_box_area.grid_columnconfigure(0, weight=1) # for expand
            self.text_box_area.grid_rowconfigure(0, weight=1) # for expand

    def volume_toggle(self):
        ''' toggle showing the volume controls '''
        if self.volume_toggle_var:
            self.volume_toggle_var = False

            self.volume_frame.grid_forget()
        else:
            self.volume_toggle_var = True

            if self.debug_toggle_var:
                self.debug_toggle()

            if self.text_input_toggle_var:
                self.text_input_toggle()

            # self.volume_frame.grid(column=0, row=0, rowspan=5, sticky='nsew')
            self.volume_frame.grid(column=0, row=0, rowspan=3, padx=5, pady=5, sticky='nsew')

        # print(self.volume_toggle_var)

    def volume_change(self, value = None):
        ''' change the volume; takes int as argument and from volume slider '''
        if (value or (value == 0)) and type(value) == int:
            # make sure it's within 0-100
            value = 100 if value > 100 else value
            value = 0 if value < 0 else value

            self.volume = value
            self.volume_slider.set(value)
        else: # if the value is not given as an argument, take the value from the volume slider
            self.volume = self.volume_slider.get()

        # print(self.volume)

    def debug_toggle(self):
        ''' toggle the debug menu '''
        if self.debug_toggle_var:
            self.debug_toggle_var = False

            self.debug_frame.grid_forget()
        else:
            self.debug_toggle_var = True

            if self.volume_toggle_var:
                self.volume_toggle()

            if self.text_input_toggle_var:
                self.text_input_toggle()

            # self.debug_frame.grid(column=0, row=0, rowspan=3, sticky='nsew')
            self.debug_frame.grid(column=0, row=0, rowspan=8, padx=5, pady=5, sticky='nsew')

            self.last_input_box.config(state='normal')
            self.last_input_box.delete('1.0', 'end')
            self.last_input_box.insert('end', str(self.last_input))
            self.last_input_box.config(state='disabled')
            self.last_input_box.config(height = (len(str(self.last_input)) / 39) + 1)


        # print(self.debug_toggle_var)

    def debug_check_update(self):
        ''' update the debug menu textboxes and values for debug settings variables '''
        self.log_output = self.log_output_var.get()
        self.classification_output = self.classification_output_var.get()
        self.chatbot_info_output = self.chatbot_info_output_var.get()
        self.save_log = self.save_log_var.get()
        # print(self.log_output_var.get(), self.classification_output_var.get(), self.chatbot_info_output_var.get(), self.save_log_var.get())

        self.log_output_box.grid_forget()
        self.classification_output_box.grid_forget()
        self.chatbot_info_output_box.grid_forget()
        self.debug_frame.grid_rowconfigure(2, weight=0)
        self.debug_frame.grid_rowconfigure(4, weight=0)
        self.debug_frame.grid_rowconfigure(6, weight=0)

        if self.log_output:
            self.log_output_box.grid(column=0, row=2, padx=5, pady=5, sticky='nsew')
            self.debug_frame.grid_rowconfigure(2, weight=1)

            self.log_output_box.config(state='normal')
            self.log_output_box.delete('1.0', 'end')
            self.log_output_box.insert('end', str(self.log['session-log']) + "\n")
            self.log_output_box.config(state='disabled')
            
        if self.classification_output:
            self.classification_output_box.grid(column=0, row=4, padx=5, pady=5, sticky='nsew')
            self.debug_frame.grid_rowconfigure(4, weight=1)

        if self.chatbot_info_output:
            self.chatbot_info_output_box.grid(column=0, row=6, padx=5, pady=5, sticky='nsew')
            self.debug_frame.grid_rowconfigure(6, weight=1)

    def text_input_toggle(self):
        if self.text_input_toggle_var:
            self.text_input_toggle_var = False

            self.text_input_frame.grid_forget()
        else:
            self.text_input_toggle_var = True

            if self.debug_toggle_var:
                self.debug_toggle()

            if self.volume_toggle_var:
                self.volume_toggle()

            self.text_input_frame.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')

    def open_settings_menu(self):
        if self.settings_menu_open:
            self.close_settings_menu()
            
        self.settings_menu_open = True

        if self.timer_alarm_menu_open:
            self.close_timer_alarm_menu()

        if self.debug_toggle_var:
            self.debug_toggle()

        if self.volume_toggle_var:
            self.volume_toggle()

        if self.text_input_toggle_var:
                self.text_input_toggle()

        self.settings_menu = tk.Toplevel(self.master)
        self.settings_menu.title("Settings")
        self.settings_menu.attributes('-fullscreen', True)
        self.settings_menu.protocol("WM_DELETE_WINDOW", self.close_settings_menu)
        self.settings_menu.bind('<Escape>', self.close_settings_menu)
        # self.settings_menu.bind('<FocusOut>', self.close_settings_menu) # problem with the color selection windows
        # same keyboard shortcuts as the main window
        self.settings_menu.bind('<Alt-x>', self.main_close)
        self.settings_menu.bind('<Control-r>', self.restart)
        self.settings_menu.bind('<Control-R>', lambda event: self.restart(hard_restart=True))

        # side bar menu
        self.tab_menu = tk.Frame(self.settings_menu, bg=self.tertiary_background_color)
        self.tab_menu.pack(side='left', fill='y')
        [self.tab_menu.grid_rowconfigure(x, weight=1) for x in range(10)]

        tk.Button(self.tab_menu, text="Close Settings", command=self.close_settings_menu, justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        tk.Button(self.tab_menu, text="Audio", command=lambda: self.settings_tab_switch(tab = 0), justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
        tk.Button(self.tab_menu, text="Speech Input", command=lambda: self.settings_tab_switch(tab = 1), justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=2, padx=5, pady=5, sticky='nsew')
        tk.Button(self.tab_menu, text="Speech Output", command=lambda: self.settings_tab_switch(tab = 2), justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=3, padx=5, pady=5, sticky='nsew')
        tk.Button(self.tab_menu, text="Theme", command=lambda: self.settings_tab_switch(tab = 3), justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=4, padx=5, pady=5, sticky='nsew')
        tk.Button(self.tab_menu, text="Browser", command=lambda: self.settings_tab_switch(tab = 4), justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=5, padx=5, pady=5, sticky='nsew')
        # tk.Button(self.tab_menu, text="test", command=lambda: self.settings_tab_switch(tab = 5), justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=6, padx=5, pady=5, sticky='nsew')
        tk.Button(self.tab_menu, text="Restart", command=self.restart, justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=7, padx=5, pady=5, sticky='nsew')
        tk.Button(self.tab_menu, text="Hard Restart", command=lambda: self.restart(hard_restart=True), justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=8, padx=5, pady=5, sticky='nsew')
        tk.Button(self.tab_menu, text="Shutdown", command=self.main_close, justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=60, width=10, height=5).grid(column=0, row=9, padx=5, pady=5, sticky='nsew')
        
        # frame where all the actual settings menus will be displayed
        self.settings_display_area = tk.Frame(self.settings_menu, bg=self.primary_background_color)
        self.settings_display_area.pack(side='right', fill='both', expand=1)

        self.settings_tab_label = tk.Label(self.settings_display_area, text="Audio", justify='center', background=self.quaternary_background_color, foreground=self.text_color, highlightthickness=2, highlightbackground=self.tertiary_background_color, font=("Arial", 20))
        self.settings_tab_label.pack(side='top', padx=10, pady=10)

        self.audio_tab_setup()
        self.speech_input_tab_setup()
        self.tts_tab_setup()
        self.theme_tab_setup()
        self.browser_tab_setup()

    def audio_tab_setup(self):
        self.audio_tab = tk.Frame(self.settings_display_area, bg=self.tertiary_background_color)
        self.audio_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)
            
    def speech_input_tab_setup(self):
        self.speech_input_tab = tk.Frame(self.settings_display_area, bg=self.tertiary_background_color)
        self.speech_input_tab.grid_columnconfigure(0, weight=1)
        # self.speech_input_tab.grid_rowconfigure(0, weight=1)

        self.wake_word_area = tk.Frame(self.speech_input_tab, bg=self.quaternary_background_color)
        self.wake_word_area.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        self.wake_word_area.grid_columnconfigure(0, weight=1)
        self.wake_word_area.grid_columnconfigure(1, weight=1)
        self.wake_word_area.grid_columnconfigure(2, weight=1)
        self.wake_word_area.grid_rowconfigure(2, weight=1)

        self.wake_word_toggle = tk.Checkbutton(self.wake_word_area, text="Listen for Wake Word", offvalue=False, onvalue=True, variable=self.listen_wake_word_var, command=self.toggle_listen_for_wake_word, background=self.quaternary_background_color, fg=self.text_color, selectcolor=self.quaternary_background_color, highlightthickness=2, highlightbackground=self.tertiary_background_color)
        self.wake_word_toggle.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        if self.listen_wake_word:
            self.wake_word_toggle.select()

        self.wake_word_label = tk.Label(self.wake_word_area, text="Wake Phrases", justify='center', background=self.quaternary_background_color, foreground=self.text_color, font=("Arial", 20))
        self.wake_word_label.grid(column=1, row=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        
        self.wake_word_box = tk.Listbox(self.wake_word_area, height = 10, width = 15, bg=self.quaternary_background_color, fg=self.text_color, activestyle = 'dotbox')
        [self.wake_word_box.insert(i, x) for i, x in enumerate(self.wake_words)]
        self.wake_word_box.grid(column=1, row=1, rowspan=2, padx=5, pady=5, sticky='nsew')

        self.wake_word_input = tk.Entry(self.wake_word_area, foreground=self.text_color, background=self.quaternary_background_color)
        self.wake_word_input.grid(column=2, row=1, columnspan=2, padx=5, pady=5, sticky='nsew')
        self.wake_word_input.bind('<Return>', self.add_wake_word)

        self.wake_word_add_button = tk.Button(self.wake_word_area, text="Add", command=self.add_wake_word, justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5)
        self.wake_word_add_button.grid(column=2, row=2, padx=5, pady=5, sticky='sew')

        self.wake_word_remove_button = tk.Button(self.wake_word_area, text="Remove", command=self.remove_wake_word, justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5)
        self.wake_word_remove_button.grid(column=3, row=2, padx=5, pady=5, sticky='sew')

    def tts_tab_setup(self):
        self.tts_tab = tk.Frame(self.settings_display_area, bg=self.tertiary_background_color)

        self.tts_toggle = tk.Checkbutton(self.tts_tab, text="Text to Speech for Output", offvalue=False, onvalue=True, variable=self.tts_on_var, command=self.tts_state_set, background=self.quaternary_background_color, fg=self.text_color, selectcolor=self.quaternary_background_color, highlightthickness=2, highlightbackground=self.tertiary_background_color)
        self.tts_toggle.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        if self.tts_on:
            self.tts_toggle.select()

    def theme_tab_setup(self):
        self.theme_tab = tk.Frame(self.settings_display_area, bg=self.tertiary_background_color)
        self.theme_tab.grid_columnconfigure(0, weight=1)
        self.theme_tab.grid_rowconfigure(2, weight=1)
        self.theme_tab.grid_rowconfigure(3, weight=1)
        tk.Label(self.theme_tab, text="Changes to theme will require a restart.", justify='center', background=self.quaternary_background_color, foreground=self.text_color, highlightthickness=2, highlightbackground=self.tertiary_background_color, font=("Arial", 20)).grid(column=0, row=0, padx=5, pady=5, sticky='nsew')

        self.color_preview_area = tk.Frame(self.theme_tab, bg='grey')
        self.color_preview_area.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
        self.color_preview_area.grid_rowconfigure(1, weight=1)
        # self.color_preview_area.grid_columnconfigure(0, weight=1)
        # self.color_preview_area.grid_columnconfigure(1, weight=1)
        # self.color_preview_area.grid_columnconfigure(2, weight=1)
        # self.color_preview_area.grid_columnconfigure(3, weight=1)
        # self.color_preview_area.grid_columnconfigure(4, weight=1)
        [self.color_preview_area.grid_columnconfigure(x, weight=1) for x in range(5)]

        tk.Label(self.color_preview_area, text="Color Scheme", justify='center', background=self.quaternary_background_color, foreground=self.text_color, font=("Arial", 20)).grid(column=0, row=0, columnspan=5, padx=5, pady=5, sticky='nsew')

        self.text_color_preview = tk.Button(self.color_preview_area, command=lambda: self.color_change(index = 0), width=12, height=6, background=self.ui_theme['color-scheme'][0])
        self.text_color_preview.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
        
        self.primary_background_color_preview = tk.Button(self.color_preview_area, command=lambda: self.color_change(index = 1), width=12, height=6, background=self.ui_theme['color-scheme'][1])
        self.primary_background_color_preview.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')

        self.secondary_background_color_preview = tk.Button(self.color_preview_area, command=lambda: self.color_change(index = 2), width=12, height=6, background=self.ui_theme['color-scheme'][2])
        self.secondary_background_color_preview.grid(column=2, row=1, padx=5, pady=5, sticky='nsew')

        self.tertiary_background_color_preview = tk.Button(self.color_preview_area, command=lambda: self.color_change(index = 3), width=12, height=6, background=self.ui_theme['color-scheme'][3])
        self.tertiary_background_color_preview.grid(column=3, row=1, padx=5, pady=5, sticky='nsew')

        self.quaternary_background_color_preview = tk.Button(self.color_preview_area, command=lambda: self.color_change(index = 4), width=12, height=6, background=self.ui_theme['color-scheme'][4])
        self.quaternary_background_color_preview.grid(column=4, row=1, padx=5, pady=5, sticky='nsew')

        # I should allow the user to save the current color scheme as a preset; have a entry box and a button that says "Save as Preset"
        # tk.Label(self.color_preview_area, text="Save Color Theme", justify='center', background=self.quaternary_background_color, foreground=self.text_color, font=("Arial", 20)).grid(column=0, row=2, columnspan=5, sticky='nsew', padx=5, pady=5)
        
        self.theme_name_input = tk.Entry(self.color_preview_area, foreground=self.text_color, background=self.quaternary_background_color)
        self.theme_name_input.grid(column=0, row=3, columnspan=4, padx=5, pady=5, sticky='nsew')
        self.theme_name_input.bind('<Return>', self.save_theme)

        self.theme_save_button = tk.Button(self.color_preview_area, text="Save Color Theme", command=self.save_theme, width=12, height=6, foreground=self.text_color, background=self.quaternary_background_color)
        self.theme_save_button.grid(column=4, row=3, padx=5, pady=5, sticky='nsew')

        # this should be made into a scrollable frame
        self.color_scheme_preset_area = tk.Frame(self.theme_tab, bg='grey')
        self.color_scheme_preset_area.grid(column=0, row=2, padx=5, pady=5, sticky='new')
        self.color_scheme_preset_area.grid_columnconfigure(0, weight=1)

        # create a grid of frames for each preset; with a button to use it and small frames for each color preview
        column_number = 10
        tk.Label(self.color_scheme_preset_area, text="Color Scheme Presets", justify='center', background=self.quaternary_background_color, foreground=self.text_color, font=("Arial", 20)).grid(column=0, row=0, columnspan=column_number, sticky='nsew', padx=5, pady=5)
        for i, preset in enumerate(self.color_scheme_presets):
            x, y = divmod(i, column_number)

            preset_area = tk.Frame(self.color_scheme_preset_area, bg='grey31') # frame for each preset
            preset_area.grid(column=y, row=x + 1, padx=5, pady=5, sticky='nsew') # locate it at the (row, column) based on it's index
            self.color_scheme_preset_area.grid_rowconfigure(x + 1, weight=1) # give its (row, column) a weight, to make things even
            self.color_scheme_preset_area.grid_columnconfigure(y, weight=1)

            # the "use this preset" button
            tk.Button(preset_area, text=preset['preset-name'], command=lambda i=i: self.use_color_scheme_preset(index = i), justify='center', background=preset['color-scheme'][4], foreground=preset['color-scheme'][0]).grid(column=0, row=0, columnspan=6, padx=5, pady=5, sticky='nsew')

            # add the color preview frames
            # [tk.Frame(preset_area, bg=color, width=15, height=15).grid(column=i + 1, row=1, padx=5, pady=5, sticky='nsew') for i, color in enumerate(preset['color-scheme'])]
            for i, color in enumerate(preset['color-scheme']):
                tk.Frame(preset_area, bg=color, width=15, height=15).grid(column=i + 1, row=1, padx=5, pady=5, sticky='nsew')
                preset_area.grid_columnconfigure(i + 1, weight=1)
    
    def browser_tab_setup(self):
        self.browser_tab = tk.Frame(self.settings_display_area, bg=self.tertiary_background_color)
        # self.theme_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)

        self.browser_path_area = tk.Frame(self.browser_tab, bg=self.quaternary_background_color)
        self.browser_path_area.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        self.browser_path_area.grid_rowconfigure(0, weight=1)
        self.browser_path_area.grid_rowconfigure(1, weight=1)
        self.browser_path_area.grid_rowconfigure(2, weight=1)
        self.browser_path_area.grid_columnconfigure(0, weight=1)
        self.browser_path_area.grid_columnconfigure(1, weight=1)
        # self.browser_path_area.pack(padx=10, pady=10, side='top', fill='x', expand=1)

        tk.Label(self.browser_path_area, text="Browser Paths", justify='center', background=self.quaternary_background_color, foreground=self.text_color, font=("Arial", 20)).grid(column=0, row=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        self.browser_name_list = tk.Listbox(self.browser_path_area, height=10, width=25, bg=self.quaternary_background_color, fg=self.text_color, activestyle = 'dotbox')
        self.browser_name_list.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')

        self.browser_path_list = tk.Listbox(self.browser_path_area, height=10, width=205, bg=self.quaternary_background_color, fg=self.text_color, activestyle = 'dotbox')
        self.browser_path_list.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')

        for i, browser_name in enumerate(self.browser_paths):
            self.browser_name_list.insert(i, browser_name)
            self.browser_path_list.insert(i, self.browser_paths[browser_name])

        self.browser_name_input = tk.Entry(self.browser_path_area, foreground=self.text_color, background=self.quaternary_background_color)
        self.browser_name_input.grid(column=0, row=2, padx=5, pady=5, sticky='nsew')
        self.browser_name_input.bind('<Return>', self.save_browser_path)

        self.browser_path_input = tk.Entry(self.browser_path_area, foreground=self.text_color, background=self.quaternary_background_color)
        self.browser_path_input.grid(column=1, row=2, padx=5, pady=5, sticky='nsew')
        self.browser_path_input.bind('<Return>', self.save_browser_path)

        # still need to make the browser_path_save function; should check for both entry boxes having text(i'm not sure how i would verify that the second input is a real browser path)
        self.browser_save_button = tk.Button(self.browser_path_area, text="Save Browser", command=self.save_browser_path, width=12, height=6, foreground=self.text_color, background=self.quaternary_background_color)
        self.browser_save_button.grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky='nsew')

    def settings_tab_switch(self, tab = None): # self.settings_tab_switch(tab = 0)
        ''' uses a match case to easily swap between which setting tab to display based on the input value '''
        self.speech_input_tab.pack_forget()
        self.tts_tab.pack_forget()
        self.theme_tab.pack_forget()
        self.audio_tab.pack_forget()
        self.browser_tab.pack_forget()

        match tab:
            case 0:
                self.audio_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)
                self.settings_tab_label.config(text="Audio")
            
            case 1:
                self.speech_input_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)
                self.settings_tab_label.config(text="Speech Input")

            case 2:
                self.tts_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)
                self.settings_tab_label.config(text="Text to Speech")
            
            case 3:
                self.theme_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)
                self.settings_tab_label.config(text="Theme")

            case 4:
                self.browser_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)
                self.settings_tab_label.config(text="Browser")
            
            # case 5:
            #     self.audio_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)
            #     self.settings_tab_label.config(text="Audio")
            
            case _:
                self.settings_tab_label.config(text="`~*##^##*~`")

    def save_browser_path(self, event = None, browser_name = "", browser_path = ""):
        if not (browser_name and browser_path): # if the name and path aren't as arguments
            if self.browser_name_input.get() and self.browser_path_input.get(): # check if entry boxes contain text
                browser_name = self.browser_name_input.get()
                browser_path = self.browser_path_input.get()

                self.browser_name_input.delete(0, 'end')
                self.browser_path_input.delete(0, 'end')

        # if (browser_name and browser_path): # if the name and path have been set, add the path
        if (browser_name and browser_path) and (browser_path[-4:] == ".exe"): # if the name and path have been set, check that the path uses an executable, add the path
            # print(browser_name, browser_path, browser_path[-4:]) # "opera": "C:\\Program Files (x86)\\Opera\\App\\opera.exe"
            self.browser_paths[browser_name] = browser_path

            # update the webbrowser register
            # [webbrowser.register(browser_name, None, webbrowser.BackgroundBrowser(self.browser_paths[browser_name])) for browser_name in self.browser_paths]
            webbrowser.register(browser_name, None, webbrowser.BackgroundBrowser(browser_path))

        # refresh the lists
        self.browser_name_list.delete(0, 'end')
        self.browser_path_list.delete(0, 'end')

        for i, browser_name in enumerate(self.browser_paths):
            self.browser_name_list.insert(i, browser_name)
            self.browser_path_list.insert(i, self.browser_paths[browser_name])

    def save_theme(self, event = None, theme_name = ""):
        if not theme_name: # if the name isn't in the argument, take it from the entry box
            theme_name = self.theme_name_input.get()
            self.theme_name_input.delete(0, 'end')

        if theme_name:
            # put together the theme dictionary, add it to the list, and set the current ui theme to it
            theme = {
                'preset-name': theme_name,
                'color-scheme': self.ui_theme['color-scheme']
            }
            self.color_scheme_presets.append(theme)
            self.ui_theme['preset-name'] = theme_name

    def tts_state_set(self):
        self.tts_on = self.tts_on_var.get()

    def toggle_listen_for_wake_word(self):
        # not completely sure why I elected to do it this way
        if self.listen_wake_word:
            self.listen_wake_word = False

            self.speech_rec_stream.stop()
        else:
            self.listen_wake_word = True

            self.speech_rec_stream.start()

    def add_wake_word(self, event=None, word = None):
        ''' add a wake phrase to the phrase list(makes it lowercase and removes punctuation) '''
        if word:
            if type(word) == str:
                # self.wake_words.append(word.lower())
                self.wake_words.append(re.sub(r'[^\w\s]', '', word.lower()))
            elif type(word) == list:
                # self.wake_words.extend(word)
                for phrase in word:
                    self.wake_words.append(re.sub(r'[^\w\s]', '', phrase.lower()))
        else:
            # print(self.wake_word_input.get())
            # self.wake_words.append(self.wake_word_input.get().lower())
            self.wake_words.append(re.sub(r'[^\w\s]', '', self.wake_word_input.get().lower()))
            self.wake_word_input.delete(0, 'end')

        # refresh the wake word box to display the updated list
        self.wake_word_box.delete(0, 'end')
        [self.wake_word_box.insert(i, x) for i, x in enumerate(self.wake_words)]

    def remove_wake_word(self, word = None):
        if word:
            if type(word) == str:
                if word in self.wake_words:
                    self.wake_words.remove(word)
            elif type(word) == list:
                [self.wake_words.remove(x) for x in word if x in self.wake_words]
        else:
            try:
                word = self.wake_word_box.get(self.wake_word_box.curselection()) # try to use the user selected wake phrase
                # print(self.wake_word_box.curselection())
            except tk.TclError:
                word = self.wake_word_box.get((-1,)) # if that is unsuccessful, choose the latest wake phrase(last in the list)
                # print(word)
            finally:
                self.wake_words.remove(word) # and finally, remove the chosen string from the list

        self.wake_word_box.delete(0, 'end')
        [self.wake_word_box.insert(i, x) for i, x in enumerate(self.wake_words)]
        # print(self.wake_words)

    def color_change(self, index = 0):
        color = cc.askcolor(color=self.ui_theme['color-scheme'][index], title="Color Chooser") # prompt the user to pick a color
        self.settings_menu.lift()

        if color: # if the user has picked a color, set the color in the scheme and update the preview display
            # print(color)
            
            self.ui_theme['color-scheme'][index] = color[1]

            self.text_color_preview.config(background=self.ui_theme['color-scheme'][0])
            self.primary_background_color_preview.config(background=self.ui_theme['color-scheme'][1])
            self.secondary_background_color_preview.config(background=self.ui_theme['color-scheme'][2])
            self.tertiary_background_color_preview.config(background=self.ui_theme['color-scheme'][3])
            self.quaternary_background_color_preview.config(background=self.ui_theme['color-scheme'][4])

    def use_color_scheme_preset(self, index = 0): # lambda i=i: self.use_color_scheme_preset(index = i)
        self.ui_theme['color-scheme'] = self.color_scheme_presets[index]['color-scheme']
        self.ui_theme['preset-name'] = self.color_scheme_presets[index]['preset-name']

        self.text_color_preview.config(background=self.ui_theme['color-scheme'][0])
        self.primary_background_color_preview.config(background=self.ui_theme['color-scheme'][1])
        self.secondary_background_color_preview.config(background=self.ui_theme['color-scheme'][2])
        self.tertiary_background_color_preview.config(background=self.ui_theme['color-scheme'][3])
        self.quaternary_background_color_preview.config(background=self.ui_theme['color-scheme'][4])

        # print(self.ui_theme['preset-name'], self.ui_theme['color-scheme'], "\n", self.color_scheme_presets[index], "\n", self.color_scheme_presets[index]['preset-name'], self.color_scheme_presets[index]['color-scheme'])
    
    def close_settings_menu(self, event=None):
        self.settings_menu_open = False

        # save the changed settings
        self.listen_wake_word = self.listen_wake_word_var.get()

        # self.master.lift()
        self.master.attributes('-topmost', 1)
        self.master.attributes('-topmost', 0)
        self.settings_menu.destroy()

    def open_timer_alarm_menu(self):
        if self.timer_alarm_menu_open:
            self.close_timer_alarm_menu()

        self.timer_alarm_menu_open = True

        if self.settings_menu_open:
            self.close_settings_menu()

        if self.debug_toggle_var:
            self.debug_toggle()

        if self.volume_toggle_var:
            self.volume_toggle()

        if self.text_input_toggle_var:
            self.text_input_toggle()

        self.timer_alarm_menu = tk.Toplevel(self.master)
        self.timer_alarm_menu.title("Timers and Alarms")
        self.timer_alarm_menu.attributes('-fullscreen', True)
        self.timer_alarm_menu.bind('<Escape>', self.close_timer_alarm_menu)
        self.timer_alarm_menu.bind('<FocusOut>', self.close_timer_alarm_menu)
        # self.timer_alarm_menu.protocol("WM_DELETE_WINDOW", self.close_timer_alarm_menu)
        self.timer_alarm_menu.bind('<Alt-x>', self.main_close)
        self.timer_alarm_menu.bind('<Control-r>', self.restart)
        self.timer_alarm_menu.bind('<Control-R>', lambda event: self.restart(hard_restart=True))

        self.timer_alarm_tab_menu = tk.Frame(self.timer_alarm_menu, bg=self.tertiary_background_color)
        self.timer_alarm_tab_menu.pack(side='left', fill='y')

        tk.Button(self.timer_alarm_tab_menu, text="Close", command=self.close_timer_alarm_menu, justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        tk.Button(self.timer_alarm_tab_menu, text="Timers", command=self.open_timer_tab, justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
        tk.Button(self.timer_alarm_tab_menu, text="Alarms", command=self.open_alarm_tab, justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=0, row=2, padx=5, pady=5, sticky='nsew')
        
        self.timer_alarm_display_area = tk.Frame(self.timer_alarm_menu, bg=self.primary_background_color)
        self.timer_alarm_display_area.pack(side='right', fill='both', expand=1)

        self.timer_alarm_tab_label = tk.Label(self.timer_alarm_display_area, text="Timers", justify='center', background=self.quaternary_background_color, foreground=self.text_color, highlightthickness=2, highlightbackground=self.tertiary_background_color, font=("Arial", 20))
        self.timer_alarm_tab_label.pack(side='top', padx=10, pady=10)

        self.timer_tab = tk.Frame(self.timer_alarm_display_area, bg=self.tertiary_background_color)
        self.timer_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)

        self.alarm_tab = tk.Frame(self.timer_alarm_display_area, bg=self.tertiary_background_color)
        # self.alarm_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)

        self.update_timer_tab()

    def open_timer_tab(self):
        self.alarm_tab.pack_forget()
        self.timer_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)
        self.timer_alarm_tab_label.config(text='Timers')
        self.update_timer_tab()

    def update_timer_tab(self):
        [x.grid_forget() for x in self.timer_tab.grid_slaves()]
        
        for i, timer in enumerate(self.timers):
            x, y = divmod(i, 4)
            timer_frame = tk.Frame(self.timer_tab, bg=self.quaternary_background_color)
            timer_frame.grid(column=y, row=x + 1, padx=5, pady=5, sticky='nsew')

            time_left_string = timer.get_time_left()[1]

            tk.Label(timer_frame, text="ID: " + timer.timer_ID, justify='center', background=self.quaternary_background_color, foreground=self.text_color).grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
            tk.Label(timer_frame, text="Message: " + timer.message, justify='center', background=self.quaternary_background_color, foreground=self.text_color).grid(column=1, row=0, padx=5, pady=5, sticky='nsew')
            tk.Label(timer_frame, text=time_left_string, justify='center', background=self.quaternary_background_color, foreground=self.text_color).grid(column=0, row=1, padx=5, pady=5, sticky='nsew')

            add_time_input_box = tk.Entry(timer_frame, foreground=self.text_color, background=self.quaternary_background_color)
            add_time_input_box.bind('<Return>', lambda event, timer=timer: self.timer_tab_add_time(timer = timer, time = add_time_input_box.get()))
            add_time_input_box.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')

            tk.Button(timer_frame, text="Add Time(sec)", command=lambda timer=timer: self.timer_tab_add_time(timer = timer, time = add_time_input_box.get()), justify='center', foreground=self.text_color, background=self.quaternary_background_color, width=10, height=5).grid(column=1, row=2, padx=5, pady=5, sticky='nsew')

            tk.Button(timer_frame, text="Stop Timer", command=lambda timer=timer: timer.stop(), justify='center', foreground=self.text_color, background=self.quaternary_background_color, wraplength=45, width=10, height=5).grid(column=2, row=1, rowspan=2, padx=5, pady=5, sticky='nsew')

    def timer_tab_add_time(self, timer, time):
        # print(time)
        if type(time) == int or time.isdigit() or time.replace('-', '').isdigit():
            timer.add_time(amount = int(time))
        else:
            print("not number")
        self.update_timer_tab()

    def open_alarm_tab(self):
        self.timer_tab.pack_forget()
        self.alarm_tab.pack(padx=10, pady=10, side='bottom', fill='both', expand=1)
        self.timer_alarm_tab_label.config(text='Alarms')

    def close_timer_alarm_menu(self, event=None):
        self.timer_alarm_menu_open = False

        self.master.attributes('-topmost', 1)
        self.master.attributes('-topmost', 0)
        self.timer_alarm_menu.destroy()

    def pop_out_mode(self):
        self.pop_out_is_open = True

        if self.debug_toggle_var:
            self.debug_toggle()

        if self.volume_toggle_var:
            self.volume_toggle()

        if self.text_input_toggle_var:
            self.text_input_toggle()

        # self.master.iconify()
        self.master.wm_state('iconic')
        
        self.pop_out_window = tk.Toplevel(self.master)
        self.pop_out_window.title("Pop Out")
        # self.pop_out_window.geometry("450x250+1086+614")
        # self.pop_out_window.geometry("450x250+1081+608")
        self.pop_out_window.geometry("450x285+1082+575")
        self.pop_out_window.config(bg=self.primary_background_color)
        self.pop_out_window.overrideredirect(True)
        self.pop_out_window.attributes('-topmost', 1)
        self.pop_out_window.bind('<Escape>', self.close_pop_out)
        # self.pop_out_window.bind('<FocusOut>', lambda event: self.close_pop_out(reopen_main=False)) # this kind of causes problems when clicking into the textbox and entry box
        self.pop_out_window.bind('<Alt-x>', self.main_close)
        self.pop_out_window.bind('<Control-r>', self.restart)
        self.pop_out_window.bind('<Control-R>', lambda event: self.restart(hard_restart=True))

        pop_out_display_area = tk.Frame(self.pop_out_window, bg=self.secondary_background_color)
        # pop_out_display_area.pack(padx=5, pady=5, side='top', fill='both', expand=1)
        pop_out_display_area.pack(padx=5, pady=5, side='top', fill='both')
        pop_out_display_area.grid_columnconfigure(0, weight=1)
        pop_out_display_area.grid_columnconfigure(1, weight=1)
        pop_out_display_area.grid_rowconfigure(0, weight=1)
        pop_out_display_area.grid_rowconfigure(1, weight=1)

        po_scroll_bar = tk.Scrollbar(pop_out_display_area, background=self.quaternary_background_color, troughcolor=self.secondary_background_color)
        po_scroll_bar.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

        self.pop_out_text_box = tk.Text(pop_out_display_area, wrap='word', background=self.quaternary_background_color, foreground=self.text_color, width=50, height=12)
        po_scroll_bar.config(command = self.pop_out_text_box.yview)
        self.pop_out_text_box.config(state='disabled', yscrollcommand = po_scroll_bar.set)
        self.pop_out_text_box.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.pop_out_text_input = tk.Entry(pop_out_display_area, foreground=self.text_color, background=self.quaternary_background_color, width=50)
        # self.pop_out_text_input.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky='nsew')
        self.pop_out_text_input.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
        self.pop_out_text_input.bind('<Return>', self.take_user_input)
        self.pop_out_text_input.bind('<Up>', self.grab_last_input)

        self.pop_out_send_button = tk.Button(pop_out_display_area, text="Send", command=self.take_user_input, justify='center', foreground=self.text_color, background=self.quaternary_background_color, width=8)
        self.pop_out_send_button.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')

        pop_out_close_button = tk.Button(self.pop_out_window, text="Close", command=self.close_pop_out, justify='center', foreground=self.text_color, background=self.quaternary_background_color)
        # pop_out_close_button.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        pop_out_close_button.pack(padx=5, pady=5, side='bottom')

    def close_pop_out(self, reopen_main = True):
        if self.pop_out_is_open:
            self.pop_out_is_open = False
            self.pop_out_window.destroy()

        if reopen_main:
            self.master.state('zoomed')
            # self.master.lift()
            self.master.attributes('-topmost', 1)
            self.master.attributes('-topmost', 0)
        
    def play_sound(self, filename, is_tts_output = False):
        def adjust_for_volume(data):
            temp = np.array(np.frombuffer(data, dtype=np.int16, count=-1))
            for i in range(len(temp)):
                temp[i] = int(round(temp[i] * (self.volume/100)))

            return bytes(temp)

        # wf = wave.open(filename, 'rb')
        with wave.open(filename, 'rb') as wf:
            p = pyaudio.PyAudio()
            chunk = 1024
            
            # Open a .Stream object to write the WAV file to
            stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True # indicates the sound will be played rather than recorded
            )

            # Read data in chunks, readframes outputs a bytes(an iterable of ints)
            data = wf.readframes(chunk)
            data = adjust_for_volume(data)

            # Play the sound by writing the audio data to the stream, as well as check if the user wants the audio to be played
            while str(data) != "b''" and ((is_tts_output and self.tts_on) or not is_tts_output):
                stream.write(data)
                data = wf.readframes(chunk)
                data = adjust_for_volume(data)

            stream.close()
            p.terminate()

    def output_to_user(self, text = "", save_to_log = True):
        text = str(text)
        self.textbox.config(state='normal')
        # self.textbox.delete(0, 'end')
        self.textbox.insert('end', "Bot: " + text + "\n")
        self.textbox.config(state='disabled')
        self.textbox.see(tk.END)

        if self.pop_out_is_open:
            self.pop_out_text_box.config(state='normal')
            self.pop_out_text_box.insert('end', "Bot: " + text + "\n")
            self.pop_out_text_box.config(state='disabled')
            self.pop_out_text_box.see(tk.END)

        if save_to_log:
            # also add it to the log
            self.log['session-log'].append({"speaker": "ASSISTANT", "text": text, "spoken-feedback": self.tts_on, "time": str(datetime.datetime.now())})

        # text to speech stuff
        if self.tts_on:
            self.tts_on = False # a bit of a flip flop to stop ongoing speech streams
            self.tts_on = True

            # self.tts_engine.say(txt)
            # self.tts_engine.runAndWait()

            filename = "speech.mp3"
            self.tts_engine.save_to_file(text, filename)
            self.tts_engine.runAndWait()

            self.play_sound(filename, is_tts_output = True)

    def take_user_input(self, event = None, input_text = "", speech_based_input = False, save_to_log = True):
        input_text = str(input_text) # deep copy?
        out = None

        if not input_text:
            if self.pop_out_is_open:
                input_text = self.pop_out_text_input.get()
                self.pop_out_text_input.delete(0, 'end')
            else:
                input_text = self.text_input.get()
                self.text_input.delete(0, 'end')

        # not sure if I want to add the user's input text to the textboxes...
        self.textbox.config(state='normal')
        self.textbox.insert('end', "User: " + input_text + "\n")
        self.textbox.config(state='disabled')
        self.textbox.see(tk.END)

        if self.pop_out_is_open:
            self.pop_out_text_box.config(state='normal')
            self.pop_out_text_box.insert('end', "User: " + input_text + "\n")
            self.pop_out_text_box.config(state='disabled')
            self.pop_out_text_box.see(tk.END)
        
        # then do the processing
        try:
            intEnt = intEntFilter.intNEnt(input_text, self.last_input['classification'])
        except Exception as e:
            print(e)
            intEnt = {"intent": None, "secondary-intent": None, "timing": None}
            out = f"Failed due to: \"{e}\" error"
        
        if self.classification_output:
            print(intEnt)
            self.classification_output_box.config(state='normal')
            self.classification_output_box.insert('end', str(intEnt) + "\n")
            self.classification_output_box.config(state='disabled')
            self.classification_output_box.see(tk.END)

        current_time = datetime.datetime.now()

        if save_to_log:
            # save input to chatlog
            self.log['session-log'].append({"speaker": "USER", "text": input_text, "intEnt": intEnt, "spoken-input": speech_based_input, "time": str(current_time)})

        if intEnt:
            # should probably put this in a try exception
            match intEnt:
                case {'intent': 'conversational'}:
                    if self.chatbot_info_output:
                        self.response = chatParser.respondWord(input_text, self.chatbot_info_output)
                        out = self.response[0]

                        print("Possible Statements(top 3):", self.response[1], "\nPossible Responses to the Most Likely Statement:", self.response[2])
                        self.chatbot_info_output_box.config(state='normal')
                        self.chatbot_info_output_box.insert('end', "Possible Statements(top 3): " + str(self.response[1]) + "\nPossible Responses to the Most Likely Statement: " + str(self.response[2]) + "\n")
                        self.chatbot_info_output_box.config(state='disabled')
                        self.chatbot_info_output_box.see(tk.END)
                    else:
                        out = chatParser.respondWord(input_text)

                # math
                case {'intent': 'math', 'secondary-intent': None}:
                    try:
                        out = f"The answer is: \"{str(mathParse.parsEval(input_text))}\"."
                    except Exception as e:
                        print(e)
                        out = f"Failed due to: \"{e}\" Error."

                # search
                case {'intent': 'search', 'secondary-intent': 'web-search', 'engine': None, 'term': term}:
                    duckduckgo_results = webSearch.ddgSrch(term) # if an engine is not specified, first try duckduckgo instant answer api
                    if duckduckgo_results[0]:
                        # out = "Using DuckDuckGo's Instant Answer API:\n" + duckduckgo_results[0] + " Sourced from " + duckduckgo_results[1] + "."
                        out = random.choice(self.output_phrases['search']['duckduckgo']).format(results = duckduckgo_results[0], source = duckduckgo_results[1])
                    else: # if the duck duck go instant answer api doesn't return anything, just search on google(opens page in browser)
                        # out = f"Searching on Google: \"{term}\"."
                        out = random.choice(self.output_phrases['search']['default-search-engine-fallback']).format(term = term)
                        webSearch.search(term)

                case {'intent': 'search', 'secondary-intent': 'web-search', 'engine': search_engine, 'term': term}:
                    # out = f"Searching on {search_engine}: \"{term}\"."
                    out = random.choice(self.output_phrases['search']['specified-search-engine']).format(search_engine = search_engine, term = term)
                    webSearch.search(term, search_engine)

                case {'intent': 'search', 'secondary-intent': 'search-definition', 'term': term}:
                    out = f"You want to know what \"{term}\" means."

                    # definition_info = word, part_of_speech, definition, source_url, num_of_meanings, request_url = webSearch.dictDef(term)
                    definition_info = webSearch.dictDef(term)

                    if definition_info:
                        word, part_of_speech, definition, source_url, num_of_meanings, num_of_definitions, request_url = definition_info

                        # print(definition_info)
                        # print(word, part_of_speech, definition, source_url, num_of_meanings, request_url)
                        # out = random.choice(self.output_phrases['search']['definition']).format(term = word, part_of_speech = part_of_speech, definition = definition, source_url = source_url, num_of_meanings = num_of_meanings, num_of_definitions = num_of_definitions)
                        out = random.choice(self.output_phrases['search']['definition']).format(term = word, part_of_speech = part_of_speech, definition = definition)
                    else:
                        out = f"Unable to get a definition for \"{term}\"."

                # weather
                # simple weather request
                case {'intent': 'weather', 'secondary-intent': None, 'location': location, 'timing': None}:
                    # out = f"You want to know what the weather is like in {location}."
                    try:
                        weather_data = weather_retrieval.get_weather_data(location = location, tmp = True, sk = True, wnd = True, humi = True)
                        # out = f"It is {weather_data[0]} and {weather_data[1]}, with wind {weather_data[2]} and {weather_data[3]} humid in {weather_data[4]}.\nWeather information sourced from Weather.gov; Last Updated: {weather_data[5]}"
                        out = random.choice(self.output_phrases['weather']['general-request']).format(temp_farenheit = weather_data[0], sky = weather_data[1], wind = weather_data[2], humidity = weather_data[3], location = weather_data[4], update_time = weather_data[5])
                    except Exception as e:
                        print(e)
                        # out = f"Failed to get weather due to \"{e}\" Error."
                        out = random.choice(self.output_phrases['weather']['error']).format(error = e)

                # precipitation
                case {'intent': 'weather', 'secondary-intent': 'weather-precipitation', 'location': location}:
                    out = f"You want to know the precipitation data for {location}."

                # temperature
                case {'intent': 'weather', 'secondary-intent': 'weather-temperature', 'location': location}:
                    try:
                        weather_data = weather_retrieval.get_weather_data(location = location, tmp = True)
                        # out = f"It is {weather_data[0]} in {weather_data[1]}.\nWeather information sourced from Weather.gov; Last Updated: {weather_data[2]}"
                        out = random.choice(self.output_phrases['weather']['temperature']).format(temp_farenheit = weather_data[0], location = weather_data[1], update_time = weather_data[2])
                    except Exception as e:
                        print(e)
                        # out = f"Failed to get weather due to \"{e}\" Error."
                        out = random.choice(self.output_phrases['weather']['error']).format(error = e)

                # humidity
                case {'intent': 'weather', 'secondary-intent': 'weather-humidity', 'location': location}:
                    # out = f"You want to know the humidity in {location}."
                    try:
                        weather_data = weather_retrieval.get_weather_data(location = location, humi = True)
                        # out = f"It is {weather_data[0]} humid in {weather_data[1]}.\nWeather information sourced from Weather.gov; Last Updated: {weather_data[2]}"
                        out = random.choice(self.output_phrases['weather']['humidity']).format(humidity = weather_data[0], location = weather_data[1], update_time = weather_data[2])
                    except Exception as e:
                        print(e)
                        # out = f"Failed to get weather due to \"{e}\" Error."
                        out = random.choice(self.output_phrases['weather']['error']).format(error = e)

                # forecast
                case {'intent': 'weather', 'secondary-intent': 'weather-forecast', 'location': location, 'timing': {'elapsed': False, 'time': given_time_period}}:
                    out = f"You want to know what the weather is like in {location} for \"{given_time_period}\"."

                case {'intent': 'weather', 'secondary-intent': 'weather-forecast', 'location': location, 'timing': {'elapsed': True, **time_period_info}}:
                    out = f"You want to know what the weather is like in {location} for {time_period_info}."

                # smarthouse
                # change state sans timing
                case {'intent': 'smarthouse', 'secondary-intent': 'smarthouse-change-state', 'room': room, 'appliance': appliance, 'state': state, 'value': value, 'timing': None}:
                    out = f"smarthouse input --> \"change\" --> room: \"{room}\", appliance: \"{appliance}\", state: \"{state}\", and value: \"{value}\""
                
                # change state avec timing
                case {'intent': 'smarthouse', 'secondary-intent': 'smarthouse-change-state', 'room': room, 'appliance': appliance, 'state': state, 'value': value, 'timing': timing}:
                    out = f"smarthouse input --> \"change\" --> room: \"{room}\", appliance: \"{appliance}\", state: \"{state}\", and value: \"{value}\" with timing: {timing}"
            
                # check state
                case {'intent': 'smarthouse', 'secondary-intent': 'smarthouse-check-state', 'room': room, 'appliance': appliance, 'state': state, 'timing': None}:
                    out = f"smarthouse input --> \"check\" --> room: \"{room}\", appliance: \"{appliance}\", and state: \"{state}\""

                # open app
                case {'intent': 'run-program', 'common-name': common_name, 'program': file_location, 'timing': None}:
                    # out = f"Attempting to open: {common_name}."
                    out = random.choice(self.output_phrases['run-program']['common-name-and-location']).format(common_name = common_name)

                    try:
                        # subprocess.call([file_location])
                        # subprocess.Popen(file_location)
                        subprocess.Popen(file_location, shell=True)
                        # subprocess.Popen(file_location, shell=True).wait()
                    except Exception as e:
                        print(e)
                        # out = f"Failed to open \"{common_name}\"; due to \"{e}\" Error."
                        out = random.choice(self.output_phrases['run-program']['error']).format(common_name = common_name, error = e)
                
                case {'intent': 'run-program', 'common-name': common_name, 'program': None, 'timing': None}:
                    out = f"You want me to open \"{common_name}\"."

                    # if ".exe" in common_name:
                    #     ffl = threading.Thread(target=self.find_file_location, args=(common_name,)) # runs the function for locating a file's path in a separate thread
                    # else:
                    #     ffl = threading.Thread(target=self.find_file_location, args=(common_name.replace(" ", "") + ".exe",)) # removes spaces and adds ".exe" extension

                    # ffl.start()

                case {'intent': 'run-program', 'common-name': common_name, 'program': file_location, 'timing': {'elapsed': True, **time_info}}:
                    out = f"You want me to open \"{common_name}\", at \"{file_location}\"; time info: {time_info}"
                
                # open website
                case {'intent': 'open_site', 'common-name': common_name, 'website': url, 'browser': None, 'timing': None}:
                    webbrowser.open(url) # open page in default browser
                    # out = f"Opening: \"{common_name}\" using default browser."
                    out = random.choice(self.output_phrases['open-website']['common-name-url-no-browser']).format(common_name = common_name, url = url)

                case {'intent': 'open_site', 'common-name': common_name, 'website': url, 'browser': browser, 'timing': None}:
                    try:
                        controller = webbrowser.get(browser) # make a controller for the specified browser
                        controller.open(url) # open page with controller
                        # out = f"Opening: \"{common_name}\" in \"{browser}\"."
                        out = random.choice(self.output_phrases['open-website']['common-name-url-browser']).format(common_name = common_name, browser = browser, url = url)
                    except Exception as e:
                        print(e)
                        # out = f"Unable to open \"{common_name}\" in {browser} due to: \"{e}\" Error. Attempting to open in default browser."
                        out = random.choice(self.output_phrases['open-website']['common-name-url-browser-error']).format(common_name = common_name, browser = browser, url = url, error = e)
                        webbrowser.open(url)

                case {'intent': 'open_site', 'common-name': common_name, 'website': url, 'browser': browser, 'timing': timing}:
                    out = f"You want me to open \"{common_name}\", at \"{url}\" in {browser}; time info {timing}"

                # time
                # current time
                case {'intent': 'time', 'secondary-intent': 'time-get-current'}:
                    # out = "You would like to know the current time."
                    # out = f"The time is {current_time.strftime('%I:%M %p')}."
                    out = random.choice(self.output_phrases['time']['current-time']).format(current_time_12_hour = current_time.strftime('%I:%M %p'))

                # start timer
                case {'intent': 'time', 'secondary-intent': 'time-start-timer', 'message': message, 'units': units, 'timing': timing}:
                    # out = f"You would like me to start a timer with message: \"{message}\", timing data of \"{units}\" and \"{timing}\"."
                    sec = 0
                    for i in timing:
                        if i == "seconds":
                            sec += timing[i]
                        elif i == "minutes":
                            sec += timing[i] * 60
                        elif i == "hours":
                            sec += timing[i] * 3600

                    message = message if message else "Time's up!"
                    new_timer = self.timer(outer_gui = self, time = sec, message = message)
                    if self.timers:
                        while any(i.timer_ID == new_timer.timer_ID for i in self.timers):
                            del new_timer
                            new_timer = self.timer(outer_gui = self, time = sec, message = message)

                    self.timers.append(new_timer)

                    out = "Starting a timer for "
                    # units = units if units else ['seconds']
                    if len(units) > 1:
                        for i, x in enumerate(units):
                            if i < len(units) - 1:
                                out += str(timing[x]) + " " + x + ", "
                            elif i == len(units) - 1:
                                out += "and " + str(timing[x]) + " " + x + "."
                    else:
                        out += str(timing[units[0]]) + " " + units[0] + "."
                    out += f" For a total of \"{sec}\" seconds. The ID for it is \"{new_timer.timer_ID}\"."
                    # out = random.choice(self.output_phrases['time']['start-timer']).format(time_in_units = None, total_seconds = sec, timer_ID = new_timer.timer_ID, message = message)

                # check timer
                case {'intent': 'time', 'secondary-intent': 'time-check-timer', 'IDTerm': '', 'ID': None}:
                    # out = "You would like to check the remaining time on a timer."
                    if self.timers: # check if there are even timers to check
                        if len(self.timers) == 1: # if there is one timer, tell the user how much time is left. if not ask them to specify the timer
                            # out = f"There is only one active timer. The time left is \"{self.timers[0].time_left}\" seconds."
                            out = random.choice(self.output_phrases['time']['check-timer']['one-active-timer']).format(time_left = self.timers[0].time_left)
                        else:
                            # out = "There is more than one active timer."
                            out = random.choice(self.output_phrases['time']['check-timer']['unspecified-timer'])
                    else:
                        # out = "There are no active timers."
                        out = random.choice(self.output_phrases['time']['check-timer']['no-active-timers'])

                case {'intent': 'time', 'secondary-intent': 'time-check-timer', 'IDTerm': None, 'ID': given_timer_ID} | {'intent': 'time', 'secondary-intent': 'time-check-timer', 'IDTerm': '', 'ID': given_timer_ID}:
                    # out = f"You would like to check the remaining time on the timer with ID: \"{given_timer_ID}\"."
                    if self.timers:
                        if len(self.timers) > 1:
                            checkedTimer = None

                            [checkedTimer := i for i in self.timers if i.timer_ID == given_timer_ID]
                            if checkedTimer:
                                # out = f"The time left on the timer with the ID \"{given_timer_ID}\" is \"{checkedTimer.time_left}\" seconds."
                                out = random.choice(self.output_phrases['time']['check-timer']['timer-ID']).format(timer_ID = given_timer_ID, time_left = checkedTimer.time_left)
                            else:
                                # out = f"Unable to find a timer with the ID \"{given_timer_ID}\"."
                                out = random.choice(self.output_phrases['time']['check-timer']['timer-ID-not-found']).format(timer_ID = given_timer_ID)
                        elif len(self.timers) == 1:
                            # out = f"There is only one active timer. The time left is \"{self.timers[0].time_left}\" seconds."
                            out = random.choice(self.output_phrases['time']['check-timer']['one-active-timer']).format(time_left = self.timers[0].time_left)
                    else:
                        # out = "There are no active timers."
                        out = random.choice(self.output_phrases['time']['check-timer']['no-active-timers'])

                case {'intent': 'time', 'secondary-intent': 'time-check-timer', 'IDTerm': term, 'ID': None}:
                    # out = f"You would like to check the remaining time on the \"{given_term}\" timer."
                    if self.timers:
                        if len(self.timers) > 1:
                            checkedTimer = None
                            
                            for i in self.timers:
                                if term in i.message:
                                    checkedTimer = i
                                    break
                            
                            if checkedTimer:
                                # out = f"The time left on the timer related to \"{given_term}\" is \"{checkedTimer.time_left}\" seconds."
                                out = random.choice(self.output_phrases['time']['check-timer']['timer-term']).format(term = term, time_left = checkedTimer.time_left)
                            else:
                                # out = f"Unable to find a timer with a message containing the term: \"{given_term}\"."
                                out = random.choice(self.output_phrases['time']['check-timer']['timer-term-not-found']).format(term = term)

                        elif len(self.timers) == 1:
                            # out = f"There is only one active timer. The time left is \"{self.timers[0].time_left}\" seconds."
                            out = random.choice(self.output_phrases['time']['check-timer']['one-active-timer']).format(time_left = self.timers[0].time_left)
                    else:
                        # out = "There are no active timers."
                        out = random.choice(self.output_phrases['time']['check-timer']['no-active-timers'])

                # end timer
                case {'intent': 'time', 'secondary-intent': 'time-end-timer', 'IDTerm': '', 'ID': None}:
                    # out = "You would like to end a timer."
                    if self.timers: # check if there are even timers to check
                        if len(self.timers) == 1: # if there is one timer, tell the user how much time is left. if not ask them to specify the timer
                            out = random.choice(self.output_phrases['time']['end-timer']['one-active-timer'])
                            self.timers[0].stop()
                        else:
                            out = random.choice(self.output_phrases['time']['end-timer']['unspecified-timer'])
                    else:
                        out = random.choice(self.output_phrases['time']['end-timer']['no-active-timers'])

                case {'intent': 'time', 'secondary-intent': 'time-end-timer', 'IDTerm': None, 'ID': 'all'} | {'intent': 'time', 'secondary-intent': 'time-end-timer', 'IDTerm': '', 'ID': 'all'}:
                    # out = "You would like to end all active timers."
                    out = random.choice(self.output_phrases['time']['end-timer']['all-timers'])
                    [x.stop() for x in self.timers]

                case {'intent': 'time', 'secondary-intent': 'time-end-timer', 'IDTerm': None, 'ID': timer_ID} | {'intent': 'time', 'secondary-intent': 'time-end-timer', 'IDTerm': '', 'ID': timer_ID}:
                    if self.timers:
                        if len(self.timers) > 1:
                            found_timer = None

                            [found_timer := i for i in self.timers if i.timer_ID == timer_ID]
                            if found_timer:
                                out = random.choice(self.output_phrases['time']['end-timer']['timer-ID']).format(given_timer_ID = timer_ID)
                                found_timer.stop()
                            else:
                                out = random.choice(self.output_phrases['time']['end-timer']['timer-ID-not-found']).format(given_timer_ID = timer_ID)
                        elif len(self.timers) == 1:
                            out = random.choice(self.output_phrases['time']['end-timer']['one-active-timer'])
                            self.timers[0].stop()
                    else:
                        # out = "There are no active timers."
                        out = random.choice(self.output_phrases['time']['end-timer']['no-active-timers'])

                case {'intent': 'time', 'secondary-intent': 'time-end-timer', 'IDTerm': term, 'ID': None}:
                    if self.timers:
                        if len(self.timers) > 1:
                            found_timer = None
                            
                            for timer in self.timers:
                                if term in timer.message:
                                    found_timer = timer
                                    break
                            
                            if found_timer:
                                out = random.choice(self.output_phrases['time']['end-timer']['timer-term']).format(given_term = term)
                                found_timer.stop()
                            else:
                                out = random.choice(self.output_phrases['time']['end-timer']['timer-term-not-found']).format(given_term = term)

                        elif len(self.timers) == 1:
                            out = random.choice(self.output_phrases['time']['end-timer']['one-active-timer'])
                            self.timers[0].stop()
                    else:
                        # out = "There are no active timers."
                        out = random.choice(self.output_phrases['time']['end-timer']['no-active-timers'])

                # date
                # today
                case {'intent': 'time', 'secondary-intent': 'time-get-date', 'timing': {'elapsed': False, 'time': 'today'}} | {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': ['day']} | {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': [], 'timing': None}:
                    # out = "You would like to know today's date."
                    # out = f"Today is {current_time.strftime('%A')}, {current_time.strftime('%B')} {str(current_time.day)}, {str(current_time.year)}, {current_time.strftime('%Y/%m/%d')}."
                    out = random.choice(self.output_phrases['time']['date']['today']).format(day_of_week = current_time.strftime('%A'), current_month = current_time.strftime('%B'), day_of_month = str(current_time.day), current_year = str(current_time.year), date_year_month_day = current_time.strftime('%Y/%m/%d'))

                # tomorrow
                case {'intent': 'time', 'secondary-intent': 'time-get-date', 'timing': {'elapsed': False, 'time': 'tomorrow'}}:
                    # out = "You would like to know tomorrow's date."
                    current_time += datetime.timedelta(days=1)
                    # out = f"Tomorrow is {current_time.strftime('%A')}, {current_time.strftime('%B')} {str(current_time.day)}, {str(current_time.year)}, {current_time.strftime('%Y/%m/%d')}."
                    out = random.choice(self.output_phrases['time']['date']['tomorrow']).format(tomorrow_day_of_week = current_time.strftime('%A'), current_month = current_time.strftime('%B'), tomorrow_day_of_month = str(current_time.day), current_year = str(current_time.year), tomorrow_date_year_month_day = current_time.strftime('%Y/%m/%d'))

                # yesterday
                case {'intent': 'time', 'secondary-intent': 'time-get-date', 'timing': {'elapsed': False, 'time': 'yesterday'}}:
                    # out = "You would like to know yesterday's date."
                    current_time += datetime.timedelta(days=-1)
                    # out = f"Yesterday was {current_time.strftime('%A')}, {current_time.strftime('%B')} {str(current_time.day)}, {str(current_time.year)}, {current_time.strftime('%Y/%m/%d')}."
                    out = random.choice(self.output_phrases['time']['date']['yesterday']).format(yesterday_day_of_week = current_time.strftime('%A'), current_month = current_time.strftime('%B'), yesterday_day_of_month = str(current_time.day), current_year = str(current_time.year), yesterday_date_year_month_day = current_time.strftime('%Y/%m/%d'))

                # blank of blank
                case {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': ['day', 'week']}:
                    # out = "You would like to know the day of the week."
                    # out = f"Today is {current_time.strftime('%A')}."
                    out = random.choice(self.output_phrases['time']['date']['blank-of-blank']['day-of-the-week']).format(day_of_week = current_time.strftime('%A'))
                    
                case {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': ['day', 'month']}:
                    # out = "You would like to know the day of the month."
                    # out = f"Today is the {current_time.strftime('%d')}th day of the month."
                    # out = f"Today is the {mathParse.digit2OrdinalFig(n = int(current_time.strftime('%d')))} day of the month."
                    # mathParse.digit2OrdinalFig(n = int(current_time.strftime('%d'))) # could use the ordinal function i made a while ago
                    out = random.choice(self.output_phrases['time']['date']['blank-of-blank']['day-of-the-month']).format(day_of_month = mathParse.digit2OrdinalFig(n = int(current_time.strftime('%d'))))

                case {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': ['day', 'year']}:
                    # out = "You would like to know the day of the year."
                    # out = f"Today is the {current_time.strftime('%j')}th day of the year."
                    # out = f"Today is the {mathParse.digit2OrdinalFig(n = int(current_time.strftime('%j')))} day of the year."
                    # mathParse.digit2OrdinalFig(n = int(current_time.strftime('%j'))) # could use the ordinal function i made a while ago
                    out = random.choice(self.output_phrases['time']['date']['blank-of-blank']['day-of-the-year']).format(day_of_year = mathParse.digit2OrdinalFig(n = int(current_time.strftime('%j'))))

                case {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': ['week', 'year']} | {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': ['week']}:
                    # out = "You would like to know the week of the year."
                    # out = f"It is the {current_time.strftime('%W')}th week of the year."
                    # out = f"It is the {mathParse.digit2OrdinalFig(n = int(current_time.strftime('%W')))} week of the year."
                    # mathParse.digit2OrdinalFig(n = int(current_time.strftime('%W'))) # could use the ordinal function i made a while ago
                    out = random.choice(self.output_phrases['time']['date']['blank-of-blank']['week-of-the-year']).format(week_of_year = mathParse.digit2OrdinalFig(n = int(current_time.strftime('%W'))))

                # single unit date request
                case {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': ['month']} | {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': ['month', 'year']}:
                    # out = "You would like to know what month it is."
                    # out = f"It is {current_time.strftime('%B')}."
                    out = random.choice(self.output_phrases['time']['date']['single-unit-date-request']['month']).format(current_month = current_time.strftime('%B'))

                case {'intent': 'time', 'secondary-intent': 'time-get-date', 'units': ['year']}:
                    # out = "You would like to know what year it is."
                    # out = f"It is {str(current_time.year)}"
                    out = random.choice(self.output_phrases['time']['date']['single-unit-date-request']['year']).format(current_year = str(current_time.year))

                # time until
                case {'intent': 'time', 'secondary-intent': 'timeTil', 'units': units, 'timing': {'elapsed': False, 'time-get-date': date}}: # something is broken wuth this
                    # out = f"You would like to know how many {units} there are until {date}."
                    formatted_date = " ".join(date.values())
                    diff = timeStuff.fromNow(formatted_date, units[0])
                    if diff >= 0:
                        # out = f"There are {str(abs(diff))} {units[0]} until {formatted_date}."
                        out = random.choice(self.output_phrases['time']['date']['time-until']['until']).format(formatted_date = formatted_date, difference_in_time = str(abs(diff)), units = units[0])
                    else:
                        # out = f"{formatted_date} was {str(abs(diff))} {units[0]} ago."
                        out = random.choice(self.output_phrases['time']['date']['time-until']['ago']).format(formatted_date = formatted_date, difference_in_time = str(abs(diff)), units = units[0])

                # random generators
                # random number
                case {'intent': 'random', 'secondary-intent': 'random-number', 'low': low, 'high': high, 'rolls': rolls}:
                    # default is a number between 1 and 10
                    low = low if low else 1
                    high = high if high else 10
                    numbers = randGen.genRandNum(rolls, low, high)

                    out = f"Here you go: {str(numbers[0])}" if len(numbers) == 1 else f"Here you go: {str(numbers)}"

                # dice
                case {'intent': 'random', 'secondary-intent': 'random-dice', 'sides': sides, 'rolls': rolls}:
                    sides = sides if sides else 6
                    numbers = randGen.dice(rolls, sides)

                    out = f"Here you go: {str(numbers[0])}" if len(numbers) == 1 else f"Here you go: {str(numbers)}"

                # coin flip
                case {'intent': 'random', 'secondary-intent': 'random-coin', 'rolls': rolls}:
                    numbers = randGen.coin(rolls)

                    out = f"Here you go: {str(numbers[0])}" if len(numbers) == 1 else f"Here you go: {str(numbers)}"

                # music
                # play music
                case {'intent': 'music', 'secondary-intent': 'music-play-song', 'term': term}:
                    try:
                        link = tube.tube(term)[0]
                        # out = f"Attempting to play: \"{term}\" at \"{link}\"."
                        out = random.choice(self.output_phrases['music']['play']).format(term = term, link = link)
                    except Exception as e:
                        out = random.choice(self.output_phrases['music']['play-error']).format(error = e, term = term)

                # lyrics
                case {'intent': 'music', 'secondary-intent': 'music-get-lyrics', 'term': term}:
                    try:
                        lyrics = tube.lyric(term)[0].replace("\n", "\n\t")
                        # out = f"Here are the lyrics for \"{term}\":\n\t" + lyrics
                        out = random.choice(self.output_phrases['music']['lyrics']).format(lyrics = lyrics, term = term)
                    except Exception as e:
                        # out = f"Unable to get the lyrics for \"{term}\" due to \"{e}\" Error."
                        out = random.choice(self.output_phrases['music']['lyrics-error']).format(error = e, term = term)

                # funfact
                case {'intent': 'funfact', 'subject': None}:
                    try:
                        out = random.choice(funfact.randPrefixes) + funfact.randFac()
                        # out = random.choice(self.output_phrases['funfact']['without-subject']).format(error = e)
                    except Exception as e:
                        out = f"Unable to retrieve fact; Failed due to: \"{e}\" Error."
                        out = random.choice(self.output_phrases['funfact']['error']).format(error = e)

                case {'intent': 'funfact', 'subject': subject}:
                    out = f"You want a fact about \"{subject}\"."

                # help
                case {'intent': 'help', 'term': None}:
                    # out = self.help_output_text
                    out = random.choice(self.output_phrases['help']['general'])

                case {'intent': 'help', 'term': term}:
                    out = f"You want help with the \"{term}\" function."

                # assistant settings
                # restart
                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-restart', 'timing': None}:
                    # out = "Restarting..."
                    out = random.choice(self.output_phrases['assistant-settings']['assistant-restart'])
                    self.restart() # need a way to give the output response before actually restarting

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-restart', 'timing': {'elapsed': True, **time_period_info}}:
                    out = f"You want me to restart; timing: {time_period_info}."

                # hard restart
                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-hard-restart', 'timing': None}:
                    # out = "Performing a full restart..."
                    out = random.choice(self.output_phrases['assistant-settings']['assistant-hard-restart'])
                    self.restart(hard_restart=True)

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-hard-restart', 'timing': {'elapsed': True, **time_period_info}}:
                    out = f"You want me to perform a full restart; timing: {time_period_info}."

                # shutdown
                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-shutdown', 'timing': None}:
                    # out = "Shutting down..."
                    out = random.choice(self.output_phrases['assistant-settings']['assistant-shutdown'])
                    self.main_close()

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-shutdown', 'timing': {'elapsed': True, **time_period_info}}:
                    out = f"You want me to shutdown; timing: {time_period_info}."

                # theme
                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-theme-change', 'term': specified_theme, 'timing': None}:
                    out = f"You want me to change the gui theme to \"{specified_theme}\"."

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-theme-check'}:
                    # out = "You want to know what the current gui theme is."
                    out = random.choice(self.output_phrases['assistant-settings']['assistant-theme-check']).format(theme = self.ui_theme['preset-name'])

                # volume
                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-volume-change', 'specified-value': specified_value, 'change-by-value': True, 'timing': None}:
                    out = f"You want me to adjust the volume by {specified_value}."
                    if (self.volume + specified_value) >= 100:
                        self.volume_change(value = 100)
                        # out = "Volume is at full."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-volume-change']['volume-full'])
                    elif (self.volume + specified_value) <= 0:
                        self.volume_change(value = 0)
                        # out = "Volume is now muted."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-volume-change']['volume-muted'])
                    else:
                        self.volume_change(value = self.volume + specified_value)
                        # out = f"Volume is now {self.volume}."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-volume-change']['change-by-success']).format(volume = self.volume, specified_value = specified_value)

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-volume-change', 'specified-value': specified_value, 'change-by-value': False, 'timing': None}:
                    # out = f"You want me to set the volume to {specified_value}."
                    if self.volume == specified_value:
                        # out = f"The volume is already set to {specified_value}."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-volume-change']['no-change']).format(specified_value = specified_value)
                    else:
                        self.volume_change(value = specified_value)
                        # out = f"Setting the volume to {specified_value}."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-volume-change']['set-to-success']).format(specified_value = specified_value)

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-volume-check', 'timing': None}:
                    # out = f"The current volume is {self.volume}%."
                    out = random.choice(self.output_phrases['assistant-settings']['assistant-volume-check']).format(volume = self.volume)

                # tts
                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-tts-on', 'timing': None}:
                    if self.tts_on:
                        # out = "Text-to-Speech is already on."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-tts-on']['no-change'])
                    else:
                        self.tts_on_var.set(value=True)
                        self.tts_on = self.tts_on_var.get()

                        # out = "Turning on Text-to-Speech."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-tts-on']['success'])

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-tts-off', 'timing': None}:
                    if self.tts_on:
                        self.tts_on_var.set(value=False)
                        self.tts_on = self.tts_on_var.get()

                        # out = "Turning off Text-to-Speech."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-tts-off']['success'])
                    else:
                        # out = "Text-to-Speech is already off."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-tts-off']['no-change'])

                # wake words/phrases
                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-add-wake-word', 'term': specified_phrase, 'timing': None}:
                    out = f"You want me to add \"{specified_phrase}\" as a wake word."

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-remove-wake-word', 'term': specified_phrase, 'timing': None}:
                    out = f"You want me to remove \"{specified_phrase}\" as a wake word."

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-list-wake-words', 'timing': None}:
                    # out = f"The current list of wake phrases is: {self.wake_words}"
                    # w = '\n\t'.join(self.wake_words)
                    # out = f"The current list of wake phrases is:\n\t{w}"
                    out = random.choice(self.output_phrases['assistant-settings']['assistant-list-wake-words']).format(wake_phrases = '\n\t'.join(self.wake_words))

                # save log
                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-save-log-on'}:
                    # out = "You want me to turn log saving on."
                    if self.save_log:
                        # out = "Log saving is already on."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-save-log-on']['no-change'])
                    else:
                        self.save_log_var.set(value=True)
                        self.save_log = self.save_log_var.get()
                        self.save_log_check.select()
                        # out = "Turning log saving on."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-save-log-on']['success'])

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-save-log-off'}:
                    # out = "You want me to turn log saving off."
                    if self.save_log:
                        self.save_log_var.set(value=False)
                        self.save_log = self.save_log_var.get()
                        self.save_log_check.deselect()
                        # out = "Turning log saving off."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-save-log-off']['success'])
                    else:
                        # out = "Log saving is already off."
                        out = random.choice(self.output_phrases['assistant-settings']['assistant-save-log-off']['no-change'])

                case {'intent': 'assistant-settings', 'secondary-intent': 'assistant-save-log-check'}:
                    # out = "Log saving is turned on." if self.save_log else "Log saving is turned off."
                    out = random.choice(self.output_phrases['assistant-settings']['assistant-save-log-check']['on']) if self.save_log else random.choice(self.output_phrases['assistant-settings']['assistant-save-log-check']['off'])
                
                case {'intent': 'simon-says', 'phrase': phrase, 'timing': None}:
                    if phrase:
                        out = phrase
                    else:
                        out = "Unable to extract phrase."
                
                case {'intent': 'repeat', 'timing': None}:
                    out = self.last_output

                case _:
                    out = random.choice(self.output_phrases['unclear-request']) if (not out) else out # if out isn't set give it a random idk response, else use the original string

        threading.Thread(target=self.output_to_user, args=(out,)).start()
        self.last_input['text'] = input_text
        self.last_input['classification'] = intEnt
        
        self.last_output = out


        if self.log_output:
            print(self.log['session-log'])
            self.log_output_box.config(state='normal')
            self.log_output_box.delete('1.0', 'end')
            self.log_output_box.insert('end', str(self.log['session-log']) + "\n")
            self.log_output_box.config(state='disabled')

    def restart(self, event = None, hard_restart = False):
        self.output_to_user(text = "Restarting...", save_to_log=False)
        self.main_close()

        if hard_restart:
            python = sys.executable
            os.execl(python, python, * sys.argv)
        else:
            # might not be the best way to go about doing this. I feel like it has the chance to cause problems?
            root = tk.Tk()
            my_gui = gui(root)
            root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = gui(root)

    root.mainloop()