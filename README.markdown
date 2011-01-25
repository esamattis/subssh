# Subssh

Homepage: https://github.com/epeli/subssh

Author: Esa-Matti Suuronen <esa-matti aet suuronen dot org>

Subssh is a small framework for building custom shells that work under a
single OpenSSH-account. It separates users from each other with SSH public keys.
This means that you don't have to create real accounts for Subssh-users.

Framework also helps you to manage the public keys. It does that by managing
keys in the authorizes\_keys-file. The file are managed in a friendly way so
that you can also keep your own keys the file. Subssh makes sure that they
remain untouched.

Subssh comes with bundled key management application which allows users
to add and remove their keys. You can manually select which Subssh applications
are activated.

Subssh is a great tool if you want to build for example a restricted
ssh-account for just [rsync][] or [rdiff-backup][] usage. For a working example
see [Revision Cask][]. It's a revision control management tool for which Subssh
was originally written for.



[rsync]: http://samba.anu.edu.au/rsync/
[rdiff-backup]: http://www.nongnu.org/rdiff-backup/
[Revision Cask]: http://esa-matti.suuronen.org/projects/revisioncask/
