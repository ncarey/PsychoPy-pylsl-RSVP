import sys
import os.path

#read_xdf_path = 'D:\Workspace\PULSD\PsychoPy-pylsl-RSVP\xdf\Python\xdf.py'
#sys.path.append(read_xdf_path)

from xdf.Python.xdf import load_xdf

xdf_path = os.path.join('D:\Workspace\PULSD\PsychoPy-pylsl-RSVP\\','recordings\RSVPTraining.xdf')
print(xdf_path)
streams = load_xdf(xdf_path)

#print(streams)
                   
