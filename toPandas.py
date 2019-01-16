#Now I need to write a script I can run ON RECORDING MACHINE LOCALLY after making a session recording.
#It will upload the .xdf file to SciServer.  It will create an entry in the sessions table describing the session.
#It will read the xdf file, inserting the eeg-time values into the session_eeg table. 
#It will read the xdf file stim markers, and if not already present on SciServer, 
# upload stim files to SciServer and create corresponding entry in image_stims table
#It will read the xdf file, inserting stim-time values into stim_timestamps table

# I will in the future need to write a streaming version of this. Something that subscribes to the pyLSL stream and updates the cloud DB in real time...

from SciServer import CasJobs, Files, Authentication
import pandas                                # data analysis tools
import numpy as np                           # numerical tools
from datetime import datetime, timedelta     # date and timestamp tools
from pprint import pprint
import sys
import os.path
import datetime
#BELOW is not necessary since we are currently running from project directory
#since we need to import libs from parent dir, need to add parent dir to path
#project_path = '/home/idies/workspace/Storage/ncarey/persistent/PULSD/PsychoPy-pylsl-RSVP/'
#if project_path not in sys.path:
#    sys.path.append(project_path)

from xdf.Python.xdf import load_xdf



session_name = 'RSVPTraining5.xdf'
session_desc = 'Name: RSVPTraining5.xdf, Dataset: HiddenCube'
subject_name = 'Nick Carey'
dataset_name = 'HiddenCube'

session_stim_length_ms = 233.3

#dest_path = os.path.join('/Storage/ncarey/persistent/PULSD/data_backup', session_name)
dest_path = '/Storage/ncarey/persistent/PULSD/data_backup/' + session_name 
local_xdf_path = os.path.join('D:\Workspace\PULSD\PsychoPy-pylsl-RSVP','recordings', session_name)
print(local_xdf_path)


#insert data time
xdf = load_xdf(local_xdf_path, verbose=False)

#print(xdf[0][0].keys())

#you will need to dbl check this. your xdf may not be indexed the same way
#I think time series is the frame count(or data), time stamps is the actual clock
target_time_series = xdf[0][0]['time_series']
target_time_stamps = xdf[0][0]['time_stamps']

eeg_time_series = xdf[0][1]['time_series']
eeg_time_stamps = xdf[0][1]['time_stamps']

stim_time_series = xdf[0][2]['time_series']
stim_time_stamps = xdf[0][2]['time_stamps']

dtype = [('session_ID','int32'),('timestamp','int32'), ('F3','float32'), ('Fz','float32'), ('F4','float32'), ('T7','float32'), ('C3','float32'),
         ('Cz','float32'), ('C4','float32'), ('T8','float32'), ('Cp3','float32'), ('Cp4','float32'), ('P3','float32'), ('Pz','float32'), ('P4','float32'),
         ('PO7','float32'), ('PO8','float32'), ('Oz','float32')]
values = []
for index in range(len(eeg_time_stamps)):
    cur_row = []
    cur_row.append(session_ID)
    cur_row.append(eeg_time_stamps[index])
    for eeg_index in range(len(eeg_time_series[index])):
        cur_row.append(eeg_time_series[index][eeg_index])
    values.append(cur_row)

index = range(len(eeg_time_stamps))

df_to_insert = pandas.DataFrame(data=values, index=index, columns=dtype)
