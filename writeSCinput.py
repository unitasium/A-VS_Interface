import codecs
from utilities import *
# from parseAbaqusInput import *

def writeSCInput(
    sc_inp, nsg,
    n_coord, #e_m_connt,
    materials,
    macro_model=3, specific_model=0,
    analysis=0, elem_flag=0, trans_flag=0, temp_flag=0,
    bk=[], sk=[], cos=[], w=1
):

    # ================================================================
    # Structures of Inputs
    # ---------------------------------
    # n_coord = [
    #     [nid1, x1, y1, z1],
    #     [nid2, x2, y2, z2],
    #     ...
    # ]
    # ---------------------------------
    # e_connt = [
    #     [eid1, mid1, nid11, nid12, nid13, ...],
    #     [eid2, mid2, nid21, nid22, nid23, ...],
    #     ...
    # ]
    # ---------------------------------
    # materials = {
    #     mid1: {
    #         'isotropy': type,
    #         'ntemp': ntemp,
    #         'elastic': [
    #             [T1, density1, const11, const12, ...]
    #             [T2, density2, const21, const22, ...]
    #             ...
    #         ]
    #     }
    #     ...
    # }
    # *** Arrangement of elastic constants ***
    # *** isotropy=0: E, nu
    # *** isotropy=1: E1, E2, E3, G12, G13, G23, nu12, nu13, nu23
    # *** isotropy=2: c1111, c1122, c1133, c1123, c1113, c1112,
    #                        c2222, c2233, c2223, c2213, c2212,
    #                               c3333, c3323, c3313, c3312,
    #                                      c2323, c2313, c2312,
    #                                             c1313, c1312,
    #                                                    c1212
    # ================================================================

    with codecs.open(sc_inp, encoding='utf-8', mode='w') as fout:
        nnode = len(n_coord)
        nmate = len(materials.keys())

        # ----- Write nodal coordinates ------------------------------
        for n in n_coord:
            # print n
            # n[0] = int(n[0])
            # print n
            writeFormat(fout, 'dEE', n)
        fout.write('\n')

        # ----- Write materials --------------------------------------
        for mid, prop in materials.items():
            writeFormat(fout, 'ddd', [mid, prop['isotropy'], prop['ntemp']])
            writeFormat(fout, 'EE', prop['elastic'][:2])
            if prop['isotropy'] == 0:
                writeFormat(fout, 'EE', prop['elastic'][2:])
            elif prop['isotropy'] == 1:
                writeFormat(fout, 'EEE', prop['elastic'][2:5])
                writeFormat(fout, 'EEE', prop['elastic'][5:8])
                writeFormat(fout, 'EEE', prop['elastic'][8:11])
            elif prop['isotropy'] == 2:
                writeFormat(fout, 'E'*6, prop['elastic'][2:8])
                writeFormat(fout, 'E'*5, prop['elastic'][8:13])
                writeFormat(fout, 'E'*4, prop['elastic'][13:17])
                writeFormat(fout, 'E'*3, prop['elastic'][17:20])
                writeFormat(fout, 'E'*2, prop['elastic'][20:22])
                writeFormat(fout, 'E'*1, prop['elastic'][22:23])
            fout.write('\n')
        fout.write('\n')

# abq_inp = r'airfoil_automation\test_1102.inp'
# abq_inp = r'test\weave2Dre2A.inp'
# sc_inp = abq_inp[:-4] + r'.sc'
# results = parseAbaqusInput(abq_inp)
# nsg = results['nsg']
# n_coord = results['nodes']
# e_connt_2d = results['elements 2d']
# e_connt_3d = results['elements 3d']
# elsets = results['element sets']
# materials = results['materials']
# densities = results['densities']
# elastics = results['elastics']
# mtr_name2id = results['material name to id']
# print elsets



# writeSCInput(
#     sc_inp, nsg, n_coord,
#     materials, densities, elastics, mtr_name2id
#     )