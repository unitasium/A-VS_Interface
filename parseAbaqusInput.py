import sys
import numpy as np
import inpParser

def parseAbaqusInput(abq_inp_name):
    # fn = r'airfoil_automation\test_1102.inp'
    # drt = r'D:\Study\Graduate\Abaqus\A-VS_Interface\airfoil_automation'
    inp = inpParser.InputFile(abq_inp_name)
    # print inp
    kws_obj = inp.parse(usePyArray=True)
    # kws_obj = inp.parse(usePyArray=False)

    # print kws_obj
    # print kw_obj[0]
    n = 0
    for kw in kws_obj:
        if kw.name == 'node':
            # print kw.data.shape
            # print kw.data[0:5]
            n_coord = kw.data
        elif kw.name == 'element':
            # print kw.parameter
            # print kw.data.shape
            # print type(kw.data.shape[1])
            # print kw.suboptions
            if kw.data.shape[1] == 4:
                e_connt_2d3 = kw.data
            elif kw.data.shape[1] == 5:
                e_connt_2d4 = kw.data
        elif kw.name == 'elset':
            n += 1
            print '---Elset', n, '---'
            print kw.parameter
            print type(kw.data)
            print kw.suboptions

    # print e_connt_2d3.shape
    # print e_connt_2d4.shape

abq_inp = r'airfoil_automation\test_1102.inp'
parseAbaqusInput(abq_inp)