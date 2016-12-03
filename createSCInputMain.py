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
sections = results['sections']
distributions = results['distribution']
orientations = results['orientation']
materials = results['materials']
densities = results['densities']
elastics = results['elastics']

# ========== Reorganize data for SwiftComp input ==========
results = reorgSCInput(
    nsg,
    nodes, elements2d, elements3d, elsets,
    sections, distributions, orientations,
    materials, densities, elastics
)
n_coord = results['nodes']
eid_all = results['all elements ids']
eid_lid = results['element to layer type']
e_connt_2d = results['elements 2d']
e_connt_3d = results['elements 3d']
distr_all = results['distributions']
layer_types = results['layer types']
materials = results['materials']

# ========== Write SwiftComp input ==========
writeSCInput(
    sc_inp, nsg, n_coord,
    eid_all, eid_lid, e_connt_2d, e_connt_3d,
    distr_all,
    layer_types,
    materials
    )