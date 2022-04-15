"""Read BrainVoyager VOI file format."""

import numpy as np


# =============================================================================
def read_voi(filename):
    """Read Brainvoyager VOI file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Voxels of interest (VOI) header.
    data : list of dictionaries
        A list of dictionaries. Each dictionary holds properties of a voxels of
        interest.

    """
    # Read non-empty lines of the input text file
    with open(filename, 'r') as f:
        lines = [r for r in (line.strip() for line in f) if r]

    # VOI header
    header = dict()
    header_rows = 12
    for line in lines[0:header_rows]:
        content = line.split(":")
        content = [i.strip() for i in content]
        if content[1].isdigit():
            header[content[0]] = int(content[1])
        else:
            header[content[0]] = content[1]

    # VOI data (x, y, z coordinates of voxels)
    count_voi = -1
    data = list()
    for r, line in enumerate(lines[header_rows:]):
        content = line.split(":")
        content = [i.strip() for i in content]

        if content[0] == "NameOfVOI":
            count_voi += 1
            data.append(dict())
            data[count_voi]["Coordinates"] = []  # Prepare for coordinates
            data[count_voi]["NameOfVOI"] = content[1]

        elif content[0] == "NrOfVOIVTCs":
            break

        elif content[0] == "ColorOfVOI":
            values = content[1].split(" ")
            values = [int(v) for v in values]
            data[count_voi]["ColorOfVOI"] = values

        elif content[0] == "NrOfVoxels":
            data[count_voi]["NrOfVoxels"] = int(content[1])

        else:
            values = content[0].split(" ")
            values = [int(v) for v in values]
            data[count_voi]["Coordinates"].append(values)

    # Handle VOI VTC information at the end
    header["NrOfVOIVTCs"] = int(content[1])
    header["VOIVTCs"] = []
    for line in lines[r+header_rows+1:]:
        header["VOIVTCs"].append(line)

    # Convert coordinates (x, y, z) to numpy arrays [nr_voxels, 3]
    for d in data:
        d["Coordinates"] = np.asarray(d["Coordinates"])

    return header, data


def voi_to_mask(voi, shape=None):
    """Convert voi information into volume masks.

    Parameters
    ----------
    voi : tuple
        Voi information (voi_header, voi_data) as returned by read_voi.
    shape : int or array-like
        (Optional) Framing cube dimensions.

    Returns
    -------
    voi_volumes : list
        A list of with one dictionariy per VOI.
        voi_volumes[voi_ix]['VOI'] contains the VOI volume.
        voi_volumes[voi_ix]['NameOfVOI'] contains the name of the VOI.

    Examples
    --------
    >>> voi_volumes = bvbabel.voi.voi_to_mask(bvbabel.voi.read_voi(filename))


    """

    voi_header, voi_data = voi

    nr_voi = voi_header['NrOfVOIs']

    if shape is None:
        dims = np.repeat(voi_header["OriginalVMRFramingCubeDim"], 3)
    else:
        if isinstance(shape, int):
            dims = np.repeat(shape, 3)
        else:
            dims = np.array(shape)

    voi_volumes = []
    for voi_i in range(nr_voi):
        coord = voi_data[voi_i]['Coordinates']
        coord = coord.T
        # Note: is this different from the usual transpose used in bvbabel?
        # which is: (0, 2, 1, 3))  # BV to Tal
        coord = np.vstack([coord[2, :],  # BV to Tal
                           coord[0, :],
                           coord[1, :]])

        coord = np.ravel_multi_index(coord, dims, order='C')

        voi_vol = np.zeros(np.prod(dims), dtype=np.int8)
        voi_vol[coord] = 1
        voi_vol = np.reshape(voi_vol, dims)
        voi_vol = voi_vol[::-1, ::-1, ::-1]  # Flip BV axes

        voi_volumes.append({'VOI': voi_vol,
                            'NameOfVOI': voi_data[voi_i]['NameOfVOI']})

    return voi_volumes

