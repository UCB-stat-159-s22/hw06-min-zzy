from ligotools import readligo as rl
#from ligotools.readligo import FileList

fn_L1 = "data/L-L1_LOSC_4_V2-1126259446-32.hdf5"
fn_H1 = "data/H-H1_LOSC_4_V2-1126259446-32.hdf5"

def test_read_L1():
	strain_L1, time_L1, chan_dict_L1 = rl.loaddata(fn_L1, 'L1')
	assert (strain_L1 not None) & (time_L1 not None) & (chan_dit_L1 not None)
	assert (len(strain_L1) == len(time_L1))

def test_read_H1():
	strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
	assert (strain_H1 not None) & (time_H1 not None) & (chan_dit_H1 not None)
	assert (len(strain_H1) == len(time_H1))

def test_hdf5_read_L1():
	assert rl.read_hdf5(fn_L1, readstrain=True)[1]== -1.8697138664279764e-18
	
def test_hdf5_read_H1():
	assert rl.read_hdf5(fn_H1, readstrain=True)[1]== 1126259446
