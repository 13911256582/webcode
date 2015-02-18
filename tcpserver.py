import socketserver
import gdb

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):

        while True:
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            #self.data = self.rfile.readline().strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)
            # just send back the same data, but upper-cased

            ret = self.command(self.data)

            self.request.sendall(bytes(ret + "\n", "utf-8"))

    def command(self, data):

        cmd = data.decode()
        print("cmd=" + cmd)
        return gdb.execute(cmd, True, True)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()