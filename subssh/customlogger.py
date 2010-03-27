# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Esa-Matti Suuronen <esa-matti@suuronen.org>

This file is part of subssh.

Subssh is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

Subssh is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public 
License along with Subssh.  If not, see 
<http://www.gnu.org/licenses/>.
"""

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
    
