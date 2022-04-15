"""Read Brainvoyager FMR file format."""

import numpy as np


# =============================================================================
def read_fmr(filename):
    """Read Brainvoyager FMR file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        FMR-information.

    """

    def is_number(string):
        """
        Check if a string is a number.
        Unlike .isnumeric(), this also discovers floats.
        """
        try:
            float(string)
            return True
        except ValueError:
            return False

    header = dict()
    with open(filename, 'r') as f:
        for line in f:
            if line == '\n':
                pass

            else:
                # special case 1
                # this key does not come with a colon (':')
                if line[:35] == 'PositionInformationFromImageHeaders':
                    # TODO test with files that have a value for this
                    key = 'PositionInformationFromImageHeaders'
                    val = line[35:]
                    header[key] = val

                # special case 2
                # this key is followed by the transformation matrix
                elif line[:24] == 'NrOfTransformationValues':
                    line = line.split(':', 1)
                    key = line[0]
                    val = line[1].strip()
                    header[key] = int(val)

                    # read transformation
                    key = 'Transformation'
                    val = []
                    # TODO this is assuming that the transformation is written maximal over 4 lines
                    for i in range(4):
                        line = f.readline()
                        if line != '\n':
                            val.append(line.split())
                    val = np.array(val).astype(np.float64)
                    header[key] = val

                # general case
                else:
                    line = line.split(':', 1)
                    key = line[0]
                    val = line[1].strip()
                    # take care of
                    # paths
                    val = val.replace('"', '')
                    # numbers
                    if is_number(val):
                        val = float(val)
                        if val % 1 == 0:
                            val = int(val)
                    header[key] = val

                # TODO convert AcqusitionTime from string to date?

    return header
