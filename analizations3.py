from audio2numpy import open_audio

from lib import *
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import noisereduce as nr

def plot_fft(f):
    n= len(f)
    fhat = np.fft.fft(f, n)
    print('done')
    dt = 1/sr
    PSD =fhat*np.conj(fhat) / n
    freq = ((1/dt)*n) * np.arange(n)
    L = np.arange(1, np.floor(n/2), dtype='int')
    plt.plot(freq[L][::10], PSD[L][::10], alpha=0.1)


fp = r'C:\Users\Dell\PycharmProjects\audiobook\org.mp3'  # change to the correct path to your file accordingly
x, sr = open_audio(fp)
# sr, x = read_mp3(r'C:\Users\Dell\PycharmProjects\audiobook\org.mp3')
# sr, x = read_mp3(r'C:\Users\Dell\PycharmProjects\audiobook\org.mp3')
x_old = x.copy()
version = 4.0
# thr1 = 1e8
thr1 = 'na'
thr2 = int(278000 * 5)
thr3 = 200
noise_indexes = [[3e5, 3.4e5], [182e5, 2e5], [6.1e5, 6.4e5], [1.41e6, 1.43e6], [1.78e6, 1.87e6], [2.02e6, 2.13e6], [2.7e6, 2.79e6], [2.99e6, 3.08e6], [3.14e6, 3.23e6]]
x_noice = []
x_new = x[:, 0]
for noise_tuple in noise_indexes:
    x_noice.extend(x_new[int(noise_tuple[0]):int(noise_tuple[1])])
print('loading')
fp = r'C:\Users\Dell\Desktop\audiobook\bracia_karamazow_fiodor_dostojewski_cz_1_audiobook_pl_4233648186062852696.mp3'
x, sr = open_audio(fp)
print('loaded')
x_new = x[:, 0]
x_noice = np.array(x_noice)
reduced_noise = nr.reduce_noise(audio_clip=x_new.astype(float), noise_clip=x_noice.astype(float), verbose=False)
# plot_fft(x_new)
# plot_fft(np.array(reduced_noise))
# plt.show()

path = Path(f'results/v{version}_thr4-{thr3}')
path.mkdir(parents=True, exist_ok=True)
a = Path(path / 'x_noice.mp3')
write_mp3(a, sr, x_noice)
a = Path(path / 'reduced_noise.mp3')
write_mp3(a, sr, np.array(reduced_noise).astype(np.int16))