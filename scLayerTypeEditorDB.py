from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class ScLayerTypeEditorDB(AFXDataDialog):

    [
        ID_INFO,
        ID_LAST
    ] = range(AFXToolsetGui.ID_LAST, AFXToolsetGui.ID_LAST+2)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        self.form = form

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Edit Layer Type',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        va_inputs = AFXVerticalAligner(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        
        # hf_all = AFXHorizontalFrame(p=self)
        # vf_labels = AFXVerticalFrame(p=hf_all)  # Left frame for labels
        # vf_fields = AFXVerticalFrame(p=hf_all)  # right frame for inputs

        # FXLabel(p=vf_labels, 'Name:')
        # FXLabel(p=vf_labels, 'Material:')
        # FXLabel(p=vf_labels, 'Angle:')
        # FXLabel(p=vf_labels, 'Section:')

        # self.label_name = FXLabel(  # Layer type name for edit mode
        #     p=vf_fields, text=form.nameKw.getValue()
        # )
        self.tf_name = AFXTextField(  # Layer type name for create mode
            p=va_inputs, ncols=12, labelText='Name:', tgt=form.nameKw, sel=0
        )

        self.cb_material = AFXComboBox(  # Select material
            p=va_inputs, ncols=0, nvis=1, text='Material:', tgt=form.materialKw, sel=0
        )
        self.cb_material.setMaxVisible(10)

        AFXTextField(  # Fiber orientation
            p=va_inputs, ncols=12, labelText='Angle:', tgt=form.angleKw, sel=0
        )
        
        self.cb_section = AFXComboBox(  # Select Abaqus Section
            p=va_inputs, ncols=0, nvis=1, text='Section:', tgt=form.abaqusSectionKw, sel=0
        )
        self.cb_section.setMaxVisible(10)

        # ============================================================
        FXMAPFUNC(self, SEL_COMMAND, self.ID_INFO, ScLayerTypeEditorDB.showInfo)
        FXButton(self, 'Check', tgt=self, sel=self.ID_INFO)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)

        self.currentModelName = getCurrentContext()['modelName']
        mdb.models[self.currentModelName].materials.registerQuery(self.updateCB_Materials)

        # if self.form.edit_mode == 'create':
        #     mdb.models[self.currentModelName].materials.registerQuery(self.updateCB_Materials)
        if self.form.edit_mode == 'edit':
            # self.tf_name.setEditable(False)
            self.tf_name.setReadOnlyState(True)
            # self.tf_name.disable()
            layer_type = mdb.customData.layerTypes[self.form.nameKw.getValue()]
            self.form.materialKw.setValue(layer_type.material)
            self.form.angleKw.setValue(layer_type.angle)
            self.form.abaqusSectionKw.setValue(layer_type.abaqusSection)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        mdb.models[self.currentModelName].materials.unregisterQuery(self.updateCB_Materials)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateCB_Materials(self):

        # modelName = getCurrentContext()['modelName']
        self.cb_material.clearItems()
        names = mdb.models[self.currentModelName].materials.keys()
        names.sort()
        for name in names:
            self.cb_material.appendItem(name)
        
        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def showInfo(self, sender, sel, ptr):

        mainWindow = getAFXApp().getAFXMainWindow()
        message = 'Layer Type Name: ' + self.form.nameKw.getValue()
        showAFXInformationDialog(mainWindow, message)
