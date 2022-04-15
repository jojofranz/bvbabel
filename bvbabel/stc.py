"""Read, write, create Brainvoyager VTC file format."""

import os
from bvbabel.fmr import read_fmr
import struct
import numpy as np
from bvbabel.utils import read_variable_length_string
from bvbabel.utils import write_variable_length_string


# =============================================================================
def read_stc(filename):
    """Read Brainvoyager STC file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        FMR-information.
    data : 3D numpy.array
        Image data.

    """

    fmr_file = filename.replace('.stc', '.fmr')
    if os.path.isfile(fmr_file):
        header = read_fmr(fmr_file)
    else:
        raise ValueError('Could not find corresponding .fmr file.')

    if header['DataStorageFormat'] != 2:
        raise ValueError('Can only read .stc files with DataStorageFormat=2.')

    DimX = header['ResolutionX']
    DimY = header['ResolutionY']
    DimZ = header['NrOfSlices']
    DimT = header['NrOfVolumes']

    data_img = np.zeros(DimZ * DimT * DimY * DimX,
                        dtype='<h')

    with open(filename, 'rb') as f:

        # 2 bytes (unsigned short)
        if header['DataType'] == 1:
            buffer = f.read(data_img.size * 2)
            data_img = np.frombuffer(buffer, dtype='<h')
        # 4 bytes (float)
        if header['DataType'] == 2:
            buffer = f.read(data_img.size * 4)
            data_img = np.frombuffer(buffer, dtype='<f')

        data_img = data_img.reshape((DimZ, DimT, DimY, DimX))
        data_img = np.transpose(data_img, (3, 2, 0, 1))  # BV to Tal
        data_img = data_img[::-1, ::-1, ::-1, :]  # Flip BV axes

    return header, data_img
