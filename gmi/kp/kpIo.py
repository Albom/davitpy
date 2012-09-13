# -*- coding: utf-8 -*-


from datetime import date
from kpDay import *
import pydarn
import h5py
import os
import sys

def readKpDay(myDate):
	"""
	*******************************
	
	kpVals = readKpDay(myDate)
	
	takes a python date object and returns kpDay object for that day

	INPUTS:
		myDate : a python date object
	OUTPUTS:
		kpVals : a list of the Kp indices in string format, e.g. '3+'

	Created by AJ
	*******************************
	"""
	import utils
	try:
		#open the file
		f = h5py.File(os.environ['DAVITPY']+'/gmi/kp/kp_index.hdf5','r')
	except:
		print 'error opening '+os.environ['DAVITPY']+'/gmi/kp/kp_index.hdf5'
		sys.exit()
	
	try:
		#get the vales for that day
		vals = f['kpVals'].value[f['kpDates'].value == utils.timeUtils.dateToYyyymmdd(myDate)]
	except:
		print 'error reading the kp file'
		sys.exit()
		
	#close the file
	f.close()
	
	#return the kpDay object
	return kpDay(myDate,vals[0])

def readKpHdf5():
	"""
	*******************************
	
	kpVals = readKpHdf5()
	
	reads the entirety of a Kp index file located at ${DAVITPY}gmi/kp/kp_index.hdf5' and returns
	the contents as a list of kpDay objects
	
	Note that getting Kp values with readKpDay() is preferred

	INPUTS:
		myDate : a python date object
	OUTPUTS:
		kpVals : a list of the Kp indices in string format, e.g. '3+'

	Created by AJ
	*******************************
	"""
	import utils
	#open the file
	f = h5py.File(os.environ['DAVITPY']+'gmi/kp/kp_index.hdf5','r')
	dates = f['kpDates'].value
	vals = f['kpVals'].value
	f.close()
	
	allKp = []
	for i in range(0,len(dates)):
		myDay = kpDay(utils.timeUtils.yyyymmddToDate(dates[i]),vals[i])
		allKp.append(myDay)
		
	return allKp

def kp2Hdf5():
	import utils
	"""
	*******************************
	
	kp2Hdf5():
	
	reads the entirety of a Kp index file located at ${DAVITPY}/gmi/kp/kp_index.ascii
	and writes out a Kp file in hdf5 format to ${DAVITPY}/gmi/kp/kp_index.hdf5

	INPUTS:
		none
	OUTPUTS:
		NONE
		
	Written by AJ 20120718
	*******************************
	"""
	
	allKp = readKpAscii()
	
	#rearrage the Kp data
	dates = []
	vals = []
	for i in range(0,len(allKp)):
		dates.append(utils.timeUtils.dateToYyyymmdd(allKp[i].day))
		vals.append(allKp[i].vals)
		
	f = h5py.File(os.environ['DAVITPY']+'/gmi/kp/kp_index.hdf5','w')
	f.create_dataset('kpDates', data=dates)
	f.create_dataset('kpVals',data=vals)
	f.close()
	
	
	
def readKpAscii():
	"""
	*******************************
	
	allKp = readKpAscii():
	
	reads the entirety of a Kp index file located at ${DAVITPY}/gmi/kp/kp_index.ascii
	
	Note that getting Kp values with readKpDay() is preferred

	INPUTS:
		none
	OUTPUTS:
		allKp : a list of kpDay objects containing the entire contents of the file
		
	Written by AJ 20120718
	*******************************
	"""
	import utils
	#open the Kp ascii file
	f = open(os.environ['DAVITPY']+'/gmi/kp/kp_index.ascii', 'r')
	allKp = []
	
	#read the first line
	myLine = f.readline()
	
	#iterate through the entire file
	while (myLine != '' ):
		myLine.replace( "\n", "" )
		
		#parse the date into a date object
		d = utils.timeUtils.yyyymmddToDate(myLine[0:8])
		
		#parse the Kp values into a list
		kpVals = []
		for i in range(0,8):
			index = 9+i*2
			kpVals.append(myLine[index:index+2])
			
		#create a kpDay object with the date and values
		myDay = kpDay(d,kpVals)
		
		allKp.append(myDay)
		
		#read the next line in the file
		myLine = f.readline()
		
	#return the array of data
	return allKp

	