# PsychoPy-pylsl-RSVP

Requires PsychoPy and pylsl

'python -m pip install pylsl' should be sufficient for pylsl

PsychoPy is a bit more tricky. Try:

'python -m pip install numpy scipy matplotlib pandas pyopengl pyglet pillow moviepy lxml openpyxl configobj psychopy'

Review http://psychopy.org/installation.html for issues with PsychoPy installation


This git project has two submodules:

SciScript-Python, for interaction with SciServer

git submodule add https://github.com/sciserver/SciScript-Python.git

Special note from SciSript-Python install: 

"To install python 3 code, run python3 setup.py install while in the ./py3 directory."


xdf, for parsing and reading xdf file formats in python

git submodule add https://github.com/sccn/xdf.git


See the git submodule documentation for maintaining and updating sub-repositories 

https://git-scm.com/book/en/v2/Git-Tools-Submodules

Pay special attention to initializing submodules after a fresh clone.

Method A: use --recurse-submodules tag in clone command, ie:

git clone --recurse-submodules https://github.com/ncarey/PsychoPy-pylsl-RSVP.git

Method B: init submodules after clone:

(in submodule repository directory):

git submodule init

git submodule update

Updating submodules in your repo:

Method A:

git submodule update --remote [submodule name?]

Method B:

(in submodule repo dir):

git fetch

git merge origin master

