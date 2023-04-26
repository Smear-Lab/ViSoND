"""
Convert Spikes and Sniffs to MIDI
Authors: Morgan Brown & Scott Sterrett
Date: 2023-04-24
"""
# %%
# 1. Imports

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
import math as math
import mido
# %%
# 2. Load data
vio=0.1 # violation threshold
mouse_id = '4131' #mouse of interest
sess = '3'
# %%
#load the data from the mat files
datapath = Path('./data/test')
# clusters = loadmat(datapath/'cluster_ids.mat')['clusters'].squeeze()
# i_locs = loadmat(datapath/'in_locs.mat')['i_locs'].squeeze()
# spike_times = loadmat(datapath/'spike_times.mat')['spikes'].squeeze()
# # %%
clusters=np.loadtxt(datapath/'clusters.csv',delimiter=',').astype('int') # spike clusters
i_locs=np.loadtxt(datapath/'locs.csv',delimiter=',') # inhilation locs
spike_times=np.loadtxt(datapath/'spike_times.csv',delimiter=',') # spike times

# %%
# 3. Prep values to feed to midi converter
un_lat = []
# mega_mids
# scale
# midsn

#!assign bounds later as desired, for no bounds 0 to locs.max()
# need to make 2 versions one for sniff and one for spikes 
beg = 0
fin = locs.max()+1 #len(locs) 
bounds = [beg,fin]

scale = [2,3,2,2,3] # sets tones to penttonic = not kid on violin
scale = np.tile(scale,(1,24))
scale = np.append([1],scale)
scale = np.cumsum(scale)
scale_ind = np.where((scale>24) & (scale<127)) # find indicies between desired range
scale = scale[scale_ind[0]] # values of scale between desired range, 3/6 used below


# not useed spikes=spike_times/30
# spikes=np.round(spikes)
# spikes=spikes.astype(np.uint64)

classic = np.unique(clusters) #set of all unique clusters of intest 

Fs=1e3
mega_mids = None
un_lat = None
un_pt = 0 # counter for spikes

# %%
# 4. Convert sniffs to midi format
fsniff = np.round(Fs/np.diff(i_locs))
fsniff = np.concatenate((fsniff,np.array([fsniff[-1]]))) # add lost from diff
fsniff = np.clip(fsniff, 0, 12) # clip to 0-12 Hz

sniffsec = i_locs/Fs
midsn = np.ones((len(i_locs), 6)) # array where sniff notes are written
midsn_diff = np.concatenate((np.diff(sniffsec),np.array([0.1025]))) # add lost from diff

for mi in range(len(sniffsec)):
    midsn[mi,2] = fsniff[mi] # note
    midsn[mi,3] = 127 # velocity
    midsn[mi,4] = sniffsec[mi] # start time
    midsn[mi,5] = midsn_diff[mi] # duration

# %%
# 5. Write sniffs to midi file
velocity = 127
# bpm = 960 # beats per minute
ini = 0.025 # internote interval
tempo = 500000 # defaul or mido.bpm2tempo(bpm) #microseconds per beat
ticks_per_quarternote = 32767 # max possible # int(5e3) # 5e3 from Matt

track = mido.MidiTrack()
outfile = mido.MidiFile(type=0, ticks_per_beat=ticks_per_quarternote) # type 1 for multiple syncd tracks

outfile.tracks.append(track)
# write first sniff

note_blank = int(1e6*sniffsec[0]*ticks_per_quarternote/tempo) # blank till first sniff in ticks
note_duration = int(1e6*(midsn[0,5] - ini)*ticks_per_quarternote/tempo) 

track.append(Message('note_on', note=int(midsn[0,2]), velocity=velocity, time=note_blank)) #start right after last note
track.append(Message('note_off', note=int(midsn[0,2]), velocity=velocity, time=note_duration))

# write all other sniffs
note_blank = int(1e6*ini*ticks_per_quarternote/tempo) # blank space between notes
for i in range(1, midsn.shape[0]): # for each note
    note_duration = int(1e6*(midsn[i,5] - ini)*ticks_per_quarternote/tempo) 
    track.append(Message('note_on', note=int(midsn[i,2]), velocity=velocity, time=note_blank)) #start right after last note
    track.append(Message('note_off', note=int(midsn[i,2]), velocity=velocity, time=note_duration))

# outfile.save('sniff3.mid')

# %%
mega_mids = np.empty(shape=(0,6)) # array where spikes notes are written
un_pt = 0 # counter for spikes
for cll in range(len(classic)):
    cl = classic[cll] #cl = cluster unit indicies of interst
    cli = int(cl) 
    clusters_ind = np.where(clusters == cli) #find indicies of cluster of interst
    spikes = spike_times[clusters_ind[0]]/Fs/30 # convert to seconds
    #add bounds here if desired
    #spikes_inB = np.where((spikes>bounds(1)) & (spikes<bounds(2)))
    #spikes = spikes[spikes_inB[0]]
    fr = len(spikes)/(np.max(spikes)-np.min(spikes)) # mean firing rate
    env = 0.01 # unused
    nenv = 1 # unused

    isi = np.diff(spikes) # inter spike interval
    rpv_ind = np.where(isi < 2/Fs) # refractory period violation indices
    rpv = len(rpv_ind[0])/len(isi) # refractory period violation rate
    #remove this option?
    if not len(isi): # if no spikes
        rpv = 1
        fr = 0
    if not len(spikes): # if no spikes
        spikes = 0
        fr = 0
    if (fr > 0.0099) & (rpv < vio) & (fr < 10): #optional, exclude firing rate over 10 hz, 
        un_pt += 1 # counter for spikes
        midsp = np.ones((len(spikes),6))
        for msp in range(len(spikes)):
            midsp[msp,0] = 2 # track
            midsp[msp,2] = scale[un_pt] # note
            midsp[msp,3] = 127 # velocity
            midsp[msp,4] = spikes[msp] # start time in seconds
            midsp[msp,5] = spikes[msp] +0.01 # spike end time in seconds
            test=0
        

        mega_mids = np.concatenate((mega_mids, midsp)) #Used below 2/6
        
        # sorting code
        # all_lat = [] # find peak for sorting, one of many options
        # for spav in range(len(spikes)):
        #     this_lat = spikesec[spav]-sniffsec
        #     this_lat_index = this_lat[np.where(abs(this_lat)<0.5)] #!confrim loop
        #     all_lat = [all_lat,this_lat]
            
        # counts, bin_edgessnff_psth=np.histogram(all_lat[1], bins = 31) #!loop bins above
        # snff_psth = counts
        # #snff_mod=max(snff_psth)-min(snff_psth) # not used

        # snff_pk = np.array(snff_psth).argmax()                   

        # un_lat=[un_lat, snff_pk] #Used below 1/6
        # test = 2
        
# %%
# collect all spikes notes
# todo make into an array/df rather than three lists
note_events_onoff = [] # note on or off id
note_events_n = [] # note number
note_events_ticktime = [] # note event time in ticks

for i in range(mega_mids.shape[0]):
    # note on
    note_events_onoff.append(1)
    note_events_n.append(i)
    note_events_ticktime.append(int(1e6*mega_mids[i,4]*ticks_per_quarternote/tempo))

    # note off
    note_events_onoff.append(0)
    note_events_n.append(i)
    note_events_ticktime.append(int(1e6*mega_mids[i,5]*ticks_per_quarternote/tempo))
# %%
# Write spikes array midi file

track = mido.MidiTrack()
outfile = mido.MidiFile(type=0, ticks_per_beat=ticks_per_quarternote) # type 1 for multiple syncd tracks

outfile.tracks.append(track)
ord = np.argsort(note_events_ticktime) # order of note events
prevticks = 0 # previous ticks

for i in range(len(ord)):
    n = note_events_n[ord[i]]
    cumticks = note_events_ticktime[ord[i]] # cumulative ticks

    if note_events_onoff[ord[i]] == 1: # note on
        track.append(mido.Message('note_on', note=int(mega_mids[n,2]), velocity=velocity, time=cumticks-prevticks))
    else: # note off
        track.append(mido.Message('note_off', note=int(mega_mids[n,2]), velocity=velocity, time=cumticks-prevticks))

    prevticks = cumticks
outfile.save('spikes.mid')

# %%
# code from morgan
# test = 3
# un_lat = np.loadtxt('un_lat.csv',delimiter=',') #np.array([])
# mega_mids = np.loadtxt('mega_mids.csv',delimiter=',') #np.array([])
# scale = np.loadtxt('scale.csv',delimiter=',') #np.array([])
# midsn = np.loadtxt('midsn.csv',delimiter=',')
# sun_lat = np.array(un_lat)
# prover_sort = np.argsort(sun_lat)[::-1]
# prenote = mega_mids[:, 2]
# renote = prenote / 0
# over_sort = zoom(prover_sort, (len(scale) / len(prover_sort), 1), order=0)
# for o in range(len(over_sort)):
#     if o < len(scale) and scale[o] <= 127:
#         renote[prenote == over_sort[o]] = scale[o]
#     else:
#         renote[prenote == over_sort[o]] = np.nan
# keeps = np.where(~np.isnan(renote))
# mega_mids[:, 2] = renote
# mega_mids = mega_mids[keeps]
# midsn = np.array([])
# tot_mids = np.vstack((midsn, mega_mids))le = np.array([])
# sun_lat = np.array(un_lat)
# prover_sort = np.argsort(sun_lat)[::-1]
# prenote = mega_mids[:, 2]
# renote = prenote / 0
# over_sort = zoom(prover_sort, (len(scale) / len(prover_sort), 1), order=0)
# for o in range(len(over_sort)):
#     if o < len(scale) and scale[o] <= 127:
#         renote[prenote == over_sort[o]] = scale[o]
#     else:
#         renote[prenote == over_sort[o]] = np.nan
# keeps = np.where(~np.isnan(renote))
# mega_mids[:, 2] = renote
# mega_mids = mega_mids[keeps]
# midsn = np.array([])
# tot_mids = np.vstack((midsn, mega_mids))









