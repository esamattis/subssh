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
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from optparse import OptionParser

from authorizedkeys import AuthorizedKeysDB
import tools
import config

class Unauthorized(Exception): pass


def add_key(username, pubkey):
    if username == config.ADMIN:
        raise Unauthorized("Cannot set admin's key over xmlrpc!")
    
    db = AuthorizedKeysDB()
    db.add_key_from_str(username, pubkey)
    db.commit()
    db.close()
    
    return True
    
def ping():
    return "pong"    
    
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/subssh/rpc2',)
    

def setup_server(listen, port):
    server = SimpleXMLRPCServer((listen, port),
                                requestHandler=RequestHandler)
    
    server.register_function(ping)
    server.register_function(add_key)
    return server    


def standalone_xmlrpc_server():
    """Standalone XML-RPC server. Can be used to manage subssh users from 
remote machine.
    """
    parser = OptionParser(usage="%s [listen address] [port]"  % sys.argv[0],
                          description=standalone_xmlrpc_server.__doc__ )
                         
    
    
    options, args = parser.parse_args()
    
    
    try:
        listen = args[0]
    except IndexError:
        listen = "127.0.0.1"
    
    try:
        port = int(args[1])
    except (IndexError, ValueError):
        port = 8000
    
    
    server = setup_server(listen, port)

    tools.errln("Starting XML-RPC server on http://%s:%s%s" % 
                (listen, port, RequestHandler.rpc_paths[0]))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except Exception, e:
        tools.errln("Got %s" % e)
        return 1

if __name__ == "__main__":
    standalone_xmlrpc_server()
    

    