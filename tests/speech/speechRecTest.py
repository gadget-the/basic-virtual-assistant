import speech_recognition as sr
from nltk import word_tokenize
import threading

def speech2Text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
        # audio = r.listen(source, phrase_time_limit = 3)

    # recognize speech
    try:
        # sp = r.recognize_sphinx(audio)
        sp = r.recognize_google(audio, language ='en-US')
        print("Meesa thinks you said:", sp)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

def speech2TextStream():
    # text = ""
    rec = sr.Recognizer()
    print("Let's speak!!")
    with sr.Microphone() as source:
        # source.pause_threshold = 1
        # audio = rec.record(source, duration=5)
        # audio = rec.record(source)
        audio = rec.listen(source)

    try:
        text = rec.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Error; {0}".format(e))
        return ""

class speechRecStream:
    def __init__(self, wakeWords = [], recogType = 0):
        self.wakeWords = wakeWords
        self.listening = True
        self.recogType = recogType

        threading.Thread(target = self.recLoop).start()
    
    def speechRec(self):
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source)
            print("Heard wake word! What do you want to say!")
            audio = rec.listen(source)

        try:
            if self.recogType == 0:
                sp = rec.recognize_google(audio, language ='en-US')
            elif self.recogType == 1:
                sp = rec.recognize_sphinx(audio)

            print("You said:", sp) # do something with the input
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Encountered an error; {0}".format(e))

    def recLoop(self):
        while self.listening:
            rec = sr.Recognizer()
            with sr.Microphone() as source:
                # audio = rec.listen(source)
                # audio = rec.listen(source, phrase_time_limit=3)
                audio = rec.listen(source, phrase_time_limit=5)
            
            if not self.listening:
                break

            try:
                if self.recogType == 0:
                    text = rec.recognize_google(audio, language ='en-US')
                elif self.recogType == 1:
                    text = rec.recognize_sphinx(audio)

                print(text)

                for word in self.wakeWords:
                    if word.lower() in text.lower():
                        self.speechRec()
                        break
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Error; {0}".format(e))

    def stop(self):
        self.listening = False

# class speech_recognition_stream:
#     def __init__(self, master, recognizer_type = 0):
#         self.master = master
#         self.recognizer_type = recognizer_type

#     def get_user_speech_input(self):
#         rec = sr.Recognizer()
#         with sr.Microphone() as source:
#             rec.adjust_for_ambient_noise(source)
#             # print("Heard wake word! What do you want to say!")
#             self.master.output_to_user(text = "Heard wake word! What do you want to say!")
#             audio = rec.listen(source)

#         try:
#             if self.recognizer_type == 0:
#                 user_input = rec.recognize_google(audio, language ='en-US')
#             elif self.recognizer_type == 1:
#                 user_input = rec.recognize_sphinx(audio)

#             self.master.take_user_input(input_text = user_input)
#         except sr.UnknownValueError:
#             self.master.output_to_user(text = "I'm sorry, I didn't understand that.")
#         except sr.RequestError as e:
#             self.master.output_to_user(text = f"Encountered an error while parsing your input; {e}")

#     def speech_rec_loop(self):
#         print("Speech Recognition Stream Started.")
#         # threading.Thread(target=self.master.output_to_user, args=("Speech Recognition Stream Started.",)).start()
#         while self.listening:
#             rec = sr.Recognizer()
#             with sr.Microphone() as source:
#                 # audio = rec.listen(source)
#                 # audio = rec.listen(source, phrase_time_limit=3)
#                 audio = rec.listen(source, phrase_time_limit=5)
            
#             if not self.listening:
#                 break

#             try:
#                 if self.recognizer_type == 0:
#                     text = rec.recognize_google(audio, language ='en-US')
#                 elif self.recognizer_type == 1:
#                     text = rec.recognize_sphinx(audio)

#                 for phrase in self.wake_words:
#                     if phrase.lower() in text.lower():
#                         self.get_user_speech_input()
#                         break
#             except sr.UnknownValueError:
#                 # print("Could not understand audio")
#                 pass
#             except sr.RequestError as e:
#                 self.master.output_to_user(text = f"Encountered an error while parsing your input; {e}")

#     def start(self):
#         print("Starting Speech Recognition Stream.")
#         # threading.Thread(target=self.master.output_to_user, args=("Starting Speech Recognition Stream.",)).start()
#         self.listening = True
#         self.wake_words = self.master.wake_words
#         threading.Thread(target = self.speech_rec_loop).start()
    
#     def stop(self):
#         self.listening = False

#         print("Speech Recognition Stream Stopped.")
#         # threading.Thread(target=self.master.output_to_user, args=("Speech Recognition Stream Stopped.",)).start()

class speech_recognition_stream:
    ''' based on example code from: https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py '''
    def __init__(self, master = None, recognizer_type = 0):
        self.master = master
        self.recognizer_type = recognizer_type

    def check_audio_stream(self, recognizer, audio):
        try:
            if self.recognizer_type == 0:
                speech_string = recognizer.recognize_google(audio, language ='en-US')
            elif self.recognizer_type == 1:
                speech_string = recognizer.recognize_sphinx(audio)

            print(speech_string)

            for phrase in self.wake_words:
                if phrase.lower() in speech_string.lower():
                    self.get_user_speech_input()
                    break
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def start(self):
        rec = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            rec.adjust_for_ambient_noise(source)

        # self.stop_listening = rec.listen_in_background(mic, self.check_audio_stream)
        self.stop_listening = rec.listen_in_background(mic, self.check_audio_stream, phrase_time_limit=5)

    def stop(self):
        # self.stop_listening()
        self.stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    # speech2Text()

    # while True:
    #     speech2Text()

    # speech2TextStream()

    # text = ""
    # while True:
    #     # text += " " + speech2TextStream()
    #     text = speech2TextStream()
    #     print("T", text)

    ww = [
        # "testing",
        "olive",
        "This is a test",
        "testing testing 123",
        "Hey Assistant"
    ]

    # test = speechRecStream(wakeWords = ww)
    # while not input("> "):
    #     print("woot")
    # test.stop()

    test = speech_recognition_stream()
    test.start()
    while not input("> "):
        print("woot")
    test.stop()

    # inPhrase = "oh wow! this is a test!"

    # inWords = word_tokenize(inPhrase.lower()) # tokenize the input phrase
    # for wakePhrase in ww: # go through each wake phrase
    #     found = False

    #     print('\n', wakePhrase)
    #     phraseWords = word_tokenize(wakePhrase.lower()) # tokenize the wake phrase

    #     for i, word in enumerate(inWords): # go through each word of the input phrase
    #         compList = list(inWords[i:]) # copying a slice, we only look at the current word and the following words
    #         # print(compList)

    #         if len(compList) < len(phraseWords): # if the remaining words are less than the amount of words in the wake phrase, skip the phrase
    #             break
    #         elif len(compList) > len(phraseWords): # if the remaining words are more than the amount of words in the wake phrase, only look at the words in the slice the size of the wake phrase
    #             compList = compList[:len(phraseWords)]

    #         print(compList)
    #         if compList == phraseWords: # if the resulting list of words is the same as the list of words in the phrase, the wake phrase was used and we want to break out of the outer loop
    #             print('wake word found')
    #             found = True
    #             break
        
    #     if found:
    #         break

'''
speechRecStream
    a good idea would be to have it constantly checking for a wake word/phrase
    and when it hears it, it should start a normal speech rec thing after notifying the user

    Think that I got it working
        I did something similar to the timer class I made
        
        it uses a while loop in a separate thread to listen for the wake word
        once it finds the wake word in the speech, it calls the actual speech rec function
        after the speechRec function finishes, it continues on

        I also added a stop function

        It has an argument for the wakewords
            wakewords would be a list of strings for it to check the speech for

        I could change the way it checks for the wake word
            I currently check if a wake phrase is in the speech(is wakePhrase in speechText?)
            
            a problem i could think of is if a word/phrase is one that is part of another?
            
            i could try tokenizing the input, then compare the tokenized version of the wake phrase too
                could do something like I did in the chatparser response thing -> list(set(statement.lower())&set(key.lower()))
                    
                    if list(set(tokenize(statement.lower()))&set(tokenize(key.lower()))) > thresholdNumber

                    essentially comparing the two lists and seeing how many unique words they have in common

                    not sure if this would make sense to do in it's current form

                should have a method of comparing them that preserves the order
                    think i've just done it

                    tokenize the input phrase
                    go through each wake phrase
                        tokenize the wake phrase
                        go through each word of the input phrase
                            copying a slice of it; we only need look at the current word and the following words
                            if the remaining words are less than the amount of words in the wake phrase, we skip the phrase entirely
                            if the remaining words are more than the amount of words in the wake phrase, we slice again as only need look at the words in a slice the size of the wake phrase
                            if the resulting list of words is the same as the words in the  wake phrase, we know the wake phrase was used and we then to break out of the outer loop(after getting the user's input)

                    not sure if this is worth it?
                        it might make things a bit slower to include it

                        it may also be a bit pointless
'''