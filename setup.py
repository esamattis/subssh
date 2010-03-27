'''
Created on Mar 27, 2010

@author: epeli
'''

import os
from distutils.core import setup



docs = [os.path.join("doc", dir) for dir in os.listdir("doc")]

setup(
      name='subssh',
      version='0.1',
      description='Bare minimal shell for using eg. Git and Subversion over SSH',
      author='Esa-Matti Suuronen',
      author_email='esa-matti@suuronen.org',
      url='http://github.com/epeli/subssh',
      license='AGPL',
      packages=['subssh', 'subssh.app', 'subssh.app.vcs'],
      package_dir={'subssh': 'subssh'},
      package_data={'subssh': ['default/*']},
      data_files=[('share/subssh/doc', docs)],
      scripts=["scripts/subssh", "scripts/subssh-admin"],
)
