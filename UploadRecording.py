#Now I need to write a script I can run ON RECORDING MACHINE LOCALLY after making a session recording.
#It will upload the .xdf file to SciServer.  It will create an entry in the sessions table describing the session.
#It will read the xdf file, inserting the eeg-time values into the session_eeg table. 
#It will read the xdf file stim markers, and if not already present on SciServer, 
# upload stim files to SciServer and create corresponding entry in image_stims table
#It will read the xdf file, inserting stim-time values into stim_timestamps table

# I will in the future need to write a streaming version of this. Something that subscribes to the pyLSL stream and updates the cloud DB in real time...

from SciServer import CasJobs
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
