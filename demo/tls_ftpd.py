#!/usr/bin/env python
# $Id: tls_ftpd.py 1012 2012-05-14 03:01:11Z g.rodola $

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

"""An RFC-4217 asynchronous FTPS server supporting both SSL and TLS.

Requires PyOpenSSL module (http://pypi.python.org/pypi/pyOpenSSL).
"""

import os

from pyftpdlib import ftpserver
from pyftpdlib.contrib.handlers import TLS_FTPHandler

CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "keycert.pem"))

def main():
    authorizer = ftpserver.DummyAuthorizer()
    authorizer.add_user('user', '12345', '.', perm='elradfmw')
    authorizer.add_anonymous('.')
    handler = TLS_FTPHandler
    handler.certfile = CERTFILE
    handler.authorizer = authorizer
    # requires SSL for both control and data channel
    #handler.tls_control_required = True
    #handler.tls_data_required = True
    ftpd = ftpserver.FTPServer(('', 21), handler)
    ftpd.serve_forever()

if __name__ == '__main__':
    main()