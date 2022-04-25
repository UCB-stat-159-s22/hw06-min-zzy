import matplotlib
matplotlib.use('Agg')
import ligotools as lg
from ligotools import readligo as rl
from ligotools.utils import write_wavfile, reqshift, whiten, plot_code
#from readligo import FileList
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import json
from ligotools import utils as ut
from scipy.interpolate import interp1d
import os
from os import path
from os.path import exists
import numpy as np
from scipy.signal import butter, filtfilt
from os import remove

fn_L1 = "data/L-L1_LOSC_4_V2-1126259446-32.hdf5"
fn_H1 = "data/H-H1_LOSC_4_V2-1126259446-32.hdf5"
strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
strain_L1, time_L1, chan_dict_L1 = rl.loaddata(fn_L1, 'L1')

# tests for readligo
def test_read_L1():
	assert (strain_L1 is not None) & (time_L1 is not None) & (chan_dict_L1 is not None)
	assert (len(strain_L1) == len(time_L1))

def test_read_H1():
	assert (strain_H1 is not None) & (time_H1 is not None) & (chan_dict_H1 is not None)
	assert (len(strain_H1) == len(time_H1))

def test_hdf5_read_L1():
	assert rl.read_hdf5(fn_L1, readstrain=True)[1]== 1126259446
	
def test_hdf5_read_H1():
	assert rl.read_hdf5(fn_H1, readstrain=True)[1]== 1126259446

# tests for utils
eventname = 'GW150914' 
fnjson = "BBH_events_v3.json"
events = json.load(open(fnjson,"r"))
event = events[eventname]
fs = event['fs'] 
NFFT = 4*fs
time = time_H1
psd_window = np.blackman(NFFT)
NOVL = NFFT/2
fband = [43.0, 300.0]
bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
Pxx_L1, freqs = mlab.psd(strain_L1, Fs = fs, NFFT = NFFT)
psd_H1 = interp1d(freqs, Pxx_H1)
psd_L1 = interp1d(freqs, Pxx_L1)
dt_H1 = time_H1[1] - time_H1[0]
dt_L1 = time_H1[1] - time_H1[0]


def test_whiten():
	wh = whiten(strain_H1, psd_H1, dt_H1)
	assert len(wh) == 131072

def test_write_wavfile():
	wh = whiten(strain_H1, psd_H1, dt_H1)
	write_wavfile("audio/temp.wav", 4096, wh)
	assert path.isfile('audio/GW150914_H1_shifted.wav') == True

def test_reqshift():
	wl = whiten(strain_L1, psd_L1, dt_L1)
	strain_L1_shift = reqshift(wl, 400.0, 4096)
	assert len(strain_L1_shift) == 131072

# test whehter the plot exists or not(replace variables with arbitrary numbers)
def test_plot_code():
	wl = whiten(strain_L1, psd_L1, dt_L1)
	strain_L1_whitenbp = filtfilt(bb, ab, wl) / normalization
	plot_code(0, 0, 1126259462.4324, 13.2, 'GW150914', 'png', 
                        1126259462.44, 0, 0, 999.74, 0, 0, 4096, 'g', 'L1', 0)
	#plot_code(0, 0, 0, 13.2, 'GW150914', 'png', 
                   #     0, 0, 0, 0, 0, 0, 4096, 'g', 'L1', strain_L1_whitenbp)
	assert exists('figurs/'+'GW150914'+"_"+"L1"+"_matchfreq."+"png")
	remove('figurs/'+'GW150914'+"_"+"L1"+"_matchfreq."+"png")
