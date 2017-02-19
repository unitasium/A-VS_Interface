# -*- coding: utf-8 -*-

# Functions
# =========
# trimIntersectCurves(sketch, curve1_id, keep1, curve2_id, keep2, near_pt)
# extendIntersectCurves(sketch, curve1_id, curve2_id, near_pt)
# findEndPoints(sketch, edge_id)
# findTwoPointsDistance(point1, point2)
# refreshSets(mdb, model_name, part_name, set_fpt)
# setViewYZ(vp=None, nsg=3, obj=None, clr=None)

from abaqus import *
# from abaqusConstants import *
import math

info  = 1
debug = 0

def trimIntersectCurves(sketch, curve1_id, keep1, curve2_id, keep2, near_pt):
    # keep1, keep2 = 1 (keep the 1st sub-curve) or 2 (keep the 2nd sub-curve)
    g = sketch.geometry
    sketch.breakCurve(curve1=g[curve1_id], point1=near_pt,
                      curve2=g[curve2_id], point2=near_pt)
    g = sketch.geometry
    gk = g.keys()
    id3 = gk[-2]
    id4 = gk[-1]
    if keep1 == 1:
        curve1_id_new = id3
        trim = (g[id4],)
    elif keep1 == 2:
        curve1_id_new = id4
        trim = (g[id3],)
    sketch.breakCurve(curve1=g[curve2_id], point1=near_pt,
                      curve2=g[id3], point2=near_pt)
    g = sketch.geometry
    gk = g.keys()
    id5 = gk[-2]
    id6 = gk[-1]
    if keep2 == 1:
        curve2_id_new = id5
        trim += (g[id6],)
    elif keep2 == 2:
        curve2_id_new = id6
        trim += (g[id5],)
    sketch.delete(objectList=trim)
    
    return [curve1_id_new, curve2_id_new]


def extendIntersectCurves(sketch, curve1_id, curve2_id, near_pt):
    g = sketch.geometry
    sketch.trimExtendCurve(curve1=g[curve1_id], point1=near_pt,
                           curve2=g[curve2_id], point2=near_pt)
    g = sketch.geometry
    gk = g.keys()
    id3 = gk[-1]
    sketch.trimExtendCurve(curve1=g[curve2_id], point1=near_pt,
                           curve2=g[id3], point2=near_pt)
    g = sketch.geometry
    gk = g.keys()
    id4 = gk[-1]
    
    return [id3, id4]


def findEndPoints(sketch, edge_id):
    g = sketch.geometry
    v = g[edge_id].getVertices()
    v1 = v[0].coords
    v2 = v[1].coords
    
    return [v1, v2]


def findTwoPointsDistance(point1, point2):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    return d


def refreshSets(mdb, model_name, part_name, set_fpt):
    p = mdb.models[model_name].parts[part_name]
    #set_fpt = mdb.customData.models[model_name]['Parts'][part_name]['Set-FacePoint']
    f = p.faces
    for rn, fpt in set_fpt.items():
        ff = f.findAt((fpt,))
        p.Set(name=rn, faces=ff)

# def getElemStats(region,elementShap):
# p = mdb.models['Model-1'].parts['Part-1']
# p.getElementType(region=region,elemShape=QUAD)


def setViewYZ(vp=None, nsg=3, obj=None, clr=None):
    # from abaqus import *
    try:
        if vp is None:
            vp = session.viewports[session.currentViewportName]
    except NameError:
        vp = None
        pass
    
    if vp is not None:
        if obj is not None:
            vp.setValues(displayedObject=obj)
        if nsg == 1 or nsg == 2:
            vp.view.setViewpoint(viewVector=(1.0, 0.0, 0.0),
                                cameraUpVector=(0.0, 0.0, 1.0))
        elif nsg == 3:
            vp.view.setViewpoint(viewVector=(1.0, 0.8, 0.6),
                                cameraUpVector=(0.0, 0.0, 1.0))
        if clr is not None:
            vp.enableMultipleColors()
            vp.setColor(initialColor='#BDBDBD')
            cmap = vp.colorMappings[clr]
            vp.setColor(colorMapping=cmap)
            vp.disableMultipleColors()
        vp.view.fitView()
    
    return vp
