# subssh #

Homepage: http://github.com/epeli/subssh

Author: Esa-Matti Suuronen <esa-matti@suuronen.org>


Subssh is a bare minimal shell for exposing minimal amount of commands for
untrusted users. Eg. if you want to restrict users access to svn- or 
git-repositories only. 


## Features ##

 - Interactive shell.
 - Git and Subversion support with repository managers.
   - Users can add, delete and rename repositories. 
   - Permissions management. Users can set who can read/write to their 
     repositories.
 - Multiple users can use single account.
   - Users are distinguished by public SSH-keys in ~/.ssh/authorized_keys file.
   - Keys can be managed from the shell.
 - Easily extendable. [Example](http://github.com/epeli/subssh/blob/master/subssh/app/example.py).

Subssh is inspired by [GitHub][h], [Gitosis][s], [YouSource (Verso)][y] and 
[CherryPy][c] (for the extension system).

[h]: http://github.com/
[s]: http://eagain.net/gitweb/?p=gitosis.git
[y]: http://sovellusprojektit.it.jyu.fi/verso/
[c]: http://cherrypy.org/

## Requirements ##

 - Should work with Python 2.4, 2.5 and 2.6. Mostly tested with 2.5.
 - OpenSSH server. Well, subssh can be run locally, but there's really no 
   point doing that...
 - Git (for the Git app).
 - Subversion (for the Subversion app).


## Installing ##

No releases are made yet, but you can try installing from git-repository.

Since is there is only a development version available, usage of a Python
[virtualenv][e] is highly recommended. In Debian based distros it can be found 
from *python-virtualenv* -package.

    $ virtualenv subsshenv
    $ source subsshenv/bin/activate

If you have also [setuptools][t] installed you can install the HEAD with 
easy_install:

    $ easy_install http://github.com/epeli/subssh/tarball/master

Otherwise you can install it manually:

    $ git clone git://github.com/epeli/subssh.git
    $ cd subssh
    $ python setup.py install

[e]: http://pypi.python.org/pypi/virtualenv
[t]: http://pypi.python.org/pypi/setuptools 

## Usage ##

Just run *subssh* and type *help*.

### Usage over SSH ###

Add a public key with subssh-admin

    $ subssh-admin --add-key desired_username ssh-rsa AAAmyekeyhere...

and login with that key.
