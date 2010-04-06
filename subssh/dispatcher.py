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


import config



import customlogger
logger = customlogger.get_logger(__name__)

access_logger = customlogger.get_logger("access", filepath=config.LOG_ACCESS)


import apprunner
import shell
import tools
import appimporter
appimporter.import_all_apps_from_config()




def dispatch():
    
    user = tools.get_user()

    
    if user.cmd:
        user.interactive = False
        return apprunner.run(user)
    else:
        user.interactive = True
        return shell.prompt(user)
        
    


