from parseAbaqusInput import *
from reorgSCInput import *
from writeSCInput import *
import os

def createSCInputMain(
    abq_inp, new_filename,
    macro_model, specific_model,
    analysis, elem_flag, trans_flag, temp_flag,
    bk, sk, cos, w
):

    if new_filename == '':
        sc_inp = abq_inp[:-4] + r'.sc'
    else:
        dir = os.path.dirname(abq_inp)
        new_filename = new_filename + '.sc'
        sc_inp = os.path.join(dir, new_filename)

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
        nsg, nodes, elements2d, elements3d, elsets,
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
        sc_inp,
        nsg, n_coord, eid_all, eid_lid, e_connt_2d, e_connt_3d,
        distr_all, layer_types, materials,
        macro_model, specific_model,
        analysis, elem_flag, trans_flag, temp_flag,
        bk, sk, cos, w
        )

    # sc_inp = os.path.basename(sc_inp)
    macro_model = str(macro_model) + 'D'
    return [sc_inp, macro_model]

# abq_inp = r'airfoil_automation\test_1102.inp'
# # abq_inp = r'test\weave2Dre2A.inp'
# # sc_inp = abq_inp[:-4] + r'.sc'
# new_filename = ''
# macro_model = 1
# specific_model = 0
# analysis = 0
# elem_flag = 0
# trans_flag = 1
# temp_flag = 0
# bk = [[0.0, 0.0, 0.0]]
# sk = [[0.0, 0.0]]
# cos = [[1.0, 0.0]]
# w = 1.0

# createSCInputMain(
#     abq_inp, new_filename,
#     macro_model, specific_model,
#     analysis, elem_flag, trans_flag, temp_flag,
#     bk[0], sk[0], cos[0], w
# )
