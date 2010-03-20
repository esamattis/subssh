'''
Created on Mar 19, 2010

@author: epeli
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer


from subssh.authorizedkeys import AuthorizedKeysDB

def add_key_(username, pubkey):
    db = AuthorizedKeysDB()
    
    db.ad
    