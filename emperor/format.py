#!/usr/bin/env python
# File created on 24 Jan 2013
from __future__ import division

__author__ = "Antonio Gonzalez Pena"
__copyright__ = "Copyright 2011, The Emperor Project"
__credits__ = ["Meg Pirrung", "Antonio Gonzalez Pena", "Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from numpy import max, min, abs

from qiime.parse import mapping_file_to_dict

def format_pcoa_to_js(header, coords, eigvals, pct_var, custom_axes=None):
    """Write the javascript necessary to represent a pcoa file in emperor

    Inputs:
    header: sample names for the pcoa file 1-D array
    coords: coordinates of the PCoA file, 2-D array
    eigvals: eigen-values of the PCoA file, 1-D array
    pct_var: percentage of variation of the PCoA file, 1-D array

    Output:
    string: javascript representation of the PCoA data inputed

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

    js_pcoa_string += '\nvar points = new Array()\n'
    for point, coord in zip(header, coords):
        js_pcoa_string += "points['%s'] = { 'name': '%s', 'color': 0, 'x': %f, 'y': %f, 'z': %f };\n" % (point, point, coord[0], coord[1], coord[2])

    js_pcoa_string += 'var segments = 16, rings = 16, radius = %f;\n' % ((max_x-min_x)*.02)
    js_pcoa_string += 'var xaxislength = %f;\n' % (abs(max_x)+abs(min_x))
    js_pcoa_string += 'var yaxislength = %f;\n' % (abs(max_y)+abs(min_y))
    js_pcoa_string += 'var zaxislength = %f;\n' % (abs(max_z)+abs(min_z))
    js_pcoa_string += 'var max_x = %f;\n' % max_x
    js_pcoa_string += 'var max_y = %f;\n' % max_y
    js_pcoa_string += 'var max_z = %f;\n' % max_z
    js_pcoa_string += 'var min_x = %f;\n' % min_x
    js_pcoa_string += 'var min_y = %f;\n' % min_y
    js_pcoa_string += 'var min_z = %f;\n' % min_z
    js_pcoa_string += 'var max = %f;\n' % maximum

    offset = 0
    # create three vars, pc1, pc2 and pc3 if no custom_axes are passed, then use
    # the values of the percent explained by the PCoA; if custom_axes are passed
    # use as many as you can (since customs axes can be either [0, 1, 2, 3])
    for i in range(0, 3):
        try:
            js_pcoa_string += 'pc%d = \"%s\";\n' % (i+1, custom_axes[i])
            offset+=1 # offset will help us retrieve the correct pcoalabels val
        except:
            # if there are custom axes then subtract the number of custom axes
            js_pcoa_string += 'pc%d = \"PC%d (%.0f %%)\";\n' % (i+1, i+1-offset,
                pcoalabels[i-offset])

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
    js_mapping_file_string += 'var headers = [%s];\n' % ','.join(["'%s'" %\
        col for col in mapping_file_headers])
    js_mapping_file_string += 'var mapping = { %s };\n' % ','.join(map_values)

    return js_mapping_file_string


EMPEROR_HEADER_HTML_STRING =\
"""<!doctype html>
<html lang="en">

<head>
    <title>Emperor</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/emperor/css/emperor.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/jquery-ui2.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/colorPicker.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/spectrum.css">
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

EMPEROR_FOOTER_HTML_STRING =\
""" </script>
</head>

<body>

<label id="pointCount" class="ontop">
</label>

<div id="finder" class="arrow-right">
</div>

<div id="labels" class="unselectable">
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
            <!-- <li><a href="#animations">Animate</a></li> -->
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
            <select id="colorbycombo" onchange="colorByMenuChanged()">
            </select>
            <div class="list" id="colorbylist">
            </div>
        </div>
        <div id="showby">
            <select id="showbycombo" onchange="showByMenuChanged()">
            </select>
            <div class="list" id="showbylist">
            </div>
        </div>
        <div id="labelby">
        <div id="labelsTop">
            <form name="plotoptions">
            <input type="checkbox" onClick="toggleLabels()">Master Label Visibility</input>
            </form>
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
        <!-- <div id="animations">
                <div id="animationsTop">
                    <a class="mediabutton" href="javascript:void(0);" onclick="javascript:resetAnimation()"><img src="emperor/img/reset.png" ></img></a>
                    <a class="mediabutton" href="javascript:void(0);" onclick="javascript:playAnimation()"><img src="emperor/img/play.png"></img></a>
                    <a class="mediabutton" href="javascript:void(0);" onclick="javascript:pauseAnimation()"><img src="emperor/img/pause.png"></img></a>
                    <br>
                    <br>
                    <label for="animationspeed" class="text">Speed</label>
                    <label id="animationspeed" class="slidervalue"></label>
                    <div id="animspeedslider" class="slider-range-max"></div>
                </div>
                    <br>
                    <label for="animationGradient" class="text">Animate Over (eg. time)</label><br>
                    <select id="animationovercombo" onchange="animationOverMenuChanged()">
                    </select>
                    <br>
                    <br>
                    <label for="animation" class="text">Animate</label><br>
                    <select id="animationcombo" onchange="animationMenuChanged()">
                    </select>
                    <div class="animationlist" id="animationlist">
                    </div>
                </div> -->
        <div id="settings">
            <input id="saveas" class="button" type="submit" value="Save as SVG" style="" onClick="saveSVG()">
            <input id="reset" class="button" type="submit" value="Recenter Camera" style="" onClick="resetCamera()">
            <br>
            <br>
            <label for="ellipseopacity" class="text">Ellipse Opacity</label>
            <label id="ellipseopacity" class="slidervalue"></label>
            <div id="eopacityslider" class="slider-range-max"></div>
            <br>
            <label for="sphereopacity" class="text">Sphere Opacity</label>
            <label id="sphereopacity" class="slidervalue"></label>
            <div id="sopacityslider" class="slider-range-max"></div>
            <br>
            <label for="sphereradius" class="text">Sphere Scale</label>
            <label id="sphereradius" class="slidervalue"></label>
            <div id="sradiusslider" class="slider-range-max"></div>
        </div>
    </div>  
</div>
</body>

</html>
"""