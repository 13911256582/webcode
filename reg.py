#test = '^done,bkpt={number="1",type="breakpoint",disp="keep",enabled="y",addr="0x0000000000400535",func="main",file="sample.c",fullname="/home/shaol/Documents/project/webcode/sample.c",line="6",thread-groups=["i1"],times="0",original-location="/home/shaol/Documents/project/webcode/sample.c:6"}'

#res = re.split(r'\bbkpt={.*}', test)

#res = re.split(',', test)

#print(res)


#!/usr/bin/python                                                                                                                                                      
# -*- coding: utf-8 -*-
# author: weisu.yxd@taobao.com
from subprocess import Popen, PIPE
import fcntl, os
import time
class Server(object):
  def __init__(self, args, server_env = None):
    if server_env:
      self.process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=server_env)
    else:
      self.process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
    fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

  def send(self, data, tail = '\n'):
    self.process.stdin.write(bytes(data + tail,"UTF-8"))
    self.process.stdin.flush()

  def recv(self, t=.1, e=1, tr=5, stderr=0):
    time.sleep(t)
    if tr < 1:
        tr = 1 
    x = time.time()+t
    r = ''
    pr = self.process.stdout
    if stderr:
      pr = self.process.stdout
    while time.time() < x or r:
        r = pr.read()
        if r is None:
            if e:
            	print(e)
            	raise Exception(e)
            else:
                break
        elif r:
            return r.rstrip()
        else:
            time.sleep(max((x-time.time())/tr, 0))
    return r.rstrip()
if __name__ == "__main__":
  #ServerArgs = ['/home/weisu.yxd/QP/trunk/bin/normalizer', '/home/weisu.yxd/QP/trunk/conf/stopfile.txt']
  ServerArgs = ['/usr/bin/python', './sample.py']
  server = Server(ServerArgs)

  #for x in test_data:
  #  server.send(x)
  #  print x, server.recv()
  while True:
  	i = input('>')

  	if i == 'exit':
  		break
  	else:
  		server.send(i)
  		print(server.recv().decode())
  	
	

	
	