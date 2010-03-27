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


import os
import sys
import socket
import shutil
from ConfigParser import SafeConfigParser

_THIS_DIR = os.path.abspath(os.path.dirname(__file__))

LOG_ACCESS = os.path.join( os.environ["HOME"], ".subssh", "access.log" )

LOG_ERROR = os.path.join( os.environ["HOME"], ".subssh", "error.log" )

LOG_USERS = os.path.join( os.environ["HOME"], ".subssh", "users" )

TRACEBACKS = os.path.join( os.environ["HOME"], ".subssh", "tracebacks" )

DISPLAY_HOSTNAME = socket.gethostname() 

SUBSSH_BIN = os.path.join(sys.prefix, "bin", "subssh")

DEFAULT_CONFIG_PATH = os.path.join(_THIS_DIR, "default", "config")

SUBSSH_HOME = os.path.join(os.environ['HOME'], ".subssh")

CONFIG_PATH = os.path.join(SUBSSH_HOME, "config")

ADMIN = "admin"

# Used to determine where subssh is installed.
SUBSSH_PYTHONPATH = ""

for dir in (SUBSSH_HOME, LOG_USERS, TRACEBACKS):
    if not os.path.exists(dir):
        os.mkdir(dir)
        
# Copy default config
if not os.path.exists(CONFIG_PATH):
    shutil.copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)


_config = SafeConfigParser()
_config.read(CONFIG_PATH)

for option, value in _config.items("general"):
    globals()[option.upper()] = value


def first_to_upper(pair_list):
    return [(first.upper(), second) for first, second in pair_list]
        

def yield_enabled_apps():
    for sec in _config.sections():
        if sec.startswith("app:"):
            yield (sec.replace("app:", "").strip(),
                   first_to_upper(_config.items(sec)))
            
        
