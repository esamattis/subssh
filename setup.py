'''
Created on Mar 27, 2010

@author: epeli
'''

import os
from distutils.core import setup



docs = [os.path.join("doc", dir) for dir in os.listdir("doc")]

f = open('subssh/version.txt', 'r')
version = f.read()
f.close()


setup(
      name='subssh',
      version=version,
      description='Bare minimal shell for using eg. Git and Subversion over SSH',
      author='Esa-Matti Suuronen',
      author_email='esa-matti@suuronen.org',
      url='http://github.com/epeli/subssh',
      license='AGPL',
      package_dir={'subssh': 'subssh'},
      package_data={'subssh': ['default/*', 'version.txt']},
      data_files=[('share/subssh/doc', docs)],
      packages=['subssh', 
                'subssh.app', 
                'subssh.app.vcs'],
      scripts=['scripts/subssh', 
               'scripts/subssh-admin', 
               'scripts/subssh-xmlrpc'],
)
