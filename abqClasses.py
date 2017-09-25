from abaqus import *
from abaqusConstants import *
from symbolicConstants import *
from customKernel import CommandRegister


class LayerType(CommandRegister):

    count = 0  # Number of layer types

    def __init__(self, name, material, angle, abq_section=''):
        CommandRegister.__init__(self)
        self.material = material
        self.angle = angle
        self.abq_section = abq_section
        # self.updateLayerName(material_name, fiber_angle)
        LayerType.count += 1

    def setAbqSection(self, abq_section):
        self.abq_section = abq_section
    
    # def updateLayerName(self, material_name, fiber_angle):
    #   self.material_name = material_name
    #   self.fiber_angle = fiber_angle
    #   fa = str(fiber_angle).strip()
    #   if '.' in fa:
    #     fa = fa.replace('.', 'd')
    #   if '-' in fa:
    #     fa = fa.replace('-', 'n')
    #   self.layerName = material_name + '=' + fa


def createSymbolicConstants(text):
    text = text.strip().upper()
    text = text.split()
    text = '_'.join(text)
    return SymbolicConstant(text)

# material = {'name': material_name, 'properties': properties}


def createMaterialInstance(modelName, material):
    material_name = material['name']
    materialProperties = material['properties']
    materialType = materialProperties['type']
    materialConstants = materialProperties['constants'][0]
    materialDensity = materialConstants['density']
    materialElastic = materialConstants['elastic']

    abqModel = mdb.models[modelName]
    abqMaterial = abqModel.Material(name=material_name)
    abqMaterial.Density(table=((materialDensity,),))
    abqMaterialType = createSymbolicConstants(materialType)
    abqMaterial.Elastic(type=abqMaterialType, table=(materialElastic,))

    return 1


mdb.customData.Repository('layerTypes', LayerType)
