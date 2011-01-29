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


This file is not for editing! You can override these settings in ~/.subssg/config -file


"""


import os
import sys
import socket
import shutil
from ConfigParser import SafeConfigParser

from subssh.dirtools import create_required_directories_or_die


_read_only_settings = set(("SUBSSH_HOME", "CONFIG_PATH", "DEFAULT_CONFIG_PATH"))
_THIS_DIR = os.path.abspath(os.path.dirname(__file__))
SUBSSH_HOME = os.path.join(os.environ['HOME'], ".subssh")
CONFIG_PATH = os.path.join(SUBSSH_HOME, "config")
# TODO: should use pkg_resources
DEFAULT_CONFIG_PATH = os.path.join(_THIS_DIR, "default", "config")


DEBUG = False
DEBUG_USER = False

LOG_ACCESS = os.path.join( os.environ["HOME"], ".subssh", "log", "access.log" )

LOG_ERROR = os.path.join( os.environ["HOME"], ".subssh", "log", "error.log" )

LOG_USERS = os.path.join( os.environ["HOME"], ".subssh", "log", "users" )

TRACEBACKS = os.path.join( os.environ["HOME"], ".subssh", "log", "tracebacks" )

DISPLAY_HOSTNAME = socket.gethostname()

SUBSSH_BIN = os.path.join(os.getcwd(),
                          os.path.dirname(sys.argv[0]),
                          "subssh")



ADMIN = "admin"

# XMLRPC shit
XMLRPC_PATH = "subssh"
XMLRPC_LOG = os.path.join( os.environ["HOME"], ".subssh", "xmlrpc.log" )
XMLRPC_LISTEN = "127.0.0.1"
XMLRPC_PORT = 8000

# Used to determine where subssh is installed.
SUBSSH_PYTHONPATH = ""


# Create necessary paths
create_required_directories_or_die((SUBSSH_HOME,
                                    os.path.dirname(LOG_ACCESS),
                                    LOG_USERS,
                                    TRACEBACKS))


# Copy default config
if not os.path.exists(CONFIG_PATH):
    try:
        shutil.copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)
    except OSError, e:
        sys.stderr.write("Cannot copy default config from '%s' to '%s' Reason: %s \n"
                         % (DEFAULT_CONFIG_PATH, CONFIG_PATH, " ".join(e.args()) ))
        sys.exit(1)





_user_config = SafeConfigParser()
_user_config.read(CONFIG_PATH)
_this_module = sys.modules[__name__]


# Override defaults with user configurations
for option, value in _user_config.items("subssh"):
    option = option.upper()

    # Don't allow funny settings
    if option in _read_only_settings or option.startswith("_"):
        # TODO: should show warning or even die
        continue # skip

    setattr(_this_module, option, value)



def _first_to_upper(pair_list):
    return [(first.upper(), second) for first, second in pair_list]


def yield_enabled_apps():
    for sec in _user_config.sections():
        if sec.startswith("app:"):
            yield (sec.replace("app:", "").strip(),
                   _first_to_upper(_user_config.items(sec)))


