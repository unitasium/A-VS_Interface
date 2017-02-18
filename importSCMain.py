# Import VABS/SwiftComp input file into Abaqus and generate a model
import utilities as utl

# Parse SC input
sc_input = r'C:\Users\tian50\Documents\Graduate\A-VS_Interface\Tests\Import_VS\test1.sc'
abaqus_input = r'C:\Users\tian50\Documents\Graduate\A-VS_Interface\Tests\Import_VS\test1.inp'
part_name = 'test1'
macro_dim = 3

with open(sc_input, 'r') as fin:
    all_lines = fin.readlines()

all_lines = [l for l in all_lines if l != '\n']
# print all_lines[:10]
ln = 0  # Line number
# Parse head
if macro_dim == 1:
    pass
elif macro_dim == 2:
    pass
elif macro_dim == 3:
    head = all_lines[:2]
    h1 = head[0].split()
    h2 = head[1].split()
    analysis = int(h1[0])
    elem_flag = int(h1[1])
    trans_flag = int(h1[2])
    temp_flag = int(h1[3])
    nsg = int(h2[0])
    nnode = int(h2[1])
    nelem = int(h2[2])
    nmate = int(h2[3])
    nslave = int(h2[4])
    nlayer = int(h2[5])
    ln = 2

# Parse nodes
node_coord = []  # Nodal coordinates      [[n1, x1, x2, x3], ...]
if nsg == 1:
    pass
elif nsg == 2:
    pass
elif nsg == 3:
    for i in range(ln, ln + nnode):
        node = all_lines[i].split()
        node_coord.append(
            [int(node[0]), float(node[1]), float(node[2]), float(node[3])]
        )
# print node_coord[:10]
ln = ln + nnode

# Parse elements
# Element connectivities [[e1, n1, n2, n3, n4, ...], ...]
elem_connt_b31_temp=[]
elem_connt_b31 = []

elem_connt_s3 = []
elem_connt_s6 = []
elem_connt_s4 = []
elem_connt_s8 = []
elem_connt_s9 = []

elem_connt_c4  = []
elem_connt_c10 = []
elem_connt_c8  = []
elem_connt_c20 = []

sections = {}

for i in range(ln, ln + nelem):
    elem = all_lines[i].split()
    elem_id = int(elem[0])
    section_id = int(elem[1])
    if section_id not in sections.keys():
        sections[section_id] = []
    sections[section_id].append(elem_id)
    elem_dim = len(elem) - 2
    elem_connt = [int(n) for n in elem[2:] if n != '0']
    elem_connt.insert(0, elem_id)
    if elem_dim >= 5 and elem_dim < 9:
        pass
    elif elem_dim >= 9 and elem_dim < 20:
        pass
    elif elem_dim >= 20:
        if len(elem_connt) == 5:
            elem_connt_c4.append(elem_connt)
        elif len(elem_connt) == 11:
            elem_connt_c10.append(elem_connt)
        elif len(elem_connt) == 9:
            elem_connt_c8.append(elem_connt)
        elif len(elem_connt) == 21:
            elem_connt_c20.append(elem_connt)

elem_connt_c4.sort()
elem_connt_c10.sort()
elem_connt_c8.sort()
elem_connt_c20.sort()

ln = ln + nelem

# Parse orientations
if trans_flag == 1:
    ln = ln + nelem
    pass

# Parse layer types
if nlayer != 0:
    ln = ln + nlayer
    pass

# Parse materials
materials = {}
# {id: [type, density, elastic]}
# type=0: elastic=[E, nu]
# type=1: elastic=[E1, E2, E3, nu12, nu13, nu23, G12, G13, G23]
# type=2: elastic=[]
for i in range(nmate):
    mate = all_lines[ln].split()
    mate_id = int(mate[0])
    # materials[mate_id] = []
    mate_type = int(mate[1])
    mate1 = all_lines[ln+1].split()
    density = float(mate1[1])
    materials[mate_id] = [mate_type, density]
    if mate_type == 0:
        # Isotropic
        elastic = map(float, all_lines[ln+2].split())
        ln = ln + 3
    elif mate_type == 1:
        # Engineering Constants
        elastic = map(float, all_lines[ln+2].split())
        elastic.append(map(float, all_lines[ln+4].split()))
        elastic.append(map(float, all_lines[ln+3].split()))
        ln = ln + 5
    elif mate_type == 2:
        # Anisotropic
        ln = ln + 8
    materials[mate_id].append(elastic)

print materials

# Write Abaqus .inp file
with open(abaqus_input, 'w') as fout:
    fout.write('*Heading\n')
    fout.write('*Preprint, echo=NO, model=NO, history=NO, contact=NO\n')

    fout.write('**\n** PARS\n**\n')
    fout.write('*Part, name=')
    fout.write(part_name)
    fout.write('\n')
    fout.write('*Node\n')
    for n in node_coord:
        utl.writeFormat(fout, 'dEEE', n, ',')
    if elem_connt_c4 != []:
        fout.write('*Element, type=C3D4\n')
        for e in elem_connt_c4:
            utl.writeFormat(fout, 'd'*5, e, ',')
    if elem_connt_c10 != []:
        fout.write('*Element, type=C3D10\n')
        for e in elem_connt_c10:
            utl.writeFormat(fout, 'd'*11, e, ',')
    if elem_connt_c8 != []:
        fout.write('*Element, type=C3D8\n')
        for e in elem_connt_c8:
            utl.writeFormat(fout, 'd'*9, e, ',')
    if elem_connt_c20 != []:
        fout.write('*Element, type=C3D20\n')
        for e in elem_connt_c20:
            utl.writeFormat(fout, 'd'*21, e, ',')

    fout.write('*End Part\n')

    fout.write('**\n** ASSEMBLY\n**\n')

    fout.write('**\n** MATERIALS\n**\n')
