from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class ScLayerTypeEditForm(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner, layerTypeName):
        
        # self.edit_mode = kwargs['editMode']  # Create or edit
        # self.layer_type_name = ''
        # if self.edit_mode == 'edit':
        self.layer_type_name = layerTypeName
        
        # print len(kwargs)

        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='',
            objectName='', registerQuery=False)
        pickedDefault = ''
        self.nameKw = AFXStringKeyword(self.cmd, 'name', True, '')
        self.materialKw = AFXStringKeyword(self.cmd, 'material', True)
        self.angleKw = AFXFloatKeyword(self.cmd, 'angle', True, 0.0)
        self.abaqusSectionKw = AFXStringKeyword(self.cmd, 'abaqusSection', True)

        self.nameKw.setValue(self.layer_type_name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import scLayerTypeEditDB
        # return scLayerTypeEditorDB.ScLayerTypeEditorDB(self, editMode=self.edit_mode)
        return scLayerTypeEditDB.ScLayerTypeEditDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
# thisPath = os.path.abspath(__file__)
# thisDir = os.path.dirname(thisPath)

# toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
# toolset.registerGuiMenuButton(
#     buttonText='scLayerTypeEditor', 
#     object=ScLayerTypeEditor_plugin(toolset),
#     messageId=AFXMode.ID_ACTIVATE,
#     icon=None,
#     kernelInitString='',
#     applicableModules=ALL,
#     version='N/A',
#     author='N/A',
#     description='N/A',
#     helpUrl='N/A'
# )
