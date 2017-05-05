from abaqus import *
from testRepository import *

mdb.customData.Repository('models', Model)
mdb.customData.Model('Model-1')
mdb.customData.models['Model-1'].Block('Block-1')

