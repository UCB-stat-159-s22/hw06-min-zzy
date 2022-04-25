import ligotools as lg
from ligotools import readligo as rl
from ligotools.utils import write_wavfile, reqshift, whiten
#from readligo import FileList
import matplotlib.mlab as mlab
import json
from ligotools import utils as ut
from scipy.interpolate import interp1d

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
Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
psd_H1 = interp1d(freqs, Pxx_H1)
dt = time_H1[1] - time_H1[0]
def test_whiten():
    WH = whiten(strain_H1,psd_H1,dt)
    assert len(starin_H1_whiten) == 131072

#def test_write_wavfile():
#write_wavfile("audio/temp.wav", fs, data)
