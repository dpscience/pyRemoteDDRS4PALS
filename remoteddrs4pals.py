# -*- coding: utf-8 -*-
"""
Created on Fri May 14 10:59:33 2021

@author: Danny Petschke
@email: danny.petschke@uni-wuerzburg.de

"""

#*************************************************************************************************
#**")
#** Copyright (c) 2021 Dr. Danny Petschke. All rights reserved.
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

__version = 1.0 

__requiredDDRS4PALS_version_major = 1
__requiredDDRS4PALS_version_minor = 17

def __information__():
    print("#******************* pyRemoteDDRS4PALS 1.0 (17.05.2021) *******************")
    print("#**")
    print("#** Copyright (C) 2021 Dr. Danny Petschke")
    print("#**")
    print("#** Contact: danny.petschke@uni-wuerzburg.de")
    print("#**")
    print("#***************************************************************************\n")

def __licence__():
    print("#*************************************************************************************************")
    print("#**")
    print("#** Copyright (c) 2021 Danny Petschke. All rights reserved.")
    print("#**")
    print("#** This program is free software: you can redistribute it and/or modify") 
    print("#** it under the terms of the GNU General Public License as published by")
    print("#** the Free Software Foundation, either version 3 of the License, or")
    print("#** (at your option) any later version.")
    print("#**")
    print("#** This program is distributed in the hope that it will be useful,") 
    print("#** but WITHOUT ANY WARRANTY; without even the implied warranty of") 
    print("#** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the")
    print("#** GNU General Public License for more details.")  
    print("#**")
    print("#** You should have received a copy of the GNU General Public License")  
    print("#** along with this program. If not, see http://www.gnu.org/licenses/.")
    print("#**")
    print("#** Contact: danny.petschke@uni-wuerzburg.de")
    print("#**")
    print("#*************************************************************************************************")

import socket

def parseBetween(data_in='',start='<reply>',stop='</reply>'):
    index_start = data_in.find(start)
    index_stop  = data_in.find(stop)
    
    if index_start == -1:
        index_start = 0
        
    if index_stop == -1:
        index_stop = len(data_in)-1
        
    if index_start+len(start) >= len(data_in[:index_stop]):
        index_start = 0
    
    return data_in[index_start+len(start):index_stop]

def send(my_socket,request_id=0):
    my_socket.sendall(str.encode('<request>{}</request>'.format(request_id)))
    
def decodeData(data_in):
    data = []
    
    i = 0
    start_index = 0
    stop_index = 0
    
    while i < len(data_in):
        if data_in[i] == '{':
            start_index = i
            
            while data_in[i] != '}':
                i += 1
                
            stop_index = i+1
        i += 1
            
        data.append(int(parseBetween(data_in=data_in[start_index:stop_index],start='{',stop='}')))
        
    return data           
        
def isRequestValid(data_in=''):
    if len(data_in) < len('<request-valid?>') + len('</request-valid?>'):
        return False
    
    if data_in.find('<request-valid?>') == -1 or data_in.find('</request-valid?>') == -1:
        return False
    
    reply = int(parseBetween(data_in=data_in,start='<request-valid?>',stop='</request-valid?>'))
    
    if reply == 1:
        reply = True
    else:
        reply = False
        
    return reply 
    
def readAll(my_socket):
    data = my_socket.recv(1024).decode('utf8')
    
    while data.find('</reply>') == -1:
        data = data + my_socket.recv(1024).decode('utf8')
                
    return parseBetween(data_in=data,start='<reply>',stop='</reply>')

def startRemoteSession(host='127.0.0.1',port=4000,my_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)):
    my_socket.connect((host,port))
    
    return my_socket
        
def closeRemoteSession(my_socket):
    my_socket.close()

def minRequiredDDRS4PALSVersionMajor():
    return __requiredDDRS4PALS_version_major

def minRequiredDDRS4PALSVersionMinor():
    return __requiredDDRS4PALS_version_minor

def handshake(my_socket):
    request_id = 17
    
    send(my_socket=my_socket,request_id=request_id)
    
    reply = readAll(my_socket=my_socket)
    
    if not isRequestValid(data_in=reply):
        return False
    
    version = parseBetween(data_in=reply,start='<reply-data>',stop='</reply-data>')
    
    v_major = int(parseBetween(data_in=version,start='<major>',stop='</major>'))
    v_minor = int(parseBetween(data_in=version,start='<minor>',stop='</minor>'))
    
    if v_minor >= minRequiredDDRS4PALSVersionMinor() and v_major >= minRequiredDDRS4PALSVersionMajor():
        return True
    
    return False

def startAcquisition(my_socket):
    request_id = 0
    
    send(my_socket=my_socket,request_id=request_id)
    
    reply = readAll(my_socket=my_socket)
       
    return isRequestValid(data_in=reply)

def getSettings(my_socket):
    request_id = 16
    
    send(my_socket=my_socket,request_id=request_id)
    
    reply = readAll(my_socket=my_socket)
    
    valid = isRequestValid(data_in=reply)
    
    settings = ""
    
    if valid:
        settings = parseBetween(data_in=reply,start='<reply-data>',stop='</reply-data>')
    
    return settings
    
def stopAcquisition(my_socket):
    request_id = 1
    
    send(my_socket=my_socket,request_id=request_id)
    
    reply = readAll(my_socket=my_socket)
       
    return isRequestValid(data_in=reply)

def isAcquisitionRunning(my_socket):
    request_id = 2
    
    send(my_socket=my_socket,request_id=request_id)
    
    reply = readAll(my_socket=my_socket)
    
    valid = isRequestValid(data_in=reply)
    
    running = 0
    
    if valid:
        running = parseBetween(data_in=reply,start='<reply-data>',stop='</reply-data>')
                
    if running == 1:
        running = True
    else:
        running = False
        
    return running
    
# returns the number of counts for a specific spectrum ...
def getCounts(my_socket,spectra_type='AB'):
    request_id = False
    
    if spectra_type == 'AB':
        request_id = 12
    elif spectra_type == 'BA':
        request_id = 13
    elif spectra_type == 'merged':
        request_id = 14
    elif spectra_type == 'prompt':
        request_id = 15
    else:
        assert request_id == True
    
    send(my_socket=my_socket,request_id=request_id)
    
    reply = readAll(my_socket=my_socket)
    
    valid = isRequestValid(data_in=reply)
    
    counts = 0
    
    if valid:
        counts = parseBetween(data_in=reply,start='<reply-data>',stop='</reply-data>')
        
    return int(counts)

def getCountsOfABSpectrum(my_socket):
    return getCounts(my_socket=my_socket,spectra_type='AB')  

def getCountsOfBASpectrum(my_socket):
    return getCounts(my_socket=my_socket,spectra_type='BA')

def getCountsOfMergedSpectrum(my_socket):
    return getCounts(my_socket=my_socket,spectra_type='merged')

def getCountsOfPromptSpectrum(my_socket):
    return getCounts(my_socket=my_socket,spectra_type='prompt')  

def resetSpectrum(my_socket,spectra_type='AB'):
    request_id = False
    
    if spectra_type == 'all':
        request_id = 3
    elif spectra_type == 'AB':
        request_id = 4
    elif spectra_type == 'BA':
        request_id = 5
    elif spectra_type == 'merged':
        request_id = 6
    elif spectra_type == 'prompt':
        request_id = 7
    else:
        assert request_id == True
        
    send(my_socket=my_socket,request_id=request_id)
    
    reply = readAll(my_socket=my_socket)
       
    return isRequestValid(data_in=reply)

def resetAllSpectra(my_socket):
    return resetSpectrum(my_socket=my_socket,spectra_type='all')

def resetABSpectrum(my_socket):
    return resetSpectrum(my_socket=my_socket,spectra_type='AB')

def resetBASpectrum(my_socket):
    return resetSpectrum(my_socket=my_socket,spectra_type='BA')

def resetMergedSpectrum(my_socket):
    return resetSpectrum(my_socket=my_socket,spectra_type='merged')

def resetPromptSpectrum(my_socket):
    return resetSpectrum(my_socket=my_socket,spectra_type='prompt')

def getData(my_socket,spectra_type='AB'):
    request_id = False
    
    if spectra_type == 'AB':
        request_id = 8
    elif spectra_type == 'BA':
        request_id = 9
    elif spectra_type == 'merged':
        request_id = 10
    elif spectra_type == 'prompt':
        request_id = 11
    else:
        assert request_id == True
        
    send(my_socket=my_socket,request_id=request_id)
    
    reply = readAll(my_socket=my_socket)
    
    valid = isRequestValid(data_in=reply)
    
    data_dict = {
                "channel-width": 0.0,
                "no-of-channel": 0,
                "integral-counts": 0,
                "spectrum-data": []
                }
    
    if valid:
        reply_data = parseBetween(data_in=reply,start='<reply-data>',stop='</reply-data>')
        
        channel_width   = parseBetween(data_in=reply_data,start='<channel-width-ps>',stop='</channel-width-ps>')
        no_of_channel   = parseBetween(data_in=reply_data,start='<number-of-channel>',stop='</number-of-channel>')
        integral_counts = parseBetween(data_in=reply_data,start='<integral-counts>',stop='</integral-counts>')
        
        lt_data = parseBetween(data_in=reply_data,start='<data>',stop='</data>')
        
        spectrum = decodeData(lt_data)
        
        data_dict["channel-width"] = channel_width
        data_dict["no-of-channel"] = no_of_channel
        data_dict["integral-counts"] = integral_counts
        data_dict["spectrum-data"] = spectrum
    
    return data_dict

def getDataOfABSpectrum(my_socket):
    return getData(my_socket=my_socket,spectra_type='AB')

def getDataOfBASpectrum(my_socket):
    return getData(my_socket=my_socket,spectra_type='BA')

def getDataOfMergedSpectrum(my_socket):
    return getData(my_socket=my_socket,spectra_type='merged')

def getDataOfPromptSpectrum(my_socket):
    return getData(my_socket=my_socket,spectra_type='prompt')
    
def waitUntilCountsForABSpectrum(my_socket,counts=10000):
    while True:
        if getCountsOfABSpectrum(my_socket=my_socket) >= counts:
            break
        
def waitUntilCountsForBASpectrum(my_socket,counts=10000):
    while True:
        if getCountsOfBASpectrum(my_socket=my_socket) >= counts:
            break

def waitUntilCountsForMergedSpectrum(my_socket,counts=10000):
    while True:
        if getCountsOfMergedSpectrum(my_socket=my_socket) >= counts:
            break
        
def waitUntilCountsForPromptSpectrum(my_socket,counts=10000):
    while True:
        if getCountsOfPromptSpectrum(my_socket=my_socket) >= counts:
            break