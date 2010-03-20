'''
Created on Mar 20, 2010

@author: epeli
'''

import unittest

from subssh.keyparsers import parse_subssh_key
from subssh.keyparsers import parse_public_key



class TestParsePubKey(unittest.TestCase):
    def test_parse(self):
        line = 'command="PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subssh foobar" ssh-rsa avain== kommentti'
        type, key, comment = parse_public_key(line)
        self.assertEquals(type, "ssh-rsa")
        self.assertEquals(key, "avain==")
        self.assertEquals(comment, "kommentti")


    def test_from_putty(self):
        input = """---- BEGIN SSH2 PUBLIC KEY ----
Comment: "rsa-key-20100320"
AAAAB3NzaC1yc2EAAAABJQAAAIEAy3BIPl4M+y2NeYI+74CzBXQn8oQjm8LU7ksq
BdVce+4SyFA666fqY9l12SVIShRGdosA51GrjaiRgUH2Ejmzdi3HnWSCIVSdAVlA
3Sahff1/bcyDZsWvTcDA+J6MD5xMsRPIIHmi3pCuXwA6j56uTDfte3gACYRUgcfC
VIXZdKs=
---- END SSH2 PUBLIC KEY ----"""
        type, key, comment = parse_public_key(input)
        self.assertEquals(type, "ssh-rsa")
        self.assertEquals(comment, "")
        self.assertEquals(key, "AAAAB3NzaC1yc2EAAAABJQAAAIEAy3BIPl4M+y2NeYI+74CzBXQn8oQjm8LU7ksqBdVce+4SyFA666fqY9l12SVIShRGdosA51GrjaiRgUH2Ejmzdi3HnWSCIVSdAVlA3Sahff1/bcyDZsWvTcDA+J6MD5xMsRPIIHmi3pCuXwA6j56uTDfte3gACYRUgcfCVIXZdKs=")


    def test_rfc_1(self):
        input = """---- BEGIN SSH2 PUBLIC KEY ----
Comment: "1024-bit RSA, converted from OpenSSH by me@example.com"
x-command: /home/me/bin/lock-in-guest.sh
AAAAB3NzaC1yc2EAAAABIwAAAIEA1on8gxCGJJWSRT4uOrR13mUaUk0hRf4RzxSZ1zRb
YYFw8pfGesIFoEuVth4HKyF8k1y4mRUnYHP1XNMNMJl1JcEArC2asV8sHf6zSPVffozZ
5TT4SfsUu/iKy9lUcCfXzwre4WWZSXXcPff+EHtWshahu3WzBdnGxm5Xoi89zcE=
---- END SSH2 PUBLIC KEY ----
"""
        type, key, comment = parse_public_key(input)
        self.assertEquals(type, "ssh-rsa")
        self.assertEquals(comment, "")
        self.assertEquals(key, "AAAAB3NzaC1yc2EAAAABIwAAAIEA1on8gxCGJJWSRT4uOrR13mUaUk0hRf4RzxSZ1zRbYYFw8pfGesIFoEuVth4HKyF8k1y4mRUnYHP1XNMNMJl1JcEArC2asV8sHf6zSPVffozZ5TT4SfsUu/iKy9lUcCfXzwre4WWZSXXcPff+EHtWshahu3WzBdnGxm5Xoi89zcE=")




    def test_rfc_2(self):
        input = """---- BEGIN SSH2 PUBLIC KEY ----
Comment: DSA Public Key for use with MyIsp
AAAAB3NzaC1kc3MAAACBAPY8ZOHY2yFSJA6XYC9HRwNHxaehvx5wOJ0rzZdzoSOXxbET
W6ToHv8D1UJ/z+zHo9Fiko5XybZnDIaBDHtblQ+Yp7StxyltHnXF1YLfKD1G4T6JYrdH
YI14Om1eg9e4NnCRleaqoZPF3UGfZia6bXrGTQf3gJq2e7Yisk/gF+1VAAAAFQDb8D5c
vwHWTZDPfX0D2s9Rd7NBvQAAAIEAlN92+Bb7D4KLYk3IwRbXblwXdkPggA4pfdtW9vGf
J0/RHd+NjB4eo1D+0dix6tXwYGN7PKS5R/FXPNwxHPapcj9uL1Jn2AWQ2dsknf+i/FAA
vioUPkmdMc0zuWoSOEsSNhVDtX3WdvVcGcBq9cetzrtOKWOocJmJ80qadxTRHtUAAACB
AN7CY+KKv1gHpRzFwdQm7HK9bb1LAo2KwaoXnadFgeptNBQeSXG1vO+JsvphVMBJc9HS
n24VYtYtsMu74qXviYjziVucWKjjKEb11juqnF0GDlB3VVmxHLmxnAz643WK42Z7dLM5
sY29ouezv4Xz2PuMch5VGPP+CDqzCM4loWgV
---- END SSH2 PUBLIC KEY ----"""
        type, key, comment = parse_public_key(input)
        self.assertEquals(type, "ssh-dss")
        self.assertEquals(comment, "")
        self.assertEquals(key, "AAAAB3NzaC1kc3MAAACBAPY8ZOHY2yFSJA6XYC9HRwNHxaehvx5wOJ0rzZdzoSOXxbETW6ToHv8D1UJ/z+zHo9Fiko5XybZnDIaBDHtblQ+Yp7StxyltHnXF1YLfKD1G4T6JYrdHYI14Om1eg9e4NnCRleaqoZPF3UGfZia6bXrGTQf3gJq2e7Yisk/gF+1VAAAAFQDb8D5cvwHWTZDPfX0D2s9Rd7NBvQAAAIEAlN92+Bb7D4KLYk3IwRbXblwXdkPggA4pfdtW9vGfJ0/RHd+NjB4eo1D+0dix6tXwYGN7PKS5R/FXPNwxHPapcj9uL1Jn2AWQ2dsknf+i/FAAvioUPkmdMc0zuWoSOEsSNhVDtX3WdvVcGcBq9cetzrtOKWOocJmJ80qadxTRHtUAAACBAN7CY+KKv1gHpRzFwdQm7HK9bb1LAo2KwaoXnadFgeptNBQeSXG1vO+JsvphVMBJc9HSn24VYtYtsMu74qXviYjziVucWKjjKEb11juqnF0GDlB3VVmxHLmxnAz643WK42Z7dLM5sY29ouezv4Xz2PuMch5VGPP+CDqzCM4loWgV")





class TestParseSubuserKey(unittest.TestCase):
    
    def test_parse(self):
        line = 'command="PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subssh --ssh foobar" ssh-rsa avain== kommentti'
        username, type, key, comment = parse_subssh_key(line)
        self.assertEquals(username, "foobar")
        self.assertEquals(type, "ssh-rsa")
        self.assertEquals(key, "avain==")
        self.assertEquals(comment, "kommentti")
        
    def test_parse_multiple_comment_words(self):
        line = 'command="PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subssh --ssh foobar" ssh-rsa avain== monisanainen kommentti'
        username, type, key, comment = parse_subssh_key(line)
        self.assertEquals(comment, "monisanainen kommentti")        
        
    
    def test_no_comment(self):
        line = 'command="PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subssh --ssh foobar" ssh-rsa avain=='
        username, type, key, comment = parse_subssh_key(line)
        self.assertEquals(comment, "")        

    def test_simple_cmd(self):
        line = 'command="subssh --ssh foobar" ssh-rsa avain== kommentti'
        username, type, key, comment = parse_subssh_key(line)
        self.assertEquals(username, "foobar")
        self.assertEquals(type, "ssh-rsa")
        self.assertEquals(key, "avain==")
        self.assertEquals(comment, "kommentti")
        