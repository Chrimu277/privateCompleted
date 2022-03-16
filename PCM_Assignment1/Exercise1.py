import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import string
import array
from joblib import Parallel, delayed
import multiprocessing
import time

# generate all Yk
def make_DFT(yj):
    n = len(yj)
    j = np.arange(n)  # erzeuge j array
    Yks = np.arange(n, dtype='complex')  # erzeuge leeres complex array für Yk

    for k in range(n):
        exps = np.exp(1j * (2 * np.pi * k * j) / n)
        Yks[k] = np.dot(yj, exps)
        print("k = " + str(k))
    return Yks

# get one Yk
def calc_Yk(yj, k, j):
    exps = np.exp(1j * (2 * np.pi * k * j) / n)
    return np.dot(yj, exps)

# look for the frequency with the highest intensity
def getBaseFreq(array):
    maxi = np.abs(array[0])
    freqindex = 0
    for i in range(int(len(array) / 2)):
        if np.abs(array[i]) > maxi:
            maxi = np.abs(array[i])
            freqindex = i;
    return freqindex * (f_sample / n)

# superposition of 3 sinus like signals with 3 amplitudes and 3 frequencies
def new_signal(t):   # I ~ A^2 -> A = sqrt(I)
    return float(np.sqrt(_intensity1) * np.sin(np.pi * 2 * _freq1 * t) + \
           np.sqrt(_intensity2) * np.sin(np.pi * 2 * _freq2 * t) + \
           np.sqrt(_intensity3) * np.sin(np.pi * 2 * _freq3 * t))

# Frequency analysis of data points and sample length
# Consider two real-valued time series, with their sample frequency and number of data points
# given in the table below
# F1 = 20khz, 10^5 samples
# F2 = 30khz, 3*10^5 samples


# ----------1a-----------
# calculate the total play length of each file

f1 = 20000
f2 = 30000
n1 = 100000
n2 = 300000

# samples = frequency * length

t1 = n1 / f1
t2 = n2 / f2
print("t1 = " + str(t1) + " sec")
print("t2 = " + str(t2) + " sec")

# -------1b----------
# How many data points will you find in frequency space for each data set after a discrete Fourier Transform
# How many of these data points contain unique information ?

# conclusion after fourier: I get as many datapoints Yk as the data yj is long
# unique information: only half of the points contain useful information ( mirrorred )


# --------1c----------
# What is the maximum frequency that can be resolved in each of these datasets ?

# According to Whittaker, Kotelnikow & Shannon, the sample frequency need to resolve a signal is more than twice the
# signal frequency.  or f_sample > 2* f_max

fmax1 = f1 / 2
fmax2 = f2 / 2
print("fmax1 = " + str(f1) + " Hz")
print("fmax2 = " + str(f2) + " Hz")

# ----------1d---------
# Implement a discrete Fourier Transform
# Transform the file "single_tone.txt" given with your own & predefined method
# samplefreq 44.1Khz

f_sample = 44100;  # sample frequency

data_pre = np.loadtxt("single_tone.txt")  # np.loadtxt   reads a file perfectly and scientific notation!!!!
data_pre2 = np.transpose(data_pre)  # -> shape[2][52xxx]
s1 = data_pre.shape  # shape holen

n = s1[0]  # data count
f_values = np.arange(n) * (f_sample / n)  # contains frequencies for x-axis
time_values = np.arange(n) * 1/f_sample

yj1 = data_pre2[0]  # contains data points signal left channel
yj2 = data_pre2[1]  # right channel

plt.figure()
plt.plot(time_values, yj1)    # plot original signal
plt.title("Plot of original signal, left track")
plt.xlabel("time / s")
plt.ylabel("Amplitude")
plt.show()

# ---FFT---

fft1: complex = np.fft.fft(yj1)  # array containing fft

# ---DFT---

print("Calculating DFTs")
start = time.time()             # measure time for DFT
dft1 = make_DFT(yj1)            # do discrete fourier transformation with own implemented method
end = time.time()
print("Finish.. " + str(end - start) + " seconds")

plt.title("DFT Signal 1")
plt.xlabel("f / Hz")
plt.ylabel("Yk")
plt.plot(f_values[0:int(n / 2)], np.real(dft1[0:int(n / 2)]))  # dft 1 plot
plt.show()

plt.title("FFT Signal 1")
plt.xlabel("f / Hz")
plt.ylabel("Yk")
plt.plot(f_values[0:int(n / 2)], np.real(fft1[0:int(n / 2)]))  # fft 1 plot
plt.show()




# ---POWER DENSITY---

pd_fft1 = np.arange(n ,dtype = float)
pd_dft1 = np.arange(n,dtype = float)

for i in range(n):
    pd_fft1[i] = np.abs(fft1[i] ** 2) / (n**2)
    pd_dft1[i] = np.abs(dft1[i] ** 2) / (n**2)

# --------1e----------

plt.plot(f_values[:int(n / 2)], pd_fft1[:int(n / 2)])  # power density plot fft1
plt.title("Power Density FFT1")
plt.show()

plt.plot(f_values[:int(n / 2)], pd_dft1[:int(n / 2)])  # power density plot dft1
plt.title("Power Density DFT1 ")
plt.show()



# -----------1f---------

_freq1 = getBaseFreq(pd_dft1)
print("f_base = " + str(_freq1) + " Hz")
# 146.83 Hz is nearest -> Note D3

# ---g--- What would be the Fourier representation of a perfect tone --> Delta Peak at base frequency and nothing else

# from power density plot read:
_intensity1 : float = 76727 / (n ** 2)
_intensity2 : float = 6497 / (n ** 2)
_intensity3 : float = 8740 / (n ** 2)

_freq2 = 2 * _freq1
_freq3 = 3 * _freq1

representation_signal = np.arange(n, dtype=float)
for i in range(n):
    representation_signal[i] = float(new_signal(time_values[i]))

plt.figure()
plt.plot(time_values, representation_signal)
plt.title("Representation of original signal with 3 frequencies")
plt.xlabel("time / s")
plt.ylabel("Amplitude")
plt.show()
