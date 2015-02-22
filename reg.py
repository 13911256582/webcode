import re

test = '^done,bkpt={number="1",type="breakpoint",disp="keep",enabled="y",addr="0x0000000000400535",func="main",file="sample.c",fullname="/home/shaol/Documents/project/webcode/sample.c",line="6",thread-groups=["i1"],times="0",original-location="/home/shaol/Documents/project/webcode/sample.c:6"}'

#res = re.split(r'\bbkpt={.*}', test)

res = re.split(',', test)

print(res)


