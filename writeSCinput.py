import codecs
from utilities import *
from parseAbaqusInput import *

# abq_inp = r'airfoil_automation\test_1102.inp'
abq_inp = r'test.inp'
sc_inp = abq_inp[:-4] + r'.sc'
# n_coord = parseAbaqusInput(abq_inp)
parameter = parseAbaqusInput(abq_inp)
print parameter

# with codecs.open(sc_inp, encoding='utf-8', mode='w') as fout:
#     nnode = len(n_coord)
#     for n in n_coord:
#         writeFormat(fout, 'dEEE', n[:4])
#     fout.write('\n')