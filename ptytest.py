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

    	global pid, fd, master, slave

    	# self.request is the TCP socket connected to the client
    	self.data = self.request.recv(1024)
    	#self.data = self.rfile.readline().strip()
    	print("{} wrote:".format(self.client_address[0]))
    	print(self.data)

    	paras = self.data.decode().split(',', 1)

    	print(paras)

    	if str(paras[0]) == 'gdb':
    		ret = self.gdb(fd, paras[1])
    		print(ret)
    		self.request.sendall(bytes(ret + "\n", "utf-8"))

    	elif str(paras[0]) == 'console':
    		ret = self.tty(master, paras[1])
    		print(ret)
    		self.request.sendall(bytes(ret + "\n", "utf-8"))

    	else:
    		pass


    def gdb(self, fd, data):

    	print(fd, data)

    	os.write(fd, bytes(data,"UTF-8"))

    	time.sleep(0.2)
    	ret = os.read(fd, 65536).decode()

    	return ret


    def tty(self, fd, data):

    	print(fd, data)

    	os.write(fd, bytes(data,"UTF-8"))

    	time.sleep(0.2)
    	ret = os.read(fd, 65536).decode()

    	return ret


if __name__ == "__main__":
    
    global pid, fd, master, slave

    HOST, PORT = "localhost", 9999

    pid, fd = os.forkpty()

    #master, slave = os.openpty()

    master, slave = os.openpty()

    print("master:", os.ttyname(master))
    print("slave:", os.ttyname(slave))


    if pid == 0:
    	#print("slave pid, fd", pid, fd)

        #flags = fcntl.fcntl(sys.stdout, fcntl.F_GETFL)
        #fcntl.fcntl(sys.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        #subprocess.call(["gdb", "--interpreter=mi"])
        #os.execv('/usr/bin/gdb', ['/usr/bin/gdb', 'a.out', '--quiet', '--interpreter=mi2', '--tty=' + os.ttyname(slave)])
        os.execv('/usr/bin/gdb', ['/usr/bin/gdb', 'a.out', '--quiet', '--interpreter=mi2'])
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
