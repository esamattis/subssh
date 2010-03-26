'''
Created on Mar 25, 2010

@author: epeli
'''


#This dictionary holds all active application in subssh
cmds = {}


def user_apps():
    return [ (app_name, app) for app_name, app in cmds.items()
             if not getattr(app, "no_user", False) ]