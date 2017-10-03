from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class Test2DB(AFXDataDialog):

    [
        ID_INFO,
        ID_LAST
    ] = range(AFXToolsetGui.ID_LAST, AFXToolsetGui.ID_LAST+2)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        self.form = form
        # self.edit_mode = kwargs['editMode']
        # self.layer_type_name = kwargs['layerTypeName']

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Edit Layer Type',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        VAligner_1 = AFXVerticalAligner(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        
        self.tf_name = AFXTextField(
            p=VAligner_1, ncols=12, labelText='Name:', tgt=self.form.nameKw, sel=0
        )
        # self.tf_name.setText(self.layer_type_name)

        self.cb_material = AFXComboBox(p=VAligner_1, ncols=0, nvis=1, text='Material:', tgt=form.materialKw, sel=0)
        self.cb_material.setMaxVisible(10)
        # cb_material.appendItem(text='Item 1')
        # cb_material.appendItem(text='Item 2')
        # cb_material.appendItem(text='Item 3')

        AFXTextField(p=VAligner_1, ncols=12, labelText='Angle:', tgt=form.angleKw, sel=0)
        
        ComboBox_2 = AFXComboBox(p=VAligner_1, ncols=0, nvis=1, text='Section:', tgt=form.abaqusSectionKw, sel=0)
        ComboBox_2.setMaxVisible(10)
        ComboBox_2.appendItem(text='Item 1')
        ComboBox_2.appendItem(text='Item 2')
        ComboBox_2.appendItem(text='Item 3')

        # ============================================================
        FXMAPFUNC(self, SEL_COMMAND, self.ID_INFO, Test2DB.showInfo)
        FXButton(self, 'Check', tgt=self, sel=self.ID_INFO)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)

        self.currentModelName = getCurrentContext()['modelName']

        # if self.form.edit_mode == 'create':
        #     mdb.models[self.currentModelName].materials.registerQuery(self.updateCB_Materials)
        # elif self.form.edit_mode == 'edit':
            # self.form.nameKw.setValue(self.form.nameKw)
            # self.tf_name.setText(self.form.nameKw.getValue())
            # self.tf_name.setEditable(False)
            # self.tf_name.setReadOnlyState(True)
        self.cb_material.appendItem('item 1')
        self.cb_material.appendItem('item 2')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        # mdb.models[self.currentModelName].materials.unregisterQuery(self.updateCB_Materials)

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
