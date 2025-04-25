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