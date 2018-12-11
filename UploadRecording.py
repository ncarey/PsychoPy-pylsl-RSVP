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

#BELOW is not necessary since we are currently running from project directory
#since we need to import libs from parent dir, need to add parent dir to path
#project_path = '/home/idies/workspace/Storage/ncarey/persistent/PULSD/PsychoPy-pylsl-RSVP/'
#if project_path not in sys.path:
#    sys.path.append(project_path)

from xdf.Python.xdf import load_xdf

user = input("SciServer Username:")
passw = input("SciServer Password:")
token = Authentication.login(user=user, password=passw)


session_name = 'RSVPTraining.xdf'
dest_path = os.path.join('/Storage/ncarey/persistent/PULSD/data_backup', session_name)
local_xdf_path = os.path.join('D:\Workspace\PULSD\PsychoPy-pylsl-RSVP','recordings', session_name)


context = "MyDB"
query_id = 'SELECT MAX(session_ID) from sessions'
df = CasJobs.executeQuery(sql=query_id, context=context)

session_ID = 0
if df['Column1'][0] is None:
    session_ID = 0
else:
    session_ID = int(df['Column1'][0]) + 1


session_datetime = '' #???? need to test inserting datetime






fileServices = Files.getFileServices()
Files.upload(fileServices[0], dest_path, local_xdf_path)

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
