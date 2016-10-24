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

EMPEROR_HEADER_HTML_STRING =\
"""<!doctype html>
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
            </form>
            <br>
            <p>Visible Taxonomy Level: <span id="taxaLevel"></span></p>
            <div id="selectTaxaLevel"></div>"""

_TAXA_LABELS_COLOR_SELECTOR = """
            <tr><td><div id="taxalabelcolor" class="colorbox"></div></td><td><label>Taxa Label Color</label></td></tr>
"""

_BIPLOT_VISIBILITY_SELECTOR = """
            <br>
            <form name="biplotsvisibility">
            <input type="checkbox" onClick="toggleBiplotVisibility(false)" checked>Taxa Sphere Visibility</input>
            <br><br>
            <input type="checkbox" onClick="toggleBiplotVisibility(true)" checked>Taxa Arrow Visibility</input>
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
            <select id="colormap-drop-down" class="emperor-tab-drop-down" onchange="colorByMenuChanged()"></select>{biplot_spheres_color_selector}
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
