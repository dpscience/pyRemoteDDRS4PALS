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

HOST = '127.0.0.1'  # the server's hostname or IP address
PORT = 4000         # the port used by the server (set in DDRS4PALS)

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
    
    # reset all spectra ...
    rcddrs4pals.resetAllSpectra(my_socket=my_session)
    
    # wait until the spectrum of A-B reached 5 Mio. counts ...
    rcddrs4pals.waitUntilCountsForABSpectrum(my_socket=my_session,counts=5E6)

    # request the data of spectrum A-B ...
    spectrum_data = rcddrs4pals.getDataOfABSpectrum(my_socket=my_session)
    
    spectrum = spectrum_data["spectrum-data"]
    
    print(spectrum_data["channel-width"]) # ps
    print(spectrum_data["no-of-channel"])
    print(spectrum_data["integral-counts"])
    
    plt.semilogy(spectrum,'bo')
    plt.show()
    
    # stop the acquisition ...
    rcddrs4pals.stopAcquisition(my_socket=my_session)
    
    # don't forget to close the session at the end ...
    rcddrs4pals.closeRemoteSession(my_socket=my_session)