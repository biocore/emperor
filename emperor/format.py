#!/usr/bin/env python
# File created on 24 Jan 2013
from __future__ import division

__author__ = "Antonio Gonzalez Pena"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Meg Pirrung", "Antonio Gonzalez Pena", "Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from copy import deepcopy
from StringIO import StringIO

from numpy import max, min, abs
from cogent.util.misc import if_

from emperor.util import keep_columns_from_mapping_file

from qiime.format import format_mapping_file
from qiime.parse import mapping_file_to_dict, parse_mapping_file
from qiime.filter import (filter_mapping_file_by_metadata_states,
    sample_ids_from_metadata_description)

def format_pcoa_to_js(header, coords, eigvals, pct_var, custom_axes=[],
                    coords_low=None, coords_high=None):
    """Write the javascript necessary to represent a pcoa file in emperor

    Inputs:
    header: sample names for the pcoa file 1-D array
    coords: coordinates of the PCoA file, 2-D array
    eigvals: eigen-values of the PCoA file, 1-D array
    pct_var: percentage of variation of the PCoA file, 1-D array
    custom_axes: list of category names for the custom axes
    coords_low: coordinates representing the lower edges of an ellipse
    coords_high: coordinates representing the highere edges of an ellipse

    Output:
    string: javascript representation of the PCoA data inputed, contains a list
    of spheres, list of ellipses (if coords_low and coords_high are present) and
    several setup variables.

    Formats the output of qiime.parse.parse_coords_file into javascript variable
    declarations.
    """
    js_pcoa_string = ''

    # ranges for the PCoA space
    max_x = max(coords[:,0:1])
    max_y = max(coords[:,1:2])
    max_z = max(coords[:,2:3])
    min_x = min(coords[:,0:1])
    min_y = min(coords[:,1:2])
    min_z = min(coords[:,2:3])
    maximum = max(abs(coords[:,:3]))
    pcoalabels = pct_var[:3]

    radius = (max_x-min_x)*.02

    # write the values for all the spheres
    js_pcoa_string += '\nvar g_spherePositions = new Array();\n'
    for point, coord in zip(header, coords):
        js_pcoa_string += ("g_spherePositions['%s'] = { 'name': '%s', 'color': "
            "0, 'x': %f, 'y': %f, 'z': %f };\n" % (point, point, coord[0],
            coord[1],coord[2]))

    # write the values for all the ellipses
    js_pcoa_string += '\nvar g_ellipsesDimensions = new Array();\n'
    if coords_low != None and coords_high != None:
        for s_header, s_coord, s_low, s_high in zip(header, coords, coords_low,
            coords_high):
            delta = abs(s_high-s_low)
            js_pcoa_string += ("g_ellipsesDimensions['%s'] = { 'name': '%s', "
                "'color': 0, 'width': %f, 'height': %f, 'length': %f , 'x': %f,"
                " 'y': %f, 'z': %f }\n" %(s_header, s_header,delta[0], delta[1],
                delta[2], s_coord[0], s_coord[1], s_coord[2]))

    js_pcoa_string += 'var g_segments = 16, g_rings = 16, g_radius = %f;\n' %\
        (radius)
    js_pcoa_string += 'var g_xAxisLength = %f;\n' % (abs(max_x)+abs(min_x))
    js_pcoa_string += 'var g_yAxisLength = %f;\n' % (abs(max_y)+abs(min_y))
    js_pcoa_string += 'var g_zAxisLength = %f;\n' % (abs(max_z)+abs(min_z))

    # use this to determine if the padding value should be positive or negative
    # radius*6 is a padding to the axes so axes don't look _small_
    padding = lambda _x: if_(_x>=0, 6*radius, -6*radius)
    js_pcoa_string += 'var g_xMaximumValue = %f;\n' % (max_x+padding(max_x))
    js_pcoa_string += 'var g_yMaximumValue = %f;\n' % (max_y+padding(max_y))
    js_pcoa_string += 'var g_zMaximumValue = %f;\n' % (max_z+padding(max_z))
    js_pcoa_string += 'var g_xMinimumValue = %f;\n' % (min_x+padding(min_x))
    js_pcoa_string += 'var g_yMinimumValue = %f;\n' % (min_y+padding(min_y))
    js_pcoa_string += 'var g_zMinimumValue = %f;\n' % (min_z+padding(min_z))
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
            js_pcoa_string += 'var g_pc%dLabel = \"PC%d (%.0f %%)\";\n' %\
                (i+1, i+1-offset, pcoalabels[i-offset])

    js_pcts = []
    if custom_axes == None: custom_axes = []
    for element in custom_axes + list(pct_var):
        try:
            # scale the percent so it's a number from 0 to 1
            js_pcts.append('%f' % (float(element)/100))
        except ValueError:
            js_pcts.append('%f' % (float(pct_var[0]/100)))
    js_pcoa_string += 'var g_fractionExplained = [%s];\n' % ', '.join(js_pcts)

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

    return js_mapping_file_string

def format_taxa_to_js(otu_coords, lineages, prevalence):
    """Write a string representing the taxa in a PCoA plot as javascript
    
    Inputs:
    otu_coords: numpy array where the taxa is positioned
    lineages: label for each of these lineages
    prevalence: score of prevalence for each of the taxa that is drawn

    Outputs:
    js_biplots_string: javascript string where the taxa information is written
    to create the spheres representing each of these, will return only the
    variable declaration if the inputs are empty.
    """
    js_biplots_string = []
    js_biplots_string.append('\nvar g_taxaPositions = new Array();\n')

    # if we have prevalence scores, calculate the taxa radii values
    if len(prevalence):
        taxa_radii = RADIUS*(MIN_TAXON_RADIUS+(MAX_TAXON_RADIUS-
            MIN_TAXON_RADIUS)*prevalence)
    else:
        taxa_radii = []

    index = 0

    # write the data in the form of a dictionary
    for taxa_label, taxa_coord, radius in zip(lineages, otu_coords, taxa_radii):
        js_biplots_string.append(("g_taxaPositions['%d'] = { 'lineage': '%s', "
            "'x': %f, 'y': %f, 'z': %f, 'radius': %f};\n") % (index,
            taxa_label, taxa_coord[0], taxa_coord[1], taxa_coord[2], radius))
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

def format_emperor_html_footer_string(has_biplots=False, has_ellipses=False,
                                    has_vectors=False):
    """Create an HTML footer according to the things being presented in the plot

    has_biplots: whether the plot has biplots or not
    has_ellipses: whether the plot has ellipses or not

    This function will remove unnecessary GUI elements from index.html to avoid
    confusions i. e. showing an ellipse opacity slider when there are no
    ellipses in the plot.
    """
    optional_strings = []

    # the order of these statemenst matter, see _EMPEROR_FOOTER_HTML_STRING
    optional_strings.append(if_(has_biplots, _BIPLOT_SPHERES_COLOR_SELECTOR,''))
    optional_strings.append(if_(has_biplots, _BIPLOT_VISIBILITY_SELECTOR, ''))
    optional_strings.append(if_(has_biplots, _TAXA_LABELS_SELECTOR, ''))
    optional_strings.append(if_(has_ellipses, _ELLIPSE_OPACITY_SLIDER, ''))
    optional_strings.append(if_(has_vectors, _VECTORS_OPACITY_SLIDER, ''))

    return _EMPEROR_FOOTER_HTML_STRING % tuple(optional_strings)


MIN_TAXON_RADIUS = 0.5
MAX_TAXON_RADIUS = 5
RADIUS = 1.0

EMPEROR_HEADER_HTML_STRING =\
"""<!doctype html>
<html lang="en">

<head>
    <title>Emperor</title>
    <meta charset="utf-8">
    <link rel="shortcut icon" href="emperor_required_resources/img/favicon.ico" />
    <meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/emperor/css/emperor.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/jquery-ui2.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/colorPicker.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/spectrum.css">
    <table id="logotable" style="vertical-align:middle;text-align:center;height:100%;width:100%;margin:0;padding:0;border:0;">
        <tr><td><img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="logo"/></td></tr>
    </table>

    <script type="text/javascript" src="emperor_required_resources/js/jquery-1.7.1.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/jquery-ui-1.8.17.custom.min.js"></script>
    <script src="emperor_required_resources/js/jquery.colorPicker.js"></script>
    <script src="emperor_required_resources/js/spectrum.js"></script>

    <script src="emperor_required_resources/js/Three.js"></script>
    <script src="emperor_required_resources/js/js/Detector.js"></script>
    <script src="emperor_required_resources/js/js/RequestAnimationFrame.js"></script>
    <script src="emperor_required_resources/emperor/js/emperor.js"></script>
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

_BIPLOT_VISIBILITY_SELECTOR = """
            <br>
            <form name="biplotsvisibility">
            <input type="checkbox" onClick="toggleBiplotVisibility()">Biplots Visibility</input>
            </form>
            <br>"""

_BIPLOT_SPHERES_COLOR_SELECTOR ="""
            <br>
            <table>
                <tr><td><div id="taxaspherescolor" class="colorbox" name="taxaspherescolor"></div></td><td title="taxacolor">Taxa Spheres Color</td></tr>
            </table>
            <br>"""

_EMPEROR_FOOTER_HTML_STRING ="""document.getElementById("logo").style.display = 'none';
document.getElementById("logotable").style.display = 'none';

 </script>
</head>

<body>

<label id="pointCount" class="ontop">
</label>

<div id="finder" class="arrow-right">
</div>

<div id="labels" class="unselectable">
</div>

<div id="taxalabels" class="unselectable">
</div>

<div id="axislabels" class="axislabels">
</div>

<div id="main_plot">
</div>

<div id="menu">
    <div id="menutabs">
        <ul>
            <li><a href="#keytab">Key</a></li>
            <li><a href="#colorby">Colors</a></li>
            <li><a href="#showby">Visibility</a></li>
            <li><a href="#labelby">Labels</a></li>
            <li><a href="#settings">Options</a></li>
        </ul>
        <div id="keytab">
            <form name="keyFilter">
            <label>Filter  </label><input name="filterBox" type="text" onkeyup="filterKey()"></input>
            </form>
            <div id="key">
            </div>
        </div>
        <div id="colorby">
            <br>%s
            <select id="colorbycombo" onchange="colorByMenuChanged()">
            </select>
            <div class="list" id="colorbylist">
            </div>
        </div>
        <div id="showby">%s
            <select id="showbycombo" onchange="showByMenuChanged()">
            </select>
            <div class="list" id="showbylist">
            </div>
        </div>
        <div id="labelby">
        <div id="labelsTop">
            <form name="plotoptions">
            <input type="checkbox" onClick="toggleLabels()">Samples Label Visibility</input>
            </form>%s
            <br>
            <label for="labelopacity" class="text">Label Opacity</label>
            <label id="labelopacity" class="slidervalue"></label>
            <div id="lopacityslider" class="slider-range-max"></div>
            <div id="labelColorHolder clearfix">
            <table><tr>
            <td><div id="labelColor" class="colorbox">
            </div></td><td><label>Master Label Color</label></td>
            </tr></table></div>
        </div>
            <br>
            <select id="labelcombo" onchange="labelMenuChanged()">
            </select>
            <div class="list" id="labellist">
            </div>
        </div>
        <div id="settings">
            <form name="settingsoptions">
            <input type="checkbox" onchange="toggleScaleCoordinates(this)" id="scale_checkbox" name="scale_checkbox">Scale coords by percent explained</input>
            </form>
            <br>
            <form name="settingsoptionscolor">
            <input type="checkbox" onchange="toggleContinuousAndDiscreteColors(this)" id="discreteorcontinuouscolors" name="discreteorcontinuouscolors">Use discrete colors</input>
            </form>
            <br>
            <br>
            <input id="saveas" class="button" type="submit" value="Save as SVG" style="" onClick="saveSVG()">
            <input id="reset" class="button" type="submit" value="Recenter Camera" style="" onClick="resetCamera()">
            <br>%s%s
            <br>
            <label for="sphereopacity" class="text">Sphere Opacity</label>
            <label id="sphereopacity" class="slidervalue"></label>
            <div id="sopacityslider" class="slider-range-max"></div>
            <br>
            <label for="sphereradius" class="text">Sphere Scale</label>
            <label id="sphereradius" class="slidervalue"></label>
            <div id="sradiusslider" class="slider-range-max"></div>
            <br>
            <table>
                <tr><td><div id="rendererbackgroundcolor"class="colorbox" name="rendererbackgroundcolor"></div></td><td title="Background Color Title">Background Color</td></tr>
            </table>
        </div>
    </div>  
</div>
</body>

</html>
"""