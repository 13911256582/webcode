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


import SocketServer
import os, time, sys
import Queue
import threading
import json
import urllib
import httplib
#import http.client


import pdb

class AsyncReadServer(object):

    def init(self, gdb_fd, target_fd):
        self.gdb_fd = gdb_fd
        self.target_fd = target_fd

        #create gdb read thread
        self.gdb_t = threading.Thread(target=self.async_gdb_read, args=("gdb", self.gdb_fd))
        self.gdb_t.daemon = True
        self.gdb_t.start()

        #create target read thread

        self.target_t = threading.Thread(target=self.async_console_read, args=("console", self.target_fd))
        self.target_t.daemon = True
        self.target_t.start()

    def async_gdb_read(self, source, fd):

        while True:
            ret = os.read(fd, 65536).decode()
            print(source, ret)
            self.post(source, ret)

    def async_console_read(self, source, fd):

        while True:
            ret = os.read(fd, 65536).decode()
            print(source, ret)
            self.post(source, ret)

    def post(self, source, data):
        params = {  'source': source,
                    'data': data
        }

        #headers = { "Content-Type": "application/json",}

        headers = {"Content-Type":"text/html", "Connection":"close"}

        httpClient = httplib.HTTPConnection("127.0.0.1:8080")
        httpClient.request("POST", "/post", json.dumps(params), headers)


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    global fd, master

    def handle_request(self, response):
        if response.error:
            print "Error:", response.error
        else:
            print response.body


        #response = httpClient.getresponse()


    #def tty_read(self, q, fd):

    #    while True:
    #        ret = os.read(fd, 65536).decode()
    #        print("console:", ret)
    #        self.post('console', ret)
    	#q.put(ret)


    #def gdb_read(self, q, fd):

    #    while True:
    #        ret = os.read(fd, 65536).decode()
    #        print("gdb:", ret)
    #        self.post('gdb', ret) 

    	#q.put(ret)



    def handle(self):

    	# self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        

        #q = Queue.Queue()
        #paras = self.data.decode().split(',', 1)
        req = json.loads(self.data.decode())

        if req['source'] == 'gdb':
            
            os.write(fd, bytearray(req['data'] + "\n","UTF-8"))
            
            #ret = self.gdb(fd, paras[1])
            #try:
            #    ret = ''
            #    ret = q.get(True, 0.3)  #wait 0.2 second
            #except:
            #    pass

            #print(ret)
            #self.request.sendall(bytearray(ret, "utf-8"))

                    

        elif req['source'] == 'console':

            if req['action'] == 'write':
                os.write(master, bytearray(req['data'] + "\n","UTF-8"))

            #elif req['action'] == 'async_read':
            #    t = threading.Thread(target=MyTCPHandler.tty_read, args=(self, q, master))
            #    t.daemon = True
            #    t.start()    		
                
                #try:
                #    ret = ''
                #    ret = q.get(True, 0.1)  #wait 0.2 second
                #except:
                #    pass

                #print(ret)
                #self.request.sendall(bytearray(ret, "utf-8"))
                #self.post('console', ret)
            
            elif req['action'] == 'sync_read':
                ret = os.read(master, 65536).decode()
                print(ret)
                self.request.sendall(bytearray(ret, "utf-8"))
            else:
                pass
        else:
            pass




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
        #os.execv('/bin/sh', ['/bin/sh'])
        #os.execv('./sample', ['./sample'])
    #    sys.exit(0)
    else :

        #set fd to async mode
        #flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        #fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        # Create the server, binding to localhost on port 9999
        server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

        async_reader = AsyncReadServer()
        async_reader.init(fd, master)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
