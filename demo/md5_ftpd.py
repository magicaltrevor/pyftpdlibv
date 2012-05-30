#!/usr/bin/env python
# $Id: md5_ftpd.py 1046 2012-05-22 12:19:30Z g.rodola $

#  pyftpdlib is released under the MIT license, reproduced below:
#  ======================================================================
#  Copyright (C) 2007-2012 Giampaolo Rodola' <g.rodola@gmail.com>
#
#                         All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#  ======================================================================

"""A basic ftpd storing passwords as hash digests (platform independent).
"""

import os
try:
    from hashlib import md5
except ImportError:
    # backward compatibility with Python < 2.5
    from md5 import new as md5

from pyftpdlib import ftpserver
from pyftpdlib.lib.compat import b


class DummyMD5Authorizer(ftpserver.DummyAuthorizer):

    def validate_authentication(self, username, password):
        hash = md5(b(password)).hexdigest()
        return self.user_table[username]['pwd'] == hash


def main():
    # get a hash digest from a clear-text password
    hash = md5(b('12345')).hexdigest()
    authorizer = DummyMD5Authorizer()
    authorizer.add_user('user', hash, os.getcwd(), perm='elradfmw')
    authorizer.add_anonymous(os.getcwd())
    handler = ftpserver.FTPHandler
    handler.authorizer = authorizer
    ftpd = ftpserver.FTPServer(('', 21), handler)
    ftpd.serve_forever()

if __name__ == "__main__":
    main()
