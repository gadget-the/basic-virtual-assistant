import pyttsx3, os, pyaudio, wave, random
# from gtts import gTTS

def pyttsDeb():
    engine = pyttsx3.init()

    def onStart(name):
        print('starting', name)

    def onWord(name, location, length):
        print('word', name, location, length)

    def onEnd(name, completed):
        print('finishing', name, completed)

    engine.connect('started-utterance', onStart)
    engine.connect('started-word', onWord)
    engine.connect('finished-utterance', onEnd)

    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()

def pyttsSave(text = ""):
    # Initialize the Pyttsx3 engine
    engine = pyttsx3.init()
    
    # We can use file extension as mp3 and wav, both will work
    engine.save_to_file(text, 'tests\\speech.mp3')
    engine.runAndWait()
    print("done")

# def gttsSave(text = ""):
#     tts = gTTS(text)
#     tts.save('tests\\speech.mp3')
#     print("done2")

def pyAudPlay(file = 'tests\\speech.wav', chunk = 1024):
    # Open the sound file 
    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True
    )

    # Read data in chunks
    data = wf.readframes(chunk)

    # Play the sound by writing the audio data to the stream
    while str(data) != "b''":
        stream.write(data)
        data = wf.readframes(chunk)

    # Close and terminate the stream
    stream.close()
    p.terminate()

def pytts_voices(utterance = "Hello there!"):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(voices)
    for voice in voices:
        print(voice, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say(utterance)
        engine.runAndWait()
        engine.stop()

def pytts_speed():
    engine = pyttsx3.init()

    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()

    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+50)

    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()

    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-100)

    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()

if __name__ == "__main__":
    # text = "To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune..."
    text = "Using DuckDuckGo's Instant Answer API:\nMcDonald's is an American fast food company, founded in 1940 as a restaurant operated by Richard and Maurice McDonald, in San Bernardino, California, United States. They rechristened their business as a hamburger stand, and later turned the company into a franchise, with the Golden Arches logo being introduced in 1953 at a location in Phoenix, Arizona. In 1955, Ray Kroc, a businessman, joined the company as a franchise agent and proceeded to purchase the chain from the McDonald brothers. McDonald's had its previous headquarters in Oak Brook, Illinois, but moved its global headquarters to Chicago in June 2018. McDonald's is the world's largest restaurant chain by revenue, serving over 69 million customers daily in over 100 countries across 37,855 outlets as of 2018. Although McDonald's is best known for its hamburgers, cheeseburgers and french fries, they feature chicken products, breakfast items, soft drinks, milkshakes, wraps, and desserts. Sourced from Wikipedia."

    # generate the file
    # pyttsSave(text)
    # gttsSave(text)

    # play the file
    # os.startfile("speech.wav")
    # os.system("start speech.mp3")
    # os.system("speech2.mp3")
    # pyAudPlay("tests\\speech.mp3")

    # pyttsDeb()
    # pytts_voices()
    pytts_speed()