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

from tools import writeln, errln, to_bool
from tools import call, check_call
from tools import InvalidArguments, UserException
from tools import safe_chars, safe_chars_only_pat
from tools import hostusername
from tools import expand_subssh_vars
from tools import get_user_object

from appexpose import expose, expose_instance

# Decorators
from appexpose import exposable_as, expose_as
from appexpose import no_interactive, no_direct_access


import config