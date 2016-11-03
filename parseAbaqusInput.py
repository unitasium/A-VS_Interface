import sys
import numpy
import inpParser

def parseAbaqusInput(abq_inp_name):
    # fn = r'airfoil_automation\test_1102.inp'
    # drt = r'D:\Study\Graduate\Abaqus\A-VS_Interface\airfoil_automation'
    inp = inpParser.InputFile(abq_inp_name)
    # print inp
    kws_obj = inp.parse(usePyArray=True)

    # print kws_obj
    # print kw_obj[0]
    
    for kw in kws_obj:
        if kw.name == 'node':
            # print kw.parameter
            print kw.data[0]
            print kw.data.shape

abq_inp = r'airfoil_automation\test_1102.inp'
parseAbaqusInput(abq_inp)