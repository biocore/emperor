# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
# flake8: noqa
"""
These are intended to be HTML formatted strings that are used throughout the
codebase and not included in for example format.py, because the length would
violate PEP-8 rules.
"""

PCOA_STRING = """Eigvals	9
0.479412119045	0.29201495623	0.247449246064	0.201496072404	0.180076127632\
	0.147806772727	0.135795927213	0.112259695609	0.0

Proportion explained	9
0.266887048633	0.162563704022	0.137754129161	0.11217215823	0.10024774995\
	0.0822835130237	0.0755971173665	0.0624945796136	0.0

Species	0	0

Site	9	9
PC.636	-0.276542163845	-0.144964375408	0.0666467344429	-0.0677109454288\
	0.176070269506	0.072969390136	-0.229889463523	-0.0465989416581\
	-0.0
PC.635	-0.237661393984	0.0460527772512	-0.138135814766	0.159061025229\
	-0.247484698646	-0.115211468101	-0.112864033263	0.0647940729676\
	-0.0
PC.356	0.228820399536	-0.130142097093	-0.287149447883	0.0864498846421\
	0.0442951919304	0.20604260722	0.0310003571386	0.0719920436501	-0.0
PC.481	0.0422628480532	-0.0139681511889	0.0635314615517	-0.346120552134\
	-0.127813807608	0.0139350721063	0.0300206887328	0.140147849223	-0.0
PC.354	0.280399117569	-0.0060128286014	0.0234854344148	-0.0468109474823\
	-0.146624450094	0.00566979124596	-0.0354299634191\
	-0.255785794275	-0.0
PC.593	0.232872767451	0.139788385269	0.322871079774	0.18334700682\
	0.0204661596818	0.0540589147147	-0.0366250872041	0.0998235721267\
	-0.0
PC.355	0.170517581885	-0.194113268955	-0.0308965283066	0.0198086158783\
	0.155100062794	-0.279923941712	0.0576092515759	0.0242481862127	-0.0
PC.607	-0.0913299284215	0.424147148265	-0.135627421345	-0.057519480907\
	0.151363490722	-0.0253935675552	0.0517306152066	-0.038738217609\
	-0.0
PC.634	-0.349339228244	-0.120787589539	0.115274502117	0.0694953933826\
	-0.0253722182853	0.067853201946	0.244447634756	-0.0598827706386\
	-0.0

Biplot	0	0

Site constraints	0	0
"""

HTML_STRING = """<!doctype html>
<html lang="en">

<head>
    <title>Emperor</title>
    <meta charset="utf-8">
    <link rel="shortcut icon" href="emperor_required_resources/img/favicon.ico" />
    <meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">

    <!-- Style files -->
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/css/emperor.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/vendor/css/jquery-ui2.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/vendor/css/colorPicker.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/vendor/css/spectrum.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/vendor/css/d3.parcoords.css">
    <link rel="stylesheet" type="text/css" href="emperor_required_resources/vendor/css/chosen.min.css">

    <!-- Emperor logo for the splash window -->
    <table id="logotable" style="vertical-align:middle;text-align:center;height:100%;width:100%;margin:0;padding:0;border:0;">
        <tr><td><img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="logo"/></td></tr>
    </table>

    <!-- JavaScript code -->

    <!-- jQuery and other plugins -->
    <script type="text/javascript" src="emperor_required_resources/vendor/js/jquery-1.7.1.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/jquery-ui-1.8.17.custom.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/jquery.colorPicker.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/spectrum.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/chosen.jquery.min.js"></script>

    <!-- D3.js for the parallel coordinates plugin -->
    <script type="text/javascript" src="emperor_required_resources/vendor/js/d3.v3.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/d3.parcoords.js"></script>

    <!-- THREE.js and plugins for screenshots -->
    <script type="text/javascript" src="emperor_required_resources/vendor/js/three.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/three.js-plugins/Detector.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/three.js-plugins/OrbitControls.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/three.js-plugins/ColorConverter.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/three.js-plugins/SVGRenderer.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/THREEx.screenshot.js"></script>

    <!-- General utilities (underscore.js and FileSaver.js) -->
    <script type="text/javascript" src="emperor_required_resources/vendor/js/underscore-min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/chroma.min.js"></script>
    <script type="text/javascript" src="emperor_required_resources/vendor/js/FileSaver.min.js"></script>

    <!-- Emperor library code -->
    <script type="text/javascript" src="emperor_required_resources/js/animate.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/draw.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/emperor.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/trajectory.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/ui.js"></script>
    <script type="text/javascript" src="emperor_required_resources/js/util.js"></script>
    <script type="text/javascript">


var g_mappingFileHeaders = ['SampleID','Treatment','DOB','Description'];
var g_mappingFileData = { 'PC.636': ['PC.636','Fast','20080116','Fasting_mouse_I.D._636'],'PC.355': ['PC.355','Control','20061218','Control_mouse_I.D._355'],'PC.607': ['PC.607','Fast','20071112','Fasting_mouse_I.D._607'],'PC.634': ['PC.634','Fast','20080116','Fasting_mouse_I.D._634'],'PC.635': ['PC.635','Fast','20080116','Fasting_mouse_I.D._635'],'PC.593': ['PC.593','Control','20071210','Control_mouse_I.D._593'],'PC.356': ['PC.356','Control','20061126','Control_mouse_I.D._356'],'PC.481': ['PC.481','Control','20070314','Control_mouse_I.D._481'],'PC.354': ['PC.354','Control','20061218','Ctrol_mouse_I.D._354'] };
var g_animatableMappingFileHeaders = ['DOB'];


var g_spherePositions = new Array();
g_spherePositions['PC.354'] = { 'name': 'PC.354', 'color': 0, 'x': -0.276542, 'y': -0.144964, 'z': 0.066647, 'P1': -0.276542, 'P2': -0.144964, 'P3': 0.066647, 'P4': -0.067711, 'P5': 0.176070, 'P6': 0.072969, 'P7': -0.229889, 'P8': -0.046599 };
g_spherePositions['PC.355'] = { 'name': 'PC.355', 'color': 0, 'x': -0.237661, 'y': 0.046053, 'z': -0.138136, 'P1': -0.237661, 'P2': 0.046053, 'P3': -0.138136, 'P4': 0.159061, 'P5': -0.247485, 'P6': -0.115211, 'P7': -0.112864, 'P8': 0.064794 };
g_spherePositions['PC.356'] = { 'name': 'PC.356', 'color': 0, 'x': 0.228820, 'y': -0.130142, 'z': -0.287149, 'P1': 0.228820, 'P2': -0.130142, 'P3': -0.287149, 'P4': 0.086450, 'P5': 0.044295, 'P6': 0.206043, 'P7': 0.031000, 'P8': 0.071992 };
g_spherePositions['PC.481'] = { 'name': 'PC.481', 'color': 0, 'x': 0.042263, 'y': -0.013968, 'z': 0.063531, 'P1': 0.042263, 'P2': -0.013968, 'P3': 0.063531, 'P4': -0.346121, 'P5': -0.127814, 'P6': 0.013935, 'P7': 0.030021, 'P8': 0.140148 };
g_spherePositions['PC.593'] = { 'name': 'PC.593', 'color': 0, 'x': 0.280399, 'y': -0.006013, 'z': 0.023485, 'P1': 0.280399, 'P2': -0.006013, 'P3': 0.023485, 'P4': -0.046811, 'P5': -0.146624, 'P6': 0.005670, 'P7': -0.035430, 'P8': -0.255786 };
g_spherePositions['PC.607'] = { 'name': 'PC.607', 'color': 0, 'x': 0.232873, 'y': 0.139788, 'z': 0.322871, 'P1': 0.232873, 'P2': 0.139788, 'P3': 0.322871, 'P4': 0.183347, 'P5': 0.020466, 'P6': 0.054059, 'P7': -0.036625, 'P8': 0.099824 };
g_spherePositions['PC.634'] = { 'name': 'PC.634', 'color': 0, 'x': 0.170518, 'y': -0.194113, 'z': -0.030897, 'P1': 0.170518, 'P2': -0.194113, 'P3': -0.030897, 'P4': 0.019809, 'P5': 0.155100, 'P6': -0.279924, 'P7': 0.057609, 'P8': 0.024248 };
g_spherePositions['PC.635'] = { 'name': 'PC.635', 'color': 0, 'x': -0.091330, 'y': 0.424147, 'z': -0.135627, 'P1': -0.091330, 'P2': 0.424147, 'P3': -0.135627, 'P4': -0.057519, 'P5': 0.151363, 'P6': -0.025394, 'P7': 0.051731, 'P8': -0.038738 };
g_spherePositions['PC.636'] = { 'name': 'PC.636', 'color': 0, 'x': -0.349339, 'y': -0.120788, 'z': 0.115275, 'P1': -0.349339, 'P2': -0.120788, 'P3': 0.115275, 'P4': 0.069495, 'P5': -0.025372, 'P6': 0.067853, 'P7': 0.244448, 'P8': -0.059883 };

var g_ellipsesDimensions = new Array();
var g_segments = 8, g_rings = 8, g_radius = 0.007557;
var g_xAxisLength = 0.629738;
var g_yAxisLength = 0.618260;
var g_zAxisLength = 0.610021;
var g_xMaximumValue = 0.280399;
var g_yMaximumValue = 0.424147;
var g_zMaximumValue = 0.322871;
var g_xMinimumValue = -0.349339;
var g_yMinimumValue = -0.194113;
var g_zMinimumValue = -0.287149;
var g_maximum = 0.424147;
var g_pc1Label = "PC1 (0.27 %)";
var g_pc2Label = "PC2 (0.16 %)";
var g_pc3Label = "PC3 (0.14 %)";
var g_number_of_custom_axes = 0;
var g_fractionExplained = [0.002669, 0.001626, 0.001378, 0.001122, 0.001002, 0.000823, 0.000756, 0.000625];
var g_fractionExplainedRounded = [0.27, 0.16, 0.14, 0.11, 0.10, 0.08, 0.08, 0.06];


var g_taxaPositions = new Array();



var g_comparisonPositions = new Array();
var g_isSerialComparisonPlot = true;


var g_vectorPositions = new Array();

document.getElementById("logo").style.display = 'none';
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
        <ul id="emperor-menu-list">
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
            <br><br>
            <select id="colorbycombo" onchange="colorByMenuChanged()" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="colorbylist">
            </div>
        </div>
        <div id="showby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td>
                        <select id="showbycombo" onchange="showByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="showbylist" style="height:100%;width:100%">
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
                        <div class="list" id="scalingbylist" style="height:100%;width:100%">
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
                </form>
                <br>
                <label for="labelopacity" class="text">Label Opacity</label>
                <label id="labelopacity" class="slidervalue"></label>
                <div id="lopacityslider" class="slider-range-max"></div>
                <div id="label-color-holder clearfix">
                    <table class="emperor-tab-table">
                        <tr><td><div id="labelColor" class="colorbox"></div></td><td><label>Master Label Color</label></td></tr>
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
                <tr><td><div id="rendererbackgroundcolor" class="colorbox" name="rendererbackgroundcolor"></div></td><td title="Background Color Title">Background Color</td></tr>
                <tr><td colspan="2">
                        <div id="pcoaviewoptions" class="">
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
