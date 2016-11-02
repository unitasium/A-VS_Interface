# -*- coding: utf-8 -*-

from odbAccess import *
from odbMaterial import *
from odbSection import *
from abaqus import *
from abaqusConstants import *
#from scVisual2D import *
#from scVisual3D import *
#from scVisual1D import *
from utilities import *
from textRepr import *
from UcheckDehoVisual import *
import os.path

# ==============================================================================
#
#   Main
#
# ==============================================================================

def visualization(vabs_input):

#    sc_input = sc_input.replace('\\','/')

    # =======================================================================
    # Read data from files
    # =======================================================================
    # vabs_input = vabs_input.replace('\\','/')
#    debug = open(sc_input + '.debug', 'w')
#    print sc_input
    # =======================================================================
    # Read data from files
    # =======================================================================
    
    
    # u_filename   = sc_input + r'.u'
    # sg_filename  = sc_input + r'.sg'
    # sn_filename  = sc_input + r'.sn'
    # sgm_filename = sc_input + r'.sgm'
    # snm_filename = sc_input + r'.snm'

    fn_u = vabs_input + '.U'
    fn_e = vabs_input + '.E'
    fn_s = vabs_input + '.S'
    fn_em = vabs_input + '.EM'
    fn_sm = vabs_input + '.SM'
    fn_en = vabs_input + '.EN'
    fn_sn = vabs_input + '.SN'
    fn_emn = vabs_input + '.EMN'
    fn_smn = vabs_input + '.SMN'
    fn_ele = vabs_input + '.ELE'
    
    project_path = os.path.dirname(vabs_input)
    project_name = os.path.basename(vabs_input)
    project_name = project_name.split('.')[0]
# #    sc_input_temp = sc_input.split('/')
# #    project_path  = '/'.join(sc_input_temp[:-1])
#     project_path = os.path.dirname(sc_input)
# #    project_name  = sc_input_temp[-1]
#     sc_input_sc = os.path.basename(sc_input)
#     checkDehoVisual(sc_input_sc, 'visual')
#     #print 'sc_input_sc %s' %sc_input_sc
#     project_name = sc_input_sc.split('.')
#     project_name = project_name[0]
#     #print 'project_name %s' %project_name
#     # check if the odb has already exist, and check if the file .sc exist or not.
#     checkDehoVisual(sc_input_sc, 'visual')
    
    
    # macro_model_dimension=str(macro_model)+'D'
    
    # if ap_flag==False:
    #     if macro_model_dimension == '1D':            # Beam
    #         skip_line = [1, 2, 3, 4]
    #     elif macro_model_dimension == '2D':          # Plate/Shell
    #         skip_line = [1, 2, 3]
    #     elif macro_model_dimension == '3D':          # Solid/Block
    #         skip_line = [1]
    # else:
    #     if macro_model_dimension == '1D':            # Beam
    #         skip_line = [1, 2, 3, 4, 5]
    #     elif macro_model_dimension == '2D':          # Plate/Shell
    #         skip_line = [1, 2, 3, 4]
    #     elif macro_model_dimension == '3D':          # Solid/Block
    #         skip_line = [1, 2 ]
            
    i = 1
    j = 1
    
    # ------------------------------------
    # Read model data from VABS input file
    
    node_coord = []  # Nodal coordinates      [(n1, x1, x2, x3), ...]
    elem_connt = []  # Element connectivities [(e1, n1, n2, n3, n4, ...), ...]
    elem_sectn = {}  # Material sections      {'s1': [e1, e2, e3, ...], ...}
    elem_label = []  # Element labels         [e1, e2, e3, ...]
    
    # elem_label_s3 = []
    # elem_label_s4 = []

    elem_connt_s3 = []
    elem_connt_s6 = []
    elem_connt_s4 = []
    elem_connt_s8 = []
    elem_connt_s9 = []
    
    # elem_connt_c4  = []
    # elem_connt_c10 = []
    # elem_connt_c8  = []
    # elem_connt_c20 = []
    
    # elem_connt_b31_temp=[]
    # elem_connt_b31 = []
    
    print '--> Reading VABS input file...'
    skip_line = [1, 2, 3]
    with open(vabs_input, 'r') as fin:
        for line in fin:
            line = line.strip()
            if line == '\n' or line == '':
                continue
            else:
                line = line.split()
                if i in skip_line:
                    i += 1
                    continue
                elif i == skip_line[-1] + 1:
                    # nsg = int(line[0])              # Read the dimension of SG
                    nnode = int(line[0])            # Read the number of nodes
                    nelem = int(line[1])            # Read the number of elements
                    
                    # print 'nsg %d'%nsg
                    # print 'nnode %d'%nnode 
                    # print 'nelem %d'%nelem
                    i += 1
                elif j <= nnode:                    # Read nodal coordinates
                    # if nsg == 1:
                    #     node_coord.append((int(line[0]), 0.0, 0.0, float(line[1])))
                    # elif nsg == 2:
                    node_coord.append((int(line[0]), 0.0, float(line[1]), float(line[2])))
                    # elif nsg == 3:
                    #     node_coord.append((int(line[0]), float(line[1]), float(line[2]), float(line[3])))
                    j += 1
                elif j <= (nnode + nelem):          # Read element connectivities
                    elem_label.append(int(line[0]))
                    # temp = line[2:]
                    temp = [int(i) for i in line if i != '0']
                    # temp = [int(line[0])] + temp
                    elem_connt.append(tuple(temp))
                    
                    # if len(line) == 7:       # 1D element
                    #     elem_connt_b31_temp.append(tuple(temp))
                    # elif len(line) == 11:       # 2D element
                    if len(temp) == 4:
                        # elem_label_s3.append(int(line[0]))
                        elem_connt_s3.append(tuple(temp))
                    elif len(temp) == 7:
                        elem_connt_s6.append(tuple(temp))
                    elif len(temp) == 5:
                        # elem_label_s4.append(int(line[0]))
                        elem_connt_s4.append(tuple(temp))
                    elif len(temp) == 9:
                        elem_connt_s8.append(tuple(temp))
                    elif len(temp) == 10:
                        elem_connt_s9.append(tuple(temp))
                    # elif len(line) >= 22:       # 3D element
                    #     if len(temp) == 5:
                    #         elem_connt_c4.append(tuple(temp))
                    #     elif len(temp) == 11:
                    #         elem_connt_c10.append(tuple(temp))
                    #     elif len(temp) == 9:
                    #         elem_connt_c8.append(tuple(temp))
                    #     elif len(temp) == 21:
                    #         elem_connt_c20.append(tuple(temp))
                    # sect = line[1]                  # Read material sections
                    # if sect not in elem_sectn.keys():
                    #     elem_sectn[sect] = []
                    # elem_sectn[sect].append(int(line[0]))
                    j += 1
                elif j <= (nnode + nelem + nelem):  # Read material sections
                    eid = int(line[0])
                    sect = int(line[1])
                    if sect not in elem_sectn.keys():
                        elem_sectn[sect] = []
                    elem_sectn[sect].append(eid)
                    j += 1
    
    elem_label.sort()
    # print elem_label[:10]

    elem_connt_s3.sort()
    elem_connt_s6.sort()
    elem_connt_s4.sort()
    elem_connt_s8.sort()
    # elem_connt_c4.sort()
    # elem_connt_c10.sort()
    # elem_connt_c8.sort()
    # elem_connt_c20.sort()
    # print len(elem_connt_s3)
    # print len(elem_connt_s6)
    # print len(elem_connt_s4)
    # print len(elem_connt_s8)
    # 1D 
    # elem_connt_b31_temp.sort()
    print '    Done.'

    # -----------------------------------------
    # Read nodal displacement data from .U file
    
    print '--> Reading result files...'
    node_label = []  # Node labels         [n1, n2, n3, ...]
    u_data     = []  # Nodal displacements [(u1, u2, u3), ...]
    
    try:
        print '    -> Reading .U file...'
        with open(fn_u, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line == '\n' or line == '':
                    continue
                else:
                    line = line.split()
                    node_label.append(int(line[0]))
                    u_data.append((float(line[3]), float(line[4]), float(line[5])))
    except:
        print '--! Cannot find .U file.'
                
    #print len(u_data)
    
    # ------------------------------------------------------
    # Read integration point strain/stress data from .e/s file
    
    sg_strain = []  # Integration point strains  [(e11,  e22,  e33, 2e23, 2e13, 2e12), ...]
    sg_stress = []  # Integration point stresses [(s11,  s22,  s33,  s23,  s13,  s12), ...]
    
    try:
        print '    -> Reading .E file...'
        with open(fn_e, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line == '\n' or line == '':
                    continue
                else:
                    line = line.split()
                    temp_e = [float(i) for i in line[2:]]
                    sg_strain.append(tuple(temp_e))
    except:
        print '--! Cannot find .E file.'

    try:
        print '    -> Reading .S file...'
        with open(fn_s, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line == '\n' or line == '':
                    continue
                else:
                    line = line.split()
                    temp_s = [float(i) for i in line[2:]]
                    sg_stress.append(tuple(temp_s))
    except:
        print '--! Cannot find .S file.'
    
    # --------------------------------------------
    # Read element nodal strain data from .en/sn file
    
    sn_strain = []  # Element nodal strains  [(en11,  en22,  en33, 2en23, 2en13, 2en12), ...]
    sn_stress = []  # Element nodal stresses [(sn11,  sn22,  sn33,  sn23,  sn13,  sn12), ...]
    
    try:
        print '    -> Reading .EN file...'
        with open(fn_en, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line == '\n' or line == '':
                    continue
                else:
                    line = line.split()
                    temp_e = [float(i) for i in line[3:]]
                    sn_strain.append(tuple(temp_e))
    except:
        print '--! Cannot find .EN file.'

    try:
        print '    -> Reading .SN file...'
        with open(fn_sn, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line == '\n' or line == '':
                    continue
                else:
                    line = line.split()
                    temp_s = [float(i) for i in line[3:]]
                    sn_stress.append(tuple(temp_s))
    except:
        print '--! Cannot find .SN file.'
        
    # ------------------------------------------------------
    # Read integration point strain/stress data under material frame from .em/sm file
    
    sgm_strain = []  # Integration point strains  [(e11,  e22,  e33, 2e23, 2e13, 2e12), ...]
    sgm_stress = []  # Integration point stresses [(s11,  s22,  s33,  s23,  s13,  s12), ...]
    
    try:
        print '    -> Reading .EM file...'
        with open(fn_em, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line == '\n' or line == '':
                    continue
                else:
                    line = line.split()
                    temp_e = [float(i) for i in line[2:]]
                    sgm_strain.append(tuple(temp_e))
    except:
        print '--! Cannot find .EM file.'

    try:
        print '    -> Reading .SM file...'
        with open(fn_sm, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line == '\n' or line == '':
                    continue
                else:
                    line = line.split()
                    temp_s = [float(i) for i in line[2:]]
                    sgm_stress.append(tuple(temp_s))
    except:
        print '--! Cannot find .SM file.'
    
    # --------------------------------------------
    # Read element nodal strain data under material frame from .emn/smn file
    
    snm_strain = []  # Element nodal strains  [(en11,  en22,  en33, 2en23, 2en13, 2en12), ...]
    snm_stress = []  # Element nodal stresses [(sn11,  sn22,  sn33,  sn23,  sn13,  sn12), ...]
    
    try:
        print '    -> Reading .EMN file...'
        with open(fn_emn, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line == '\n' or line == '':
                    continue
                else:
                    line = line.split()
                    temp_e = [float(i) for i in line[3:]]
                    snm_strain.append(tuple(temp_e))
    except:
        print '--! Cannot find .EMN file.'

    try:
        print '    -> Reading .SMN file...'
        with open(fn_smn, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line == '\n' or line == '':
                    continue
                else:
                    line = line.split()
                    temp_s = [float(i) for i in line[3:]]
                    snm_stress.append(tuple(temp_s))
    except:
        print '--! Cannot find .SMN file.'
    
    print '    Done.'
    
    #=========================================================
    # tranfer sn data for nsg==1:  only work for cases that each edge contains the same number of B31 elements!
    #=========================================================
#     new_conn = []
#     if nsg == 1:
#         print '--> Convert beam element infomation...'
        
# #        elem_connt_b31_temp : element_id_aba,  element connectivity                           
#         nelem_edge=len(elem_connt_b31_temp[0]) -2  # nelem_edge per edge/(element of swiftcomp)
        
#         if nelem_edge == 1:
#             elem_connt_b31= elem_connt_b31_temp
#             print '--> Two noded beam element are implemented, no convertion is necessary. '
    
            
#         else:
#             elem_label = []
#             for item in elem_connt_b31_temp:
#                 elabel = (item[0] - 1) * nelem_edge + 1
#                 for i in range(nelem_edge):
#                     elem_label.append(elabel + i)
#                 if nelem_edge == 4:
#                     new_conn.append((elabel, item[1], item[3]))
#                     new_conn.append((elabel + 1, item[3], item[5]))
#                     new_conn.append((elabel + 2, item[5], item[4]))
#                     new_conn.append((elabel + 3, item[4], item[2]))
#                 elif nelem_edge == 3:
#                     new_conn.append((elabel, item[1], item[3]))
#                     new_conn.append((elabel + 1, item[3], item[4]))
#                     new_conn.append((elabel + 2, item[4], item[2]))
#                 elif nelem_edge == 2:
#                     new_conn.append((elabel, item[1], item[3]))
#                     new_conn.append((elabel + 1, item[3], item[2]))
                
#             elem_connt_b31 = new_conn
         
#             elem_sectn_new = {}
#             for sect, elems in elem_sectn.iteritems():
#                 elem_sectn_new[sect] = []
#                 for i in range(len(elems)):
#                     temp_i = [(elems[i]-1) * nelem_edge + 1 + j for j in range(nelem_edge)]
#                     elem_sectn_new[sect] = elem_sectn_new[sect] + temp_i
#             elem_sectn = elem_sectn_new
#             new_strain = []
#             new_stress = []
                
#             nedge = len(elem_label) / nelem_edge
#             print 'number of beam elements in the 1D SG model: '
#             print nedge
                
#             if nelem_edge == 4:
#                 nodes_edge = [0,2,2,4,4,3,3,1]
#             elif nelem_edge == 3:
#                 nodes_edge = [0,2,2,3,3,1]
#             elif nelem_edge == 2:
#                 nodes_edge = [0,2,2,1]
    
#             for edge_i in range(nedge):
#                 for j in range(len(nodes_edge)):
#                     new_strain.append(sn_strain[nodes_edge[j] + (nelem_edge+1) * edge_i])
#                     new_stress.append(sn_stress[nodes_edge[j] + (nelem_edge+1) * edge_i])
#             sn_strain = new_strain
#             sn_stress = new_stress

    # =======================================================================
    # Create odb file and import data
    # =======================================================================
    
    # ---------------------
    # Create a new odb file
    print '--> Creating ODB file...'
    odb_name = project_name
    odb_title = project_name
    odb_file_name = os.path.join(project_path, project_name + '.odb')

    odb = Odb(name = odb_name, 
              analysisTitle = odb_title, 
              description = 'VABS Dehomogenization', 
              path = odb_file_name)
    
    # if nsg == 2:
    visualization2D(
        odb, project_name, node_coord, elem_connt_s3, elem_connt_s6, 
        elem_connt_s4, elem_connt_s8, elem_connt_s9, elem_sectn, node_label, 
        elem_label, u_data, sg_strain, sg_stress, sn_strain, sn_stress, 
        sgm_strain, sgm_stress, snm_strain, snm_stress)
    # elif nsg == 3:
    #     visualization3D(odb, project_name, node_coord, elem_connt_c4, elem_connt_c10, 
    #                     elem_connt_c8, elem_connt_c20, elem_sectn, node_label, elem_label, 
    #                     u_data, sg_strain, sg_stress, sn_strain, sn_stress, 
    #                     sgm_strain, sgm_stress, snm_strain, snm_stress)
    # elif nsg == 1:
    #     visualization1D(odb, project_name, node_coord, elem_connt_b31, elem_sectn, node_label, elem_label, 
    #                     u_data, sg_strain, sg_stress, sn_strain, sn_stress)
                        
    print '    Done.'
    
    session.odbs[odb_name].close()
    odb = openOdb(odb_file_name)
    
    # Customize the viewport
    da = session.drawingArea
    da_width = da.width
    da_height = da.height
    da_origin = da.origin
    
    vp1 = session.viewports[session.currentViewportName]
    vp1.setValues(origin = da_origin, width = da_width / 2.0, height = da_height)
    da_origin = (da_origin[0] + da_width / 2.0, da_origin[1])
    setViewYZ(vp=vp1, nsg=2, obj=odb)
    vp1.odbDisplay.setPrimaryVariable(variableLabel = 'EN', 
                                      outputPosition = ELEMENT_NODAL, 
                                      refinement = (COMPONENT, 'EN11'))
    vp1.restore()
    
    font_family = 'consolas'
    font_style  = 'medium'
    font_size   = 140
    view_font = '-*-' + font_family + '-' + font_style + '-r-normal-*-*-' + str(font_size) + '-*-*-m-*-*-*'
    vp1.viewportAnnotationOptions.setValues(
        triadFont = view_font, 
        legendFont = view_font, 
        titleFont = view_font, 
        stateFont = view_font, 
        legendMinMax = ON, 
        legendDecimalPlaces = 6, 
        legendBackgroundStyle = TRANSPARENT)
    vp1.odbDisplay.display.setValues(plotState = CONTOURS_ON_DEF)
    vp1.odbDisplay.commonOptions.setValues(visibleEdges=FEATURE)
    
    vp2 = session.Viewport(name = 'Viewport: 2', 
                           origin = da_origin, width = da_width / 2.0, height = da_height)
    setViewYZ(vp=vp2, nsg=2, obj=odb)
    vp2.odbDisplay.setPrimaryVariable(variableLabel = 'SN', 
                                     outputPosition = ELEMENT_NODAL, 
                                     refinement = (COMPONENT, 'SN11'))

    vp1.makeCurrent()
                                     
    session.linkedViewportCommands.setValues(linkViewports=True)
    session.linkedViewportCommands.setValues(fieldOutput=False)

    return 1



# ====================================================================
#
#   Visualization of 2D SG
#
# ====================================================================

def visualization2D(
    odb_vis, project_name, node_coord, elem_connt_s3, elem_connt_s6, 
    elem_connt_s4, elem_connt_s8, elem_connt_s9, elem_sectn, node_label, 
    elem_label, u_data, sg_strain, sg_stress, sn_strain, sn_stress, 
    sgm_strain, sgm_stress, snm_strain, snm_stress
    ):

    # -----------------------
    # Create a dummy material
    print '    -> Creating a dummy material...'
    material_name = 'Elastic material'
    material_1 = odb_vis.Material(name = material_name)
    material_1.Elastic(type = ISOTROPIC, 
                       temperatureDependency = OFF, 
                       dependencies = 0, 
                       noCompression = OFF, 
                       noTension = OFF, 
                       moduli = LONG_TERM, 
                       table = ((12000, 0.3), ))
                       
    # -------------------------
    # Create different sections
    print '    -> Creating sections...'
    section_name_g = 'Homogeneous shell section'
    abq_section = {}
    for k in elem_sectn.keys():
        section_name = section_name_g + '-' + str(k)
        abq_section[k] = odb_vis.HomogeneousShellSection(
            name = section_name, material = material_name, thickness = 0.1
            )
    s_cat = odb_vis.SectionCategory(name = 'S5', description = '')
    sp_bot = s_cat.SectionPoint(number = 1, description = 'Bottom')
    
    # -----------------
    # Create a new part
    print '    -> Creating a new part...'
    part_1 = odb_vis.Part(name = 'Part-1', embeddedSpace = THREE_D, type = DEFORMABLE_BODY)
    node_coord = tuple(node_coord)
    # Import nodes
    part_1.addNodes(nodeData = node_coord, nodeSetName = 'nSet-1')
    odb_vis.save()
    
#    elem_connt = tuple(elem_connt)
    # Import elements
    if elem_connt_s3 != []:
        # print elem_connt_s3
        elem_connt_s3 = tuple(elem_connt_s3)
        part_1.addElements(
            elementData=elem_connt_s3, type='DS3', 
            elementSetName='eSet-s3', sectionCategory=s_cat
            )
    if elem_connt_s6 != []:
        elem_connt_s6 = tuple(elem_connt_s6)
        part_1.addElements(
            elementData=elem_connt_s6, type='DS6', 
            elementSetName='eSet-s6', sectionCategory=s_cat
            )
    if elem_connt_s4 != []:
        # print elem_connt_s4
        elem_connt_s4 = tuple(elem_connt_s4)
        part_1.addElements(
            elementData=elem_connt_s4, type='DS4', 
            elementSetName='eSet-s4', sectionCategory=s_cat
            )
    if elem_connt_s8 != []:
        elem_connt_s8 = tuple(elem_connt_s8)
        part_1.addElements(
            elementData=elem_connt_s8, type='DS8', 
            elementSetName='eSet-s8', sectionCategory=s_cat
            )
    if elem_connt_s9 != []:
        elem_connt_s9 = tuple(elem_connt_s9)
        part_1.addElements(
            elementData=elem_connt_s9, type='M3D9', 
            elementSetName='eSet-s9', sectionCategory=s_cat
            )
    odb_vis.save()
    
    # ---------------------
    # Create a new instance
    print '    -> Creating a new instance...'
    instance_1 = odb_vis.rootAssembly.Instance(name = 'Part-1-1', object = part_1)
    for k in elem_sectn.keys():  # Assign sections to element sets
        section_name = section_name_g + ' - ' + str(k)
        elem_sectn_label = elem_sectn[k]
        # elem_sectn_label.sort()
        # print elem_sectn_label
        elem_set = odb_vis.rootAssembly.instances['Part-1-1'].\
            ElementSetFromElementLabels(name = section_name, elementLabels = elem_sectn_label)
        instance_1.assignSection(region = elem_set, section = abq_section[k])
    odb_vis.save()
    
    # ---------------------------
    # Create a new step and frame
    print '    -> Creating a new step...'
    step_1 = odb_vis.Step(name = 'Step-1', description = '', domain = TIME, timePeriod = 1.0)
    analysis_time = 0.1
    frame_1 = step_1.Frame(incrementNumber = 1, frameValue = analysis_time, description = '')
    
    # ------------------------
    # Import displacement data
    print '    -> Importing displacements...'
    if u_data != []:
        u_data = tuple(u_data)
        u_field = frame_1.FieldOutput(name = 'U', description = 'Displacements.', type = VECTOR,
                                      validInvariants=(MAGNITUDE,),)
        u_field.addData(position = NODAL, 
                        instance = instance_1, 
                        labels = node_label, 
                        data = u_data)
        step_1.setDefaultDeformedField(u_field)
        odb_vis.save()
    
    # -----------------------------
    # Import strain and stress data
    
    # with open('strains.dat', 'w') as f:
    #     j = 0
    #     for eid in elem_label:
    #         if eid in elem_label_s3:
    #             for i in range(3):
    #                 f.write('{0:4d}'.format(eid))
    #                 writeFormat(f, 'E'*6, sg_strain[j])
    #                 j += 1
    #         elif eid in elem_label_s4:
    #             for i in range(4):
    #                 f.write('{0:4d}'.format(eid))
    #                 writeFormat(f, 'E'*6, sg_strain[j])
    #                 j += 1

    # ---- GLOBAL COORDINATES ----
    # Strains at integration points
    # print len(sg_strain)
    if sg_strain != []:
        print '    -> Importing strains at Gaussian points...'
        s_field = frame_1.FieldOutput(
            name='E',
            description='Strains at Gaussian points in the global coordinates.',
            type=TENSOR_3D_FULL,
            componentLabels=('E11', '2E12', '2E13', 'E22', '2E23', 'E33'),
            validInvariants=(MISES, TRESCA, PRESS, INV3, MAX_PRINCIPAL, MID_PRINCIPAL, MIN_PRINCIPAL),
            )
        s_field.addData(
            position=INTEGRATION_POINT, 
            sectionPoint=sp_bot, 
            instance=instance_1, 
            labels=elem_label, 
            data=sg_strain
            )
        odb_vis.save()
    
    # Stresses at integration points
    if sg_stress != []:
        print '    -> Importing stresses at Gaussian points...'
        s_field = frame_1.FieldOutput(
            name = 'S', 
            description = 'Stresses at Gaussian points in the global coordinates.', 
            type = TENSOR_3D_FULL, 
            componentLabels = ('S11', 'S12', 'S13', 'S22', 'S23', 'S33'),
            validInvariants=(MISES, TRESCA, PRESS, INV3, MAX_PRINCIPAL, MID_PRINCIPAL, MIN_PRINCIPAL),
            )
        s_field.addData(
            position = INTEGRATION_POINT, 
            sectionPoint = sp_bot, 
            instance = instance_1, 
            labels = elem_label, 
            data = sg_stress
            )
        odb_vis.save()
    
    # Strains at elemental nodes
    if sn_strain != []:
        print '    -> Importing strains at elemental nodes...'
        e_field = frame_1.FieldOutput(
            name = 'EN', 
            description = 'Strains at nodes in the global coordinates.', 
            type = TENSOR_3D_FULL, 
            componentLabels = ('EN11', '2EN12', '2EN13', 'EN22', '2EN23', 'EN33'),
            validInvariants=(MISES, TRESCA, PRESS, INV3, MAX_PRINCIPAL, MID_PRINCIPAL, MIN_PRINCIPAL),
            )
        e_field.addData(
            position = ELEMENT_NODAL, 
            sectionPoint = sp_bot, 
            instance = instance_1, 
            labels = elem_label, 
            data = sn_strain
            )
#        step_1.setDefaultField(e_field)
        odb_vis.save()
    
    # Stresses at elemental nodes
    if sn_stress != []:
        print '    -> Importing stresses at elemental nodes...'
        s_field = frame_1.FieldOutput(
            name = 'SN', 
            description = 'Stresses at nodes in the global coordinates.', 
            type = TENSOR_3D_FULL, 
            componentLabels = ('SN11', 'SN12', 'SN13', 'SN22', 'SN23', 'SN33'),
            validInvariants=(MISES, TRESCA, PRESS, INV3, MAX_PRINCIPAL, MID_PRINCIPAL, MIN_PRINCIPAL),
            )
        s_field.addData(
            position = ELEMENT_NODAL, 
            sectionPoint = sp_bot, 
            instance = instance_1, 
            labels = elem_label, 
            data = sn_stress
            )
        odb_vis.save()
    
    # ---- MATERIAL COORDINATES ----
    # Strains at integration points
    if sgm_strain != []:
        print '    -> Importing strains at Gaussian points in material coordinates...'
        s_field = frame_1.FieldOutput(
            name = 'EM', 
            description = 'Strains at Gaussian points in the material coordinates.', 
            type = TENSOR_3D_FULL, 
            componentLabels = ('EM11', '2EM12', '2EM13', 'EM22', '2EM23', 'EM33'),
            validInvariants=(MISES, TRESCA, PRESS, INV3, MAX_PRINCIPAL, MID_PRINCIPAL, MIN_PRINCIPAL),
            )
        s_field.addData(
            position = INTEGRATION_POINT, 
            sectionPoint = sp_bot, 
            instance = instance_1, 
            labels = elem_label, 
            data = sgm_strain
            )
        odb_vis.save()
    
    # Stresses at integration points
    if sgm_stress != []:
        print '    -> Importing stresses at Gaussian points in material coordinates...'
        s_field = frame_1.FieldOutput(
            name = 'SM', 
            description = 'Stresses at Gaussian points in the material coordinates.', 
            type = TENSOR_3D_FULL, 
            componentLabels = ('SM11', 'SM12', 'SM13', 'SM22', 'SM23', 'SM33'),
            validInvariants=(MISES, TRESCA, PRESS, INV3, MAX_PRINCIPAL, MID_PRINCIPAL, MIN_PRINCIPAL),
            )
        s_field.addData(
            position = INTEGRATION_POINT, 
            sectionPoint = sp_bot, 
            instance = instance_1, 
            labels = elem_label, 
            data = sgm_stress
            )
        odb_vis.save()
    
    # Strains at elemental nodes
    if snm_strain != []:
        print '    -> Importing strains at elemental nodes in material coordinates...'
        e_field = frame_1.FieldOutput(
            name = 'EMN', 
            description = 'Strains at nodes in the material coordinates.', 
            type = TENSOR_3D_FULL, 
            componentLabels = ('EMN11', '2EMN12', '2EMN13', 'EMN22', '2EMN23', 'EMN33'),
            validInvariants=(MISES, TRESCA, PRESS, INV3, MAX_PRINCIPAL, MID_PRINCIPAL, MIN_PRINCIPAL),
            )
        e_field.addData(
            position = ELEMENT_NODAL, 
            sectionPoint = sp_bot, 
            instance = instance_1, 
            labels = elem_label, 
            data = snm_strain
            )
        odb_vis.save()
    
    # Stresses at elemental nodes
    if snm_stress != []:
        print '    -> Importing stresses at elemental nodes in material coordinates...'
        s_field = frame_1.FieldOutput(
            name = 'SMN', 
            description = 'Stresses at nodes in the material coordinates.', 
            type = TENSOR_3D_FULL, 
            componentLabels = ('SMN11', 'SMN12', 'SMN13', 'SMN22', 'SMN23', 'SMN33'),
            validInvariants=(MISES, TRESCA, PRESS, INV3, MAX_PRINCIPAL, MID_PRINCIPAL, MIN_PRINCIPAL),
            )
        s_field.addData(
            position = ELEMENT_NODAL, 
            sectionPoint = sp_bot, 
            instance = instance_1, 
            labels = elem_label, 
            data = snm_stress
            )
        odb_vis.save()
        
    return 1
    

