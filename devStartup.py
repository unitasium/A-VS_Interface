from abaqus import mdb, session
import customKernel

myAppName = 'My App'
myAppData = customKernel.AbaqusAppData()
myAppData.majorVersion = 1
myAppData.minorVersion = 1
myAppData.updateVersion = 1
customKernel.setAppData(myAppName, myAppData)

def verifyMdb(mdbAppData):
	if mdbAppData == None:
		initializeMdb()
		return

	if not mdbAppData.has_key(myAppName):
		initializeMdb()
		return

customKernel.setVerifyMdb(myAppName, verifyMdb)

def initializeMdb():
	mdb.Model('test')

customKernel.setInitializeMdb(myAppName, initializeMdb)

customKernel.processInitialMdb(myAppName)
