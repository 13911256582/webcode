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
status_class = ('*running', '*stopped')


class GdbParser(object):

	def __init__(self):
		self.gdb_type = ''
		self.gdb_result = ''
		self.gdb_status = ''
		self.gdb_data = ''
		self.gdb_out_of_band = ''
		self.gdb_details = ''

	def gdbParse(self, lines):

		print("parse in >>>> ")
		print(lines)

		lines = lines.splitlines()
		response = []

		for i in lines:
			item = {}
			self.gdb_type = ''
			self.gdb_result = ''
			self.gdb_status = ''
			self.gdb_data = ''
			self.gdb_out_of_band = ''

			self.gdbParseLine(i)

			if self.gdb_type == 'skip':
				continue
			
			item['type'] = self.gdb_type

			if self.gdb_data:
				item['data'] = json.loads('{' + self.gdb_data + '}')
			else:
				item['data'] = ''

			if self.gdb_result:
				item['details'] = self.gdb_result
			elif self.gdb_status:
				item['details'] = self.gdb_status
			elif self.gdb_out_of_band:
				item['details'] = self.gdb_out_of_band
			else:
				item['details'] = self.gdb_details



			response.append(item)
			#response = item

		print("parse out <<<< ")
		print(response)

		return response

	def gdbParseLine(self, line):
		#print('input line:', line)

		line = line.lstrip()
		if len(line) == 0:
			self.gdb_type = 'skip'
			return

		if line.rstrip() == '(gdb)':
			self.gdb_type = 'complete'
			self.gdb_details = '(gdb)'
			return
		#handle cases with no parameters
		if line in result_class:
			self.gdb_type = 'result'
			self.gdb_result = line[1:]
			return

		if line in status_class:
			self.gdb_type = 'status'
			self.gdb_status = line[1:]
			return

		if line[0] in stream_output:
			self.gdb_type = 'stream'
			self.gdb_details = line[1:]
			return

		if line[0] == '=':
			#this is out of band response, we don't process out of band message
			self.gdb_type = "out_of_band"
			self.gdbParseNotification(line)
			return		

		if line[0] == '^':
			self.gdb_type = 'result'
			self.gdbParseResult(line)
				#print(self.gdb_data)
			return

		if line[0] == '*':
			self.gdb_type = 'status'
			self.gdbParseStatus(line)
			return
		
		self.gdb_type = 'others'
		self.gdb_details = line

	def gdbParseNotification(self, line):
		words = line.split(',', 1)

		self.gdb_out_of_band = words[0][1:]
		self.gdb_data = self.parse(words[1])

				
	def gdbParseStatus(self, line):
		words = line.split(',' , 1)

		if words[0] in status_class:
			if words[0] == '*running':
				self.gdb_status = 'running'
				self.gdb_data = self.parse(words[1])

			elif words[0] == '*stopped':
				self.gdb_status = 'stopped'
				self.gdb_data = self.parse(words[1])	
		else:
			raise "gdb status class error"	


	def gdbParseResult(self, line):

		words = line.split(',' , 1)

		if words[0] in result_class:
			if words[0] == '^done':
				self.gdb_result = 'done'
				self.gdb_data = self.parse(words[1])

			elif words[0] == '^error':
				self.gdb_result = 'error'
				self.gdb_data = self.parse(words[1])
			
			elif words[0] == '^running':
				self.gdb_result = 'running'
				self.gdb_data = self.parse(words[1])
				
		else:
			raise "gdb result class error"

	def parse(self, line):
		delimited = ['{', '}', ',', '[', ']']
		remaining = line
		output = ''
		bracketFlag = 0

		while len(remaining) > 0:
			if remaining[0] in delimited:
				output = output + remaining[0]
				if remaining[0] == '[':
					remaining = remaining[1:]
					#need to handle bracket carefully
					bracketFlag = bracketFlag + 1

					if remaining[0] == '"':
						while True:
							match = re.search(r'\".*?\"', remaining)
							if match:
								output = output + remaining[:match.end()]
								remaining = remaining[match.end():]
								if remaining[0] == ']':
									bracketFlag = bracketFlag - 1
									output = output + ']'
									remaining = remaining[1:]
									break
					else:
						continue

				elif remaining[0] == ']':
					bracketFlag = bracketFlag - 1
					remaining = remaining[1:]
				else:
					remaining = remaining[1:]
    			
			else:
				match = re.search(r'=', remaining)
				if match:
					#to check the corner case in bracket mode
					if remaining[match.end()] == '{' and bracketFlag > 0:
						remaining = remaining[match.end():]
						continue
					else:
						key = remaining[:match.start()]
						output = output + '"' + key + '"' + ':'
						remaining = remaining[match.end():]

						if remaining[0] == '"':
							match = re.search(r'\".*?\"', remaining)
							output = output + remaining[:match.end()]
							remaining = remaining[match.end():]
							continue
				else:
					break
		return output


if __name__ == "__main__":
	test_string = '''^done,bkpt={number="1",type="breakpoint",disp="keep",enabled="y",addr="0x000000000040058f",func="main",file="sample.c",fullname="/home/shaol/Documents/project/webcode/sample.c",line="8",thread-groups=["i1"],times="0",original-location="/home/shaol/Documents/project/webcode/sample.c:8"}
'''

	gdbParse = GdbParser()
	output = gdbParse.gdbParse(test_string)

	#print(output)
	#print(json.dumps(output))


