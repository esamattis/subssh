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

import readline

import apprunner
import tools
import config
import active

def complete(text, state):
    for cmd, app in active.user_apps():
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1

readline.set_completer_delims(' `~!@#$%^&*()=+[{]}\|;:\'",<>/?')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def parse_command(cmd_string):

    parts = cmd_string.split()

    try:
        cmd = parts[0]
    except IndexError:
        return "", []

    return cmd, parts[1:]

def prompt(user):
    exit_status = 0
    cmd = ""
    args = []
    promt_str = "%s@%s> " % (user.username, config.DISPLAY_HOSTNAME)

    while cmd not in ("exit", "logout"):
        try:
            input = raw_input(promt_str)
        except KeyboardInterrupt:
            print
            continue
        except EOFError:
            print "exit",
            return 0

        cmd, args = parse_command(input)

        if not cmd:
            continue

        user.cmd = cmd
        user.args = args
        exit_status = apprunner.run(user)

    return exit_status
