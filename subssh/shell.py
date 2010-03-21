'''
Created on Mar 20, 2010

@author: epeli
'''


import readline
import traceback

import apploader
import tools
import config




def complete(text, state):
    for cmd in apploader.user_apps():
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


def prompt(username):
    

    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    
    exit_status = 0
    cmd = ""
    args = []
    promt_str = "%s@%s> " % (username, config.PROMPT_HOST)
    
    while cmd not in ("exit", "logout"):
        try:
            input = raw_input(promt_str)
        except KeyboardInterrupt:
            print
            continue
        except EOFError:
            print "logout",
            return 0
        
        cmd, args = tools.to_cmd_args(input)
        
        if not cmd:
            continue
        
        try:
            exit_status = apploader.run(username, cmd, args)
        except Exception, e:
            if username == tools.admin_name():
                traceback.print_exc()
            else:
                tools.errln(e.args[0])
    
    return exit_status

    
