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

import sys
import os
import traceback

import config
import buildins
import tools
import active



def run(user):
    # Log all commands that are ran
    # TODO: preserve history for prompt


    user.logger.info("%s %s" % (user.cmd, user.args))

    try:
        app = active.cmds[user.cmd]
    except KeyError:
        sys.stderr.write("Unknown command '%s'\n" % user.cmd)
        return 1



    try:
        # Ignore "user" which is always supplied.
        tools.assert_args(app, user.args, ignore=1)
        # Execute the app
        return app(user, *user.args)
    except tools.InvalidArguments, e:
        tools.errln("Invalid arguments. %s" % e.args[0])
        buildins.show_doc(user, user.cmd)
        return 1
    except tools.UserException, e:
        # Expected exception. Print error to user.
        tools.errln("%s: %s" % (e.__class__.__name__, e.args[0]))
        if config.DEBUG_USER:
            tools.set_text_color("green")
            tools.errln("USER DEBUG MODE (no real error):")
            traceback.print_exc()
            tools.reset_text_color()
        return 1
    except Exception, e:
        # Unexpected exception! Log it!

        #  We can just print the traceback if user is admin or if we are in debug mode
        if user.username == config.ADMIN or config.DEBUG:
            tools.set_text_color("red")
            traceback.print_exc()
            tools.reset_text_color()
        else:
            # Log traceback
            import time
            timestamp = time.time()

            f = open(os.path.join(config.TRACEBACKS,
                                  "%s-%s" % (timestamp, user.username)),
                    "w")

            f.write("%s %s\n" % (user.cmd, user.args))
            traceback.print_exc(file=f)
            f.close()

            try:
                message = e.args[0]
            except IndexError:
                message = "..."
            tools.errln("System error (%s): %s: %s" % (timestamp,
                                                   e.__class__.__name__,
                                                   message))
        tools.errln("Could be a bug in the software. "
                    "Please report: https://github.com/epeli/revisioncask/issues")

        return 1


