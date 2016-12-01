import numpy as np

def reorgSCInput(
    nsg,
    nodes, elements2d, elements3d, elsets,
    materials, densities, elastics, mtr_name2id
):

    material_type = {
        'ISOTROPIC': 0,
        'ENGINEERINGCONSTANTS': 1,
        'ORTHOTROPIC': 2,
        'ANISOTROPIC': 2
        }

    # ----- Nodal coordinates ----------------------------------------
    nid = nodes[:, 0]
    if nsg == 1:
        n_coord = nodes[:, [3,]]
    elif nsg == 2:
        n_coord = nodes[:, [2, 3]]
    elif nsg == 3:
        n_coord = nodes[:, [1, 2, 3]]

    # print n_coord[0]

    # ----- Materials ------------------------------------------------
    mtr = {}
    nmate = len(materials)
    for i in range(nmate):
        mtr_name = materials[i].parameter['name']
        mtr_id = mtr_name2id[mtr_name]
        try:
            mtr_type = elastics[i].parameter['type']
        except KeyError:
            mtr_type = 'ISOTROPIC'
        mtr_type = material_type[mtr_type]
        mtr[mtr_id] = {'isotropy': mtr_type, 'ntemp': 1, 'elastic': []}
        rho = densities[i].data[0][0]
        # print elastics[i].data
        # els = np.array(elastics[i].data).ravel()
        els = []
        for j in elastics[i].data:
            for k in j:
                if k is not None:
                    els.append(k)
        # print els
        if mtr_type == 0:
            elastic = els
        elif mtr_type == 1:
            elastic = [
                els[0], els[1], els[2],
                els[6], els[7], els[8],
                els[3], els[4], els[5]
            ]
        elif mtr_type == 2:
            if len(els) == 9:
                elastic = [
                    els[0], els[1], els[3],    0.0,    0.0,    0.0,
                            els[2], els[4],    0.0,    0.0,    0.0,
                                    els[5],    0.0,    0.0,    0.0,
                                            els[8],    0.0,    0.0,
                                                    els[7],    0.0,
                                                            els[6]
                ]
            elif len(els) == 21:
                elastic = [
                    els[0], els[1], els[3], els[15], els[10], els[6],
                            els[2], els[4], els[16], els[11], els[7],
                                    els[5], els[17], els[12], els[8],
                                            els[20], els[19], els[18],
                                                     els[14], els[13],
                                                              els[9]
                ]
        elastic = np.hstack(([20.0, rho], elastic))
        # print elastic
        mtr[mtr_id]['elastic'].append(elastic)

    return {
        'node ids': nid,
        'nodes': n_coord,
        # 'elements': e_connt,
        'materials': mtr
    }