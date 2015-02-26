# Copyright (C) 2012-2014 Free Software Foundation, Inc.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import socketserver
import os, time, sys
import fcntl

import pdb

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):

    	global pid, fd

    	# self.request is the TCP socket connected to the client
    	self.data = self.request.recv(1024)
    	#self.data = self.rfile.readline().strip()
    	print("{} wrote:".format(self.client_address[0]))
    	print(self.data)
    	# just send back the same data, but upper-cased
    	ret = self.command(self.data)
    	self.request.sendall(bytes(ret + "\n", "utf-8"))

    def command(self, data):

        global pid, fd

        gdb_cmd = data.decode()
        print(gdb_cmd)

        cmd = bytes(gdb_cmd,"UTF-8")
        os.write(fd, cmd)

        time.sleep(0.2)
        
        txt = os.read(fd, 65536).decode()
        #while True:
        #	time.sleep(0.2)
        #	try:
        #		txt = ''
        #		txt = os.read(fd, 1024)

        #		if txt is None:
        #			print("read end, break")
        #			break
        #		else:
        #		self.request.sendall(bytes(txt.decode() + "\n", "utf-8"))
        #	except:
        #		pass
        #	if not r.strip():
        #		break
        #	else:
        #		txt = txt + r.decode()
        #lines = txt.splitlines()
        #for line in lines:
        #    if line == '(gdb)':
        #        print(gdb_cmd, line)
        #    else:
        #        parseGDB(gdb_cmd, line)
        return txt


if __name__ == "__main__":
    
    global pid, fd

    HOST, PORT = "localhost", 9999

    pid, fd = os.forkpty()


    if pid == 0:
    	#print("slave pid, fd", pid, fd)

        #flags = fcntl.fcntl(sys.stdout, fcntl.F_GETFL)
        #fcntl.fcntl(sys.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        #subprocess.call(["gdb", "--interpreter=mi"])
        os.execv('/usr/bin/gdb', ['/usr/bin/gdb', '--quiet', '--interpreter=mi2'])
        #os.execv('/usr/bin/python', ['/usr/bin/python', './sample.py'])
        #os.execv('./sample', ['./sample'])
    #    sys.exit(0)
    else :
    
        print("master, child pid is", pid, fd)

        #set fd to async mode
        #flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        #fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
