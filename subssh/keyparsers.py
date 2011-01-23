# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Esa-Matti Suuronen <esa-matti@suuronen.org>

This file is part of subssh.

Subssh is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

Subssh is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with Subssh.  If not, see
<http://www.gnu.org/licenses/>.
"""

import re
import tempfile
import subprocess

class PubKeyException(Exception):
    pass


pubkey_pattern = re.compile(
                    # Starts with command. After that is other optional
                    # options until we hit space
                    r"[^ ]* *"
                    # Key type. Must start with rsa or dsa
                    r"(ssh-(?:rsa|dss)) +"
                    # Key itself. No spaces in it
                    r"([^ ]+) *"
                    # In the end there is is an optional comment
                    r"(.*)"
                    )


def parse_public_key(key):
    match = pubkey_pattern.search(key)

    # Was not in required format. Try to convert with ssh-keygen
    if not match:
        tmp = tempfile.NamedTemporaryFile(prefix="subssh_tmp_")
        tmp.write(key)
        tmp.flush()
        p  = subprocess.Popen(("ssh-keygen", "-i", "-f", tmp.name),
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        p.wait()
        tmp.close()
        if p.returncode == 0:
            match = pubkey_pattern.search(p.stdout.read())

    if not match:
        raise PubKeyException("Invalid public key")

    type = match.group(1).strip()
    key = match.group(2).strip()
    comment = match.group(3).strip()
    return type, key, comment






options_pattern = re.compile(
                             # Starts with subssh command. command will
                             # determine the user
                             r"^command=\"[^\"]*subssh -t ([a-z0-9]+)\"[^ ]* +"
                             # Key type. Must start with rsa or dsa
                             r"(ssh-(?:rsa|dss)) +"
                             # Key itself. No spaces in it
                             r"([^ ]+) *"
                             # In the end there is is an optional comment
                             r"(.*)"
                             )
def parse_subssh_key(line):
    """
    Detects if public key line is created by Subssh and extracts username
    from it
    """
    match = options_pattern.search(line)
    if not match:
        raise PubKeyException("Not created by Subssh")

    username = match.group(1).strip()
    type = match.group(2).strip()
    key = match.group(3).strip()
    comment = match.group(4).strip()

    return username, type, key, comment



