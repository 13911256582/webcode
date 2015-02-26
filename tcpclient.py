import socket
import sys

HOST, PORT = "localhost", 9999
#data = " ".join(sys.argv[1:])

data = ''



try:
    
    while True:


        data = raw_input('>')


        if data == 'exit':
            break

        else:

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            
            print("Sent:     {}".format(data))
            sock.sendall(bytearray(data + "\n", "utf-8"))

            #Receive data from the server and shut down
            received = str(sock.recv(65536))
            print("Received: {}".format(received))

            sock.close()

finally:
    sock.close()