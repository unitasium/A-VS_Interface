import codecs
from utilities import *
from parseAbaqusInput import *

def writeSCInput(
    sc_inp, nsg,
    n_coord, #e_m_connt, 
    # 
    macro_model=3, specific_model=0,
    analysis=0, elem_flag=0, trans_flag=0, temp_flag=0,
    bk=[], sk=[], cos=[], w=1
):

    with codecs.open(sc_inp, encoding='utf-8', mode='w') as fout:
        nnode = len(n_coord)
        for n in n_coord:
            writeFormat(fout, 'dEEE', n[:4])
        fout.write('\n')


abq_inp = r'airfoil_automation\test_1102.inp'
# abq_inp = r'test\weave2Dre2A.inp'
sc_inp = abq_inp[:-4] + r'.sc'
nsg, n_coord = parseAbaqusInput(abq_inp)
writeSCInput(sc_inp, nsg, n_coord)