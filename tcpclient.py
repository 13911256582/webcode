import socket
import sys
import os
import pdb
import time


#1. gdb,-file-exec-and-symbols a.out
#2. gdb,tty /dev/pts/* to change the tty of the target program, here the /dev/pts/* coming from master, slave = openpty(), ttyname(slave)
#   this is the key to set tty /dev/pts/* the same as the return of ttyname
#3. gdb,-exec-run
#4. use os.read(master) to read the output from a.out



def test_pty():

    

    mw, sr = os.openpty()
    mr, sw = os.openpty()
    print("mw:", mw, os.ttyname(mw))
    print("mr:", mr, os.ttyname(mr))

    #os.close(slave)

    #pid, fd = os.forkpty()

    pid = os.fork()

    if pid == 0:
        #print("slave pid, fd", pid, fd)

        #flags = fcntl.fcntl(sys.stdout, fcntl.F_GETFL)
        #fcntl.fcntl(sys.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        #subprocess.call(["gdb", "--interpreter=mi"])

        #ttyname = os.ttyname(slave)

        #fd_r = os.open(ttyname, 'r')
        fd_w = open(ttyname, 'rw')

        os.dup2(fd_w, 0)
        os.dup2(fd_w, 1)
        #os.open("/dev/pts/0")
        os.execv('./a.out', ['./a.out'])
        #os.execv('/usr/bin/python', ['/usr/bin/python', './sample.py'])
        #os.execv('./sample', ['./sample'])
    #    sys.exit(0)
    else :


        #pdb.set_trace()
        while True:
            ret = tty(master, master, "20\n")
            print(ret)



def tty(fd_r, fd_w, data):

    #pdb.set_trace()

    #x = bytearray(data,"UTF-8")

    #os.write(fd_w, x)

    time.sleep(0.2)

    ret = os.read(fd_r, 65536)

    return ret


#try:
try:

    #test_pty()

    HOST, PORT = "localhost", 9999

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

except:
    pass