#!/usr/bin/env python

import os
import math
import itertools

def listAll():
	allAttributes = globals().keys()
	return [x for x in allAttributes if not x.startswith('_') and x not in ['os', 'math', 'itertools', 'listAll']]


# def powerflow(analysisName):
# 	pngs = []
# 	for study in os.listdir('analyses/' + analysisName + '/studies/'):
# 		for fileName in os.listdir('analyses/' + analysisName + '/studies/' + study):
# 			if fileName.endswith('.png'): pngs.append('studies/' + study + '/' + fileName)
# 	return {'reportType':'powerflow', 'pngs':pngs}

def runtimeStats(analysisName):
	stdouts = []
	for study in os.listdir('analyses/' + analysisName + '/studies/'):
		with open('analyses/' + analysisName + '/studies/' + study + '/stdout.txt', 'r') as stdout:
		# Hack: drop leading \r newlines:
			stdouts.append(study.upper() + '\n\n' + stdout.read().replace('\r',''))
	return {'reportType':'runtimeStats', 'stdouts':stdouts}

def capacitorActivation(analysisName):
	dataTree = {}
	pathPrefix = './analyses/' + analysisName
	for study in os.listdir(pathPrefix + '/studies/'):
		dataTree[study] = {}
		capFileNames = filter(lambda x:x.startswith('Capacitor_') and x.endswith('.csv'), os.listdir(pathPrefix + '/studies/' + study))
		for capacitor in capFileNames:
			dataTree[study][capacitor.replace('.csv','')] = __csvToArray__(pathPrefix + '/studies/' + study + '/' + capacitor)
	return {'reportType':'capacitorActivation', 'dataTree':dataTree}

def regulatorPowerflow(analysisName):
	dataTree = {}
	pathPrefix = './analyses/' + analysisName
	for study in os.listdir(pathPrefix + '/studies/'):
		dataTree[study] = {}
		regFileNames = [x for x in os.listdir(pathPrefix + '/studies/' + study) if x.startswith('Regulator_') and x.endswith('.csv')]
		for regulator in regFileNames:
			cleanReg = regulator.replace('.csv','')
			dataTree[study][cleanReg] = {}
			fullArray = __csvToArray__(pathPrefix + '/studies/' + study + '/' + regulator)
			dataTree[study][cleanReg]['realPower'] = [[row[0], row[4], row[6], row[8]] for row in fullArray]
			dataTree[study][cleanReg]['reactivePower'] = [[row[0], row[5], row[7], row[9]] for row in fullArray]
			dataTree[study][cleanReg]['tapPositions'] = [[row[0],row[1],row[2],row[3]] for row in fullArray]
			# NOTE: we operate on the values [1:] then put the headers back in a second step.
			dataTree[study][cleanReg]['apparentPower'] = [[row[0], __pyth__(row[4],row[5]), __pyth__(row[6],row[7]), __pyth__(row[8],row[9])] for row in fullArray[1:]]
			dataTree[study][cleanReg]['apparentPower'].insert(0,['# timestamp','Tap_A','Tap_B','Tap_C'])
			dataTree[study][cleanReg]['powerFactor'] = [[row[0], math.cos(math.atan((row[5]+row[7]+row[9])/(row[4]+row[6]+row[8])))] for row in fullArray[1:]]
			dataTree[study][cleanReg]['powerFactor'].insert(0,['# timestamp','Power Factor'])
	return {'reportType':'regulatorPowerflow', 'dataTree':dataTree}

def studyDetails(analysisName):
	studies = []
	climates = [['location','marker']]
	pathPrefix = './analyses/' + analysisName
	with open(pathPrefix + '/metadata.txt','r') as anaMdFile:
		created = eval(anaMdFile.read())['created']
	for study in os.listdir(pathPrefix + '/studies/'):
		with open(pathPrefix + '/studies/' + study + '/metadata.txt', 'r') as mdFile:
			metadata = eval(mdFile.read())
		climates.append([metadata['climate'],1])
		studies.append([metadata['name'], metadata['sourceFeeder']])
	return {'reportType':'studyDetails', 'climates':climates, 'studies':studies, 'created':created}

def voltageBand(analysisName):
	dataTree = {}
	pathPrefix = './analyses/' + analysisName
	for study in os.listdir(pathPrefix + '/studies/'):
		dataTree[study] = {}
		for fileName in os.listdir(pathPrefix + '/studies/' + study):
			if 'VoltageJiggle.csv' == fileName:
				fullArray = __csvToArray__(pathPrefix + '/studies/' + study + '/' + fileName)
				dataTree[study] = [[row[0],row[1]/2,row[2]/2,row[3]/2] for row in fullArray[1:]]
				dataTree[study].insert(0,[fullArray[0][0],fullArray[0][1],fullArray[0][2],fullArray[0][3]])
	return {'reportType':'voltageBand', 'dataTree':dataTree}

def __csvToArray__(fileName):
	''' Take a filename to a list of timeseries vectors. Internal method. '''
	def strClean(x):
		# Helper function that translates csv values to reasonable floats (or header values to strings):
		if x == 'OPEN':
			return 1.0
		elif x == 'CLOSED':
			return 0.0
		elif x[0] == '+':
			return float(x[1:])
		elif x[0] == '-':
			return float(x)
		elif x[0].isdigit() and x[-1].isdigit():
			return float(x)
		else:
			return x
	with open(fileName) as openfile:
		data = openfile.read()
	lines = data.splitlines()
	array = map(lambda x:x.split(','), lines)
	cleanArray = [map(strClean, x) for x in array]
	# Magic number 8 is the number of header rows in each csv.
	arrayNoHeaders = cleanArray[8:]
	# Drop the timestamp column:
	return arrayNoHeaders

def __pyth__(x,y):
	''' helper function to compute the third side of the triangle'''
	return math.sqrt(x**2 + y**2)

def __flat1__(aList):
	''' Flatten one level. Go from e.g. [[1],[2],[3,4],[[5,6],[7,8]]] to [1,2,3,4,[5,6],[7,8]]'''
	return list(itertools.chain(*aList))

# # TEST CODE
# stuff = regulatorPowerflow('clothing')
# from pprint import pprint
# pprint(stuff)
# stuff = voltageBand('clothing')
# sample = stuff['dataTree']['shirt']
# print sample
