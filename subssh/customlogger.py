'''
Created on Mar 21, 2010

@author: epeli
'''

import os.path
import logging
logging.root.setLevel(logging.DEBUG)

from logging.handlers import TimedRotatingFileHandler

import config


def get_logger(name, filepath=config.LOG_ERROR, level=logging.DEBUG):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        fh = TimedRotatingFileHandler(filepath, when='W0')
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger


def get_user_logger(username):
    
    logger = logging.getLogger(username)
    
    filepath = os.path.join(config.LOG_USERS, username + ".log" )
    
    if not logger.handlers:
        fh = TimedRotatingFileHandler(filepath, when='W0')
        formatter = logging.Formatter("%(asctime)s %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger    
    
