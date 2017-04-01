from abaqus import *
from abaqusConstants import *
from symbolicConstants import *

def createSymbolicConstants(text):
    text = text.strip().upper()
    text = text.split()
    text = '_'.join(text)
    return SymbolicConstant(text)

# material = {'name': materialName, 'properties': properties}
def createMaterialInstance(modelName, material):
    materialName = material['name']
    materialProperties = material['properties']
    materialType = materialProperties['type']
    materialConstants = materialProperties['constants'][0]
    materialDensity = materialConstants['density']
    materialElastic = materialConstants['elastic']

    abqModel = mdb.models[modelName]
    abqMaterial = abqModel.Material(name=materialName)
    abqMaterial.Density(table=((materialDensity,),))
    abqMaterialType = createSymbolicConstants(materialType)
    abqMaterial.Elastic(type=abqMaterialType, table=(materialElastic,))

    return 1

