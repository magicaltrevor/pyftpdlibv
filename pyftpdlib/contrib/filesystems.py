#!/usr/bin/env python
# $Id: filesystems.py 977 2012-01-22 23:05:09Z g.rodola $

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

from pyftpdlib.ftpserver import AbstractedFS
from fs.memoryfs import MemoryFS
from fs.s3fs import S3FS

__all__ = ['UnixFilesystem']


class UnixFilesystem(AbstractedFS):
    """Represents the real UNIX filesystem.

    Differently from AbstractedFS the client will login into
    /home/<username> and will be able to escape its home directory
    and navigate the real filesystem.
    """

    def __init__(self, root, cmd_channel):
        AbstractedFS.__init__(self, root, cmd_channel)
        # initial cwd was set to "/" to emulate a chroot jail
        self.cwd = root

    def ftp2fs(self, ftppath):
        return self.ftpnorm(ftppath)

    def fs2ftp(self, fspath):
        return fspath

    def validpath(self, path):
        # validpath was used to check symlinks escaping user home
        # directory; this is no longer necessary.
        return True
    
class VirtualFilesystem(AbstractedFS):
    """Represents a virtual filesystem (currently only memory and s3 are supported)
    """
    
    def __init__(self, root, cmd_channel):
        AbstractedFS.__init__(self, root, cmd_channel)
        self.cwd = cmd_channel.root
        self.type = cmd_channel.type
        self.s3_bucket = cmd_channel.s3_bucket
        self.aws_access_key = cmd_channel.aws_access_key
        self.aws_secret_key = cmd_channel.aws_secret_key
        self.seperator = cmd_channel.seperator
        self.thread_synchronize = cmd_channel.thread_synchronize
        self.key_sync_timeout = cmd_channel.key_sync_timeout
        if self.type == "memory":
            self.fs_obj = MemoryFS()
        elif self.type == "s3":
            self.fs_obj = S3FS(bucket=self.bucket, prefix=self.prefix, aws_access_key=self.aws_access_key, aws_secret_key=self.aws_secret_key, separator=self.seperator, thread_synchronize=self.thread_synchronize, key_sync_timeout=self.key_sync_timeout)
            

    def ftp2fs(self, ftppath):
        return self.ftpnorm(ftppath)

    def fs2ftp(self, fspath):
        return fspath

    def validpath(self, path):
        # validpath was used to check symlinks escaping user home
        # directory; this is no longer necessary.
        return True
    
    def open(self, filename, mode):
            return self.fs_obj.open(filename, mode)
    
    def mkdir(self, path):
        return self.fs_obj.makedir(path)
        
    def chdir(self, path):
        return self.fs_obj.opendir(path)
    
    def listdir(self,path):
        return self.fs_obj.listdir(path)
    
    def rmdir(self, path):
        return self.fs_obj.removedir(path)
    
    def remove(self, path):
        return self.fs_obj.remove(path)
    
    def rename(self, src, dst):
        return self.fs_obj.rename(src, dst)
    
    def chmod(self, path, mode):
        return True
    
    def readlink(self, path):
        return self.ftp2fs(path)
    
    def isfile(self, path):
        return self.fs_obj.isfile(path)
    
    def islink(self, path):
        return False
    
    def getsize(self, path):
        return self.fs_obj.getsize(path)
    
    def getmtime(self, path):
        return self.fs_obj.getinfo(path)['modified_time']
    
    def realpath(self, path):
        return path
    
    def lexists(self, path):
        return self.fs_obj.exists(path)
    
    def mkstemp(self, suffix='', prefix='', mode='wb'):
        from tempfile import _RandomNameSequence as RandomName
        name = RandomName()
        if suffix != '':
            suffix = 'tmp'
        fname = suffix + name.next()
        return self.fs_obj.open(fname,mode)
        
        
    
    
