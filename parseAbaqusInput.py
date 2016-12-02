import sys
import numpy as np
import inpParser

def parseAbaqusInput(abq_inp_name):
    # fn = r'airfoil_automation\test_1102.inp'
    # drt = r'D:\Study\Graduate\Abaqus\A-VS_Interface\airfoil_automation'
    inp = inpParser.InputFile(abq_inp_name)
    kws_obj = inp.parse(usePyArray=True)

    el_2d3_type = ['S3', 'S3R']
    el_2d4_type = ['S4', 'S4R']
    el_2d6_type = []
    el_2d8_type = ['S8R',]
    el_3d4_type = []
    el_3d8_type = ['C3D8', 'C3D8R',]
    el_3d10_type = ['C3D10',]
    el_3d20_type = ['C3D20',]

    e_connt_2d3 = np.array([0]*4)
    e_connt_2d4 = np.array([0]*5)
    e_connt_2d6 = np.array([0]*7)
    e_connt_2d8 = np.array([0]*9)
    e_connt_3d4 = np.array([0]*5)
    e_connt_3d8 = np.array([0]*9)
    e_connt_3d10 = np.array([0]*11)
    e_connt_3d20 = np.array([0]*21)

    elsets_raw = []
    distributions = []
    orientations = []
    solidsections = []
    materials = []
    densities = []
    elastics = []

    mtr_name2id = {}
    lyt_name2id = {}

    mid = 0
    lid = 0
    for kw in kws_obj:
        # print kw.name
        if kw.name == 'parameter':
            # print kw.parameter
            try:
                nsg = kw.parameter['sgdim']
            except KeyError:
                nsg = 3
        elif kw.name == 'node':
            # print np.array(kw.data)[:,:4]
            # print kw.data[0]
            # n_coord = np.array(kw.data)[:,:4]
            n_coord = kw.data
            # print n_coord[0]
        elif kw.name == 'element':
            et = kw.parameter['type']
            if et in el_2d3_type:
                e_connt_2d3 = np.vstack((e_connt_2d3, kw.data))
            elif et in el_2d4_type:
                e_connt_2d4 = np.vstack((e_connt_2d4, kw.data))
            elif et in el_2d6_type:
                e_connt_2d6 = np.vstack((e_connt_2d6, kw.data))
            elif et in el_2d8_type:
                e_connt_2d8 = np.vstack((e_connt_2d8, kw.data))
            elif et in el_3d4_type:
                e_connt_3d4 = np.vstack((e_connt_3d4, kw.data))
            elif et in el_3d8_type:
                e_connt_3d8 = np.vstack((e_connt_3d8, kw.data))
            elif et in el_3d10_type:
                e_connt_3d10 = np.vstack((e_connt_3d10, kw.data))
            elif et in el_3d20_type:
                e_connt_3d20 = np.vstack((e_connt_3d20, kw.data))
        elif kw.name == 'elset':
            elsets_raw.append(kw)
        elif kw.name == 'distribution':
            distributions.append(kw)
        elif kw.name == 'orientation':
            orientations.append(kw)
        elif kw.name == 'solidsection':
            lid += 1
            lname = kw.parameter['elset']
            lyt_name2id[lname] = lid
            solidsections.append(kw)
            # elset = kw.parameter['elset']
            # solidsections[elset] = {}
            # mtr = kw.parameter['material']
            # try:
            #     ori = kw.parameter['orientation']
            # except KeyError:
            #     ori = 'none'
            #     pass
            # solidsections[elset]['material'] = mtr
            # solidsections[elset]['orientation'] = ori
        elif kw.name == 'material':
            mid += 1
            mname = kw.parameter['name']
            mtr_name2id[mname] = mid
            materials.append(kw)
        elif kw.name == 'density':
            densities.append(kw)
        elif kw.name == 'elastic':
            elastics.append(kw)

    e_connt_2d = {3:e_connt_2d3, 4:e_connt_2d4, 6:e_connt_2d6, 8:e_connt_2d8}
    e_connt_3d = {4:e_connt_3d4, 8:e_connt_3d8, 10:e_connt_3d10, 20:e_connt_3d20}

    elsets = {}
    for elset in elsets_raw:
        elset_name = elset.parameter['elset']
        # print elset
        if 'generate' in elset.parameter.keys():
            [start, stop, step] = elset.data[0]
            elsets[elset_name] = np.arange(start, stop+1, step)
        else:
            elsets[elset_name] = np.array(elset.data).ravel()

    # print elsets
    # print n_coord[0]
    return {
        'nsg': nsg,
        'nodes': n_coord,
        'elements 2d': e_connt_2d,
        'elements 3d': e_connt_3d,
        'element sets': elsets,
        'sections': solidsections,
        'distribution': distributions,
        'orientation': orientations,
        'materials': materials,
        'densities': densities,
        'elastics': elastics
        }
    
# ====================================================================
# Structures of Outputs
# -------------------------
# n_coord: array([
#              [id1 x1 y1 z1]
#              [id2 x2 y2 z2]
#              ...
#          ])
# e_connt: array([
#              [id1 n11 n12 n13 ...]
#              [id2 n21 n22 n23 ...]
#              ...
#          ])
# elsets: {'name1':array([e11, e12, e13, ...]),
#          'name2':array([e21, e22, e23, ...]),
#          ...
#         }
# 
# ====================================================================

# abq_inp = r'airfoil_automation\test_1102.inp'
# abq_inp = r'test.inp'
# parseAbaqusInput(abq_inp)
