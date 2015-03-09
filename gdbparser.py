import re

#test = '^done,bkpt={number="1",type="breakpoint",disp="keep",enabled="y",addr="0x0000000000400535",func="main",file="sample.c",fullname="/home/shaol/Documents/project/webcode/sample.c",line="6",thread-groups=["i1"],times="0",original-location="/home/shaol/Documents/project/webcode/sample.c:6"}'

#res = re.split(r'\bbkpt={.*}', test)

#res = re.split(',', test)

#print(res)
out_of_band = ('*', '+', '=')
stream_output = ('~', '@', '&')
result_class = ('^done', '^running', '^connected', '^error', '^exit')


class GdbParser(object):

	def gdbParse(lines, cmd):
		lines = lines.splitlines()

		for i in lines:
			gdbParseLine(i)


	def gdbOutOfBand(lines, cmd):


	def gdbParseLine(line, cmd):
		

		if line[0] == '^':
			gdbParseResultRecord(line,cmd)
		elif line[0] in out_of_band:
			if line[0] == '*':
				gdbParseExecAsyncOutput(line, cmd)
			elif line[0] == '=':
				return
			elif line[0] == '+':
				return
			else:
				pass
		elif line[0] in stream_output:
			return
		elif:
			#match (gdb)
			rs = re.match(r'\b(gdb)', line)
			if rs:
				self.gdb_status = 'waiting'
			else:
				raise "gdb line parse error"

		else:
			raise "gdb line parse error"

	def gdbParseExecAsyncOutput(line, cmd)

	def gdbParseResultRecord(line, cmd):

		words = line.split(',' , 1)

		if words[0] in result_class:
			if words[0] == '^done':
				return
			elif words[0] == '^error':
				gdbParseError(word[1], cmd)
			elif words[0] == '^running':
				self.gdb_status = 'running'
				
		else:
			raise "gdb result class error"


class gdbResult(object)