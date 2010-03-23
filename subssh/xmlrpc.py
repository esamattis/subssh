'''
Created on Mar 19, 2010

@author: epeli
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

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
    



def standalone_xmlrpc_server(listen, port):
    server = SimpleXMLRPCServer((listen, port),
                                requestHandler=RequestHandler)
    
    server.register_function(ping)
    server.register_function(add_key)
    tools.errln("Starting XML-RPC server on http://%s:%s%s" % 
                (listen, port, RequestHandler.rpc_paths[0]))
    server.serve_forever()

if __name__ == "__main__":
    standalone_xmlrpc_server("localhost", 8001)
    

    