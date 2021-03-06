import os
import os.path
import sys
import datetime
import webbrowser
import argparse

class CommandArgs:
	def __init__ (self):
		self.argParser = argparse.ArgumentParser ()
	
		self.argParser.add_argument ('-c', '--clean', help = 'clean source tree', action = 'store_true')
		self.argParser.add_argument ('-d', '--docs', help = 'make docs', action = 'store_true')
		self.argParser.add_argument ('-f', '--fcall', help = 'test fast calls', action = 'store_true')
		
		self.__dict__.update (self.argParser.parse_args () .__dict__)

commandArgs = CommandArgs ()
		
if commandArgs.clean:
	answer0 = input ('\nWARNING: THIS PROGRAM MAY ERRONEOUSLY DELETE MANY VALUABLE FILES!\nUsing it is entirely at your own risk.\nRead the sourcecode if you want to know what it does.\nIf you\'re not sure that its harmless in your situation, DON\'T USE IT!!!\n\nARE YOU SURE YOU WANT TO CONTINUE? (y = yes, n = no) ')
	if answer0 != 'y':
		print ('\nShipment test aborted')
		sys.exit (1)
		
cleanFromTime = datetime.datetime.now ()

shipDir = os.path.dirname (os.path.abspath (__file__)) .replace ('\\', '/')
appRootDir = '/'.join  (shipDir.split ('/')[ : -2])

def getAbsPath (relPath):
	return '{}/{}'.format (appRootDir, relPath)

def test (relPath, fileNamePrefix, run = False, switches = ''):
	os.chdir (getAbsPath (relPath))
	
	os.system ('run_transcrypt -b -m -dm -dt {}{}.py'.format (switches, fileNamePrefix))

	if run:
		os.chdir (getAbsPath (relPath))
		os.system ('run_transcrypt -r {}.py'.format (fileNamePrefix))		
	
	webbrowser.open ('file://{}/{}.html'.format (getAbsPath (relPath), fileNamePrefix), new = 2)
	
	filePath = '{}/{}.min.html'.format (getAbsPath (relPath), fileNamePrefix)
	if os.path.isfile (filePath):
		webbrowser.open ('file://{}'.format (filePath), new = 2)
	
# Perform all tests
for fcallSwitch in (('', '-f ') if commandArgs.fcall else ('',)):
	test ('development/automated_tests/hello', 'autotest', True, fcallSwitch)
	test ('development/automated_tests/transcrypt', 'autotest', True, fcallSwitch)
	test ('development/manual_tests/module_random', 'module_random', False, fcallSwitch)
	test ('demos/hello', 'hello', False, fcallSwitch)
	test ('demos/jquery_demo', 'jquery_demo', False, fcallSwitch)
	test ('demos/d3js_demo', 'd3js_demo', False, fcallSwitch)
	test ('demos/ios_app', 'ios_app', False, fcallSwitch)
	test ('demos/react_demo', 'react_demo', False, fcallSwitch)
	test ('demos/pong', 'pong', False, fcallSwitch)
	test ('demos/turtle_demos', 'star', False, fcallSwitch + '-p .user ')
	test ('demos/turtle_demos', 'snowflake', False, fcallSwitch + '-p .user ')
	test ('demos/turtle_demos', 'mondrian', False, fcallSwitch + '-p .user ')
	test ('demos/turtle_demos', 'mandala', False, fcallSwitch + '-p .user ')
	test ('demos/terminal_demo', 'terminal_demo', False, fcallSwitch)

# Make docs optionally since they cause a lot of diffs	
# Make them before target files are erased, since they are to be included in the docs
if commandArgs.docs:
	sphinxDir = '/'.join ([appRootDir, 'docs/sphinx'])
	os.chdir (sphinxDir)
	os.system ('touch *.rst')
	os.system ('make html')

# Optionally remove all targets	except documentation
if commandArgs.clean:
	removalList = []
	
	for rootDir, dirNames, fileNames in os.walk (appRootDir):
		rootDir = rootDir.replace ('\\', '/')
		
		if not '/docs/' in rootDir:
			for fileName in fileNames:
				filePath = '{}/{}'.format (rootDir.replace ('\\', '/'), fileName)
				if filePath.endswith ('.pyc') or datetime.datetime.fromtimestamp (os.path.getmtime (filePath)) >= cleanFromTime:
					removalList.append (filePath)
				
	print ('THE FOLLOWING FILES WILL ALL BE REMOVED:\n')

	for filePath in removalList:
		print (filePath)
		
	answer1 = input ('\nARE YOU SURE YOU WANT TO REMOVE ALL OF THE ABOVE FILES? (y = yes, n = no) ')

	if answer1 == 'y':
		for filePath in removalList:
			os.remove (filePath)
	else:
		print ('\nShipment test aborted')
		sys.exit (1)
		
print ('\nShipment test ready')
