"""
    Notebook for streaming data from a microphone in realtime
    audio is captured using pyaudio
    then converted from binary data to ints using struct
    then displayed using matplotlib
    if you don't have pyaudio, then run
    >>> pip install pyaudio
    note: with 2048 samples per chunk, I'm getting 20FPS

    https://www.youtube.com/watch?v=0_wde7Db48E
    https://github.com/qxresearch/qxresearch-event-1/tree/master/Applications/Audio%20Visualization%20Tool
"""

import pyaudio, os, struct, time, wave
import numpy as np
import matplotlib.pyplot as plt
from tkinter import TclError

# use this backend to display in separate Tk window
56

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

# create matplotlib figure and axes
fig, ax = plt.subplots(1, figsize=(15, 7))

# pyaudio class instance
p = pyaudio.PyAudio()

# # get list of availble inputs
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):
#         if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#             print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

# # select input
# audio_input = input("\n\nSelect input by Device id: ")

# # stream object to get data from microphone
# stream = p.open(
#     input_device_index=int(audio_input),
#     format=FORMAT,
#     channels=CHANNELS,
#     rate=RATE,
#     input=True,
#     output=True,
#     frames_per_buffer=CHUNK
# )

filename = 'tests\\speech.mp3'
wf = wave.open(filename, 'rb')
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
    channels = wf.getnchannels(),
    rate = wf.getframerate(),
    output = True
)
data = wf.readframes(CHUNK)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)

# create a line object with random data
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# basic formatting for the axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# show the plot
plt.show(block=False)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

# while True:
while str(data) != "b''":

    # binary data
    # data = stream.read(CHUNK)
    stream.write(data)
    data = wf.readframes(CHUNK)

    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128

    line.set_ydata(data_np)

    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1

    except TclError:

        # calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)

        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break
stream.close()
p.terminate()