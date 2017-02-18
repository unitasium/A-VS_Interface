from abaqus import *
from math import *
from datetime import *
from subprocess import call
from utilities import *
from createVABSInputMain import *
import os.path
import shutil
import codecs
import time


def VABSMain(
    recover_flag, gen_inp_only, vabs_inp_name='', abq_inp_name='',
    timoshenko_flag='', thermal_flag='', trapeze_flag='',
    vlasov_flag='', curve_flag='', k='', oblique_flag='', cos='',
    model_recover='', vabs_rec_name='', vabs_inp_name2='',
    u='', c='', sf='', sm='', df='', dm='',
    gamma='', kappa='', kappa_p=''
):
    
    st = datetime.now()
    print st.strftime("%m-%d-%Y %H:%M:%S")

    if recover_flag == 1:
        # vabs_input = getVABSInput(
        #     vabs_inp_name, abq_inp_name, timoshenko_flag, thermal_flag,
        #     trapeze_flag, vlasov_flag, curve_flag, k, oblique_flag, cos
        # )
        vabs_input = createVABSInputMain(
            abq_inp_name, vabs_inp_name,
            timoshenko_flag, thermal_flag, trapeze_flag, vlasov_flag,
            curve_flag, k, oblique_flag, cos
        )
    elif recover_flag == 2:
        vabs_input = getRecoverInput(
            vabs_rec_name, vabs_inp_name2, model_recover,
            u, c, sf, sm, df, dm, gamma, kappa, kappa_p
        )

    print vabs_input

    if not gen_inp_only:
        try:
            print 'Running VABS...'
            vabsTimeStart = time.clock()
            os.system('VABSIII ' + vabs_input)
            vabsTimeEnd = time.clock()
            vabsTime = vabsTimeEnd - vabsTimeStart
            print 'VABS TIME: ' + str(vabsTime)
        except:
            raise WindowsError(
                'Unexpected error happened. Please check the Command line window for more information.'
            )

    return 1


def getRecoverInput(
    vabs_rec_name, vabs_inp_name2, model_recover,
    u, c, sf, sm, df, dm, gamma, kappa, kappa_p
    ):

    dr = os.path.dirname(vabs_inp_name2)

    fn_ech = vabs_inp_name2 + '.ech'
    fn_k   = vabs_inp_name2 + '.K'
    fn_opt = vabs_inp_name2 + '.opt'
    fn_v0  = vabs_inp_name2 + '.v0'
    fn_v1s = vabs_inp_name2 + '.v1S'
    fn_v22 = vabs_inp_name2 + '.v22'


    fn_inp_rec = os.path.join(dr, vabs_rec_name + '.dat')
    # shutil.copyfile(vabs_inp_name2, fn_inp_rec)
    shutil.copyfile(fn_ech, fn_inp_rec + '.ech')
    shutil.copyfile(fn_k, fn_inp_rec + '.K')
    shutil.copyfile(fn_opt, fn_inp_rec + '.opt')
    shutil.copyfile(fn_v0, fn_inp_rec + '.v0')
    if model_recover == 2:
        shutil.copyfile(fn_v1s, fn_inp_rec + '.v1S')
        shutil.copyfile(fn_v22, fn_inp_rec + '.v22')

    
    with open(fn_inp_rec, 'w') as fout:
        with open(vabs_inp_name2, 'r') as fin:
            before_change = True
            for line in fin:
                if before_change:
                    flags = line.split()
                    if len(flags) == 3:
                        flags = [int(flags[0]), 1, int(flags[2])]
                        writeFormat(fout, 'ddd', flags)
                        before_change = False
                        continue
                fout.write(line)

        writeFormat(fout, 'EEE', u[0])
        fout.write('\n')
        writeFormat(fout, 'EEE', c[0])
        writeFormat(fout, 'EEE', c[1])
        writeFormat(fout, 'EEE', c[2])
        fout.write('\n')
        if model_recover == 3:
            # Vlasov model
            writeFormat(fout, 'E'*7, gamma[0]+kappa[0]+kappa_p[0])
            fout.write('\n')
        else:
            writeFormat(fout, 'E'*4, [sf[0][0],]+list(sm[0]))
            if model_recover == 2:
                # Timoshenko model
                writeFormat(fout, 'EE', sf[0][1:])
                writeFormat(fout, 'E'*6, df[0]+dm[0])
                writeFormat(fout, 'E'*6, df[1]+dm[1])
                writeFormat(fout, 'E'*6, df[2]+dm[2])
                writeFormat(fout, 'E'*6, df[3]+dm[3])
        fout.write('\n')

    return fn_inp_rec

