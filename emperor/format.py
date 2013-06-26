#!/usr/bin/env python
# File created on 24 Jan 2013
from __future__ import division

__author__ = "Antonio Gonzalez Pena"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Meg Pirrung", "Antonio Gonzalez Pena", "Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "0.9.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from copy import deepcopy
from StringIO import StringIO

from cogent.util.misc import if_
from numpy import max, min, abs, argsort, array

from emperor.util import keep_columns_from_mapping_file

from qiime.format import format_mapping_file
from qiime.parse import mapping_file_to_dict, parse_mapping_file
from qiime.filter import (filter_mapping_file_by_metadata_states,
    sample_ids_from_metadata_description)

class EmperorLogicError(ValueError):
    """Exception raised when a requirement for the Emperor GUI is not met"""
    pass

def format_pcoa_to_js(header, coords, eigvals, pct_var, custom_axes=[],
                    coords_low=None, coords_high=None, number_of_axes=10):
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
    
    # validating that the number of coords in coords
    if number_of_axes>len(coords[0]):
        number_of_axes = len(coords[0])
    # validating that all the axes are above 0.51%, this accounts for really
    # small variations explained in some axes that end up being not practical
    # the GUI has some problems when presenting those values on screen
    valid_pcoalabels = len([i for i in pct_var if i>0.51])
    if number_of_axes>valid_pcoalabels:
        number_of_axes = valid_pcoalabels
    if number_of_axes<3:
        raise EmperorLogicError, "Due to the variation explained, Emperor "+\
            "could not plot at least 3 axes, check the input files to ensure"+\
            " that the percent explained is greater than 0.5 in at least "+\
            "three axes."

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
    if coords_low != None and coords_high != None:
        for s_header, s_coord, s_low, s_high in zip(header, coords, coords_low,
            coords_high):
            delta = abs(s_high-s_low)
            all_coords = ', '.join(["'P%d': %f" % (i+1,s_coord[i]) for i in range(number_of_axes)])
            js_pcoa_string += ("g_ellipsesDimensions['%s'] = { 'name': '%s', "
                "'color': 0, 'width': %f, 'height': %f, 'length': %f , 'x': %f,"
                " 'y': %f, 'z': %f, %s }\n" % (s_header, s_header,delta[0], delta[1],
                delta[2], s_coord[0], s_coord[1], s_coord[2], all_coords))

    js_pcoa_string += 'var g_segments = 16, g_rings = 16, g_radius = %f;\n' % (radius)
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
            js_pcoa_string += 'var g_pc%dLabel = \"PC%d (%.0f %%)\";\n' %\
                (i+1, i+1-offset, pcoalabels[i-offset])
    js_pcoa_string += 'var g_number_of_custom_axes = %d;\n' % offset
    
    js_pcts = []
    js_pcts_round = []
    if custom_axes == None: custom_axes = []
    for element in custom_axes + list(pct_var[:number_of_axes]):
        try:
            # scale the percent so it's a number from 0 to 1
            js_pcts.append('%f' % (float(element)/100))
            js_pcts_round.append('%d' % (round(element)))
        except ValueError:
            js_pcts.append('%f' % (float(pct_var[0]/100)))
            js_pcts_round.append('%d' % (round(pct_var[0])))
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

def format_comparison_bars_to_js(coords_data, coords_headers, clones):
    """Format coordinates data to create a comparison plot

    Inputs:
    coords_data: numpy array with the replicated coordinates
    cooreds_headers: list with the headers for each of replicated coordinates
    clones: number of replicates in the coords_data and coords_headers

    Outputs:
    Javascript object that contains the data for the comparison plot

    Raises:
    AssertionError if the coords_data and coords_headers don't have the same
    length.
    AssertionError if the number of clones doesn't concord with the samples
    being presented.
    """

    js_comparison_string = []
    js_comparison_string.append('\nvar g_comparisonPositions = new Array();\n')

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
        coords_headers = array(coords_headers)[indices, :].tolist()

        # in steps of the number of clones iterate through the headers and the
        # coords to create the javascript object with the coordinates
        for index in xrange(0, headers_length, clones):
            # 1st object must have _0 as a suffix, trim it reveal the sample id
            sample_id = coords_headers[index].rstrip('_0')

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

    This function will remove unnecessary GUI elements from index.html to avoid
    confusions i. e. showing an ellipse opacity slider when there are no
    ellipses in the plot.
    """
    optional_strings = []

    # the order of these statements matter, see _EMPEROR_FOOTER_HTML_STRING
    optional_strings.append(if_(has_biplots, _BIPLOT_SPHERES_COLOR_SELECTOR,''))
    optional_strings.append(if_(has_biplots, _BIPLOT_VISIBILITY_SELECTOR, ''))
    optional_strings.append(if_(has_biplots, _TAXA_LABELS_SELECTOR, ''))
    optional_strings.append(if_(has_ellipses, _ELLIPSE_OPACITY_SLIDER, ''))
    optional_strings.append(if_(has_vectors, _VECTORS_OPACITY_SLIDER, ''))
    optional_strings.append(if_(has_edges, _EDGES_VISIBILITY_SELECTOR, ''))

    return _EMPEROR_FOOTER_HTML_STRING % tuple(optional_strings)


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
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/d3.parcoords.css">
    <table id="logotable" style="vertical-align:middle;text-align:center;height:100%;width:100%;margin:0;padding:0;border:0;">
        <tr><td><img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="logo"/></td></tr>
    </table>
    <script type="text/javascript" src="emperor_required_resources/js/d3.v3.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/d3.parcoords.js"></script>
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
            <input type="checkbox" onClick="toggleEdgesVisibility()">Edges Visibility</input>
            </form>
            <br>"""

_EMPEROR_FOOTER_HTML_STRING ="""document.getElementById("logo").style.display = 'none';
document.getElementById("logotable").style.display = 'none';

 </script>
</head>

<body>    

<div id="plotToggle">
    <form>
      <div id="plottype">
        <input id="pcoa" type="radio" id="pcoa" name="plottype" checked="checked" /><label for="pcoa">PCoA</label>
        <input id="parallel" type="radio" id="parallel" name="plottype" /><label for="parallel">Parallel</label>
      </div>
    </form>
</div>
<div id="pcoaPlotWrapper" class="plotWrapper">
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
</div>

<div id="parallelPlotWrapper" class="plotWrapper">
</div>

<div id="menu">
    <div id="menutabs">
        <ul>
            <li><a href="#keytab">Key</a></li>
            <li><a href="#colorby">Colors</a></li>
            <li><a href="#showby">Visibility</a></li>
            <li><a href="#scalingby">Scaling</a></li>
            <li><a href="#labelby">Labels</a></li>
            <li><a href="#axes">Axes</a></li>
            <li><a href="#view">View</a></li>
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
            <select id="colorbycombo" onchange="colorByMenuChanged()" size="3">
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
        <div id="scalingby">
            <select id="scalingbycombo" onchange="scalingByMenuChanged()">
            </select>
            <div class="list" id="scalingbylist">
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
        <div id="axes">
            <div id="pcoaaxes">
                <div class="list" id="axeslist">
                </div>
            </div>
        </div>
        <div id="view">
            <table>
                <tr><td><div id="axeslabelscolor" class="colorbox" name="axeslabelscolor"></div></td><td title="Axes Labels Color">Axes Labels Color</td></tr>
                <tr><td><div id="axescolor" class="colorbox" name="axescolor"></div></td><td title="Axes Color Title">Axes Color</td></tr>
                <tr><td><div id="rendererbackgroundcolor"class="colorbox" name="rendererbackgroundcolor"></div></td><td title="Background Color Title">Background Color</td></tr>
            </table>
            <br>
            <form name="settingsoptionscolor">
            <input type="checkbox" onchange="toggleContinuousAndDiscreteColors(this)" id="discreteorcontinuouscolors" name="discreteorcontinuouscolors">  Use gradient colors</input>
            </form>
            <div id="pcoaviewoptions" class="">
                <br>
                <input id="reset" class="button" type="submit" value="Recenter Camera" style="" onClick="resetCamera()">
                <br>%s%s%s
                <br>
                <label for="sphereopacity" class="text">Sphere Opacity</label>
                <label id="sphereopacity" class="slidervalue"></label>
                <div id="sopacityslider" class="slider-range-max"></div>
                <br>
                <label for="sphereradius" class="text">Sphere Scale</label>
                <label id="sphereradius" class="slidervalue"></label>
                <div id="sradiusslider" class="slider-range-max"></div>
                <br>
            </div>
            <br>
        </div>
        <div id="settings">
            <br>
            <input id="saveas" class="button" type="submit" value="Save as SVG" style="" onClick="saveSVG()">
            <br>
            <br>
            <div id="pcoaoptions" class="">
                <form name="settingsoptions">
                    <input type="checkbox" onchange="toggleScaleCoordinates(this)" id="scale_checkbox" name="scale_checkbox">Scale coords by percent explained</input>
                </form>
            </div>
            <br>
            <div id="paralleloptions" class="">
            </div>
        </div>
    </div>  
</div>
</body>

</html>
"""
