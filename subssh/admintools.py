'''
Created on Mar 21, 2010

@author: epeli
'''

import shutil

from authorizedkeys import AuthorizedKeysDB
import config

def rewrite_authorized_keys():
    db = AuthorizedKeysDB()
    db.commit()
    db.close()
    return 0

def restore_config():
    shutil.copy(config.DEFAULT_CONFIG_PATH, config.CONFIG_PATH)
    return 0


