# from abaqus import *
# from testRepository import *
from parseUserInput import *

fn_materials = r'C:\Users\unita\sall\s02-study\s01-graduate\g01-projects\p03-mcq\t0918\Materials.xml'
fn_layups = r'C:\Users\unita\sall\s02-study\s01-graduate\g01-projects\p03-mcq\t0918\Layups.xml'

materials = {}
laminas = {}

parseMaterialsFromXML(fn_materials, materials, laminas)

print materials
print laminas

layups = {}
layer_types = {}

parseLayupsFromXML(fn_layups, layups, layer_types, laminas)

for k, v in layer_types.items():
    print '{0}: {1}'.format(k, v)
for k, v in layups.items():
    print k, v
