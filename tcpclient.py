import socket
import sys

HOST, PORT = "localhost", 9999
#data = " ".join(sys.argv[1:])

data = ''

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    
    while True:

        data = raw_input('>')

        if data == 'exit':
            break

        else:
            sock.sendall(bytearray(data + "\n", "utf-8"))

            #Receive data from the server and shut down
            received = str(sock.recv(1024))
            print("Sent:     {}".format(data))
            print("Received: {}".format(received))

    sock.close()
finally:
    sock.close()

