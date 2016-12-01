from parseAbaqusInput import *
from reorgSCInput import *
from writeSCInput import *

abq_inp = r'airfoil_automation\test_1102.inp'
# abq_inp = r'test\weave2Dre2A.inp'
sc_inp = abq_inp[:-4] + r'.sc'

# ========== Parse data from Abaqus input ==========
results = parseAbaqusInput(abq_inp)
nsg = results['nsg']
nodes = results['nodes']
elements2d = results['elements 2d']
elements3d = results['elements 3d']
elsets = results['element sets']
materials = results['materials']
densities = results['densities']
elastics = results['elastics']
mtr_name2id = results['material name to id']

# ========== Reorganize data for SwiftComp input ==========
results = reorgSCInput(
    nsg,
    nodes, elements2d, elements3d, elsets,
    materials, densities, elastics, mtr_name2id
)
n_coord = results['nodes']
# e_connt = results['elements']
materials = results['materials']

# ========== Write SwiftComp input ==========
writeSCInput(
    sc_inp, nsg, n_coord,
    materials
    )