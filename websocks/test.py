import re
import json

if __name__ == "__main__":
	test_string = 'thread-groups={"i1", "ok", {"hello"}},another={"hello"}'

	match = re.search(r'{.*},', test_string)

	print(match.group(0))
	print(test_string[:match.start()])
	print(test_string[match.end():])