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


#This dictionary holds all active application in subssh
cmds = {}

def user_apps():
    return [ (app_name, app) for app_name, app in cmds.items()
             if not getattr(app, "disable_interactive", False) ]
    
def direct_apps():
    return [ (app_name, app) for app_name, app in cmds.items()
             if not getattr(app, "disable_direct", False) ]    