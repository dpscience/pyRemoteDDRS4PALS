# -*- coding: utf-8 -*-
"""
Created on Fri May 14 10:59:33 2021

@author: Danny Petschke
@email: danny.petschke@uni-wuerzburg.de

"""

#*************************************************************************************************
#**")
#** Copyright (c) 2021 Danny Petschke. All rights reserved.
#**")
#** This program is free software: you can redistribute it and/or modify
#** it under the terms of the GNU General Public License as published by
#** the Free Software Foundation, either version 3 of the License, or
#** (at your option) any later version.
#**
#** This program is distributed in the hope that it will be useful,
#** but WITHOUT ANY WARRANTY; without even the implied warranty of
#** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#** GNU General Public License for more details.
#**")
#** You should have received a copy of the GNU General Public License
#** along with this program. If not, see http://www.gnu.org/licenses/.
#**
#** Contact: danny.petschke@uni-wuerzburg.de
#**
#*************************************************************************************************

# include 'remoteDDRS4PALS' module
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