#!/usr/bin/env python
# File created on 24 Jan 2013
from __future__ import division

__author__ = "Antonio Gonzalez Pena"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Meg Pirrung", "Antonio Gonzalez Pena", "Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "0.9.51"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Release"


from sys import argv
from copy import deepcopy
from os.path import abspath
from datetime import datetime
from StringIO import StringIO
from socket import gethostname

from numpy import max, min, abs, argsort, array

from emperor.util import (keep_columns_from_mapping_file,
    get_emperor_library_version)

from emperor.qiime_backports.format import format_mapping_file
from emperor.qiime_backports.parse import (mapping_file_to_dict,
    parse_mapping_file)
from emperor.qiime_backports.filter import (
    filter_mapping_file_by_metadata_states,sample_ids_from_metadata_description)
from emperor.qiime_backports.util import MetadataMap
from emperor.qiime_backports import __version__ as qiime_backports_version

class EmperorLogicError(ValueError):
    """Exception raised when a requirement for the Emperor GUI is not met"""
    pass

def format_pcoa_to_js(header, coords, eigvals, pct_var, custom_axes=[],
                    coords_low=None, coords_high=None, number_of_axes=10,
                    number_of_segments=8):
    """Write the javascript necessary to represent a pcoa file in emperor

    Inputs:
    header: sample names for the pcoa file 1-D array
    coords: coordinates of the PCoA file, 2-D array
    eigvals: eigen-values of the PCoA file, 1-D array
    pct_var: percentage of variation of the PCoA file, 1-D array
    custom_axes: list of category names for the custom axes
    coords_low: coordinates representing the lower edges of an ellipse
    coords_high: coordinates representing the highere edges of an ellipse
    number_of_axes: number of axes to be returned
    number_of_segments: number of segments and rings for each sphere

    Output:
    string: javascript representation of the PCoA data inputed, contains a list
    of spheres, list of ellipses (if coords_low and coords_high are present) and
    several setup variables.

    Formats the output of qiime.parse.parse_coords_file into javascript variable
    declarations.
    """
    js_pcoa_string = ''

    # validating that the number of coords in coords
    if number_of_axes>len(coords[0]):
        number_of_axes = len(coords[0])

    # validating that all the axes are above 0.01%, this accounts for really
    # small variations explained in some axes that end up being not practical
    # as the GUI has some problems when presenting those values on screen
    valid_pcoalabels = len([i for i in pct_var if i>0.01])
    if number_of_axes>valid_pcoalabels:
        number_of_axes = valid_pcoalabels
    if number_of_axes < 3:
        raise EmperorLogicError("Due to the variation explained, Emperor "
                                "could not plot at least 3 axes, check the "
                                "input files to ensure that the percent "
                                "explained is greater than 0.01 in at least "
                                "three axes.")

    # ranges for the PCoA space
    max_x = max(coords[:,0:1])
    max_y = max(coords[:,1:2])
    max_z = max(coords[:,2:3])
    min_x = min(coords[:,0:1])
    min_y = min(coords[:,1:2])
    min_z = min(coords[:,2:3])
    maximum = max(abs(coords[:,:number_of_axes]))
    pcoalabels = pct_var[:number_of_axes]

    radius = (max_x-min_x)*.012

    # write the values for all the spheres
    js_pcoa_string += '\nvar g_spherePositions = new Array();\n'
    for point, coord in zip(header, coords):
        all_coords = ', '.join(["'P%d': %f" % (i+1,coord[i]) for i in range(number_of_axes)])
        js_pcoa_string += ("g_spherePositions['%s'] = { 'name': '%s', 'color': "
            "0, 'x': %f, 'y': %f, 'z': %f, %s };\n" % (point, point, coord[0],
            coord[1],coord[2], all_coords))

    # write the values for all the ellipses
    js_pcoa_string += '\nvar g_ellipsesDimensions = new Array();\n'
    if coords_low is not None and coords_high is not None:
        for s_header, s_coord, s_low, s_high in zip(header, coords, coords_low,
            coords_high):
            delta = abs(s_high-s_low)
            all_coords = ', '.join(["'P%d': %f" % (i+1,s_coord[i]) for i in range(number_of_axes)])
            js_pcoa_string += ("g_ellipsesDimensions['%s'] = { 'name': '%s', "
                "'color': 0, 'width': %f, 'height': %f, 'length': %f , 'x': %f,"
                " 'y': %f, 'z': %f, %s }\n" % (s_header, s_header,delta[0], delta[1],
                delta[2], s_coord[0], s_coord[1], s_coord[2], all_coords))

    js_pcoa_string += 'var g_segments = %d, g_rings = %d, g_radius = %f;\n' % (number_of_segments,
        number_of_segments, radius)
    js_pcoa_string += 'var g_xAxisLength = %f;\n' % (abs(max_x)+abs(min_x))
    js_pcoa_string += 'var g_yAxisLength = %f;\n' % (abs(max_y)+abs(min_y))
    js_pcoa_string += 'var g_zAxisLength = %f;\n' % (abs(max_z)+abs(min_z))
    js_pcoa_string += 'var g_xMaximumValue = %f;\n' % (max_x)
    js_pcoa_string += 'var g_yMaximumValue = %f;\n' % (max_y)
    js_pcoa_string += 'var g_zMaximumValue = %f;\n' % (max_z)
    js_pcoa_string += 'var g_xMinimumValue = %f;\n' % (min_x)
    js_pcoa_string += 'var g_yMinimumValue = %f;\n' % (min_y)
    js_pcoa_string += 'var g_zMinimumValue = %f;\n' % (min_z)
    js_pcoa_string += 'var g_maximum = %f;\n' % maximum

    offset = 0

    # create three vars, pc1, pc2 and pc3 if no custom_axes are passed, then use
    # the values of the percent explained by the PCoA; if custom_axes are passed
    # use as many as you can (since customs axes can be either [0, 1, 2, 3])
    for i in range(0, 3):
        try:
            js_pcoa_string += 'var g_pc%dLabel = \"%s\";\n' % (i+1,
                custom_axes[i])
            offset+=1 # offset will help us retrieve the correct pcoalabels val
        except:
            # if there are custom axes then subtract the number of custom axes
            js_pcoa_string += 'var g_pc%dLabel = \"PC%d (%.2f %%)\";\n' %\
                (i+1, i+1-offset, pcoalabels[i-offset])
    js_pcoa_string += 'var g_number_of_custom_axes = %d;\n' % offset

    js_pcts = []
    js_pcts_round = []
    if custom_axes == None: custom_axes = []
    for element in custom_axes + list(pct_var[:number_of_axes]):
        try:
            # scale the percent so it's a number from 0 to 1
            js_pcts.append('%f' % (float(element)/100))
            js_pcts_round.append('%.2f' % (element))
        except ValueError:
            js_pcts.append('%f' % (float(pct_var[0]/100)))
            js_pcts_round.append('%.2f' % (pct_var[0]))
    js_pcoa_string += 'var g_fractionExplained = [%s];\n' % ', '.join(js_pcts)
    js_pcoa_string += 'var g_fractionExplainedRounded = [%s];\n' % ', '.join(js_pcts_round)

    return js_pcoa_string

def format_mapping_file_to_js(mapping_file_data, mapping_file_headers, columns):
    """Write a javascript representation of the mapping file

    Inputs:
    mapping_file_data: contents of the mapping file
    mapping_file_headers: headers of the mapping file
    columns: valid columns to use, usually a subset of mapping_file_headers

    Outputs:
    string: javascript representation of the mapping file
    """
    js_mapping_file_string = ''

    mapping_file_dict = mapping_file_to_dict(mapping_file_data,
        mapping_file_headers)

    map_values = []
    for k,v in mapping_file_dict.items():
        if 'SampleID' in columns:
            vals = ["'%s'" % k] + ["'%s'" % v[col]\
                for col in mapping_file_headers[1:]]
        else:
            vals = ["'%s'" % v[col] for col in mapping_file_headers[1:]]
        map_values.append("'%s': [%s]" % (k, ','.join(vals)))

    if 'SampleID' not in columns:
        mapping_file_headers = mapping_file_headers[1:]

    # format the mapping file as javascript objects
    js_mapping_file_string += 'var g_mappingFileHeaders = [%s];\n' % ','.join(
        ["'%s'" % col for col in mapping_file_headers])
    js_mapping_file_string += 'var g_mappingFileData = { %s };\n' % ','.join(
        map_values)

    map_object = MetadataMap(mapping_file_dict, [])
    # make sure the comparison for SampleID is made first because otherwise
    # if the metadata map tries to check 'SampleID' it will raise an exception
    animatable_categories = [category for category in columns\
        if category != 'SampleID' and map_object.isNumericCategory(category)]
    js_mapping_file_string += 'var g_animatableMappingFileHeaders = [%s];\n' %\
        ','.join(["'%s'" % col for col in animatable_categories])

    return js_mapping_file_string

def format_taxa_to_js(otu_coords, lineages, prevalence, min_taxon_radius=0.5,
                    max_taxon_radius=5, radius=1.0):
    """Write a string representing the taxa in a PCoA plot as javascript

    Inputs:
    otu_coords: numpy array where the taxa is positioned
    lineages: label for each of these lineages
    prevalence: score of prevalence for each of the taxa that is drawn

    *These parameters should work more as constants and once we find out that
    there's a value that is too big to be presented, the proper checks should
    be put into place. Currently we haven't found such cases in any study*
    min_taxon_radius: minimum value for the radius of the spheres on the plot
    max_taxon_radious: maximum value for the radius of the spheres on the plot
    radius: default value size

    Outputs:
    js_biplots_string: javascript string where the taxa information is written
    to create the spheres representing each of these, will return only the
    variable declaration if the inputs are empty.
    """
    js_biplots_string = []
    js_biplots_string.append('\nvar g_taxaPositions = new Array();\n')

    # if we have prevalence scores, calculate the taxa radii values
    if len(prevalence):
        taxa_radii = radius*(min_taxon_radius+(max_taxon_radius-
            min_taxon_radius)*prevalence)
    else:
        taxa_radii = []

    index = 0

    # write the data in the form of a dictionary
    for taxa_label, taxa_coord, t_radius in zip(lineages,otu_coords,taxa_radii):
        js_biplots_string.append(("g_taxaPositions['%d'] = { 'lineage': '%s', "
            "'x': %f, 'y': %f, 'z': %f, 'radius': %f};\n") % (index,
            taxa_label, taxa_coord[0], taxa_coord[1], taxa_coord[2], t_radius))
        index += 1
    js_biplots_string.append('\n')
    # join the array of strings as a single string
    return ''.join(js_biplots_string)

def format_vectors_to_js(mapping_file_data, mapping_file_headers, coords_data,
                        coords_headers, connected_by_header,
                        sorted_by_header=None):
    """Write a string representing the vectors in a PCoA plot as javascript

    Inputs:
    mapping_file_data: contents of the mapping file
    mapping_file_headers: headers of the mapping file
    coords_data: coordinates of the PCoA plot in a numpy 2-D array or a list of
    numpy 2-D arrays for jackknifed input
    coords_headers: headers of the coords in the PCoA plot or a list of lists
    with the headers for jackknifed input
    connected_by_header: header of the mapping file that represents how the
    lines will be connected
    sorted_by_header: numeric-only header name to sort the samples in the
    vectors

    Output:
    js_vectors_string: string that represents the vectors in the shape of a
    javascript object

    Notes:
    If using jackknifed input, the coordinates and headers that will be used are
    the ones belonging to the master coords i. e. the first element.
    """

    js_vectors_string = []
    js_vectors_string.append('\nvar g_vectorPositions = new Array();\n')

    if connected_by_header != None:
        # check if we are processing jackknifed input, if so just get the master
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
            mapping_file_headers, columns_to_keep)

        # format the mapping file to use this with the filtering function
        mf_string = format_mapping_file(mapping_file_headers, mapping_file_data)

        index = mapping_file_headers.index(connected_by_header)
        connected_by = list(set([line[index] for line in mapping_file_data]))

        for category in connected_by:
            # convert to StringIO to for each iteration; else the object
            # won't be usable after the first iteration & you'll get an error
            sample_ids = sample_ids_from_metadata_description(
                StringIO(mf_string),'%s:%s' % (connected_by_header,category))

            # if there is a sorting header, sort the coords using these values
            if sorted_by_header:
                sorting_index = mapping_file_headers.index(sorted_by_header)
                to_sort = [line for line in mapping_file_data if line[0] in\
                    sample_ids]

                # get the sorted sample ids from the sorted-reduced mapping file
                sample_ids = zip(*sorted(to_sort,
                    key=lambda x: float(x[sorting_index])))[0]

            # each category value is a new vector
            js_vectors_string.append("g_vectorPositions['%s'] = new Array();\n"
                % (category))

            for s in sample_ids:
                index = coords_headers.index(s)

                # print the first three elements of each coord for each sample
                js_vectors_string.append("g_vectorPositions['%s']['%s'] = %s;\n"
                    % (category, s, coords_data[index, :3].tolist()))

    return ''.join(js_vectors_string)

def format_comparison_bars_to_js(coords_data, coords_headers, clones,
                                is_serial_comparison=True):
    """Format coordinates data to create a comparison plot

    Inputs:
    coords_data: numpy array with the replicated coordinates
    cooreds_headers: list with the headers for each of replicated coordinates
    clones: number of replicates in the coords_data and coords_headers
    is_serial_comparison: whether the samples will be connected one after the
    other (True) or all will originate in the first set of coordinates.

    Outputs:
    Javascript object that contains the data for the comparison plot

    Raises:
    AssertionError if the coords_data and coords_headers don't have the same
    length.
    AssertionError if the number of clones doesn't concord with the samples
    being presented.

    Unless the value of clones is > 0 this function will return an empty
    javascript object initialization.
    """

    js_comparison_string = []
    js_comparison_string.append('\nvar g_comparisonPositions = new Array();\n')

    if is_serial_comparison:
        js_comparison_string.append('var g_isSerialComparisonPlot = true;\n')
    else:
        js_comparison_string.append('var g_isSerialComparisonPlot = false;\n')

    if clones:
        headers_length = len(coords_headers)

        # assert some sanity checks
        assert headers_length == len(coords_data), "The coords data and"+\
            "the coords headers must have the same length"
        assert headers_length%clones == 0, "There has to be an exact "+\
            "number of clones of the data"

        # get the indices that the sample names get sorted by, this will group
        # all the samples with the same prefix together, and since the suffixes
        # are numeric, the samples will be one after the other i. e. sample_0,
        # sample_1, sample_2 and other_0, other_1, other_2 and so on. With these
        # indices sort the coordinates and then the headers themselves, though
        # convert to a numpy array first & back to a list to avoid sorting again
        indices = argsort(coords_headers)
        coords_data = coords_data[indices, :]
        coords_headers = array(coords_headers)[indices].tolist()

        # in steps of the number of clones iterate through the headers and the
        # coords to create the javascript object with the coordinates
        for index in xrange(0, headers_length, clones):
            # 1st object must have _0 as a suffix, trim it reveal the sample id
            assert coords_headers[index].endswith('_0'), "There's an internal"+\
                " inconsistency with the sample ids"
            sample_id = coords_headers[index][:-2]

            # convert all elements in the numpy array into a string before
            # formatting the elements into the javascript dictionary object
            js_comparison_string.append("g_comparisonPositions['%s'] = [%s];\n"%
                (sample_id, str(', '.join(map(str,
                coords_data[index:(index+clones), 0:3].tolist())))))
    return ''.join(js_comparison_string)


def format_emperor_html_footer_string(has_biplots=False, has_ellipses=False,
                                    has_vectors=False, has_edges=False):
    """Create an HTML footer according to the things being presented in the plot

    has_biplots: whether the plot has biplots or not
    has_ellipses: whether the plot has ellipses or not
    has_vectors: whether the plot has vectors or not
    has_edges: whether the plot has edges between samples (comparison plot)


    This function will remove unnecessary GUI elements from index.html to avoid
    confusions i. e. showing an ellipse opacity slider when there are no
    ellipses in the plot.
    """
    optional_strings = []

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

    language: language to which it will be formatted as a multi-line comment

    """

    # supported open and closing of multi-line comments for different languages
    _languages = {'HTML':('<!--', '-->'), 'Python':('"""', '"""'), 'C':('/*',
        '*/'), 'Bash':('<<COMMENT', 'COMMENT')}

    assert language in _languages.keys(), '%s is not a supported language' %\
        language

    autograph = []
    autograph.append(_languages[language][0])
    autograph.append("*Summary of Emperor's Information*")

    # add the day and time at which the command was called
    autograph.append(datetime.now().strftime('Command executed on %B %d, %Y at'
        ' %H:%M:%S'))

    # add library version and SHA-1 if available
    autograph.append('Emperor Version: %s' %  get_emperor_library_version())
    autograph.append('QIIME Version: %s' % qiime_backports_version)
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


EMPEROR_HEADER_HTML_STRING =\
"""<!doctype html>
<html lang="en">

<head>
    <title>Emperor</title>
    <meta charset="utf-8">
    <link rel="shortcut icon" href="emperor_required_resources/img/favicon.ico" />
    <meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">

    <!-- Style files -->
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/emperor/css/emperor.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/jquery-ui2.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/colorPicker.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/spectrum.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/d3.parcoords.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/chosen.min.css">

    <!-- Emperor logo for the splash window -->
    <table id="logotable" style="vertical-align:middle;text-align:center;height:100%;width:100%;margin:0;padding:0;border:0;">
        <tr><td><img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="logo"/></td></tr>
    </table>

    <!-- JavaScript code -->

    <!-- jQuery and other plugins -->
    <script type="text/javascript" src="emperor_required_resources/js/jquery-1.7.1.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/jquery-ui-1.8.17.custom.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/jquery.colorPicker.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/spectrum.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/chosen.jquery.min.js"></script>

    <!-- D3.js for the parallel coordinates plugin -->
    <script type="text/javascript" src="emperor_required_resources/js/d3.v3.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/d3.parcoords.js"></script>

    <!-- THREE.js and plugins for screenshots -->
    <script type="text/javascript" src="emperor_required_resources/js/three.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/js/Detector.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/js/OrbitControls.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/js/ColorConverter.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/js/SVGRenderer.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/THREEx.screenshot.js"></script>

    <!-- General utilities (underscore.js and FileSaver.js) -->
    <script type="text/javascript" src="emperor_required_resources/js/underscore-min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/chroma.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/FileSaver.min.js"></script>

    <!-- Emperor library code -->
    <script type="text/javascript" src="emperor_required_resources/emperor/js/animate.js"></script>
    <script type="text/javascript" src="emperor_required_resources/emperor/js/draw.js"></script>
    <script type="text/javascript" src="emperor_required_resources/emperor/js/emperor.js"></script>
    <script type="text/javascript" src="emperor_required_resources/emperor/js/trajectory.js"></script>
    <script type="text/javascript" src="emperor_required_resources/emperor/js/ui.js"></script>
    <script type="text/javascript" src="emperor_required_resources/emperor/js/util.js"></script>

    <script type="text/javascript">

"""

_ELLIPSE_OPACITY_SLIDER = """
            <br>
            <label for="ellipseopacity" class="text">Ellipse Opacity</label>
            <label id="ellipseopacity" class="slidervalue"></label>
            <div id="eopacityslider" class="slider-range-max"></div>"""

_VECTORS_OPACITY_SLIDER = """
            <br>
            <label for="vectorsopacity" class="text">Vectors Opacity</label>
            <label id="vectorsopacity" class="slidervalue"></label>
            <div id="vopacityslider" class="slider-range-max"></div>"""

_TAXA_LABELS_SELECTOR = """
            <form name="biplotoptions">
            <input type="checkbox" onClick="toggleTaxaLabels()">Biplots Label Visibility</input>
            </form>"""

_TAXA_LABELS_COLOR_SELECTOR = """
            <tr><td><div id="taxalabelcolor" class="colorbox"></div></td><td><label>Taxa Label Color</label></td></tr>
"""

_BIPLOT_VISIBILITY_SELECTOR = """
            <br>
            <form name="biplotsvisibility">
            <input type="checkbox" onClick="toggleBiplotVisibility()" checked>Biplots Visibility</input>
            </form>
            <br>"""

_BIPLOT_SPHERES_COLOR_SELECTOR ="""
            <br>
            <table>
                <tr><td><div id="taxaspherescolor" class="colorbox" name="taxaspherescolor"></div></td><td title="taxacolor">Taxa Spheres Color</td></tr>
            </table>
            <br>"""

_EDGES_VISIBILITY_SELECTOR = """
            <br>
            <form name="edgesvisibility">
            <input type="checkbox" onClick="toggleEdgesVisibility()" checked>Edges Visibility</input>
            </form>
            <br>"""

_EDGES_COLOR_SELECTOR = """
            <tr><td><div id="edgecolorselector_a" class="colorbox" name="edgecolorselector_a"></div></td><td title="edgecolor_a">Edge Color Selector A</td></tr>
            <tr><td><div id="edgecolorselector_b" class="colorbox" name="edgecolorselector_b"></div></td><td title="edgecolor_b">Edge Color Selector B</td></tr>
"""

_EMPEROR_FOOTER_HTML_STRING ="""document.getElementById("logo").style.display = 'none';
document.getElementById("logotable").style.display = 'none';

 </script>
</head>

<body>

<div id="overlay">
    <div>
    <img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="small-logo"/>
        <h1>WebGL is not enabled!</h1>
        <p>Emperor's visualization framework is WebGL based, it seems that your system doesn't have this resource available. Here is what you can do:</p>
        <p id="explanation"><strong>Chrome:</strong> Type "chrome://flags/" into the address bar, then search for "Disable WebGL". Disable this option if you haven't already. <em>Note:</em> If you follow these steps and still don't see an image, go to "chrome://flags/" and then search for "Override software rendering list" and enable this option.</p>
        <p id="explanation"><strong>Safari:</strong> Open Safari's menu and select Preferences. Click on the advanced tab, and then check "Show Developer" menu. Then open the "Developer" menu and select "Enable WebGL".</p>
        <p id="explanation"><strong>Firefox:</strong> Go to Options through Firefox > Options or Tools > Options. Go to Advanced, then General. Check "Use hardware acceleration when available" and restart Firefox.</p>
        <p id="explanation"><strong>Other browsers:</strong> The only browsers that support WebGL are Chrome, Safari, and Firefox. Please switch to these browsers when using Emperor.</p>
        <p id="explanation"><em>Note:</em> Once you went through these changes, reload the page and it should work!</p>
        <p id="source">Sources: Instructions for <a href="https://www.biodigitalhuman.com/home/enabling-webgl.html">Chrome and Safari</a>, and <a href="http://www.infewbytes.com/?p=144">Firefox</a></p>
    </div>
</div>

<div id="emperor-plot-toggle">
    <form>
      <div id="plottype">
        <input id="pcoa" type="radio" id="pcoa" name="plottype" checked="checked" /><label for="pcoa">PCoA</label>
        <input id="parallel" type="radio" id="parallel" name="plottype" /><label for="parallel">Parallel</label>
      </div>
    </form>
</div>
<div id="pcoaPlotWrapper" class="emperor-plot-wrapper">
    <label id="pointCount" class="ontop">
    </label>

    <div id="finder" class="arrow-right">
    </div>

    <div id="labels" class="unselectable">
    </div>

    <div id="taxalabels" class="unselectable">
    </div>

    <div id="axislabels" class="axis-labels">
    </div>

    <div id="main-plot">
    </div>
</div>

<div id="parallelPlotWrapper" class="emperor-plot-wrapper">
</div>

<div id="emperor-separator" class="emperor-separator" ondblclick="separatorDoubleClick()"></div>

<div id="emperor-menu">
    <div id="emperor-menu-tabs">
        <ul>
            <li><a href="#keytab">Key</a></li>
            <li><a href="#colorby">Colors</a></li>
            <li><a href="#showby">Visibility</a></li>
            <li><a href="#scalingby">Scaling</a></li>
            <li><a href="#labelby">Labels</a></li>
            <li><a href="#axes">Axes</a></li>
            <li><a href="#animations">Animations</a></li>
            <li><a href="#options">Options</a></li>
        </ul>
        <div id="keytab" class="emperor-tab-div">
            <form name="keyFilter">
                <label>Filter  </label><input name="filterBox" id="searchBox" type="text" onkeyup="filterKey()"></input>
            </form>
            <div id="key">
            </div>
        </div>
        <div id="colorby" class="emperor-tab-div">
            <select id="colormap-drop-down" class="emperor-tab-drop-down" onchange="colorByMenuChanged()"></select>
            {biplot_spheres_color_selector}
            <br><br>
            <select id="colorbycombo" onchange="colorByMenuChanged()" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="colorbylist">
            </div>
        </div>
        <div id="showby" class="emperor-tab-div">{biplot_visibility_selector}
            <table class="emperor-tab-table">
                <tr>
                    <td>
                        <select id="showbycombo" onchange="showByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="showbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereopacity" class="text">Global Sphere Opacity</label>
                        <label id="sphereopacity" class="slidervalue"></label>
                        <div id="sopacityslider" class="slider-range-max"></div>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <button id="toggle-visibility-selection-button" onClick="toggleVisibleCategories()">Invert Selected</button>
                    </td>
                </tr>
            </table>
        </div>
        <div id="scalingby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td>
                        <select id="scalingbycombo" onchange="scalingByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="scalingbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereradius" class="text">Global Sphere Scale</label>
                        <label id="sphereradius" class="slidervalue"></label>
                        <div id="sradiusslider" class="slider-range-max"></div>
                    </td>
                </tr>
            </table>
        </div>
        <div id="labelby" class="emperor-tab-div">
            <div id="labels-top">
                <form name="plotoptions">
                    <input type="checkbox" onClick="toggleLabels()">Samples Label Visibility</input>
                </form>{taxa_labels_selector}
                <br>
                <label for="labelopacity" class="text">Label Opacity</label>
                <label id="labelopacity" class="slidervalue"></label>
                <div id="lopacityslider" class="slider-range-max"></div>
                <div id="label-color-holder clearfix">
                    <table class="emperor-tab-table">
                        <tr><td><div id="labelColor" class="colorbox"></div></td><td><label>Master Label Color</label></td></tr>{taxa_labels_color_selector}
                        <br><br>
                </table></div>
            </div>
            <br>
            <select id="labelcombo" onchange="labelMenuChanged()" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="label-list">
            </div>
        </div>
        <div id="axes" class="emperor-tab-div">
            <div id="pcoaaxes">
                <div class="list" id="axeslist">
                </div>
            </div>
        </div>
        <div id="animations" class="emperor-tab-div">
            <table class="emperor-tab-table-with-sliders">
                <tr>
                    <td>
                        <a id="reset-button" class="media-button" href="javascript:void(0);" onclick="javascript:resetAnimation()"><img src="emperor_required_resources/img/reset.png" ></img></a>
                        <a id="play-button" class="media-button" href="javascript:void(0);" onclick="javascript:playAnimation()"><img src="emperor_required_resources/img/play.png"></img></a>
                        <a id="pause-button" class="media-button" href="javascript:void(0);" onclick="javascript:pauseAnimation()"><img src="emperor_required_resources/img/pause.png"></img></a>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="animation-speed" class="text">Speed</label>
                        <label id="animation-speed" class="slidervalue"></label>
                        <div id="animation-speed-slider" class="slider-range-max"></div>
                        <div id="labelColorHolder clearfix">
                    </td>
                </tr>
                <tr>
                    <td>
                        <br><label for="gradient-category-drop-down" class="text">Gradient Category</label><br>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="gradient-category-drop-down" class="emperor-tab-drop-down"></select><br>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label for="trajectory-category-drop-down" class="text">Trajectory Category</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="trajectory-category-drop-down" class="emperor-tab-drop-down" onchange="colorAnimationsByCategoryChanged()"></select>
                    </td>
                </tr>
                <tr>
                    <td id="emperor-animation-color-selector">
                    </td>
                </tr>
            </table>
        </div>
        <div id="options" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr><td><div id="axeslabelscolor" class="colorbox" name="axeslabelscolor"></div></td><td title="Axes Labels Color">Axes Labels Color</td></tr>
                <tr><td><div id="axescolor" class="colorbox" name="axescolor"></div></td><td title="Axes Color Title">Axes Color</td></tr>
                <tr><td><div id="rendererbackgroundcolor" class="colorbox" name="rendererbackgroundcolor"></div></td><td title="Background Color Title">Background Color</td></tr>{edges_color_selector}
                <tr><td colspan="2">
                        <div id="pcoaviewoptions" class="">{ellipse_opacity_slider}{vectors_opacity_slider}{edges_visibility_selector}
                            <form name="settingsoptionscolor">
                            </form>
                            <div id="pcoaoptions" class="">
                                <form name="settingsoptions">
                                    <input type="checkbox" onchange="toggleScaleCoordinates(this)" id="scale_checkbox" name="scale_checkbox">Scale coords by percent explained</input>
                                </form>
                            </div>
                            <br><input id="reset" class="button" type="submit" value="Recenter Camera" style="" onClick="resetCamera()">
                            <br><br>
                            <hr class='section-break'>
                            <br>Filename <small>(only letters, numbers, ., - and _)</small>:
                            <br><input name="saveas_name" id="saveas_name" value="screenshot" type="text"/>
                            <br><input id="saveas_legends" class="checkbox" type="checkbox" style=""> Create legend
                            <input id="saveas" class="button" type="submit" value="Save as SVG" style="" onClick="saveSVG()"/>
                            <br><br>For a PNG, simply press 'ctrl+p'.
                            <div id="paralleloptions" class="">
                            </div>
                        </div>
                        <br>
                </td></tr>
            </table>
        </div>
    </div>
</div>
</body>

</html>
"""
