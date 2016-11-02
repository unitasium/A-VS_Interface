# from abaqus import *
from math import *
from datetime import *
from subprocess import call
from utilities import *
from readAbaqusInput import *
import os.path
import codecs
import time
import sys


def VABSMain(recover_flag, gen_inp_only, vabs_inp_name='', abq_inp_name='',
             timoshenko_flag='', thermal_flag='', trapeze_flag='',
             vlasov_flag='', curve_flag='', k='', oblique_flag='', cos='',
             model_recover='', vabs_rec_name='', vabs_inp_name2='',
             u='', c='', sf='', sm='', df='', dm='',
             gamma='', kappa='', kappa_p=''):
    
    # st = datetime.now()
    # print st.strftime("%m-%d-%Y %H:%M:%S")

    if recover_flag == 1:
        vabs_input = getVABSInput(
            vabs_inp_name, abq_inp_name, timoshenko_flag, thermal_flag,
            trapeze_flag, vlasov_flag, curve_flag, k, oblique_flag, cos
        )
    # elif recover_flag == 2:

    if not gen_inp_only:
        try:
            vabsTimeStart = time.clock()
            os.system('VABS ' + vabs_input)
            vabsTimeEnd = time.clock()
            vabsTime = vabsTimeEnd - vabsTimeStart
            print 'VABS TIME: ' + str(vabsTime)
        except:
            raise WindowsError(
                'Unexpected error happened. Please check the Command line window for more information.'
            )

    return 1


def getVABSInput(vabs_inp_name, abq_inp_name, timoshenko_flag, thermal_flag,
                 trapeze_flag, vlasov_flag, curve_flag, ik, oblique_flag, cos):

    if vabs_inp_name == '':
        out_file_name = abq_inp_name[:-4] + r'_vabs.dat'
    else:
        if not '.dat' in vabs_inp_name:
            vabs_inp_name = vabs_inp_name + '.dat'
        dr = os.path.dirname(abq_inp_name)
        out_file_name = os.path.join(dr, vabs_inp_name)

    if timoshenko_flag:
        timoshenko_flag = 1
    else:
        timoshenko_flag = 0

    if thermal_flag:
        thermal_flag = 3
    else:
        thermal_flag = 0

    if trapeze_flag:
        trapeze_flag = 1
    else:
        trapeze_flag = 0

    if vlasov_flag:
        vlasov_flag = 1
    else:
        vlasov_flag = 0

    if curve_flag:
        curve_flag = 1
    else:
        curve_flag = 0

    if oblique_flag:
        oblique_flag = 1
    else:
        oblique_flag = 0

    n_coord, e_connt, e_set, section, orientation, material = readAbaqusInput(abq_inp)
    
    material_type = {'ISOTROPIC': 0, 'ENGINEERING CONSTANTS': 1,
                     'ORTHOTROPIC': 2, 'ANISOTROPIC': 2}

    nnode = len(n_coord.keys())
    nelem = len(e_connt.keys())
    nmate = len(material.keys())

    

    e_list = []
    distr_list = {}
    # {eid: [a, b, c], ...}
    layer_type = {}
    # {lyt_id: [material_name, theta3], ...}
    eid_maid = {}
    # {eid: lyt_id}

    layer = 0
    for sect in section:
        set = sect['elset']
        mtr = sect['material']
        ori = sect['orientation']
        elem = e_set[set]
        # print set
        # print elem[:10]
        theta3 = orientation[ori]['data'][4]
        ma = [mtr, theta3]
        if not ma in layer_type.values():
            layer += 1
            layer_type[layer] = ma
        nindex_b = orientation[ori]['data'][2] - 1
        nindex_c = orientation[ori]['data'][0] - 1
        for e in elem:
            ns = e_connt[e]
            a = [1.0, 0.0, 0.0]
            b = [0.0, 
                 n_coord[ns[nindex_b]][0] - n_coord[ns[nindex_c]][0], 
                 n_coord[ns[nindex_b]][1] - n_coord[ns[nindex_c]][1]]
            c = [0.0, 0.0, 0.0]
            distr_list[e] = a + b + c
            eid_maid[e] = layer

    # print distr_list[1]
    # print layer_type
    nlayer = len(layer_type.keys())

    for k, v in material.items():
        ep = v['elastic']
        tp = ep[0]
        if tp == 'TRACTION':
            e1 = ep[1]
            e2 = e1 / 100.0
            e3 = e1 / 100.0
            nu = 0.3
            g12 = ep[2]
            g13 = g12
            g23 = e2 / (2 * (1 + nu))
            material[k]['elastic'] = [
                'ENGINEERING CONSTANTS', 
                e1, e2, e3, g12, g13, g23, nu, nu, nu]
    # print material['NEXUS_3']

    # n_debug = n_coord
    # for k, v in e_connt.items():
    #     for n in v:
    #         if n in n_debug.keys():
    #             del n_debug[n]

    # print n_debug
            

    # milestone('Writing VABS inputs...')
    with codecs.open(out_file_name, encoding='utf-8', mode='w') as fout:
        nlayer = len(layer_type)

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

        # nnode  nelem  nmate
        writeFormat(fout, 'ddd', [nnode, nelem, nmate])
        fout.write('\n')

        for k, v in n_coord.items():
            n = [k] + v[:2]
            writeFormat(fout, 'dEE', n)
        fout.write('\n')

        for k, v in e_connt.items():
            if len(v) == 3:
                v = v + [0]*6
            elif len(v) == 4:
                v = v + [0]*5
            elif len(v) == 6:
                v = v[:3] + [0] + v[3:] + [0]*2
            elif len(v) == 8:
                v = v + [0]
            e = [k] + v
            writeFormat(fout, 'd'*10, e)
        fout.write('\n')

        for e in e_list:
            ma = eid_maid[e]
            writeFormat(fout, 'ddE', [e, ma, 0.0])
        for e, abc in distr_list.items():
            lyt_id = eid_maid[e]
            t1 = degrees(atan2(abc[5], abc[4]))  # b3, b2
            if t1 < 0:
                t1 += 360.0
            if t1 == 360.0:
                t1 = 0.0
            writeFormat(fout, 'ddE', [e, lyt_id, t1])
        fout.write('\n')

        if nlayer != 0:
            for k, v in layer_type.items():
                mn = v[0]
                mid = material[mn]['id']
                v[0] = mid
                writeFormat(fout, 'ddE', [k] + v)
            fout.write('\n')

        if nmate != 0:
            for i in material.values():
                # material_id  isotropy
                ep = i['elastic']
                t = material_type[ep[0]]
                writeFormat(fout, 'dd', [i['id'], t])
                if t == 0:  # isotropic
                    writeFormat(fout, 'EE', ep[1:3])
                elif t == 1:  # engineering constants
                    writeFormat(fout, 'EEE', ep[1:4])
                    writeFormat(fout, 'EEE', ep[7:10])
                    writeFormat(fout, 'EEE', ep[4:7])
                elif t == 2:
                    if len(i) == 12:   # orthotropic
                        c1111 = i[3]
                        c1122 = i[4]
                        c2222 = i[5]
                        c1133 = i[6]
                        c2233 = i[7]
                        c3333 = i[8]
                        c1212 = i[9]
                        c1313 = i[10]
                        c2323 = i[11]
                        writeFormat(fout, 'E'*6,
                                    [c1111,     0,     0, c1122,     0, c1133])
                        writeFormat(fout, 'E'*5,
                                    [       c1212,     0,     0,     0,     0])
                        writeFormat(fout, 'E'*4,
                                    [              c1313,     0,     0,     0])
                        writeFormat(fout, 'E'*3,
                                    [                     c2222,     0, c2233])
                        writeFormat(fout, 'E'*2,
                                    [                            c2323,     0])
                        writeFormat(fout, 'E'*1,
                                    [                                   c3333])
                    elif len(i) == 24:  # anisotropic
                        c1111, c1122, c2222 = i[3], i[4], i[5]
                        c1133, c2233, c3333 = i[6], i[7], i[8]
                        c1112, c2212, c3312 = i[9], i[10], i[11]
                        c1212, c1113, c2213 = i[12], i[13], i[14]
                        c3313, c1213, c1313 = i[15], i[16], i[17]
                        c1123, c2223, c3323 = i[18], i[19], i[20]
                        c1223, c1323, c2323 = i[21], i[22], i[23]
                        writeFormat(fout, 'E'*6,
                                    [c1111, c1112, c1113, c1122, c1123, c1133])
                        writeFormat(fout, 'E'*5,
                                    [       c1212, c1213, c2212, c1223, c3312])
                        writeFormat(fout, 'E'*4,
                                    [              c1313, c2213, c1323, c3313])
                        writeFormat(fout, 'E'*3,
                                    [                     c2222, c2223, c2233])
                        writeFormat(fout, 'E'*2,
                                    [                            c2323, c3323])
                        writeFormat(fout, 'E'*1,
                                    [                                   c3333])
                writeFormat(fout, 'E', [i['density']])
                fout.write('\n')
            fout.write('\n')

    vabs_input = os.path.basename(out_file_name)

    return vabs_input


# abq_inp = r'E:\SHARE\CATIA-VABS_Demo\Assembly_43500.inp'
abq_inp = sys.argv[1]
st = datetime.now()
print st.strftime("%m-%d-%Y %H:%M:%S")
VABSMain(
    recover_flag=1, gen_inp_only=0, vabs_inp_name='', 
    abq_inp_name=abq_inp, timoshenko_flag=True, thermal_flag=False, 
    trapeze_flag=False, vlasov_flag=False, curve_flag=False, k='', 
    oblique_flag=False, cos='', model_recover='', vabs_rec_name='', 
    vabs_inp_name2='', u='', c='', sf='', sm='', df='', dm='',
    gamma='', kappa='', kappa_p='')
st = datetime.now()
print st.strftime("%m-%d-%Y %H:%M:%S")

