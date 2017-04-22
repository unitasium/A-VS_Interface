# -*- coding: utf-8 -*-

# from abaqus import *
# from abaqusConstants import *
import math

info  = 1
debug = 0


def writeFormat(file, format, content, delimiter=''):
    # delimiter = '' space, default
    #           = ','

    str_fmt = ''
    for i, t in enumerate(format):
        if t == 'd':
            str_fmt += '{0[' + str(i) + ']:10d}'
        elif t == 'e' or t == 'E':
            str_fmt += '{0[' + str(i) + ']:16.6' + t + '}'
        if delimiter != '':
            str_fmt += delimiter
    if delimiter != '':
        str_fmt = str_fmt.rstrip(delimiter)
    str_fmt += '\n'
    #print str_fmt
    file.write(str_fmt.format(content))
    return


def strFormat(format):
#formata='ddEEEEEEEEE'    
    strFormat = ''
    for i, t in enumerate(format):
        if t == 'd' or t == 'D':
            strFormat += '{0[' + str(i) + ']:10d}'
            
#==============================================================================
#         if t == 's' or t == 'S':
#             strFormat += '{0[' + str(i) + ']:10s}'
#==============================================================================
        elif t == 'e' or t == 'E':
            strFormat += '{0[' + str(i) + ']:16.6' + t + '}'
        elif t == 'f' or t == 'F':
            strFormat += '{0[' + str(i) + ']:16.6' + t + '}'
    strFormat += '\n'
    
#strinfo_fmt
#g=[1220,4,1442,1443,272,273,0, 0,0 ,0,0]
#print strinfo_fmt.format(g)

    return strFormat


def eleFormat(format1, format2):
    #formata='ddEEEEEEEEE'    
    eleFormat = ''
    for i, t in enumerate(format1):
        if (t == 'd' or t == 'D'):
            eleFormat += '{0[' + str(i) + ']:10d}'

    for i, t in enumerate(format2):
        if (t == 'd' or t == 'D'):
            eleFormat += '{0[2][' + str(i) + ']:10d}'
            
        elif t == 'e' or t == 'E':
            eleFormat += '{0[2][' + str(i) + ']::16.6' + t + '}'
        elif t == 'f' or t == 'F':
            strFormat += '{0[' + str(i) + ']:16.6' + t + '}'
    eleFormat += '\n'

    return eleFormat

