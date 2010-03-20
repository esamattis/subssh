'''
Created on Mar 19, 2010

@author: epeli
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


from authorizedkeys import AuthorizedKeysDB
from keyparsers import parse_public_key, PubKeyException


def add_key(username, pubkey):
    db = AuthorizedKeysDB()
    type, key, comment = parse_public_key(pubkey)
    db.add_key(username, type, key, comment)
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
    server.serve_forever()

if __name__ == "__main__":
    standalone_xmlrpc_server("localhost", 8001)
    

    