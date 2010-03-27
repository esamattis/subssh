# subssh #

Homepage: http://github.com/epeli/subssh

Subssh is a bare minimal shell for exposing minimal amount of commands for
untrusted users. Eg. if you want to share  svn- or git-repositories. 


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

## Installing ##

No stable release is made yet, but you can try installing from git-repository.
Since this is development version usage of Python a [virtualenv][4] recommended.
In Debian based distros it can be found from *python-virtualenv* -package.

[4]: http://pypi.python.org/pypi/virtualenv

    $ virtualenv subsshenv
    $ source subsshenv/bin/activate
    $ git clone git://github.com/epeli/subssh.git
    $ cd subssh
    $ python setup.py install

## Usage ##

Just run *subssh* and type *help*.

### Usage over SSH ###

Add a public key with subssh-admin

    $ subssh-admin --add-key desired_username ssh-rsa AAAmyekeyhere...

and login with that key.
