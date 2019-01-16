from SciServer import CasJobs, Files, Authentication
import sys
import os.path
import statistics
from matplotlib import pyplot as plt
import pandas
import numpy as np
import mne
from sklearn.utils import shuffle


#BELOW is necessary since we are not currently running from project directory
#since we need to import libs from parent dir, need to add parent dir to path
project_path = '/home/idies/workspace/Storage/ncarey/persistent/PULSD/PsychoPy-pylsl-RSVP/'
if project_path not in sys.path:
    sys.path.append(project_path)

import importlib
EEGModels = importlib.import_module("arl-eegmodels.EEGModels")


user = input("SciServer Username:")
passw = input("SciServer Password:")
token = Authentication.login(UserName=user, Password=passw)
context = "MyDB"


session_ID=5
var_set = False

for session_ID in range(5,19):
    print("querying session {0}".format(session_ID))
    #Lets get this data
    channel_names = ['F3', 'Fz', 'F4', 'T7', 'C3', 'Cz', 'C4', 'T8', 'Cp3', 'Cp4', 'P3', 'Pz', 'P4', 'PO7', 'PO8', 'Oz']
    channel_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
    sfreq = 512
    montage = 'standard_1005'
    info = mne.create_info(channel_names, sfreq, channel_types, montage)
    info['description'] = 'EEGNet test'

    raw_query = "select * from session_eeg where session_ID = {0} order by timestamp".format(session_ID)
    raw_df = CasJobs.executeQuery(sql=raw_query, context=context)

    raw_data = []
    for index in range(len(channel_names)):
        raw_data.append(raw_df[channel_names[index]].values)

    custom_raw = mne.io.RawArray(raw_data, info)

    #we do this query to get the data reading index at which the stims appear.  IE, instead of 
    # saying stim X was presented at time Y (as it is in the raw data), we want to 
    #say stim X appeared at data reading index Z
    stim_index_query = '''
        with stim_timestamps_index(index_value, timestamp) as (
        select count(*), stim_timestamps.timestamp from session_eeg, stim_timestamps 
        where session_eeg.session_ID = {0} and stim_timestamps.session_ID = {0} and session_eeg.timestamp < stim_timestamps.timestamp 
        group by stim_timestamps.timestamp
        )

        select stim_timestamps_index.index_value, stim_timestamps.stim_ID from stim_timestamps_index, stim_timestamps 
        where stim_timestamps.session_ID = {0} and stim_timestamps.timestamp = stim_timestamps_index.timestamp
        order by stim_timestamps_index.index_value'''.format(session_ID)

    stim_index_df = CasJobs.executeQuery(sql=stim_index_query, context=context)

    stim_ind = stim_index_df['index_value'].values
    stim_ID = stim_index_df['stim_ID'].values

    events = []
    for i in range(len(stim_ind)):
        events.append([stim_ind[i]+1, 0, stim_ID[i]])

    event_id = dict(t_04=0, t_03=1, t_02=2, t_01=3, d_10=4, d_09=5, d_08=6, d_07=7, d_06=8, d_05=9, d_04=10, d_03=11, d_02=12, d_01=13)
    epochs = mne.Epochs(raw=custom_raw, events=events, event_id=event_id, tmin=0, tmax=1)

    #Now we load the epochs into their respective target and distractor arrays of epochs
    # More importantly, we downsample to 128Hz, which is the input sampling rate EEGNet is setup for

    t_epochs = epochs['t_01', 't_02', 't_03', 't_04']
    t_epochs.load_data()
    t_epochs_resampled = t_epochs.copy().resample(128, npad='auto')


    d_epochs = epochs['d_01', 'd_02', 'd_03', 'd_04', 'd_05', 'd_06', 'd_07', 'd_08', 'd_09', 'd_10']
    d_epochs.load_data()
    d_epochs_resampled = d_epochs.copy().resample(128, npad='auto')

    target_data = t_epochs_resampled.get_data()  #32 epochs of 16 channels x 128 readings
    distract_data = d_epochs_resampled.get_data()

    if not var_set:
        input_epochs = np.array(target_data[0], ndmin=4)
        result = np.array([1,0], ndmin=2)
        var_set=True
    else:
        input_epochs = np.append(input_epochs, np.array(target_data[0], ndmin=4), axis=0)
        cur_result = np.array([1,0], ndmin=2)
        result = np.append(result, cur_result, axis=0)

    for i in range(1, len(target_data)):
        cur_epoch = np.array(target_data[i], ndmin=4)
        input_epochs = np.append(input_epochs, cur_epoch, axis=0)
        cur_result = np.array([1,0], ndmin=2)
        result = np.append(result, cur_result, axis=0)
    
    for i in range(0, len(distract_data)):
        cur_epoch = np.array(distract_data[i], ndmin=4)
        input_epochs = np.append(input_epochs, cur_epoch, axis=0)
        cur_result = np.array([0,1], ndmin=2)
        result = np.append(result, cur_result, axis=0)


#shuffles initial dimension of both in sync
shuffled_input_epochs, shuffled_result = shuffle(input_epochs, result, random_state=0)


model = EEGModels.EEGNet(nb_classes = 2, Chans=16, Samples=128)
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
fitted = model.fit(x=shuffled_input_epochs, y=shuffled_result, epochs=30, validation_split=.2)
#print(fitted)
#print(predicted)
#print(model.predict(x=np.array(input_epochs[-3], ndmin=4)))
