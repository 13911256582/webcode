from django.test import TestCase

# Create your tests here.
code = "x = 4" + "\n" + "print x"

pythonFile = open('sample.py','w')
pythonFile.write(code)
pythonFile.close()