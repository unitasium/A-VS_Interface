# ====================================================================
# Function: readMaterialsFromXML(materialDBName)
#   This function read materials data from an .xml file
#   into a Python dictionary.
#   Input:
#   1. materialDBName (String)
#        Complete directory and file name of the database
#   Output:
#   1. materials = {
#          materialID1: {'name': materialName1, 'properties': properties1},
#          materialID2: {'name': materialName2, 'properties': properties2},
#          ...
#      }
#      properties = {
#          'type': 'materialType',
#          'temperatures': numberOfTemperatures
#          'constants': [
#              {'temperature': temperature1, 'density': density1, 'elastic': [elastic1]},
#              {'temperature': temperature2, 'density': density2, 'elastic': [elastic2]},
#              ...
#          ]
#      }
#      elastic = E, nu
#      elastic = E1, E2, E3, nu12, nu13, nu23, G12, G13, G23
#      elastic = d1111, d1122, d2222, d1133, d2233, d3333, 
#                d1212, d1313, d2323
#      elastic = d1111, d1122, d2222, d1133, d2233, d3333, 
#                d1112, d2212, d3312, d1212, d1113, d2213, 
#                d3313, d1213, d1313, d1123, d2223, d3323, 
#                d1223, d1323, d2323
#   2. materialsIDToName = {
#          materialID1: materialName1,
#          materialID2: materialName2,
#          ...
#      }
#   3. materialsNameToID = {
#          materialName1: materialID1,
#          materialName2: materialID2,
#          ...
#      }
# ====================================================================

import xml.etree.ElementTree as et

def readMaterialsFromXML(materialDBName):
    materials = {}
    materialsIDToName = {}
    materialsNameToID = {}

    materialTree = et.parse(materialDBName)
    materialRoot = materialTree.getroot()

    materialID = 0
    for material in materialRoot:
        materialID += 1
        materialName = material.find('name').text.strip()
        materialsIDToName[materialID] = materialName
        materialsNameToID[materialName] = materialID

        properties = {}        
        materialType = material.get('type').strip()
        properties['type'] = materialType
        properties['temperatures'] = 1
        properties['constants'] = []

        constants = {}
        temperature = 20.0
        constants['temperature'] = temperature

        density = material.find('density')
        if not density == None:
            density = float(density.text)
        else:
            density = 1.0
        constants['density'] = density

        if materialType.upper() == 'ISOTROPIC':
            e = float(material.find('e').text.strip())
            nu = float(material.find('nu').text.strip())
            elastic = [e, nu]
        elif materialType.upper() == 'ENGINEERING CONSTANTS':
            e1   = float(material.find('e1').text.strip())
            e2   = float(material.find('e2').text.strip())
            e3   = float(material.find('e3').text.strip())
            g12  = float(material.find('g12').text.strip())
            g13  = float(material.find('g13').text.strip())
            g23  = float(material.find('g23').text.strip())
            nu12 = float(material.find('nu12').text.strip())
            nu13 = float(material.find('nu13').text.strip())
            nu23 = float(material.find('nu23').text.strip())
            elastic = [e1, e2, e3, nu12, nu13, nu23, g12, g13, g23]
        elif materialType.upper() == 'ORTHOTROPIC':
            d1111 = float(material.find('d1111').text.strip())
            d1122 = float(material.find('d1122').text.strip())
            d2222 = float(material.find('d2222').text.strip())
            d1133 = float(material.find('d1133').text.strip())
            d2233 = float(material.find('d2233').text.strip())
            d3333 = float(material.find('d3333').text.strip())
            d1212 = float(material.find('d1212').text.strip())
            d1313 = float(material.find('d1313').text.strip())
            d2323 = float(material.find('d2323').text.strip())
            elastic = [d1111, d1122, d2222, d1133, d2233, d3333, 
                       d1212, d1313, d2323]
        elif materialType.upper() == 'ANISOTROPIC':
            d1111 = float(material.find('d1111').text.strip())
            d1122 = float(material.find('d1122').text.strip())
            d2222 = float(material.find('d2222').text.strip())
            d1133 = float(material.find('d1133').text.strip())
            d2233 = float(material.find('d2233').text.strip())
            d3333 = float(material.find('d3333').text.strip())
            d1112 = float(material.find('d1112').text.strip())
            d2212 = float(material.find('d2212').text.strip())
            d3312 = float(material.find('d3312').text.strip())
            d1212 = float(material.find('d1212').text.strip())
            d1113 = float(material.find('d1113').text.strip())
            d2213 = float(material.find('d2213').text.strip())
            d3313 = float(material.find('d3313').text.strip())
            d1213 = float(material.find('d1213').text.strip())
            d1313 = float(material.find('d1313').text.strip())
            d1123 = float(material.find('d1123').text.strip())
            d2223 = float(material.find('d2223').text.strip())
            d3323 = float(material.find('d3323').text.strip())
            d1223 = float(material.find('d1223').text.strip())
            d1323 = float(material.find('d1323').text.strip())
            d2323 = float(material.find('d2323').text.strip())
            elastic = [d1111, d1122, d2222, d1133, d2233, d3333, 
                       d1112, d2212, d3312, d1212, d1113, d2213, 
                       d3313, d1213, d1313, d1123, d2223, d3323, 
                       d1223, d1323, d2323]
        constants['elastic'] = elastic

        properties['constants'].append(constants)

        materials[materialID] = {
            'name': materialName, 'properties': properties
        }

    return {
        'materials': materials,
        'materialsIDToName': materialsIDToName,
        'materialsNameToID': materialsNameToID
    }
