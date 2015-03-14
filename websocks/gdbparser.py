import re
import json
import pdb

#test = '^done,bkpt={number="1",type="breakpoint",disp="keep",enabled="y",addr="0x0000000000400535",func="main",file="sample.c",fullname="/home/shaol/Documents/project/webcode/sample.c",line="6",thread-groups=["i1"],times="0",original-location="/home/shaol/Documents/project/webcode/sample.c:6"}'

#res = re.split(r'\bbkpt={.*}', test)

#res = re.split(',', test)

#print(res)
out_of_band = ('*', '+', '=')
stream_output = ('~', '@', '&')
result_class = ('^done', '^running', '^connected', '^error', '^exit')
char_set = ('{', '}', '[', ']')


class GdbParser(object):

	def gdbParse(self, lines, cmd):
		lines = lines.splitlines()

		for i in lines:
			gdbParseLine(i)


	def gdbOutOfBand(self, lines, cmd):
		pass


	def gdbParseLine(self, line, cmd):
		

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
		#elif:
			#match (gdb)
		#	rs = re.match(r'\b(gdb)', line)
		#	if rs:
		#		self.gdb_status = 'waiting'
		#	else:
		#		raise "gdb line parse error"

		else:
			raise "gdb line parse error"

	def gdbParseExecAsyncOutput(self, line, cmd):
		pass

	def gdbParseResultRecord(self, line, cmd):

		words = line.split(',' , 1)

		if words[0] in result_class:
			if words[0] == '^done':
				gdbParseDone(words[1])

			elif words[0] == '^error':
				gdbParseError(word[1], cmd)
			
			elif words[0] == '^running':
				self.gdb_status = 'running'
				
		else:
			raise "gdb result class error"

	def gdbParseDone(self, line):
		rs = re.match(r'\bbkpt={.*}', line)


	def lineParser(self, line):
		output = {}

		#rule_a = re.compile(r'{.*}')
		#rule_b = re.compile(r'\[.*\]')

		remaining = line
		print("remaining:", remaining)
		print("\n")

		while len(remaining) > 0:

			words = remaining.split('=', 1)
			key = words[0]
			remaining = words[1]

			if remaining[0] == '{':
				match = re.search(r'{.*}', remaining)
				af_match = remaining[match.end():]

				res = self.parseObject(match.group(0).strip('\{').strip('\}'))
				output[key] = res
				remaining = af_match.lstrip(',')

			elif remaining[0] == '[':
				match = re.search(r'\[.*\]', remaining)
				af_match = remaining[match.end():]

				res = self.parseArray(match.group(0).strip('\[').strip('\]'))
				output[key] = res
				remaining = af_match.lstrip(',')

			else:
				words = remaining.split(',', 1)
				if len(words) == 1:
					output[key] = words[0].strip('\"').strip('\"')
					remaining = ''
				else:
					output[key] = words[0].strip('\"').strip('\"')
					remaining = words[1]

		return output

	def parseObject(self, line):
		return self.lineParser(line)	

	def parseArray(self, line):
		output = []

		words = line.split(',')

		for word in words:
			output.append(word.strip('\"').strip('\"'))

		return output

	def no():
		pass




if __name__ == "__main__":
	test_string = 'bkpt={number="1",type="breakpoint",disp="keep",enabled="y",addr="0x0000000000400535",func="main",file="sample.c",fullname="/home/shaol/Documents/project/webcode/sample.c",line="6",thread-groups=["i1"],times="0",original-location="/home/shaol/Documents/project/webcode/sample.c:6"}'
	gdbParse = GdbParser()
	output = gdbParse.lineParser(test_string)

	print(output)
	print(json.dumps(output))


