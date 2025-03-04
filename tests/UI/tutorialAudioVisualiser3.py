import IPython.display as ipd
import librosa
import librosa.display
import matplotlib.pyplot as plt

'''
https://analyticsindiamag.com/step-by-step-guide-to-audio-visualization-in-python/
'''

# ipd.Audio('tests\\speech.mp3')

plt.figure(figsize=(15,4))

filename = 'tests\\speech.mp3'

data, sample_rate1 = librosa.load(filename)
# data, sample_rate1 = librosa.load(filename,
#     sr=22050,
#     mono=True,
#     offset=0.0,
#     duration=50,
#     res_type='kaiser_best'
# )

librosa.display.waveplot(data,
    sr=sample_rate1,
    max_points=50000.0,
    x_axis='time',
    offset=0.0,
    max_sr=1000
)

plt.show()