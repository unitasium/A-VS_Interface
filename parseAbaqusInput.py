import sys
import numpy as np
import inpParser

def parseAbaqusInput(abq_inp_name):
    # fn = r'airfoil_automation\test_1102.inp'
    # drt = r'D:\Study\Graduate\Abaqus\A-VS_Interface\airfoil_automation'
    inp = inpParser.InputFile(abq_inp_name)
    kws_obj = inp.parse(usePyArray=True)

    elsets = []
    distributions = []
    orientations = []
    solidsections = []
    materials = []
    densities = []
    elastics = []
    for kw in kws_obj:
        print kw.name
        if kw.name == 'parameter':
            print kw.parameter
            nsg = kw.parameter['sgdim']
        elif kw.name == 'node':
            n_coord = kw.data
        elif kw.name == 'element':
            if kw.data.shape[1] == 4:
                e_connt_2d3 = kw.data
            elif kw.data.shape[1] == 5:
                e_connt_2d4 = kw.data
        elif kw.name == 'elset':
            elsets.append(kw)
        elif kw.name == 'distribution':
            distributions.append(kw)
        elif kw.name == 'orientation':
            orientations.append(kw)
        elif kw.name == 'solidsection':
            solidsections.append(kw)
        elif kw.name == 'material':
            materials.append(kw)
        elif kw.name == 'density':
            densities.append(kw)
        elif kw.name == 'elastic':
            elastics.append(kw)

    return nsg, n_coord
    # print e_connt_2d3.shape
    # print e_connt_2d4.shape

# abq_inp = r'test\weave2Dre2A.inp'
# parseAbaqusInput(abq_inp)
