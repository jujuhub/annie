import numpy as np
import pulseObject as pu
import sys
import random
import matplotlib.pyplot as plt


lengthOfWindow = 500

def getValidInput(fig):
	holder = raw_input("Press h for a list of commands: ")
	if not(plt.get_fignums()):
		print pu.cactusTime('YOU CLOSED MY WINDOW')
	elif holder.lower() == 'h':
		print 'E to exit \nN to advance \nH for help \nW to change the length of the window'
	elif holder.lower() == 'e':
		plt.close(fig)
		sys.exit(1)
	elif holder == 'n':
		plt.close(fig)
		return(True)
	elif holder == 'w':
		holder = raw_input("Input a number for the window size: ")
		while True:
			try:
				holder = int(holder)
				global lengthOfWindow
				lengthOfWindow = holder
				break
			except ValueError:
				holder = raw_input("Please enter a number: ")
				continue
			return True		


def plotData(pulseObjects):
	dataToPlot = []
	keepGoing = True
	startPoint = 0
	while keepGoing == True:
		fig = plt.figure()

		for val in pulseObjects:
			fig.set_size_inches(val.size)
			holderData = val.getData((startPoint, startPoint + lengthOfWindow))
			dataToPlot.append(holderData)

			#print 'LENGTH: ' + str(len(holderData))
		
		#print 'DATA FROM ' + str(counter*lengthOfWindow) + " TO " + str((counter+1)*lengthOfWindow) + " " + str(dataToPlot)
		for num, val in enumerate(dataToPlot):
				xVals = range(1, len(val) + 1)
				plt.plot(xVals, val, label = pulseObjects[num].label)
		plt.ticklabel_format(useOffset=False)
		plt.xlabel('SAMPLES', fontsize = 24)
		plt.ylabel('COUNTS ', fontsize = 24)
		plt.title('SAMPLES ' + str(startPoint) + ' TO ' + str(startPoint + len(dataToPlot[0])), fontsize = 32)
		plt.legend()
		#plt.imshow(xVals, val, aspect='auto')
		plt.draw()
		plt.pause(0.1)
		startPoint = startPoint + lengthOfWindow
		print 'LENGTH OF WINDOW: ' + str(lengthOfWindow)
		while not(getValidInput(fig)):
			pass

		if len(holderData) < lengthOfWindow:
			keepGoing = False
			break
		dataToPlot = []


def getFileNames():
	fileNames = []

	if len(sys.argv) == 1:
		print 'NOT ENOUGH ARGUMENTS. CACTUS TIME'
		pu.cactusTime('HOW THE **** CAN I PLOT WITHOUT AN INPUT FILE', 32)
	else:
		for val in sys.argv[1:]:
			fileNames.append(val)

	return fileNames


listOfFiles = getFileNames()
pulseObjects = []
dataToPlot = []

for val in listOfFiles:
	pulseObjects.append(pu.pulseObject(val, (6, 6), val))


plotData(pulseObjects)







