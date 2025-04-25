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

#Text file data is logged into
LogFile = "ScriptLog.txt" # Change string to name of your text file or uncomment line below to allow you to choose file upon runtime
#LogFile = input("Enter File (including '.txt' extension) Name to log data into")
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
    
def main():
    
    investigator = input("Investigator Name:  ")   # Enter Your Name at this prompt
    targetFolder = input("Enter Target Folder: ")  # Enter pathway of folder to be examined
    
    # Remove any old logging script
    if os.path.isfile(LogFile):   
        os.remove(LogFile)
    
    # configure the python logger
    logging.basicConfig(filename=LogFile, level=logging.DEBUG, format='%(process)d-%(levelname)s-%(asctime)s %(message)s')
    logging.info("Script Start\n")
    
    sysInfo = getSystemInfo()
    
    if sysInfo: #Writes system info to LogFile
        logging.info(f"Investigator Name:  {investigator}")
        logging.info(f"Target Folder:      {targetFolder}")
        logging.info("=" * spacerLen) # visual spacers
        logging.info("")
        logging.info("*****SYSTEM INFO*****")
        for key, value in sysInfo.items():
            logging.info(f"     {key}:   {value}")
        logging.info("=" * spacerLen) # visual spacers
        logging.info("")
        
    fileCount = 0   
    for currentRoot, dirList, fileList in os.walk(targetFolder): 
    
        for nextFile in fileList: 
            try:
                fullPath = os.path.join(currentRoot, nextFile)
                absPath  = os.path.abspath(fullPath)
                
                success, errInfo, fileSize, macTimeList = GetFileMetaData(absPath) #calls function to retrieve meta data about file
                success, errInfo, hexDigest = HashFile(absPath) #calls function to hash file          
            
                logging.info(f"     Path:          {fullPath}") 
                logging.info(f"     File Size:     {fileSize}") 
                logging.info(f"     Last-Modified: {macTimeList[0]}") 
                logging.info(f"     Last Accessed: {macTimeList[1]}") 
                logging.info(f"     Created:       {macTimeList[2]}") 
                logging.info(f"     SHA-256:       {hexDigest}") 
                logging.info("=" * spacerLen) # visual spacers
                logging.info("")
                fileCount += 1 #increment count
            except Exception as err:
                print('Error:   ', str(err))
    
    formattedTime = FindRunTime()
    
    logging.info(f"Files Processed:        {fileCount}")
    logging.info(f"Elapesed Time hh:mm:ss: {formattedTime}")
                
    logging.info("Status:   Script Ended")
    
if __name__ == '__main__':
    main()
    print("\nScript End")