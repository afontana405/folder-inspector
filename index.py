# Python Standard Libaries 
import os
import re
import logging
import platform
import socket
import uuid
import time
import hashlib

import psutil  # pip install psutil

LogFile = input("Enter File (including '.txt' extension) Name to log data into")
startTime = time.time()
spacerLen = 40

#local functions
def getSystemInfo():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return info
    except Exception as e:
        logging.exception(e)
        return False
    
def HashFile(absPath): #returns sha-256 hash of file
    try:
        with open(absPath, 'rb') as target:
            
            fileContents = target.read()
            
            sha256Obj = hashlib.sha256()
            sha256Obj.update(fileContents)
            hexDigest = sha256Obj.hexdigest()
            return True, None, hexDigest
    except Exception as err:
        sys.exit("\nException: "+str(err))
 
def GetFileMetaData(absPath):
    ''' 
        obtain filesystem metadata
        from the specified file
        specifically, fileSize and MAC Times
    '''
    try:
        metaData         = os.stat(absPath)       # Use the stat method to obtain meta data
        fileSize         = metaData.st_size         # Extract fileSize and MAC Times in human readable format
        timeLastModified = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(metaData.st_mtime))
        timeLastAccess   = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(metaData.st_atime))
        timeCreated      = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(metaData.st_ctime))
        
        macTimeList = [timeLastModified, timeLastAccess, timeCreated] # Group the MAC Times in a List
        return True, None, fileSize, macTimeList
    
    except Exception as err:
        return False, str(err), None, None 