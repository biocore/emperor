# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import division


from sys import argv
from os.path import abspath
from datetime import datetime
from StringIO import StringIO
from socket import gethostname

import numpy as np

from emperor.util import (keep_columns_from_mapping_file,
                          get_emperor_library_version)
from emperor._format_strings import (_ELLIPSE_OPACITY_SLIDER,
                                     _VECTORS_OPACITY_SLIDER,
                                     _TAXA_LABELS_SELECTOR,
                                     _TAXA_LABELS_COLOR_SELECTOR,
                                     _BIPLOT_VISIBILITY_SELECTOR,
                                     _BIPLOT_SPHERES_COLOR_SELECTOR,
                                     _EDGES_VISIBILITY_SELECTOR,
                                     _EDGES_COLOR_SELECTOR,
                                     _EMPEROR_FOOTER_HTML_STRING)
from emperor.qiime_backports.format import format_mapping_file
from emperor.qiime_backports.parse import mapping_file_to_dict
from emperor.qiime_backports.filter import (
    sample_ids_from_metadata_description)
from emperor.qiime_backports.util import MetadataMap


class EmperorLogicError(ValueError):
    """Exception raised when a requirement for the Emperor GUI is not met"""
    pass


def format_pcoa_to_js(header, coords, pct_var, custom_axes=[],
                      coords_low=None, coords_high=None, number_of_axes=10,
                      number_of_segments=8):
    """Write the javascript necessary to represent a pcoa file in emperor

    Parameters
    ----------
    header : list of str
        sample names for the pcoa file 1-D array
    coords : array_like
        coordinates of the PCoA file, 2-D array
    pct_var : array_like
        percentage of variation of the PCoA file, 1-D array
    custom_axes : list of str, optional
        list of category names for the custom axes
    coords_low : array_like, optional
        coordinates representing the lower edges of an ellipse
    coords_high : array_like, optional
        coordinates representing the highere edges of an ellipse
    number_of_axes : int, optional
        number of axes to be returned
    number_of_segments : int, optional
        number of segments and rings for each sphere

    Returns
    -------
    str
        javascript representation of the PCoA data inputed, contains a list of
        spheres, list of ellipses (if coords_low and coords_high are present)
        and several setup variables.

    Raises
    ------
    EmperorLogicError
        If the variation explained by at least three axes is not greater than
        0.01.

    Notes
    -----
    Formats the output of qiime_backports.parse.parse_coords_file into
    javascript variable declarations.
    """

    # validating that the number of coords in coords
    if number_of_axes > len(coords[0]):
        number_of_axes = len(coords[0])

    # validating that all the axes are above 0.01%, this accounts for really
    # small variations explained in some axes that end up being not practical
    # as the GUI has some problems when presenting those values on screen
    valid_pcoalabels = len([i for i in pct_var if i > 0.01])
    if number_of_axes > valid_pcoalabels:
        number_of_axes = valid_pcoalabels
    if number_of_axes < 3:
        raise EmperorLogicError("Due to the variation explained, Emperor "
                                "could not plot at least 3 axes, check the "
                                "input files to ensure that the percent "
                                "explained is greater than 0.01 in at least "
                                "three axes.")

    # ranges for the PCoA space
    max_x = np.max(coords[:, 0:1])
    max_y = np.max(coords[:, 1:2])
    max_z = np.max(coords[:, 2:3])
    min_x = np.min(coords[:, 0:1])
    min_y = np.min(coords[:, 1:2])
    min_z = np.min(coords[:, 2:3])
    maximum = np.max(np.abs(coords[:, :number_of_axes]))
    pcoalabels = pct_var[:number_of_axes]

    radius = (max_x-min_x)*.012

    # write the values for all the spheres
    pcoa_str = []
    pcoa_str.append('\nvar g_spherePositions = new Array();\n')
    for point, coord in zip(header, coords):
        pcnts = ["'P%d': %f" % (i+1, coord[i]) for i in range(number_of_axes)]
        all_coords = ', '.join(pcnts)
        pcoa_str.append("g_spherePositions['%s'] = { 'name': '%s', 'color': "
                        "0, 'x': %f, 'y': %f, 'z': %f, %s };\n" %
                        (point, point, coord[0], coord[1], coord[2],
                         all_coords))

    # write the values for all the ellipses
    pcoa_str.append('\nvar g_ellipsesDimensions = new Array();\n')
    if coords_low is not None and coords_high is not None:
        for s_header, s_coord, s_low, s_high in zip(header, coords, coords_low,
                                                    coords_high):
            delta = np.abs(s_high - s_low)
            pcnts = ["'P%d': %f" % (i + 1, s_coord[i]) for i in
                     range(number_of_axes)]
            all_coords = ', '.join(pcnts)

            pcoa_str.append("g_ellipsesDimensions['%s'] = { 'name': '%s', "
                            "'color': 0, 'width': %f, 'height': %f, 'length': "
                            "%f , 'x': %f, 'y': %f, 'z': %f, %s }\n" %
                            (s_header, s_header, delta[0], delta[1], delta[2],
                             s_coord[0], s_coord[1], s_coord[2], all_coords))

    pcoa_str.append('var g_segments = %d, g_rings = %d, g_radius = %f;\n' %
                    (number_of_segments, number_of_segments, radius))
    pcoa_str.append('var g_xAxisLength = %f;\n' % (np.abs(max_x) +
                                                   np.abs(min_x)))
    pcoa_str.append('var g_yAxisLength = %f;\n' % (np.abs(max_y) +
                                                   np.abs(min_y)))
    pcoa_str.append('var g_zAxisLength = %f;\n' % (np.abs(max_z) +
                                                   np.abs(min_z)))
    pcoa_str.append('var g_xMaximumValue = %f;\n' % (max_x))
    pcoa_str.append('var g_yMaximumValue = %f;\n' % (max_y))
    pcoa_str.append('var g_zMaximumValue = %f;\n' % (max_z))
    pcoa_str.append('var g_xMinimumValue = %f;\n' % (min_x))
    pcoa_str.append('var g_yMinimumValue = %f;\n' % (min_y))
    pcoa_str.append('var g_zMinimumValue = %f;\n' % (min_z))
    pcoa_str.append('var g_maximum = %f;\n' % maximum)

    offset = 0

    # create three vars, pc1, pc2 and pc3 if no custom_axes are passed, then
    # use the values of the percent explained by the PCoA; if custom_axes are
    # passed use as many as you can (since customs axes can be either [0, 1, 2,
    # 3])
    for i in range(0, 3):
        try:
            pcoa_str.append('var g_pc%dLabel = \"%s\";\n' % (i + 1,
                                                             custom_axes[i]))
            # offset will help us retrieve the correct pcoalabels val
            offset += 1
        except:
            # if there are custom axes then subtract the number of custom axes
            pcoa_str.append('var g_pc%dLabel = \"PC%d (%.2f %%)\";\n' %
                            (i + 1, i + 1 - offset, pcoalabels[i - offset]))
    pcoa_str.append('var g_number_of_custom_axes = %d;\n' % offset)

    js_pcts = []
    js_pcts_round = []
    if custom_axes is None:
        custom_axes = []
    for element in custom_axes + list(pct_var[:number_of_axes]):
        try:
            # scale the percent so it's a number from 0 to 1
            js_pcts.append('%f' % (float(element)/100))
            js_pcts_round.append('%.2f' % (element))
        except ValueError:
            js_pcts.append('%f' % (float(pct_var[0]/100)))
            js_pcts_round.append('%.2f' % (pct_var[0]))
    pcoa_str.append('var g_fractionExplained = [%s];\n' % ', '.join(js_pcts))
    pcoa_str.append('var g_fractionExplainedRounded = [%s];\n' %
                    ', '.join(js_pcts_round))

    return ''.join(pcoa_str)


def format_mapping_file_to_js(mapping_file_data, mapping_file_headers,
                              columns):
    """Write a javascript representation of the mapping file

    Parameters
    ----------
    mapping_file_data : list of str
        contents of the mapping file
    mapping_file_headers : list of list of str
        headers of the mapping file
    columns : list of str
        valid columns to use, usually a subset of mapping_file_headers

    Returns
    -------
    str
        JavaScript representation of the mapping file
    """
    map_str = []

    mapping_file_dict = mapping_file_to_dict(mapping_file_data,
                                             mapping_file_headers)

    map_values = []
    for k, v in mapping_file_dict.items():
        if 'SampleID' in columns:
            vals = ["'%s'" % k] + ["'%s'" % v[col]
                                   for col in mapping_file_headers[1:]]
        else:
            vals = ["'%s'" % v[col] for col in mapping_file_headers[1:]]
        map_values.append("'%s': [%s]" % (k, ','.join(vals)))

    if 'SampleID' not in columns:
        mapping_file_headers = mapping_file_headers[1:]

    # format the mapping file as javascript objects
    map_str.append('var g_mappingFileHeaders = [%s];\n' %
                   ','.join(["'%s'" % col for col in mapping_file_headers]))
    map_str.append('var g_mappingFileData = { %s };\n' % ','.join(map_values))

    map_object = MetadataMap(mapping_file_dict, [])
    # make sure the comparison for SampleID is made first because otherwise
    # if the metadata map tries to check 'SampleID' it will raise an exception
    animatable_categories = [category for category in columns
                             if category != 'SampleID' and
                             map_object.isNumericCategory(category)]
    map_str.append('var g_animatableMappingFileHeaders = [%s];\n' %
                   ','.join(["'%s'" % col for col in animatable_categories]))

    return ''.join(map_str)


def format_taxa_to_js(otu_coords, lineages, prevalence, min_taxon_radius=0.5,
                      max_taxon_radius=5, radius=1.0):
    """Write a string representing the taxa in a PCoA plot as javascript

    Parameters
    ----------
    otu_coords : array_like
        Numpy array where the taxa is positioned
    lineages : array_like
        Label for each of these lineages
    prevalence : array_like
        Score of prevalence for each of the taxa that is drawn
    min_taxon_radius : float, optional
        Smallest radius for a sphere.
    max_taxon_radius : float, optional
        Largest radius for a spehere.
    radius : float, optional
        Base radius for a sphere.

    Outputs
    -------
    str
        JavaScript string where the taxa information is written to create the
        spheres representing each of these, will return only the variable
        declaration if the inputs are empty.

    Notes
    -----
    These parameters should work more as constants and once we find out that
    there's a value that is too big to be presented, the proper checks should
    be put into place. Currently we haven't found such cases in any study*
    min_taxon_radius: minimum value for the radius of the spheres on the plot
    max_taxon_radious: maximum value for the radius of the spheres on the plot
    radius: default value size
    """
    js_biplots_string = []
    js_biplots_string.append('\nvar g_taxaPositions = new Array();\n')

    # if we have prevalence scores, calculate the taxa radii values
    if len(prevalence):
        taxa_radii = radius * (min_taxon_radius + (max_taxon_radius -
                               min_taxon_radius) * prevalence)
    else:
        taxa_radii = []

    index = 0

    # write the data in the form of a dictionary
    for taxa_label, taxa_coord, t_radius in zip(lineages,
                                                otu_coords, taxa_radii):
        js_biplots_string.append("g_taxaPositions['%d'] = { 'lineage': '%s', "
                                 "'x': %f, 'y': %f, 'z': %f, 'radius': %f};\n"
                                 % (index, taxa_label, taxa_coord[0],
                                    taxa_coord[1], taxa_coord[2], t_radius))
        index += 1
    js_biplots_string.append('\n')

    # join the array of strings as a single string
    return ''.join(js_biplots_string)


def format_vectors_to_js(mapping_file_data, mapping_file_headers, coords_data,
                         coords_headers, connected_by_header,
                         sorted_by_header=None):
    """Write a string representing the vectors in a PCoA plot as javascript

    Parameters
    ----------
    mapping_file_data : list of list of str
        contents of the mapping file
    mapping_file_headers : list of str
        headers of the mapping file
    coords_data : array_like
        coordinates of the PCoA plot in a numpy 2-D array or a list of numpy
        2-D arrays for jackknifed input
    coords_headers : list of str
        headers of the coords in the PCoA plot or a list of lists with the
        headers for jackknifed input
    connected_by_header : list of str
        header of the mapping file that represents how the lines will be
        connected
    sorted_by_header : str, optional
        numeric-only header name to sort the samples in the vectors

    Returns
    -------
    str
        string that represents the vectors in the shape of a javascript object

    Notes
    -----
    If using jackknifed input, the coordinates and headers that will be used
    are the ones belonging to the master coords i. e. the first element.
    """

    vectors_str = []
    vectors_str.append('\nvar g_vectorPositions = new Array();\n')

    if connected_by_header is not None:
        # check if we are processing jackknifed input, if so just get the
        # master
        if type(coords_data) == list:
            coords_data = coords_data[0]
            coords_headers = coords_headers[0]

        columns_to_keep = ['SampleID', connected_by_header]

        # do not ad None if sorted_by_header is None or empty
        if sorted_by_header:
            columns_to_keep.append(sorted_by_header)

        # reduce the amount of data by keeping the required fields only
        mapping_file_data, mapping_file_headers =\
            keep_columns_from_mapping_file(mapping_file_data,
                                           mapping_file_headers,
                                           columns_to_keep)

        # format the mapping file to use this with the filtering function
        mf_string = format_mapping_file(mapping_file_headers,
                                        mapping_file_data)

        index = mapping_file_headers.index(connected_by_header)
        connected_by = list(set([line[index] for line in mapping_file_data]))

        for category in connected_by:
            # convert to StringIO to for each iteration; else the object
            # won't be usable after the first iteration & you'll get an error
            sample_ids = sample_ids_from_metadata_description(StringIO(
                mf_string), '%s:%s' % (connected_by_header, category))

            # if there is a sorting header, sort the coords using these values
            if sorted_by_header:
                sorting_index = mapping_file_headers.index(sorted_by_header)
                to_sort = [line for line in mapping_file_data if line[0] in
                           sample_ids]

                # get the sorted sample ids from the sorted-reduced mapping
                # file
                sample_ids = zip(
                    *sorted(to_sort, key=lambda x: float(x[sorting_index])))[0]

            # each category value is a new vector
            vectors_str.append("g_vectorPositions['%s'] = new Array();\n"
                               % category)

            for s in sample_ids:
                index = coords_headers.index(s)

                # print the first three elements of each coord for each sample
                vectors_str.append("g_vectorPositions['%s']['%s'] = %s;\n"
                                   % (category, s,
                                      coords_data[index, :3].tolist()))

    return ''.join(vectors_str)


def format_comparison_bars_to_js(coords_data, coords_headers, clones,
                                 is_serial_comparison=True):
    """Format coordinates data to create a comparison plot

    Parameters
    ----------
    coords_data : array_like
        numpy array with the replicated coordinates
    coords_headers : list of str
        list with the headers for each of replicated coordinates
    clones : int
        number of replicates in the coords_data and coords_headers
    is_serial_comparison : bool, optional
        whether the samples will be connected one after the other (True) or all
        will originate in the first set of coordinates.

    Returns
    -------
    str
        JavaScript object that contains the data for the comparison plot

    Raises
    ------
    AssertionError
        If the coords_data and coords_headers don't have the same length.
        If the number of clones doesn't concord with the samples being
        presented.

    Notes
    -----
    Unless the value of clones is > 0 this function will return an empty
    javascript object initialization.
    """

    comparison_str = []
    comparison_str.append('\nvar g_comparisonPositions = new Array();\n')

    if is_serial_comparison:
        comparison_str.append('var g_isSerialComparisonPlot = true;\n')
    else:
        comparison_str.append('var g_isSerialComparisonPlot = false;\n')

    if clones:
        headers_length = len(coords_headers)

        # assert some sanity checks
        assert headers_length == len(coords_data), ("The coords data and"
                                                    "the coords headers must "
                                                    "have the same length")
        assert headers_length % clones == 0, ("There has to be an exact number"
                                              "of clones of the data")

        # get the indices that the sample names get sorted by, this will group
        # all the samples with the same prefix together, and since the suffixes
        # are numeric, the samples will be one after the other i. e. sample_0,
        # sample_1, sample_2 and other_0, other_1, other_2 and so on. With
        # these indices sort the coordinates and then the headers themselves,
        # though convert to a numpy array first & back to a list to avoid
        # sorting again
        indices = np.argsort(coords_headers)
        coords_data = coords_data[indices, :]
        coords_headers = np.array(coords_headers)[indices].tolist()

        # in steps of the number of clones iterate through the headers and the
        # coords to create the javascript object with the coordinates
        for index in xrange(0, headers_length, clones):
            # 1st object must have _0 as a suffix, trim it reveal the sample id
            assert coords_headers[index].endswith('_0'), ("There's an internal"
                                                          " inconsistency with"
                                                          " the sample ids")
            sample_id = coords_headers[index][:-2]

            # convert all elements in the numpy array into a string before
            # formatting the elements into the javascript dictionary object
            comparison_str.append("g_comparisonPositions['%s'] = [%s];\n" %
                                  (sample_id, str(', '.join(map(str,
                                   coords_data[index:(index + clones),
                                               0:3].tolist())))))
    return ''.join(comparison_str)


def format_emperor_html_footer_string(has_biplots=False, has_ellipses=False,
                                      has_vectors=False, has_edges=False):
    """Format a footer according to the things being presented in the plot

    This function will remove unnecessary GUI elements from index.html to avoid
    confusions i. e. showing an ellipse opacity slider when there are no
    ellipses in the plot.

    Parameters
    ----------
    has_biplots : bool, optional
        whether the plot has biplots or not
    has_ellipses : bool, optional
        whether the plot has ellipses or not
    has_vectors : bool, optional
        whether the plot has vectors or not
    has_edges : bool, optional
        whether the plot has edges between samples (comparison plot)

    Returns
    -------
    str
        Formatted footer string
    """

    # we use python's built-in ternary operator to add or not a string
    # see _EMPEROR_FOOTER_HTML_STRING
    format_dict = {'biplot_spheres_color_selector':
                   _BIPLOT_SPHERES_COLOR_SELECTOR if has_biplots else '',
                   'biplot_visibility_selector':
                   _BIPLOT_VISIBILITY_SELECTOR if has_biplots else '',
                   'taxa_labels_selector':
                   _TAXA_LABELS_SELECTOR if has_biplots else '',
                   'taxa_labels_color_selector':
                   _TAXA_LABELS_COLOR_SELECTOR if has_biplots else '',
                   'edges_color_selector':
                   _EDGES_COLOR_SELECTOR if has_edges else '',
                   'ellipse_opacity_slider':
                   _ELLIPSE_OPACITY_SLIDER if has_ellipses else '',
                   'vectors_opacity_slider':
                   _VECTORS_OPACITY_SLIDER if has_vectors else '',
                   'edges_visibility_selector':
                   _EDGES_VISIBILITY_SELECTOR if has_edges else ''}

    return _EMPEROR_FOOTER_HTML_STRING.format(**format_dict)


def format_emperor_autograph(metadata_fp, coords_fp, language='HTML'):
    """Create a signature with some meta-data of the Emperor package

    Parameters
    ----------
    metadata_fp : str
        Absolute file path to the metadata mapping file
    coords_fp : str
        Absolute file path to the coordinates file
    language : {'HTML', 'Python', 'C', 'Bash'}, optional
        Language to which it will be formatted as a multi-line comment

    Returns
    -------
    str
        String with information about the executed command

    Raises
    ------
    AssertionError
        If the file is not allowed.
    """

    # supported open and closing of multi-line comments for different languages
    _languages = {'HTML': ('<!--', '-->'), 'Python': ('"""', '"""'),
                  'C': ('/*', '*/'), 'Bash': ('<<COMMENT', 'COMMENT')}

    assert language in _languages.keys(), ('%s is not a supported language' %
                                           language)

    autograph = []
    autograph.append(_languages[language][0])
    autograph.append("*Summary of Emperor's Information*")

    # add the day and time at which the command was called
    autograph.append(datetime.now().strftime('Command executed on %B %d, %Y at'
                                             ' %H:%M:%S'))

    # add library version and SHA-1 if available
    autograph.append('Emperor Version: %s' % get_emperor_library_version())
    autograph.append('HostName: %s' % gethostname())

    # full path to input files
    autograph.append('Metadata: %s' % abspath(metadata_fp))
    autograph.append('Coordinates: %s' % abspath(coords_fp))

    if any([True for element in argv if 'make_emperor.py' in element]):
        autograph.append('Command: %s' % ' '.join(argv))
    else:
        autograph.append('Command: Cannot find direct call to make_emperor.py')
    autograph.append(_languages[language][1])

    return '%s' % '\n'.join(autograph)
