import requests
import os
import random
import string
import json
from appJar import gui
from pathlib import Path

''' 
 This program will prompt the user for their regulations.gov API Key, as well as the IP and port
 of the work server they want to connect to. It will set up the config.json file, store the user's
 API Key, and generate a random ClientID.
'''

app = gui('Mirrulations Login', geom='300x50')

app.addLabel('IPv4 Address', text='IPv4 Address:', column=0, row=0)
app.addNumericEntry('IP1', column=1, row=0)
app.addLabel('.1', text='.', column=2, row=0)
app.addNumericEntry('IP2', column=3, row=0)
app.addLabel('.2', text='.', column=4, row=0)
app.addNumericEntry('IP3', column=5, row=0)
app.addLabel('.3', text='.', column=6, row=0)
app.addNumericEntry('IP4', column=7, row=0)
app.addLabel('.4', text=':', column=8, row=0)
app.addNumericEntry('Port', column=9, row=0)
app.setEntryDefault('Port', 'Port')
app.addLabel('API Key:', column=0, row=1)
app.addEntry('API Key', column=1, row=1, colspan=9)

app.go()
