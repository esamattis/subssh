'''
Created on Mar 27, 2010

@author: epeli

'''

import os
from setuptools import find_packages, setup





setup(
    name='subssh',
    version="1.0",
    description='Bare minimal shell for using eg. Git and Subversion over SSH',
    author='Esa-Matti Suuronen',
    author_email='esa-matti@suuronen.org',
    url='http://github.com/epeli/subssh',
    license='AGPL',
    package_dir={'subssh': 'subssh'},
    include_package_data = True,
    package_data = {
        'subssh': [
            'default/*',
        ],
    },
    packages = find_packages(),
    entry_points = """
        [console_scripts]
        subssh = subssh.entry_points:main
        subssh-admin = subssh.entry_points:admin_tools
        subssh-xmlrpc-server = subssh.entry_points:xmlrpc_server
    """
)
