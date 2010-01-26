#!/usr/bin/python
#    Copyright 2010 David Jensen 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import mailbox
import smtpd
import asyncore
from optparse import OptionParser

class DevBox(smtpd.SMTPServer):

    def __init__(self,port,maildir):
        smtpd.SMTPServer.__init__(self,('localhost',port),('localhost',25))
        self.mbox = mailbox.Maildir(maildir)

    def process_message(self, peer, mailfrom, rcpttos, data):
        self.mbox.lock()
        self.mbox.add(data)
        self.mbox.flush()
        self.mbox.unlock()
        print "Added a msg from ",mailfrom

if __name__ == '__main__':
    usage=""" %prog [options]
    
%prog is debugging SMTP server bound to localhost. Useful
for when you need to test outgoing mail but do not want any
mail actually sent. All incoming  messages are saved in a maildir 
for later perusal regardless of any possible address. 
What comes in won't come out."""
    
    parser = OptionParser(usage,version="%prog 0.1")
    parser.add_option("-m", "--maildir",action="store", type="string", 
                      dest="maildir",default='~/.devbox',help='sets the path to the maildir [default: %default]')
    parser.add_option("-p", "--port",action="store", type="int", 
                      dest="port",default=25, help='sets the port the server listens to [default: %default]')
    (options, args) = parser.parse_args()

    print "Starting server on localhost:%i, with maildir %s" % (options.port,options.maildir)
    dn = DevBox(options.port,options.maildir)
    
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
