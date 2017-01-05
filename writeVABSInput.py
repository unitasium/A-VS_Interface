import codecs
import math
import numpy as np
from utilities import *
# from parseAbaqusInput import *

def writeVABSInput(
    vabs_inp,
    nsg, n_coord, eid_all, eid_lid, e_connt_2d,
    distr_all, layer_types, materials,
    timoshenko_flag=0, thermal_flag=0, trapeze_flag=0, vlasov_flag=0,
    curve_flag=0, ik=[], oblique_flag=0, cos=[]
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
    #     [eid1, mid1/lid1, nid11, nid12, nid13, ...],
    #     [eid2, mid2/lid2, nid21, nid22, nid23, ...],
    #     ...
    # ]
    # ---------------------------------
    # distr_all = [
    #     [eid1, a11, a12, a13, b11, b12, b13, c11, c12, c13],
    #     [eid2, a21, a22, a23, b21, b22, b23, c21, c22, c23],
    #     ...
    # ]
    # ---------------------------------
    # layer_type = [
    #     [lid1, mid1, fiber_orient1],
    #     [lid2, mid2, fiber_orient2],
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

    with codecs.open(vabs_inp, encoding='utf-8', mode='w') as fout:
        nnode = len(n_coord)
        nelem = len(e_connt_2d)
        nmate = len(materials.keys())
        nlayer = len(layer_types)

        # ----- Write header -----------------------------------------
        # format_flag  nlayer
        writeFormat(fout, 'dd', [1, nlayer])
        fout.write('\n')

        # timoshenko_flag  recover_flag  thermal_flag
        writeFormat(fout, 'ddd',
                    [timoshenko_flag, 0, thermal_flag])
        fout.write('\n')

        # curve_flag  oblique_flag  trapeze_flag  vlasov_flag
        writeFormat(fout, 'd'*4,
                    [curve_flag, oblique_flag, trapeze_flag, vlasov_flag])
        fout.write('\n')

        if curve_flag == 1:
            writeFormat(fout, 'EEE', ik[0])
            fout.write('\n')

        if oblique_flag == 1 and timoshenko_flag == 0:
            writeFormat(fout, 'EE', cos[0])
            fout.write('\n')

        writeFormat(fout, 'ddd', [nnode, nelem, nmate])
        fout.write('\n')

        # ----- Write nodal coordinates ------------------------------
        for n in n_coord:
            # print n[[0, 2, 3]]
            writeFormat(fout, 'dEE', n[[0, 2, 3]])
        fout.write('\n')

        # ----- Write element connectivities -------------------------
        # eid_lid = {eid1: lid1, eid2: lid2, ...}
        for e in e_connt_2d:
            writeFormat(fout, 'd'*10, e)
        fout.write('\n')

        # ----- Write local coordinates ------------------------------
        for distr in distr_all:
            eid = int(distr[0])
            lid = eid_lid[eid]
            eid_all.remove(eid)
            t1 = math.degrees(math.atan2(distr[6], distr[5]))
            if t1 < 0:
                t1 += 360.0
            if t1 == 360.0:
                t1 = 0.0
            writeFormat(fout, 'ddE', [eid, lid, t1])
        if len(eid_all) > 0:
            for eid in eid_all:
                lid = eid_lid[eid]
                writeFormat(fout, 'ddE', [eid, lid, 0.0])
        fout.write('\n')

        # ----- Write layer types ------------------------------------
        for lyt in layer_types:
            # print lyt
            writeFormat(fout, 'ddE', lyt)
        fout.write('\n')

        # ----- Write materials --------------------------------------
        for mid, prop in materials.items():
            writeFormat(fout, 'dd', [mid, prop['isotropy']])
            if prop['isotropy'] == 0:
                writeFormat(fout, 'EE', prop['elastic'][0][2:])
            elif prop['isotropy'] == 1:
                writeFormat(fout, 'EEE', prop['elastic'][0][2:5])
                writeFormat(fout, 'EEE', prop['elastic'][0][5:8])
                writeFormat(fout, 'EEE', prop['elastic'][0][8:11])
            elif prop['isotropy'] == 2:
                writeFormat(fout, 'E'*6, prop['elastic'][0][2:8])
                writeFormat(fout, 'E'*5, prop['elastic'][0][8:13])
                writeFormat(fout, 'E'*4, prop['elastic'][0][13:17])
                writeFormat(fout, 'E'*3, prop['elastic'][0][17:20])
                writeFormat(fout, 'E'*2, prop['elastic'][0][20:22])
                writeFormat(fout, 'E'*1, prop['elastic'][0][22:23])
            writeFormat(fout, 'E', [prop['elastic'][0][1]])
            fout.write('\n')
        fout.write('\n')

