def readAbaqusInput(abq_inp_name):

    keywords = ['*NODE', '*ELEMENT', '*ELSET', '*ORIENTATION',
                '*DISTRIBUTION', '*SOLID SECTION',
                '*SHELL SECTION', '*MATERIAL', '*DENSITY', '*ELASTIC']

    n_coord = {}
    # {id: [x, y(, z)], ...}
    e_connt = {}
    # {id: [n1, n2, ...], ...}
    e_set   = {}
    # {'name', [e1, e2, ...], ...}
    section = []
    # [{'elset': 'name', 'material': 'name', 'orientation': 'name'}, ...]
    orientation = {}
    # {'name': {'definition': CONSTANT, 'system': CONSTANT(, 'data': [])}, ...}
    material = {}
    # {'name': {'density': 1.0, 'elastic': []}, ...}

    nnode = 0
    nelem = 0

    with open(abq_inp_name, 'r') as fin:
        key = ''
        name = ''
        argument = ''

        for line in fin:
            line = line.strip().split(',')
            kw = line[0].strip().upper()
            if kw.startswith('**'):
                continue
            elif kw.startswith('*') and kw not in keywords:
                key = ''
                continue
            elif kw.startswith('*NODE'):
                key = 'node'
                continue
            elif kw.startswith('*ELEMENT'):
                key = 'element'
                continue
            elif kw.startswith('*ELSET'):
                key = 'eset'
                argument = 'list'
                for i, arg in enumerate(line):
                    if 'elset' in arg:
                        name = arg.split('=')[-1].strip()
                    if 'generate' in arg:
                        argument = 'generate'
                if not name in e_set.keys():
                    e_set[name] = []
                continue
            elif kw.startswith('*ORIENTATION'):
                key = ''
                definition = 'coordinates'
                system = 'rectangular'
                for i, arg in enumerate(line):
                    if 'name' in arg:
                        name = arg.split('=')[-1].strip()
                orientation[name] = {}
                for i, arg in enumerate(line):
                    if 'definition' in arg:
                        definition = arg.split('=')[-1].strip()
                    if 'system' in arg:
                        system = arg.split('=')[-1].strip()
                orientation[name]['definition'] = definition
                orientation[name]['system'] = system
                if definition.upper() == 'OFFSET TO NODE':
                    key = 'orientation'
                    orientation[name]['data'] = []
                continue
            elif kw.startswith('*SOLID SECTION'):
                key = ''
                orient = ''
                sect = {}
                for i, arg in enumerate(line):
                    if 'elset' in arg:
                        sect['elset'] = arg.split('=')[-1].strip()
                    if 'material' in arg:
                        sect['material'] = arg.split('=')[-1].strip()
                    if 'orientation' in arg:
                        orient = arg.split('=')[-1].strip()
                    sect['orientation'] = orient
                section.append(sect)
                continue
            elif kw.startswith('*MATERIAL'):
                key = ''
                name = line[1].split('=')[1].strip()
                mid = len(material.keys()) + 1
                material[name] = {'id': mid, 'density': 1.0}
                continue
            elif kw.startswith('*DENSITY'):
                key = 'density'
                continue
            elif kw.startswith('*ELASTIC'):
                key = 'elastic'
                tp = 'ISOTROPIC'
                for arg in line:
                    if 'type' in arg or 'TYPE' in arg:
                        tp = arg.split('=')[-1].strip()
                material[name]['elastic'] = [tp]
                continue


            if key == '':
                continue
            elif key == 'node':
                nid = int(line[0].strip())
                coord = []
                for c in line[1:]:
                    coord.append(float(c.strip()))
                n_coord[nid] = coord
            elif key == 'element':
                eid = int(line[0].strip())
                connt = []
                for n in line[1:]:
                    connt.append(int(n.strip()))
                e_connt[eid] = connt
            elif key == 'eset':
                if argument == 'list':
                    for e in line:
                        if e.strip() == '':
                            continue
                        else:
                            e_set[name].append(int(e.strip()))
                elif argument == 'generate':
                    start = int(line[0].strip())
                    stop  = int(line[1].strip()) + 1
                    step  = int(line[2].strip())
                    for e in range(start, stop, step):
                        e_set[name].append(e)
            elif key == 'orientation':
                if len(line) == 3:
                    for n in line:
                        orientation[name]['data'].append(int(n.strip()))
                elif len(line) == 2:
                    orientation[name]['data'].append(int(line[0].strip()))
                    orientation[name]['data'].append(float(line[1].strip()))
            elif key == 'density':
                material[name]['density'] = float(line[0].strip())
            elif key == 'elastic':
                for v in line:
                    if v.strip() != '':
                        material[name]['elastic'].append(float(v.strip()))



    return n_coord, e_connt, e_set, section, orientation, material


# abq_inp = r'C:\Users\tian50\Documents\Abaqus\Python\Abaqus_SwiftComp_GUI_0720\catia\UpperSKin-Test R26SP3.3D_Section.2.inp'
# n_coord, e_connt, e_set, section, orientation, material = readAbaqusInput(abq_inp)
# print material

