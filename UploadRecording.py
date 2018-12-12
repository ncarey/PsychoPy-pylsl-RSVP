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

user = input("SciServer Username:")
passw = input("SciServer Password:")
token = Authentication.login(UserName=user, Password=passw)


session_name = 'RSVPTraining5.xdf'
session_desc = 'Name: RSVPTraining5.xdf, Dataset: HiddenCube'
subject_name = 'Nick Carey'
dataset_name = 'HiddenCube'

session_stim_length_ms = 233.3

#dest_path = os.path.join('/Storage/ncarey/persistent/PULSD/data_backup', session_name)
dest_path = '/Storage/ncarey/persistent/PULSD/data_backup/' + session_name 
local_xdf_path = os.path.join('D:\Workspace\PULSD\PsychoPy-pylsl-RSVP','recordings', session_name)
print(local_xdf_path)

context = "MyDB"
query_id = 'SELECT MAX(session_ID) from sessions'
df = CasJobs.executeQuery(sql=query_id, context=context)

session_ID = 0
if df['Column1'][0] is None:
    session_ID = 0
else:
    session_ID = int(df['Column1'][0]) + 1


session_datetime = datetime.datetime.now()
#UNCOMMENT
#fileServices = Files.getFileServices()
#Files.upload(fileServices[0], path=dest_path, localFilePath=local_xdf_path)

insert_query ='''INSERT INTO sessions
(session_ID, session_datetime, session_filepath, session_desc, session_stim_length_ms, subject_name, dataset_name)
VALUES
({0}, '{1}', '{2}', '{3}', {4}, {5}, {6})'''.format(session_ID, session_datetime, dest_path, session_desc, session_stim_length_ms, subject_name, dataset_name)

#UNCOMMENT THIS
#print(insert_query)
#response = CasJobs.executeQuery(sql=insert_query, context=context)

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


insert_query_template = '''INSERT INTO session_eeg
(session_ID, timestamp, F3, Fz, F4, T7, C3, Cz, C4, T8, Cp3, Cp4, P3, Pz, P4, PO7, PO8, Oz)
VALUES
({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17})'''

#Below is way too slow. talking 2 inserts per second for 100,000 inserts..
# maybe try this? SciServer.CasJobs.uploadPandasDataFrameToTable(dataFrame, tableName, context='MyDB')
#for index in range(len(eeg_time_series)):
#    cur_time_stamp = eeg_time_stamps[index]
#    cur_eeg_reading = eeg_time_series[index]
#    insert_query = insert_query_template.format(session_ID, cur_time_stamp, cur_eeg_reading[0],
#                                                cur_eeg_reading[1], cur_eeg_reading[2], cur_eeg_reading[3],
#                                                cur_eeg_reading[4], cur_eeg_reading[5], cur_eeg_reading[6],
#                                                cur_eeg_reading[7], cur_eeg_reading[8], cur_eeg_reading[9],
#                                                cur_eeg_reading[10], cur_eeg_reading[11], cur_eeg_reading[12],
#                                                cur_eeg_reading[13], cur_eeg_reading[14], cur_eeg_reading[15])
#    print(insert_query)
#    response = CasJobs.executeQuery(sql=insert_query, context=context)

doc = '''
SciServer.Files.upload(fileService, path, data='', localFilePath=None, quiet=True)
Uploads data or a local file into a path defined in the file system.

Parameters:	
fileService – name of fileService (string), or object (dictionary) that defines a file service. A list of these kind of objects available to the user is returned by the function Files.getFileServices().
path – path (in the remote file service) to the destination file (string), starting from the root volume level. Example: rootVolume/userVolumeOwner/userVolume/destinationFile.txt
data – string containing data to be uploaded, in case localFilePath is not set.
localFilePath – path to a local file to be uploaded (string),
userVolumeOwner – name (string) of owner of the userVolume. Can be left undefined if requester is the owner of the user volume.
quiet – If set to False, it will throw an error if the file already exists. If set to True. it will not throw an error.
Raises:	
Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the FileService API returns an error.

Example:	
fileServices = Files.getFileServices(); Files.upload(fileServices[0], “myRootVolume”, “myUserVolume”, “/myUploadedFile.txt”, None, None, localFilePath=”/myFile.txt”);
'''
