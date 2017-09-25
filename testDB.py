from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class TestDB(AFXDataDialog):

    [
        ID_REFRESH,
        ID_SAVE,
        ID_LAST
    ] = range(AFXToolsetGui.ID_LAST, AFXToolsetGui.ID_LAST+3)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        self.form = form

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Title',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        
        self.appendActionButton('Refresh', self, self.ID_REFRESH)
        self.appendActionButton('Save', self, self.ID_SAVE)

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')

        # ============================================================

        FXMAPFUNC(self, SEL_COMMAND, self.ID_REFRESH, TestDB.refresh)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_SAVE, TestDB.save)

        # ============================================================
            
        vf = FXVerticalFrame(self, FRAME_SUNKEN|FRAME_THICK|LAYOUT_FILL_X,
            0,0,0,0, 0,0,0,0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table = AFXTable(
            vf, 6, 4, 6, 4, form.layertypeKw, 0, 
            AFXTABLE_COLUMN_RESIZABLE|AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        table.setLeadingRows(1)
        # table.setLeadingColumns(1)
        table.setColumnWidth(-1, 100)
        # table.setColumnEditable(0, False)
        table.setColumnType(0, AFXTable.TEXT)  # LayerType name
        table.setColumnType(1, AFXTable.TEXT)  # LayerType material
        table.setColumnType(2, AFXTable.FLOAT)  # LayerType angle
        table.setColumnType(3, AFXTable.TEXT)  # LayerType abq_section
        table.setLeadingRowLabels('Name\tMaterial\tAngle\tSection')
        table.setStretchableColumn( table.getNumColumns()-1 )
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)
        
        layertypes = mdb.customData.layerTypes
        list_layertypes = []
        for lt in layertypes.values():
            tuple_layertype = (lt.name, lt.material, lt.angle, lt.abq_section)
            list_layertypes.append(str(tuple_layertype))
        str_layertypes = ','.join(list_layertypes)
        self.form.layertypeKw.setValues(str_layertypes)

    def refresh(self, sender, sel, ptr):

        layertypes = mdb.customData.layerTypes
        list_layertypes = []
        for lt in layertypes.values():
            tuple_layertype = (lt.name, lt.material, lt.angle, lt.abq_section)
            list_layertypes.append(str(tuple_layertype))
        str_layertypes = ','.join(list_layertypes)
        self.form.layertypeKw.setValues(str_layertypes)

    def save(self, sender, sel, ptr):


        self.refresh(sender, sel, ptr)
        pass
