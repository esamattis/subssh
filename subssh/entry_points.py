

import sys


def xmlrpc_server():
    from subssh import xmlrpc
    sys.exit(xmlrpc.standalone_xmlrpc_server() or 0)

def admin_tools():
    from subssh import admintools
    sys.exit(admintools.handle_cmdline() or 0)

def main():
    from subssh import dispatcher
    sys.exit(dispatcher.dispatch() or 0)
