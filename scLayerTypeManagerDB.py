from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
from scLayerTypeEditorForm import ScLayerTypeEditorForm
from scLayerTypeEditForm import ScLayerTypeEditForm
from test2Form import Test2Form

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class ScLayerTypeManagerDB(AFXDataDialog):

    [
        ID_INFO,
        ID_CREATE,
        ID_EDIT,
        ID_REFRESH,
        ID_SAVE,
        ID_LAST
    ] = range(AFXToolsetGui.ID_LAST, AFXToolsetGui.ID_LAST+6)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, **kwargs):

        self.form = form
        self.owner = kwargs['owner']

        self.select_name = ''

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Layer Type Manager',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        
        self.appendActionButton('Refresh', self, self.ID_REFRESH)
        self.appendActionButton('Save', self, self.ID_SAVE)

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')

        # ============================================================

        # FXMAPFUNC(self, SEL_COMMAND, self.ID_CREATE)
        # FXMAPFUNC(self, SEL_COMMAND, self.ID_EDIT)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_REFRESH, ScLayerTypeManagerDB.refresh)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_SAVE, ScLayerTypeManagerDB.save)

        # ============================================================
            
        vf = FXVerticalFrame(self, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)


        self.table_layertypes = AFXTable(
            vf, 6, 4, 6, 4, form.layertypeKw, 0, 
            AFXTABLE_COLUMN_RESIZABLE|AFXTABLE_ROW_MODE|AFXTABLE_SINGLE_SELECT|LAYOUT_FILL_X
        )
        # self.ci_layertypename = AFXColumnItems(
        #     referenceColumn=0, tgt=
        # )
        self.table_layertypes.setLeadingRows(1)
        # self.table_layertypes.setLeadingColumns(1)
        self.table_layertypes.setColumnWidth(-1, 100)
        self.table_layertypes.setColumnEditable(-1, False)
        self.table_layertypes.setColumnType(0, AFXTable.TEXT)  # LayerType name
        self.table_layertypes.setColumnType(1, AFXTable.TEXT)  # LayerType material
        self.table_layertypes.setColumnType(2, AFXTable.FLOAT)  # LayerType angle
        self.table_layertypes.setColumnType(3, AFXTable.TEXT)  # LayerType abaqusSection
        self.table_layertypes.setLeadingRowLabels('Name\tMaterial\tAngle\tSection')
        self.table_layertypes.setStretchableColumn( self.table_layertypes.getNumColumns()-1 )
        self.table_layertypes.showHorizontalGrid(True)
        # self.table_layertypes.showVerticalGrid(True)

        # ============================================================

        # FXButton(self, 'Create...', tgt=self, sel=self.ID_CREATE)
        # FXButton(self, 'Edit...', tgt=self, sel=self.ID_EDIT)
        self.button_create = FXButton(
            self, 'Create...',
            tgt=ScLayerTypeEditorForm(
                self.owner, editMode='create', layerTypeName=''
            ),
            sel=AFXMode.ID_ACTIVATE
        )

        self.button_edit = FXButton(
            self, 'Edit...',
            # tgt=Test2Form(
            #     self.owner, editMode='edit', layerTypeName='bbb'
            # ),
            sel=AFXMode.ID_ACTIVATE
        )

        # ============================================================
        FXMAPFUNC(self, SEL_COMMAND, self.ID_INFO, ScLayerTypeManagerDB.showInfo)
        FXButton(self, 'Check', tgt=self, sel=self.ID_INFO)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)
        
        layertypes = mdb.customData.layerTypes
        list_layertypes = []
        for lt in layertypes.values():
            tuple_layertype = (lt.name, lt.material, lt.angle, lt.abaqusSection)
            list_layertypes.append(str(tuple_layertype))
        str_layertypes = ','.join(list_layertypes)
        self.form.layertypeKw.setValues(str_layertypes)

    def refresh(self, sender, sel, ptr):

        layertypes = mdb.customData.layerTypes
        list_layertypes = []
        for lt in layertypes.values():
            tuple_layertype = (lt.name, lt.material, lt.angle, lt.abaqusSection)
            list_layertypes.append(str(tuple_layertype))
        str_layertypes = ','.join(list_layertypes)
        self.form.layertypeKw.setValues(str_layertypes)

    def save(self, sender, sel, ptr):


        self.refresh(sender, sel, ptr)
        pass

    # def showEditor(self, sender, sel, ptr):
    #     if SELID(sel) == self.ID_CREATE:

    def processUpdates(self):
        if self.table_layertypes.getNumRows() > 1 and self.table_layertypes.isAnyItemInColumnSelected(0):
            row = self.table_layertypes.getCurrentRow()
            self.select_name = self.table_layertypes.getItemText(row, 0)
            self.button_edit.setTarget(
                ScLayerTypeEditorForm(
                    self.owner, editMode='edit', layerTypeName=self.select_name
                )
            )

    def showInfo(self, sender, sel, ptr):
        mainWindow = getAFXApp().getAFXMainWindow()
        message = 'Layer Type Name: ' + self.select_name
        showAFXInformationDialog(mainWindow, message)

