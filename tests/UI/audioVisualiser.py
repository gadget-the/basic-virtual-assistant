import librosa
import numpy as np
import pygame
import sys
import tkinter as tk

'''
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
'''

# for time in stft:
#     points = []
#     for freq in time:
#         x = center[0] + float(np.cos(freq * angle) * level)
#         y = center[1] + float(np.sin(freq * angle) * level)
#         points.append((x, y))
#     points.append(points[0])

def mainLoop():
    pygame.init()

    filename = "tests\\speech.mp3"

    time_series, sample_rate = librosa.load(filename) # getting information from the file
    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4)) # getting a matrix which contains amplitude values according to frequency and time indexes
    # print(stft)
    # for time in stft:
    #     # print(time)
    #     for freq in time:
    #         print(freq)

    spectrogram = librosa.amplitude_to_db(stft, ref=np.max) # converting the matrix to decibel matrix
    # print(spectrogram, spectrogram[0], len(spectrogram))
    # for i in range(len(spectrogram)):
    #     print(len(spectrogram[i]))
        # for f in spectrogram[i]:
        #     print(f)

    frequencies = librosa.core.fft_frequencies(n_fft=2048*4) # getting an array of frequencies
    # print(frequencies)

    times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4) # getting an array of time periodic
    # print(times)

    time_index_ratio = len(times)/times[len(times) - 1]

    frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

    def get_decibel(target_time, freq):
        return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]

    size = width, height = 500, 500
    BLACK = (0, 0, 0)
    GREY = (100, 100, 100)
    center = [width/2, height/2]
    level = 50
    angle = 1.40625
    # BLUE = (0, 0, 150)
    # angle = 360 / 256
    # ciR = 75
    # maxR = 100

    screen = pygame.display.set_mode(size)

    # points_time = []
    # for time in stft:
    #     points = []
    #     for freq in time:
    #         x = center[0] + float(np.cos(freq * angle) * level)
    #         y = center[1] + float(np.sin(freq * angle) * level)
    #         points.append((x, y))
    #     points.append(points[0])
    #     points_time.append(points)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(BLACK)
        # for time in stft:
        #     points = []
        #     for freq in time:
        #         x = center[0] + float(np.cos(freq * angle) * level)
        #         y = center[1] + float(np.sin(freq * angle) * level)
        #         points.append((x, y))
        #     points.append(points[0])
        #     pygame.draw.polygon(screen, GREY, points)

        # for points in points_time:
        #     pygame.draw.polygon(screen, GREY, points)

        # pygame.draw.circle(screen, GREY, center, level)
        pygame.display.flip()

def mainLoop2():
    filename = "tests\\speech.mp3"
    time_series, sample_rate = librosa.load(filename) # getting information from the file
    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4)) # getting a matrix which contains amplitude values according to frequency and time indexes

    size = width, height = 500, 500
    center = [width/2, height/2]
    level = 257
    ciR = 75
    maxR = 100
    specSidNumb = 256
    # angleInc = 1.40625
    angleInc = 360/len(stft[0][:specSidNumb + 1])

    top = tk.Tk()
    myCanvas = tk.Canvas(top, bg="white", height=height, width=width)
    myCanvas.pack()

    # for time in stft:
    #     points = []
    #     for freq in time:
    #         x = center[0] + (ciR + float(np.cos(freq * angle) * level))
    #         y = center[1] + (ciR + float(np.sin(freq * angle) * level))
    #         points.append(x)
    #         points.append(y)
    #     points.append(points[0])
    #     points.append(points[1])
    #     poly = myCanvas.create_polygon(points)
    #     del poly

    points = []
    # for freq in stft[0]:
    for i in range(len(stft[0][:specSidNumb + 1])): # spectrum.slice(0, specSidNumb + 1).length
		# let x = cos(radians(i * angle)) * (map(spectrum[i], 0, 255, ciR + map(level, 0, 1, 0, 120), maxR + map(level, 0, 1, 0, 120)));
        x = float(np.cos(np.radians(i * angleInc) * remap(stft[0][i], 0, 255, ciR + level, maxR + level)))
        y = float(np.sin(np.radians(i * angleInc) * remap(stft[0][i], 0, 255, ciR + level, maxR + level)))
        points.append(x + center[0])
        points.append(y + center[1])
    points.append(points[0])
    points.append(points[1])
    # print(points)
    poly = myCanvas.create_polygon(points)

    # oval = myCanvas.create_oval(center[0] + level, center[1] + level, center[0] - level, center[1] - level)

    top.mainloop()

def remap(x, a, b, c, d):
    ''' maps an input number from one range to another(basically p5's map()) '''
    return x * ((b - a)/(d - c))

if __name__ == '__main__':
    # mainLoop()
    mainLoop2()