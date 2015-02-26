from django.shortcuts import render_to_response
from django.http import HttpResponse

import commands
import os
import socket
import sys
from subprocess import Popen, PIPE


#global pty_pid, pty_fd

# Create your views here.
def submit(req):

	if req.method == 'POST':

		code = req.POST['code']
		#print "[python:]"
		#print  code

		#write the submitted code to a file
		#pythonFile = open('./sample.py','wb+')
		try:
			pythonFile = open('./sample.c', 'wb+')
			pythonFile.write(code)
		except:
			print "open and write sample.c failed"
		finally:
			pythonFile.close()

		#run python code in a command terminal
		#cmd = 'python' + ' ' + 'sample.py'
		#print "[python:]", cmd
		cmd = 'gcc -g sample.c'

		try:
			(status, output) = commands.getstatusoutput(cmd)
			if status != 0:
				return HttpResponse(output)
			else:
				return HttpResponse("build successful, click run to execute")
		except:
			print "gcc sample.c error"
			return HttpResponse("compile error")

		#print "[python exec result:]", output

		#if not output.strip():
		#	out = 'build success'
		
	return render_to_response('code.html', {'response': res})


def run(req):

	if req.method == 'GET':

		print "run command"

		#code = req.POST['code']
		#print "[python:]"
		#print  code

		#write the submitted code to a file
		#pythonFile = open('./sample.py','wb+')
		#pythonFile = open('./sample.c', 'wb+')
		#pythonFile.write(code)
		#pythonFile.close()

		#run python code in a command terminal
		#cmd = 'python' + ' ' + 'sample.py'
		#print "[python:]", cmd

		cmd = './a.out'
		print "run ./a.out"
		(status, output) = commands.getstatusoutput(cmd)

		#print "[python exec result:]", output
		return HttpResponse(output)

def debug(req):

	global gdb_sock

	if req.method == 'GET':
		print("debug start")
		#gdb_sock = gdb_connect("localhost", 9999)
		return HttpResponse("debug start")

def gdb(req):

	global gdb_sock

	if req.method == 'POST':
		gdb_cmd = req.POST['gdb_cmd']

		# Create a socket (SOCK_STREAM means a TCP socket)
		gdb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		gdb_sock.connect(("localhost", 9999))

		print gdb_cmd
		output = gdb_command(gdb_cmd)

		gdb_sock.close()
		return HttpResponse(output)


def gdb_connect(HOST, PORT):

	#HOST, PORT = "localhost", 9999

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock.connect((HOST, PORT))

	return sock


def gdb_command(cmd):

	global gdb_sock
	#sock = gdb_connect("localhost", 9999)

	#cmd.rstrip('\n')
	#cmd = cmd + '\n'

	gdb_sock.sendall(bytearray(cmd + "\n", "utf-8"))
	received = str(gdb_sock.recv(4096))
	return received


def index(req):
	return render_to_response('index.html', {})