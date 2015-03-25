import re
import json
from pyparsing import *
import pdb

#if __name__ == "__main__":
	#test_string = 'thread-groups={"i1", "ok", {"hello"}},another={"hello"}'

	#test_string = '{{"fist"}, {"second"}, {"third"}}'

	#left = test_string
	#while len(left) > 0:
	#match = re.search(r'({.*?})', test_string)

	#print(match.group())

   # define grammar of a greeting
# jsonParser.py
#
# Implementation of a simple JSON parser, returning a hierarchical
# ParseResults object support both list- and dict-style data access.
#
# Copyright 2006, by Paul McGuire
#
# Updated 8 Jan 2007 - fixed dict grouping bug, and made elements and
#   members optional in array and object collections
#
json_bnf = """
object 
    { members } 
    {} 
members 
    string = value 
    members , string = value 
array 
    [ elements ]
    [] 
elements 
    value 
    elements , value 
value 
    string
    number
    object
    array
    true
    false
    null
"""

#from pyparsing import *

TRUE = Keyword("true").setParseAction( replaceWith(True) )
FALSE = Keyword("false").setParseAction( replaceWith(False) )
NULL = Keyword("null").setParseAction( replaceWith(None) )

jsonString = dblQuotedString.setParseAction( removeQuotes )
jsonNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + Word(nums) ) +
                    Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )

jsonObject = Forward()
jsonValue = Forward()
jsonElements = delimitedList( jsonValue )
jsonArray = Group(Suppress('[') + Optional(jsonElements) + Suppress(']') )
jsonValue << ( jsonString | jsonNumber | Group(jsonObject)  | jsonArray | TRUE | FALSE | NULL )
#memberDef = Group( jsonString + Suppress(':') + jsonValue )
memberDef = Group( jsonString + Suppress('=') + jsonValue )
jsonMembers = delimitedList( memberDef )
jsonObject << Dict( Suppress('{') + Optional(jsonMembers) + Suppress('}') )

jsonComment = cppStyleComment 
jsonObject.ignore( jsonComment )

def convertNumbers(s,l,toks):
    n = toks[0]
    try:
        return int(n)
    except ValueError, ve:
        return float(n)
        
jsonNumber.setParseAction( convertNumbers )

def parse(line):
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
    testdata = """
    {
        "glossary": {
            "title": "example glossary",
            "GlossDiv": {
                "title": "S",
                "GlossList": 
                    {
                    "ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "TrueValue": true,
                    "FalseValue": false,
                    "Gravity": -9.8,
                    "LargestPrimeLessThan100": 97,
                    "AvogadroNumber": 6.02E23,
                    "EvenPrimesGreaterThan2": null,
                    "PrimesLessThan10" : [2,3,5,7],
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986",
                    "GlossDef": "A meta-markup language, used to create markup languages such as DocBook.",
                    "GlossSeeAlso": ["GML", "XML", "markup"],
                    "EmptyDict" : {},
                    "EmptyList" : []
                    }
            }
        }
    }
    """

    #testdata = '{BreakpointTable={nr_rows="3",nr_cols="6",hdr=[{width="7",alignment="-1",col_name="number",colhdr="Num"}]}}'
    #test_string = '{BreakpointTable={nr_rows="3",nr_cols="6",hdr=[{width="7",alignment="-1",col_name="number",colhdr="Num"},{width="14",alignment="-1",col_name="type",colhdr="Type"},{width="4",alignment="-1",col_name="disp",colhdr="Disp"},{width="3",alignment="-1",col_name="enabled",colhdr="Enb"},{width="18",alignment="-1",col_name="addr",colhdr="Address"},{width="40",alignment="2",col_name="what",colhdr="What"}]}}'
    test_string = '{BreakpointTable={nr_rows="3",nr_cols="6",hdr=[{width="7",alignment="-1",col_name="number",colhdr="Num"},{width="14",alignment="-1",col_name="type",colhdr="Type"},{width="4",alignment="-1",col_name="disp",colhdr="Disp"},{width="3",alignment="-1",col_name="enabled",colhdr="Enb"},{width="18",alignment="-1",col_name="addr",colhdr="Address"},{width="40",alignment="2",col_name="what",colhdr="What"}],body=[bkpt={number="1",type="breakpoint",disp="keep",enabled="y",addr="0x000000000040058f",func="main",file="sample.c",fullname="/home/shaol/Documents/project/webcode/sample.c",line="8",thread-groups=["i1"],times="1",original-location="/home/shaol/Documents/project/webcode/sample.c:8"},bkpt={number="2",type="breakpoint",disp="keep",enabled="y",addr="0x0000000000400585",func="main",file="sample.c",fullname="/home/shaol/Documents/project/webcode/sample.c",line="6",thread-groups=["i1"],times="0",original-location="/home/shaol/Documents/project/webcode/sample.c:6"},bkpt={number="3",type="breakpoint",disp="keep",enabled="y",addr="0x0000000000400598",func="main",file="sample.c",fullname="/home/shaol/Documents/project/webcode/sample.c",line="9",thread-groups=["i1"],times="0",original-location="/home/shaol/Documents/project/webcode/sample.c:9"}]}}'
    output = parse(test_string)
    print(output)

    obj = json.loads(output)

    print(obj)



    

def jsonObject(testdata):
    import pprint
    results = jsonObject.parseString(testdata)
    pprint.pprint( results.asList() )
    print

    def testPrint(x):
    	print type(x),repr(x)
    	print results.glossary.GlossDiv.GlossList.keys()

    testPrint( results.glossary.title )
    testPrint( results.glossary.GlossDiv.GlossList.ID )
    testPrint( results.glossary.GlossDiv.GlossList.FalseValue )
    testPrint( results.glossary.GlossDiv.GlossList.Acronym )
    testPrint( results.glossary.GlossDiv.GlossList.EvenPrimesGreaterThan2 )
    testPrint( results.glossary.GlossDiv.GlossList.PrimesLessThan10 )