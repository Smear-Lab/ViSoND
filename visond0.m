

function visond0(Fs, units, spike_times, clusters, time_bounds, midfile_name)

%%
%
% Fs=sampling rate of your spike times
% units=indices identifying your units
% spike_times= nspikes X 1 vector with all the spike times in your recording
% clusters= nspikes X 1 vector with the unit numbers for each spike
% time_bounds=[0 inf]; %range of time to include (units in seconds)
% midfile_name = name to save to


bounds=time_bounds.*Fs;

un_pt=0;% a pointer for mapping a unit's spikes to a note
mega_mids=[];



for cll=1:length(units)%
    cl=units(cll);



    spikes=round(double(spike_times(clusters==cl )));% find the spike times for a given unit
    spikes=spikes(spikes>bounds(1) & spikes<bounds(2));


    un_pt=un_pt+1;

    midsp=ones(length(spikes),6);

    midsp(:,3)=un_pt;%the note for that spike

    midsp(:,4)=(127);%the velocity for the note, range 0-127

    spikesec=(spikes)./Fs;%
    midsp(:,5)=spikesec-bounds(1)./Fs;
    midsp(:,6)=midsp(:,5)+0.01;% offset time of the notes, just set to 10 ms
    mega_mids=[mega_mids; midsp];% piles up the notes for each unit

end

% remap the note mapping to some kind of tuning
scale=[2 3 2 2 3]';%pentatonic scale (i think this is the major one)
scale=[1; repmat(scale,24,1)];
scale=cumsum(scale);

prenote=mega_mids(:,3);
renote=prenote.*0;
for o=1:length(over_sort)

    if o<=length(scale) && (36+scale(o))<=127
        renote(prenote==over_sort(o))=36+scale(o);
    else
        renote(prenote==over_sort(o))=nan;
    end
end

mega_mids(:,3)=renote;

mega_mids=mega_mids(keeps,:);

midi_new = matrix2midi_bpm(mega_mids,5e3,960);% I slightly modified the original code to specify the bpm of the file
% the bpm is set to 960 to
% give the maximum possible
% dynamic range for
% slowdowns (ableton's max
% bpm is 999)
% midfile_name=[mouse_id '_' sess 'spike_midi.mid'];
s2mfile_dir = [userd '/Dropbox/MATLAB/FM_Ephys/spike2midi/'];

cd(s2mfile_dir)
writemidi(midi_new, midfile_name);


