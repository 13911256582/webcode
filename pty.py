import os, sys, time, fcntl
import pty
import subprocess
import pdb

result_class = ['^done', '^running', '^connected', '^error', '^exit']
async_class = ['*stopped', '*running']
gdb_end = '(gdb)'


pdb.set_trace()
pid, fd = os.forkpty()

if pid == 0:
    print("slave pid, fd", pid, fd)
    #subprocess.call(["gdb", "--interpreter=mi"])
    os.execv('/usr/bin/gdb', ['/usr/bin/gdb', '--quiet', '--interpreter=mi2'])
    #os.execv('/usr/bin/python3', ['usr/bin/python3', 'ptytest.py'])
    sys.exit(0)
else :
    
    print("master, child pid is", pid, fd)
    #flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    #fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    while True:

        data = input('>')

        if data == 'exit':
            sys.exit(0)

        gdb_cmd = bytes(data + '\n',"UTF-8")
        os.write(fd, gdb_cmd)

        time.sleep(0.5)
            
        txt = os.read(fd, 65535).decode()
        #lines = txt.splitlines()
        #for line in lines:
        #    if line == '(gdb)':
        #        print(gdb_cmd, line)
        #    else:
        #        parseGDB(gdb_cmd, line)

        print(txt)
            

def parseGDB(cmd, line):
    if line[0] == '^':
        parseResultRecord(cmd, line)
    elif line[0] == '*':
        parseExecOuput(cmd, line)


def parseResultRecord(line):
    #split the first word
    words = line.split(',' , maxsplit=1)




