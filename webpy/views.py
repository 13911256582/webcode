from django.shortcuts import render_to_response
from django.http import HttpResponse

import commands

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
		cmd = 'gcc' + ' ' + 'sample.c'

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
		


def index(req):
	return render_to_response('index.html', {})