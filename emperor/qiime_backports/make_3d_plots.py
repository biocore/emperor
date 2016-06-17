#!/usr/bin/env python
#file make_3d_plots.py

__author__ = "Dan Knights"
__copyright__ = "Copyright 2011, The QIIME Project" 
__credits__ = ["Dan Knights"]
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from numpy import (array, append, transpose, column_stack, hstack,
    apply_along_axis, nan, isnan, asarray)

def get_custom_coords(axis_names,mapping, coords):
    """Gets custom axis coords from the mapping file.
       Appends custom as first column(s) of PCoA coords matrix.

       Params:
        axis_names, the names of headers of mapping file columns
        mapping, the mapping file object (with list of headers in element 0)
        coords, the PCoA coords object, with coords matrix in element 1
    """
    for i, axis in enumerate(reversed(axis_names)):
        if not axis in mapping[0]:
            raise ValueError('Warning: could not find custom axis %s in map '
                             'headers: %s' % (axis, mapping[0]))
        else:
            # get index of column in mapping file
            col_idx = mapping[0].index(axis)
            # extract column data
            col = list(zip(*mapping[1:]))[col_idx]
            sample_IDs = list(zip(*mapping[1:]))[0]
            new_coords = array([])
            # load custom coord for this axis for each sample ID 
            for id in coords[0]:
                if id in sample_IDs:
                    row_idx = list(sample_IDs).index(id)
                    try:
                        as_float = float(col[row_idx])
                        new_coords = append(new_coords,as_float)
                    except ValueError:
                        new_coords = append(new_coords,nan)
            new_coords = transpose(column_stack(new_coords))
            # append new coords to beginning column of coords matrix
            coords[1] = hstack((new_coords,coords[1]))

def remove_nans(coords):
    """Deletes any samples with NANs in their coordinates"""
    s = apply_along_axis(sum,1,isnan(coords[1])) == 0
    coords[0] = (asarray(coords[0])[s]).tolist()
    coords[1] = coords[1][s,:]

def scale_custom_coords(custom_axes,coords):
    """Scales custom coordinates to match min/max of PC1"""

    # the target min and max
    to_mn = min(coords[1][:,len(custom_axes)])
    to_mx = 2*max(coords[1][:,len(custom_axes)])

    # affine transformation for each custom axis
    for i in range(len(custom_axes)):
        from_mn = min(coords[1][:,i])
        from_mx = max(coords[1][:,i])
        coords[1][:,i] = (coords[1][:,i]  - from_mn) / (from_mx - from_mn)
        coords[1][:,i] = (coords[1][:,i]) * (to_mx-to_mn) + to_mn
