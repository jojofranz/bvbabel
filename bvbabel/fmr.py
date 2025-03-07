"""Read, write, create BrainVoyager FMR file format."""

import os
import numpy as np
from bvbabel.stc import read_stc, write_stc


# =============================================================================
def read_fmr(filename):
    """Read BrainVoyager FMR (and the paired STC) file.

    Parameters
    ----------
    filename : string
        Path to file.

    Returns
    -------
    header : dictionary
        Pre-data and post-data headers.
    data : 4D numpy.array, (x, y, slices, time)
        Image data.

    """
    header = dict()
    info_pos = dict()
    info_tra = dict()
    info_multiband = dict()

    with open(filename, 'r') as f:
        lines = f.readlines()
        for j in range(0, len(lines)):
            line = lines[j]
            content = line.strip()
            content = content.split(":", 1)
            content = [i.strip() for i in content]

            # -----------------------------------------------------------------
            # NOTE[Faruk]: Quickly skip entries starting with number. This is
            # because such entries belong to other structures and are dealth
            # with below in transformations and multiband sections
            if content[0].isdigit():
                pass
            elif content[0] == "FileVersion":
                header[content[0]] = content[1]
            elif content[0] == "NrOfVolumes":
                header[content[0]] = int(content[1])
            elif content[0] == "NrOfSlices":
                header[content[0]] = int(content[1])
            elif content[0] == "NrOfSkippedVolumes":
                header[content[0]] = content[1]
            elif content[0] == "Prefix":
                header[content[0]] = content[1].strip("\"")
            elif content[0] == "DataStorageFormat":
                header[content[0]] = int(content[1])
            elif content[0] == "DataType":
                header[content[0]] = int(content[1])
            elif content[0] == "TR":
                header[content[0]] = content[1]
            elif content[0] == "InterSliceTime":
                header[content[0]] = content[1]
            elif content[0] == "TimeResolutionVerified":
                header[content[0]] = content[1]
            elif content[0] == "TE":
                header[content[0]] = content[1]
            elif content[0] == "SliceAcquisitionOrder":
                header[content[0]] = content[1]
            elif content[0] == "SliceAcquisitionOrderVerified":
                header[content[0]] = content[1]
            elif content[0] == "ResolutionX":
                header[content[0]] = int(content[1])
            elif content[0] == "ResolutionY":
                header[content[0]] = int(content[1])
            elif content[0] == "LoadAMRFile":
                header[content[0]] = content[1].strip("\"")
            elif content[0] == "ShowAMRFile":
                header[content[0]] = content[1]
            elif content[0] == "ImageIndex":
                header[content[0]] = content[1]
            elif content[0] == "LayoutNColumns":
                header[content[0]] = content[1]
            elif content[0] == "LayoutNRows":
                header[content[0]] = content[1]
            elif content[0] == "LayoutZoomLevel":
                header[content[0]] = content[1]
            elif content[0] == "SegmentSize":
                header[content[0]] = content[1]
            elif content[0] == "SegmentOffset":
                header[content[0]] = content[1]
            elif content[0] == "NrOfLinkedProtocols":
                header[content[0]] = content[1]
            elif content[0] == "ProtocolFile":
                header[content[0]] = content[1].strip("\"")
            elif content[0] == "InplaneResolutionX":
                header[content[0]] = content[1]
            elif content[0] == "InplaneResolutionY":
                header[content[0]] = content[1]
            elif content[0] == "SliceThickness":
                header[content[0]] = content[1]
                # NOTE[Faruk]: This is duplicate entry that appears in position
                # information header too. I decided to use the last occurance
                # as the true value for both header entries. These two entries
                # should always match if the source file is not manipulated in
                # some way.
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceGap":
                header[content[0]] = content[1]
            elif content[0] == "VoxelResolutionVerified":
                header[content[0]] = content[1]

            # -----------------------------------------------------------------
            # Position information
            elif content[0] == "PositionInformationFromImageHeaders":
                pass  # No info to be stored here
            elif content[0] == "PosInfosVerified":
                info_pos[content[0]] = content[1]
            elif content[0] == "CoordinateSystem":
                info_pos[content[0]] = content[1]
            elif content[0] == "Slice1CenterX":
                info_pos[content[0]] = content[1]
            elif content[0] == "Slice1CenterY":
                info_pos[content[0]] = content[1]
            elif content[0] == "Slice1CenterZ":
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceNCenterX":
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceNCenterY":
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceNCenterZ":
                info_pos[content[0]] = content[1]
            elif content[0] == "RowDirX":
                info_pos[content[0]] = content[1]
            elif content[0] == "RowDirY":
                info_pos[content[0]] = content[1]
            elif content[0] == "RowDirZ":
                info_pos[content[0]] = content[1]
            elif content[0] == "ColDirX":
                info_pos[content[0]] = content[1]
            elif content[0] == "ColDirY":
                info_pos[content[0]] = content[1]
            elif content[0] == "ColDirZ":
                info_pos[content[0]] = content[1]
            elif content[0] == "NRows":
                info_pos[content[0]] = content[1]
            elif content[0] == "NCols":
                info_pos[content[0]] = content[1]
            elif content[0] == "FoVRows":
                info_pos[content[0]] = content[1]
            elif content[0] == "FoVCols":
                info_pos[content[0]] = content[1]
            elif content[0] == "SliceThickness":
                # NOTE[Faruk]: This is duplicate entry that appears twice.
                # ee header['SliceThickness'] section above.
                pass
            elif content[0] == "GapThickness":
                info_pos[content[0]] = content[1]

            # -----------------------------------------------------------------
            # Transformations section
            elif content[0] == "NrOfPastSpatialTransformations":
                info_tra[content[0]] = int(content[1])
            elif content[0] == "NameOfSpatialTransformation":
                info_tra[content[0]] = content[1]
            elif content[0] == "TypeOfSpatialTransformation":
                info_tra[content[0]] = content[1]
            elif content[0] == "AppliedToFileName":
                info_tra[content[0]] = content[1]
            elif content[0] == "NrOfTransformationValues":
                info_tra[content[0]] = content[1]

                # NOTE(Faruk): I dont like this matrix reader but I don't see a
                # more elegant way for now.
                nr_values = int(content[1])
                affine = []
                v = 0  # Counter for values
                n = 1  # Counter for lines
                while v < nr_values:
                    line = lines[j + n]
                    content = line.strip()
                    content = content.split()
                    for val in content:
                        affine.append(float(val))
                    v += len(content)  # Count values
                    n += 1  # Iterate line
                affine = np.reshape(np.asarray(affine), (4, 4))
                info_tra["Transformation matrix"] = affine

            # -----------------------------------------------------------------
            # This part only contains a single information
            elif content[0] == "LeftRightConvention":
                header[content[0]] = content[1]

            # -----------------------------------------------------------------
            # Multiband section
            elif content[0] == "FirstDataSourceFile":
                info_multiband[content[0]] = content[1]
            elif content[0] == "MultibandSequence":
                info_multiband[content[0]] = content[1]
            elif content[0] == "MultibandFactor":
                info_multiband[content[0]] = content[1]
            elif content[0] == "SliceTimingTableSize":
                info_multiband[content[0]] = int(content[1])

                # NOTE(Faruk): I dont like this matrix reader but I don't see a
                # more elegant way for now.
                nr_values = int(content[1])
                slice_timings = []
                for n in range(1, nr_values+1):
                    line = lines[j + n]
                    content = line.strip()
                    slice_timings.append(float(content))
                info_multiband["Slice timings"] = slice_timings

            elif content[0] == "AcqusitionTime":
                info_multiband[content[0]] = content[1]

    header["Position information"] = info_pos
    header["Transformation information"] = info_tra
    header["Multiband information"] = info_multiband

    # -------------------------------------------------------------------------
    # Access data from the separate STC file
    dirname = os.path.dirname(filename)
    filename_stc = os.path.join(dirname, "{}.stc".format(header["Prefix"]))

    data_img = read_stc(filename_stc, nr_slices=header["NrOfSlices"],
                        nr_volumes=header["NrOfVolumes"],
                        res_x=header["ResolutionX"],
                        res_y=header["ResolutionY"],
                        data_type=header["DataType"])

    return header, data_img


# =============================================================================
def write_fmr(filename, header, data_img):
    """Protocol to write BrainVoyager FMR (and the paired STC) file.

    Parameters
    ----------
    filename : string
        Path to file.
    header : dictionary
        Information that will be written into FMR file.
    data_img : 4D numpy.array, (x, y, slices, time)
        Image data.

    """
    info_pos = header["Position information"]
    info_tra = header["Transformation information"]
    info_multiband = header["Multiband information"]
    basepath = filename.split(os.extsep, 1)[0]
    basename = os.path.basename(basepath)

    with open(filename, 'w') as f:
        f.write("\n")

        data = header["FileVersion"]
        f.write("FileVersion:                   {}\n".format(data))
        data = header["NrOfVolumes"]
        f.write("NrOfVolumes:                   {}\n".format(data))
        data = header["NrOfSlices"]
        f.write("NrOfSlices:                    {}\n".format(data))
        data = header["NrOfSkippedVolumes"]
        f.write("NrOfSkippedVolumes:            {}\n".format(data))
        data = basename  # NOTE: This is updated to new filename.
        f.write("Prefix:                        \"{}\"\n".format(data))
        data = header["DataStorageFormat"]
        f.write("DataStorageFormat:             {}\n".format(data))
        data = header["DataType"]
        f.write("DataType:                      {}\n".format(data))
        data = header["TR"]
        f.write("TR:                            {}\n".format(data))
        data = header["InterSliceTime"]
        f.write("InterSliceTime:                {}\n".format(data))
        data = header["TimeResolutionVerified"]
        f.write("TimeResolutionVerified:        {}\n".format(data))
        data = header["TE"]
        f.write("TE:                            {}\n".format(data))
        data = header["SliceAcquisitionOrder"]
        f.write("SliceAcquisitionOrder:         {}\n".format(data))
        data = header["SliceAcquisitionOrderVerified"]
        f.write("SliceAcquisitionOrderVerified: {}\n".format(data))
        data = header["ResolutionX"]
        f.write("ResolutionX:                   {}\n".format(data))
        data = header["ResolutionY"]
        f.write("ResolutionY:                   {}\n".format(data))
        if "LoadAMRFile" in header:
            data = header["LoadAMRFile"]
        else:
            data = ""
        f.write("LoadAMRFile:                   \"{}\"\n".format(data))
        data = header["ShowAMRFile"]
        f.write("ShowAMRFile:                   {}\n".format(data))
        data = header["ImageIndex"]
        f.write("ImageIndex:                    {}\n".format(data))
        data = header["LayoutNColumns"]
        f.write("LayoutNColumns:                {}\n".format(data))
        data = header["LayoutNRows"]
        f.write("LayoutNRows:                   {}\n".format(data))
        data = header["LayoutZoomLevel"]
        f.write("LayoutZoomLevel:               {}\n".format(data))
        data = header["SegmentSize"]
        f.write("SegmentSize:                   {}\n".format(data))
        data = header["SegmentOffset"]
        f.write("SegmentOffset:                 {}\n".format(data))
        data = header["NrOfLinkedProtocols"]
        f.write("NrOfLinkedProtocols:           {}\n".format(data))
        if "ProtocolFile" in header:
            data = header["ProtocolFile"]
        else:
            data = ""
        f.write("ProtocolFile:                  \"{}\"\n".format(data))
        data = header["InplaneResolutionX"]
        f.write("InplaneResolutionX:            {}\n".format(data))
        data = header["InplaneResolutionY"]
        f.write("InplaneResolutionY:            {}\n".format(data))
        data = header["SliceThickness"]
        f.write("SliceThickness:                {}\n".format(data))
        data = header["SliceGap"]
        f.write("SliceGap:                      {}\n".format(data))
        data = header["VoxelResolutionVerified"]
        f.write("VoxelResolutionVerified:       {}\n".format(data))
        f.write("\n")

        # ---------------------------------------------------------------------
        # Position information
        f.write("\n")
        f.write("PositionInformationFromImageHeaders\n")
        f.write("\n")
        data = info_pos["PosInfosVerified"]
        f.write("PosInfosVerified: {}\n".format(data))
        data = info_pos["CoordinateSystem"]
        f.write("CoordinateSystem: {}\n".format(data))
        data = info_pos["Slice1CenterX"]
        f.write("Slice1CenterX:    {}\n".format(data))
        data = info_pos["Slice1CenterY"]
        f.write("Slice1CenterY:    {}\n".format(data))
        data = info_pos["Slice1CenterZ"]
        f.write("Slice1CenterZ:    {}\n".format(data))
        data = info_pos["SliceNCenterX"]
        f.write("SliceNCenterX:    {}\n".format(data))
        data = info_pos["SliceNCenterY"]
        f.write("SliceNCenterY:    {}\n".format(data))
        data = info_pos["SliceNCenterZ"]
        f.write("SliceNCenterZ:    {}\n".format(data))
        data = info_pos["RowDirX"]
        f.write("RowDirX:          {}\n".format(data))
        data = info_pos["RowDirY"]
        f.write("RowDirY:          {}\n".format(data))
        data = info_pos["RowDirZ"]
        f.write("RowDirZ:          {}\n".format(data))
        data = info_pos["ColDirX"]
        f.write("ColDirX:          {}\n".format(data))
        data = info_pos["ColDirY"]
        f.write("ColDirY:          {}\n".format(data))
        data = info_pos["ColDirZ"]
        f.write("ColDirZ:          {}\n".format(data))
        data = info_pos["NRows"]
        f.write("NRows:            {}\n".format(data))
        data = info_pos["NCols"]
        f.write("NCols:            {}\n".format(data))
        data = info_pos["FoVRows"]
        f.write("FoVRows:          {}\n".format(data))
        data = info_pos["FoVCols"]
        f.write("FoVCols:          {}\n".format(data))
        data = info_pos["SliceThickness"]
        f.write("SliceThickness:   {}\n".format(data))
        data = info_pos["GapThickness"]
        f.write("GapThickness:     {}\n".format(data))
        f.write("\n")

        # ---------------------------------------------------------------------
        # Transformations section
        if info_tra["NrOfPastSpatialTransformations"] > 0:
            f.write("\n")
            data = info_tra["NrOfPastSpatialTransformations"]
            f.write("NrOfPastSpatialTransformations: {}\n".format(data))

            f.write("\n")
            data = info_tra["NameOfSpatialTransformation"]
            f.write("NameOfSpatialTransformation: {}\n".format(data))
            data = info_tra["TypeOfSpatialTransformation"]
            f.write("TypeOfSpatialTransformation: {}\n".format(data))
            data = info_tra["AppliedToFileName"]
            f.write("AppliedToFileName:           {}\n".format(data))
            data = info_tra["NrOfTransformationValues"]
            f.write("NrOfTransformationValues:    {}\n".format(data))

            affine = info_tra["Transformation matrix"]
            for i in range(4):
                f.write(" {:8.5f}  ".format(affine[i, 0]))
                f.write(" {:8.5f}  ".format(affine[i, 1]))
                f.write(" {:8.5f}  ".format(affine[i, 2]))
                f.write(" {:8.5f}  \n".format(affine[i, 3]))
            f.write("\n")

        # -----------------------------------------------------------------
        # This part only contains a single information
        f.write("\n")
        data = header["LeftRightConvention"]
        f.write("LeftRightConvention: {}\n".format(data))
        f.write("\n")

        # -----------------------------------------------------------------
        # Multiband section
        if len(info_multiband.keys()) > 0:
            f.write("\n")
            data = info_multiband["FirstDataSourceFile"]
            f.write("FirstDataSourceFile: {}\n".format(data))

            f.write("\n")
            data = info_multiband["MultibandSequence"]
            f.write("MultibandSequence: {}\n".format(data))
            data = info_multiband["MultibandFactor"]
            f.write("MultibandFactor:   {}\n".format(data))

            f.write("\n")
            data = info_multiband["SliceTimingTableSize"]
            f.write("SliceTimingTableSize: {}\n".format(data))
            slice_timings = info_multiband["Slice timings"]
            for i in range(info_multiband["SliceTimingTableSize"]):
                f.write("{}\n".format(slice_timings[i]))

            f.write("\n")
            data = info_multiband["AcqusitionTime"]
            f.write("AcqusitionTime: {}\n".format(data))
            f.write("\n")

    # -------------------------------------------------------------------------
    # Write voxel data as a separate STC file
    dirname = os.path.dirname(filename)
    filename_stc = os.path.join(dirname, "{}.stc".format(basename))
    write_stc(filename_stc, data_img, data_type=header["DataType"])


def create_fmr():
    """Create BrainVoyager FMR file with default values."""
    header = dict()
    info_pos = dict()

    header["FileVersion"] = 7
    header["NrOfVolumes"] = 10
    header["NrOfSlices"] = 64
    header["NrOfSkippedVolumes"] = 0
    header["Prefix"] = "bvbabel_default_fmr"
    header["DataStorageFormat"] = 2
    header["DataType"] = 2
    header["TR"] = 2000
    header["InterSliceTime"] = 31
    header["TimeResolutionVerified"] = 1
    header["TE"] = 30
    header["SliceAcquisitionOrder"] = 5
    header["SliceAcquisitionOrderVerified"] = 1
    header["ResolutionX"] = 100
    header["ResolutionY"] = 100
    header["LoadAMRFile"] = ""
    header["ShowAMRFile"] = 1
    header["ImageIndex"] = 0
    header["LayoutNColumns"] = 8
    header["LayoutNRows"] = 8
    header["LayoutZoomLevel"] = 1
    header["SegmentSize"] = 10
    header["SegmentOffset"] = 0
    header["NrOfLinkedProtocols"] = 0
    header["ProtocolFile"] = ""
    header["InplaneResolutionX"] = 2
    header["InplaneResolutionY"] = 2
    header["SliceThickness"] = 2
    header["SliceGap"] = 0
    header["VoxelResolutionVerified"] = 1

    # -------------------------------------------------------------------------
    # Position information
    info_pos["PosInfosVerified"] = 1
    info_pos["CoordinateSystem"] = 1
    info_pos["Slice1CenterX"] = -8.34283
    info_pos["Slice1CenterY"] = -13.0168
    info_pos["Slice1CenterZ"] = -12.9074
    info_pos["SliceNCenterX"] = -8.34283
    info_pos["SliceNCenterY"] = 23.4012
    info_pos["SliceNCenterZ"] = 107.715
    info_pos["RowDirX"] = 1
    info_pos["RowDirY"] = 0
    info_pos["RowDirZ"] = 0
    info_pos["ColDirX"] = 0
    info_pos["ColDirY"] = 0.957319
    info_pos["ColDirZ"] = -0.289032
    info_pos["NRows"] = 100
    info_pos["NCols"] = 100
    info_pos["FoVRows"] = 200
    info_pos["FoVCols"] = 200
    info_pos["SliceThickness"] = 2
    info_pos["GapThickness"] = 0

    header["Position information"] = info_pos
    # -------------------------------------------------------------------------
    # Transformations section
