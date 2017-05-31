from abaqus import *
from abaqusConstants import *
from symbolicConstants import *
from customKernel import CommandRegister

class LayerType(CommandRegister):

    count = 0  # Number of layer types

    def __init__(self, name, materialName, fiberAngle):
        CommandRegister.__init__(self)
        self.materialName = materialName
        self.fiberAngle = fiberAngle
        self.updateLayerName(materialName, fiberAngle)
        LayerType.count += 1

    def updateLayerName(self, materialName, fiberAngle):
        self.materialName = materialName
        self.fiberAngle = fiberAngle
        fa = str(fiberAngle).strip()
        if '.' in fa:
            fa = fa.replace('.', 'd')
        if '-' in fa:
            fa = fa.replace('-', 'n')
        self.layerName = materialName + '=' + fa


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

