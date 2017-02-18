from abaqus import *
from parseAbaqusInput import *
from reorgAbaqusInput import *
from writeVABSInput import *
import os

def createVABSInputMain(
    abq_inp, new_filename,
    timoshenko_flag, thermal_flag, trapeze_flag, vlasov_flag,
    curve_flag, ik, oblique_flag, cos
):

    if new_filename == '':
        vabs_inp = abq_inp[:-4] + r'_vabs.dat'
    else:
        dir = os.path.dirname(abq_inp)
        new_filename = new_filename + '.dat'
        vabs_inp = os.path.join(dir, new_filename)

    # ========== Parse data from Abaqus input ==========
    milestone('Parsing data from Abaqus input...')
    results = parseAbaqusInput(abq_inp)
    # nsg = results['nsg']
    nsg = 2
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

    # ========== Reorganize data for VABS input ==========
    milestone('Reorganizing data for VABS input...')
    results = reorgAbaqusInput(
        nsg, nodes, elements2d, elements3d, elsets,
        sections, distributions, orientations,
        materials, densities, elastics
    )
    n_coord = results['nodes']
    eid_all = results['all elements ids']
    eid_lid = results['element to layer type']
    e_connt_2d = results['elements 2d']
    # e_connt_3d = results['elements 3d']
    distr_all = results['distributions']
    layer_types = results['layer types']
    materials = results['materials']

    # ========== Write VABS input ==========
    milestone('Writing VABS input...')
    writeVABSInput(
        vabs_inp,
        nsg, n_coord, eid_all, eid_lid, e_connt_2d,
        distr_all, layer_types, materials,
        timoshenko_flag, thermal_flag, trapeze_flag, vlasov_flag,
        curve_flag, ik, oblique_flag, cos
    )

    # vabs_inp = os.path.basename(vabs_inp)
    return vabs_inp

