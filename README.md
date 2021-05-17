Support this project and keep always updated about recent software releases, bug fixes and major improvements by [following on researchgate](https://www.researchgate.net/project/DDRS4PALS-a-software-for-the-acquisition-and-simulation-of-positron-annihilation-lifetime-spectra-PALS-using-the-DRS4-evaluation-board) or [github](https://github.com/dpscience?tab=followers).

[![badge-researchGate](https://img.shields.io/badge/project-researchGate-brightgreen)](https://www.researchgate.net/project/DDRS4PALS-a-software-for-the-acquisition-and-simulation-of-positron-annihilation-lifetime-spectra-PALS-using-the-DRS4-evaluation-board)

![badge-followers](https://img.shields.io/github/followers/dpscience?style=social)
![badge-stars](https://img.shields.io/github/stars/dpscience/DDRS4PALS?style=social)
![badge-forks](https://img.shields.io/github/forks/dpscience/DDRS4PALS?style=social)

# pyRemoteDDRS4PALS <img src="https://github.com/dpscience/DDRS4PALS/blob/be98df3e02c6a6c5b997b15cda37005d92f6d994/iconDesign/IconPNGRounded_red.png" width="25" height="25">

![badge-license](https://img.shields.io/badge/OS-Windows-blue)
![badge-language](https://img.shields.io/badge/language-Python-blue)
![badge-license](https://img.shields.io/badge/license-GPL-blue)

Copyright (c) 2021 Danny Petschke (danny.petschke@uni-wuerzburg.de) All rights reserved.<br>

<b>pyRemoteDDRS4PALS</b> - A python module providing remote control of DDRS4PALS software enabling its full integration into any measurement environment. <br>

# Quickstart Guide

* import the 'pyRemoteDDRS4PALS' module

```python
import remoteddrs4pals as rcddrs4pals
```

* initiate a session

```python
HOST = '127.0.0.1'  # the server's hostname or IP address
PORT = 4000         # the port used by the server (set in DDRS4PALS)

my_session = rcddrs4pals.startRemoteSession(host=HOST,port=PORT)
```
* optional: check if the versions of 'pyRemoteDDRS4PALS' module and DDRS4PALS are matching

```python
valid_handshake = True

if not rcddrs4pals.handshake(my_socket=my_session):
  print('version handshake failed ...')
  
  valid_handshake = False
        
assert valid_handshake == True
```

* ... do your stuff (see examples) ...

* close your session

```python
rcddrs4pals.closeRemoteSession(my_socket=my_session)
```
# Available Remote Control Functions

* initiates a remote session
```python
startRemoteSession(host,port) : returns: socket
```

* closes a remote session
```python
closeRemoteSession(my_socket) : returns: void
```

* performs a handshake between the 'pyRemoteDDRS4PALS' module (client) and DDRS4PALS (server) versions
```python
handshake(my_socket) : returns: True/False
```

* start the acquisition
```python
startAcquisition(my_socket) : returns: True/False
```

* stop the acquisition
```python
stopAcquisition(my_socket) : returns: True/False
```

* returns if an acquisition is running
```python
isAcquisitionRunning(my_socket) : returns: True/False
```

* returns the counts of spectrum A-B
```python
getCountsOfABSpectrum(my_socket) : returns: int
```

* returns the counts of spectrum B-A
```python
getCountsOfBASpectrum(my_socket) : returns: int
```

* returns the counts of the merged spectrum
```python
getCountsOfMergedSpectrum(my_socket) : returns: int
```

* returns the counts of the prompt spectrum
```python
getCountsOfPromptSpectrum(my_socket) : returns: int
```

* prompts a reset of spectrum A-B
```python
resetABSpectrum(my_socket) : returns: True/False
```

* prompts a reset of spectrum B-A
```python
resetBASpectrum(my_socket) : returns: True/False
```

* prompts a reset of the merged spectrum
```python
resetMergedSpectrum(my_socket) : returns: True/False
```

* prompts a reset of the prompt spectrum
```python
resetPromptSpectrum(my_socket) : returns: True/False
```

* prompts a reset of all spectra together
```python
resetAllSpectra(my_socket) : returns: True/False
```

* returns the data of spectrum A-B
```python
getDataOfABSpectrum(my_socket) : returns: dictionary = {
                                          "channel-width": int,
                                          "no-of-channel": int,
                                          "integral-counts": int,
                                          "spectrum-data": np.array
                                          }
```

* returns the data of spectrum B-A
```python
getDataOfBASpectrum(my_socket) : returns: dictionary = {
                                          "channel-width": int,
                                          "no-of-channel": int,
                                          "integral-counts": int,
                                          "spectrum-data": np.array
                                          }
```

* returns the data of the merged spectrum
```python
getDataOfMergedSpectrum(my_socket) : returns: dictionary = {
                                          "channel-width": int,
                                          "no-of-channel": int,
                                          "integral-counts": int,
                                          "spectrum-data": np.array
                                          }
```

* returns the data of the prompt spectrum
```python
getDataOfPromptSpectrum(my_socket) : returns: dictionary = {
                                          "channel-width": int,
                                          "no-of-channel": int,
                                          "integral-counts": int,
                                          "spectrum-data": np.array
                                          }
```

* halts until the desired 'counts' are reached in spectrum A-B
```python
waitUntilCountsForABSpectrum(my_socket,counts) : returns: void
```

* halts until the desired 'counts' are reached in spectrum B-A
```python
waitUntilCountsForBASpectrum(my_socket,counts) : returns: void
```

* halts until the desired 'counts' are reached in the merged spectrum
```python
waitUntilCountsForMergedSpectrum(my_socket,counts) : returns: void
```

* halts until the desired 'counts' are reached in the prompt spectrum
```python
waitUntilCountsForPromptSpectrum(my_socket,counts) : returns: void
```

* returns the currently loaded settings in DDRS4PALS
```python
getSettings(my_socket,counts) : returns: xml-string
```

# Examples

Examples can be found in the folder '/examples'.

## Example 1: in-situ measurement

```python
import remoteddrs4pals as rcddrs4pals

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

HOST = '127.0.0.1'  # the server's hostname or IP address
PORT = 4000         # the port used by the server (set in DDRS4PALS)

number_of_runs           = 1000
number_of_counts_per_run = 1E5

if __name__ == '__main__':
    rcddrs4pals.__information__()
    
    # initiate a remote session to communicate with DDRS4PALS ...
    my_session = rcddrs4pals.startRemoteSession(host=HOST,port=PORT)
    
    # check for the correct protocol versions between DDRS4PALS and the remoteddrs4pals module ... 
    valid_handshake = True
    if not rcddrs4pals.handshake(my_socket=my_session):
        print('version handshake failed ...')
        valid_handshake = False
        
    assert valid_handshake == True
    
    # start the aquisition ...
    if not rcddrs4pals.isAcquisitionRunning(my_socket=my_session):
        rcddrs4pals.startAcquisition(my_socket=my_session)
        
    # start in-situ runs ...
    for i in range(0,number_of_runs):
    
        # reset spectrum of A-B ...
        rcddrs4pals.resetABSpectrum(my_socket=my_session)
    
        # wait until the spectrum of A-B reached the desired counts ...
        rcddrs4pals.waitUntilCountsForABSpectrum(my_socket=my_session,counts=number_of_counts_per_run)

        # request the data of spectrum A-B ...
        spectrum_data = rcddrs4pals.getDataOfABSpectrum(my_socket=my_session)
        
        # save your spectrum ...
        filename = 'your_directory/spec{}_{}.txt'.format(i,datetime.now().strftime("%m_%d_%Y_%H_%M_%S"))
        
        np.savetxt(filename,spectrum_data["spectrum-data"],fmt='%0d',newline='\n',header='counts at channel-width {}ps'.format(spectrum_data["channel-width"]))
    
    # stop the acquisition ...
    rcddrs4pals.stopAcquisition(my_socket=my_session)
    
    # don't forget to close the session at the end ...
    rcddrs4pals.closeRemoteSession(my_socket=my_session)
```

# How to cite this Program?

* <b>When running this software for your research purposes you should at least cite the following publication.</b><br>

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.softx.2019.100261-yellowgreen)](https://doi.org/10.1016/j.softx.2019.100261)

[DDRS4PALS: A software for the acquisition and simulation of lifetime spectra using the DRS4 evaluation board](https://www.sciencedirect.com/science/article/pii/S2352711019300676)<br>

* <b>Additionally, you must cite the applied version of this software in your study.</b><br>

You can cite all released software versions by using the <b>DOI 10.5281/zenodo..4767301</b>. This DOI represents all versions, and will always resolve to the latest one.<br>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4767301.svg)](https://doi.org/10.5281/zenodo.4767301)

## ``v1.x``
<b>pyRemoteDDRS4PALS v1.0 (minimum required version DDRS4PALS v1.17)</b><br>[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4767302.svg)](https://doi.org/10.5281/zenodo.4767302)<br>
 
 # License of pyRemoteDDRS4PALS (GNU General Public License) 
 Copyright (c) 2021 Danny Petschke (danny.petschke@uni-wuerzburg.de) All rights reserved.<br>

<p align="justify">This program is free software: you can redistribute it and/or modify<br>
it under the terms of the GNU General Public License as published by<br>
the Free Software Foundation, either version 3 of the License, or<br>
(at your option) any later version.<br><br>

This program is distributed in the hope that it will be useful,<br>
but WITHOUT ANY WARRANTY; without even the implied warranty of<br>
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.<br><br></p>

For more details see [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0)
