# -*- coding: utf-8 -*-

# ******************************************************************************
# Custom VABS GUI Application 
# This script creates and launches the Beam GUI application 
# ******************************************************************************

from abaqusGui import AFXApp
import sys
from devCaeMainWindow import DEVCaeMainWindow


# Initialize application object 
# In AFXApp, appName and vendorName are displayed if productName is set to ''
# otherwise productName is displayed. 
# app = AFXApp(appName = 'ABAQUS/CAE', 
#              vendorName = 'SIMULIA', 
#              productName = 'A-SC/V GUI DEV', 
#              majorNumber = 6, 
#              minorNumber = 16, 
#              updateNumber = 0, 
#              prerelease = False)
app = AFXApp('Abaqus/CAE', 'SIMULIA')

app.init(sys.argv)

# Construct main window
DEVCaeMainWindow(app)

# Create application
app.create()

# Run application
app.run()
