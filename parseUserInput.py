import xml.etree.ElementTree as et
import globalConstants as gcs

# ====================================================================
# Function: parseMaterialsFromXML(material_db_name, materials, laminas)
#   Inputs:
#   1. material_db_name (String)
#        Complete directory and file name of the database
#   2. materials = {
#          material_name: {'id': material_id, 'properties': properties1},
#          material_name: {'id': material_id, 'properties': properties2},
#          ...
#      }
#      where
#      properties = {
#          'type': 'material_type',
#          'n_temperatures': number_of_temperatures,
#          'constants': [
#              {'temperature': temperature1, 'density': density1, 'elastic': [elastic1]},
#              {'temperature': temperature2, 'density': density2, 'elastic': [elastic2]},
#              ...
#          ]
#      }
#      where
#      elastic = E, nu
#      elastic = E1, E2, E3, nu12, nu13, nu23, G12, G13, G23
#      elastic = d1111, d1122, d2222, d1133, d2233, d3333,
#                d1212, d1313, d2323
#      elastic = d1111, d1122, d2222, d1133, d2233, d3333,
#                d1112, d2212, d3312, d1212, d1113, d2213,
#                d3313, d1213, d1313, d1123, d2223, d3323,
#                d1223, d1323, d2323
#   3. laminas = {
#        lamina_name: {'id': lamina_id, 'material': material_name, 'thickness': thickness},
#        lamina_name: {'id': lamina_id, 'material': material_name, 'thickness': thickness},
#        ...
#      }
# ====================================================================
def parseMaterialsFromXML(material_db_name, materials, laminas):
    """
    This function parse materials data from an .xml file into materials and laminas.
    """

    n_materials = len(materials)  # number of materials
    n_laminas = len(laminas)  # number of laminas

    materials_tree = et.parse(material_db_name)
    materials_root = materials_tree.getroot()

    material_id = n_materials
    lamina_id = n_laminas

    for element in materials_root:
        if element.tag == 'material':
            material_id += 1
            material_name = element.get('name').strip()
            material_type = element.get('type').strip()

            properties = {'type': material_type}
            properties['n_temperatures'] = 1
            # for different properties under different temperatures
            properties['constants'] = []

            # For each temperature
            constants = {'temperature': 20.0}
            density = element.find('density')
            if not density is None:
                density = float(density.text.strip())
            else:
                density = 1.0
            constants['density'] = density

            elastic = []
            element_elastic = element.find('elastic')
            for label in gcs.LABELS_ELASTIC[material_type.upper()]:
                elastic.append(float(element_elastic.find(label).text.strip()))
            constants['elastic'] = elastic

            properties['constants'].append(constants)

            materials[material_name] = {
                'id': material_id, 'properties': properties
            }

        elif element.tag == 'lamina':
            lamina_id += 1
            lamina_name = element.get('name').strip()
            material_name = element.find('material').text.strip()
            thickness = float(element.find('thickness').text.strip())
            laminas[lamina_name] = {
                'id': lamina_id,
                'material': material_name,
                'thickness': thickness
            }

    return 0




# ====================================================================
# layups = {
#     layup_name: {'id': layup_id, 'thickness': thickness, 'layers': layers},
#     ...
# }
# where
# layers = [
#     [layer_type_id, thickness],
#     ...
# ]
#
# layer_types = {
#     layer_type_id: [material_name, angle],
#     ...
# }
# ====================================================================
def parseLayupsFromXML(layup_db_name, layups, layer_types, laminas):
    """
    This function parse layup data from an .xml file into layups.
    """

    n_layups = len(layups)
    n_layer_types = len(layer_types)

    layups_tree = et.parse(layup_db_name)
    layups_root = layups_tree.getroot()

    layup_id = n_layups
    # layer_type_id = n_layer_types

    for element_layup in layups_root:
        layup_id += 1
        layup_name = element_layup.get('name').strip()
        total_thickness = 0.0
        layers = []
        for element_layer in element_layup:
            lamina_name = element_layer.get('lamina').strip()
            angle = 0.0
            n_stack = 1
            angle_stack = element_layer.text
            if not angle_stack is None:
                angle_stack = angle_stack.strip().split(':')
                angle = float(angle_stack[0])
                if len(angle_stack) == 2:
                    n_stack = int(angle_stack[1])

            material_name = laminas[lamina_name]['material']
            lamina_thickness = laminas[lamina_name]['thickness']
            layer_type = [material_name, angle]
            layer_type_id = 0
            for k, v in layer_types.items():
                if v == layer_type:
                    layer_type_id = k
                    break
            if layer_type_id == 0:
                layer_type_id = len(layer_types) + 1
                layer_types[layer_type_id] = layer_type
            
            for i in range(n_stack):
                layers.append([layer_type_id, lamina_thickness])
                total_thickness += lamina_thickness
        layups[layup_name] = {
            'id': layup_id, 'thickness': total_thickness, 'layers': layers
        }
    
    return 0
            