# -*- coding: utf-8 -*-

# ******************************************************************************
# Custom VABS GUI Application 
# This script creates and launches the Beam GUI application 
# ******************************************************************************

from abaqusGui import AFXApp
import sys
from vabsCaeMainWindow import VABSCaeMainWindow

# Initialize application object 
# In AFXApp, appName and vendorName are displayed if productName is set to ''
# otherwise productName is displayed. 
app = AFXApp(appName = 'ABAQUS/CAE', 
             vendorName = 'SIMULIA', 
             productName = 'Abaqus-VABS GUI', 
             majorNumber = 6, 
             minorNumber = 16, 
             updateNumber = 0, 
             prerelease = False)

app.init(sys.argv)

# Construct main window
VABSCaeMainWindow(app)

# Create application
app.create()

# Run application
app.run()
