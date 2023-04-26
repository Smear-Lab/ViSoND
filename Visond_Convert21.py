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
vio=0.1
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
un_pt = 0

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
# write first note
# starts at sniffsec[0] 

note_blank = int(1e6*sniffsec[0]*ticks_per_quarternote/tempo) # blank till first sniff in ticks
note_duration = int(1e6*(midsn[0,5] - ini)*ticks_per_quarternote/tempo) 

track.append(Message('note_on', note=int(midsn[0,2]), velocity=velocity, time=note_blank)) #start right after last note
track.append(Message('note_off', note=int(midsn[0,2]), velocity=velocity, time=note_duration))

# write all other notes
note_blank = int(1e6*ini*ticks_per_quarternote/tempo) # blank space between notes
for i in range(1, midsn.shape[0]): # for each note
    note_duration = int(1e6*(midsn[i,5] - ini)*ticks_per_quarternote/tempo) 
    track.append(Message('note_on', note=int(midsn[i,2]), velocity=velocity, time=note_blank)) #start right after last note
    track.append(Message('note_off', note=int(midsn[i,2]), velocity=velocity, time=note_duration))

outfile.save('sniff3.mid')
# %%
# 
# %%
for cll in range(len(classic)):
    #this is in the loop
    cl = classic[cll] #cl = cluster unit indicies of interst
    if cl == 0: # prep the sniff
        # i_locs = locs # don't need to reassign here so commented out
        #add back in with updated bounds
        #spikes=spikes[(spikes>bounds[0]) & (spikes<bounds[1])]
        fsniff = np.round(Fs/np.diff(i_locs))
        fsniff = np.concatenate((fsniff,np.array([fsniff[-1]]))) # add lost from diff
        fsniff = np.clip(fsniff, 0, 12) # clip to 0-12 Hz

        sniffsec = i_locs/Fs
        midsn = np.ones((len(i_locs), 6)) # array where sniff notes are written
        midsn_tmp = np.concatenate((np.diff(sniffsec),np.array([0.1025]))) # add lost from diff
       
        for mi in range(len(sniffsec)):
            midsn[mi,2] = fsniff[mi]
            midsn[mi,3] = 127 # this one is velocity not notes
            midsn[mi,4] = sniffsec[mi] #-bounds[1]/Fs #removed not used
            midsn[mi,5] = midsn[mi,4]+midsn_tmp[mi]-0.025 #%Used below 4/6

    else: #prep the spikes
        cli = int(cl) 
        clusters_ind = np.where(clusters == cli) #find indicies of cluster of interst
        spikes=spike_times[clusters_ind[0]]
        #add bounds here if desired
        #spikes_inB = np.where((spikes>bounds(1)) & (spikes<bounds(2)))
        #spikes = spikes[spikes_inB[0]]
        over = len(spikes)/(np.max(spikes)-np.min(spikes))
        over = Fs*over
        env = 0.01
        nenv = 1
        #move this section below first 2 if statments?
        interv = np.diff(spikes)
        rpv_int = np.where(interv < 2)
        rpv = len(rpv_int[0])/len(interv)
        #remove this option?
        if not len(interv):
            rpv = 1
            over = 0
        if not len(spikes):
            spikes = 0
            over = 0
        if (over > 0.0099) & (rpv < vio) & (over < 10): #optional, exclude firing rate over 10 hz, 
            un_pt = un_pt + 1
            spikesec=spikes/Fs
            midsp = np.ones((len(spikes),6))
            for msp in range(len(spikes)):
                midsp[msp,0] = 2 # track
                midsp[msp,2] = un_pt # assign note
                midsp[msp,3] = 127 #np.round(127*nenv) #! reset to 127 velocity
                midsp[msp,4] = spikesec[msp]/30 # spikes start!!! added to convert, possibly move?- bounds[1]/Fs
                midsp[msp,5] = (midsp[msp,4]+0.01)/30 # spike end !!! same
                test=0
            test = 1

            mega_mids = [mega_mids, midsp] #Used below 2/6
          
            all_lat = [] # find peak for sorting, one of many options
            for spav in range(len(spikes)):
                this_lat = spikesec[spav]-sniffsec
                this_lat_index = this_lat[np.where(abs(this_lat)<0.5)] #!confrim loop
                all_lat = [all_lat,this_lat]
                
            counts, bin_edgessnff_psth=np.histogram(all_lat[1], bins = 31) #!loop bins above
            snff_psth = counts
            #snff_mod=max(snff_psth)-min(snff_psth) # not used

            snff_pk = np.array(snff_psth).argmax()                   

            un_lat=[un_lat, snff_pk] #Used below 1/6
            test = 2
        

test = 3
