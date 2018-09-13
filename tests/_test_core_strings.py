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

PCOA_STRING = u"""Eigvals	9
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

HTML_STRING = u"""
<script type="text/javascript">

if ($("#emperor-css").length == 0){{
    $("head").append([

        '<link id="emperor-css" rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/css/emperor.css">',
        '<link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/css/jquery-ui.min.css">',
        '<link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/css/slick.grid.min.css">',
        '<link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/css/spectrum.min.css">',
        '<link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/css/chosen.min.css">',
        '<link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/css/jquery.contextMenu.min.css">'
    ]);
}}
</script>

<div id='emperor-notebook-0x9cb72f54' style="position: relative; width:100%; height:500px;">
  <div class='loading' style="position: absolute;top: 50%;left: 50%;margin-left: -229px; margin-top: -59px; z-index: 10000;height:118px;width:458px;padding:0px"><img src='https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/img/emperor.png' alt='Emperor resources missing. Expected them to be found in https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files'></div>
</div>
</div>

<script type="text/javascript">
// When running in the Jupyter notebook we've encountered version conflicts
// with some dependencies. So instead of polluting the global require context,
// we define a new context.
var emperorRequire = require.config({
'context': 'emperor',
// the left side is the module name, and the right side is the path
// relative to the baseUrl attribute, do NOT include the .js extension
'paths': {
  /* jQuery */
  'jquery': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/jquery-2.1.4.min',
  'jqueryui': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/jquery-ui.min',
  'jquery_drag': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/jquery.event.drag-2.2.min',

  /* jQuery plugins */
  'chosen': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/chosen.jquery.min',
  'spectrum': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/spectrum.min',
  'position': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/jquery.ui.position.min',
  'contextmenu': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/jquery.contextMenu.min',

  /* other libraries */
  'underscore': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/underscore-min',
  'chroma': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/chroma.min',
  'filesaver': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/FileSaver.min',
  'blob': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/Blob',
  'canvastoblob': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/canvas-toBlob',
  'd3': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/d3.min',

  /* THREE.js and plugins */
  'three': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/three.min',
  'orbitcontrols': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/three.js-plugins/OrbitControls',
  'projector': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/three.js-plugins/Projector',
  'svgrenderer': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/three.js-plugins/SVGRenderer',
  'canvasrenderer': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/three.js-plugins/CanvasRenderer',

  /* SlickGrid */
  'slickcore': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/slick.core.min',
  'slickgrid': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/slick.grid.min',
  'slickformatters': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/slick.editors.min',
  'slickeditors': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/slick.formatters.min',

  /* Emperor's objects */
  'util': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/util',
  'model': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/model',
  'view': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/view',
  'controller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/controller',
  'draw': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/draw',
  'scene3d': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/sceneplotview3d',
  'shapes': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shapes',
  'animationdirector': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/animate',
  'trajectory': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/trajectory',

  /* controllers */
  'abcviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/abc-view-controller',
  'viewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/view-controller',
  'colorviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/color-view-controller',
  'visibilitycontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/visibility-controller',
  'opacityviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/opacity-view-controller',
  'scaleviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/scale-view-controller',
  'shapecontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shape-controller',
  'axescontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/axes-controller',
  'animationscontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/animations-controller',

  /* editors */
  'shape-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shape-editor',
  'color-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/color-editor',
  'scale-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/scale-editor'

},
/*
   Libraries that are not AMD compatible need shim to declare their
   dependencies.
 */
'shim': {
  'jquery_drag': {
    'deps': ['jquery', 'jqueryui']
  },
  'chosen': {
    'deps': ['jquery'],
    'exports': 'jQuery.fn.chosen'
  },
  'contextmenu' : {
    'deps': ['jquery', 'jqueryui', 'position']
  },
  'filesaver' : {
    'deps': ['blob']
  },
  'canvastoblob' : {
    'deps': ['blob']
  },
  'slickcore': ['jqueryui'],
  'slickgrid': ['slickcore', 'jquery_drag', 'slickformatters', 'slickeditors']
}
});

emperorRequire(
["jquery", "model", "controller"],
function($, model, EmperorController) {
  var DecompositionModel = model.DecompositionModel;

  var div = $('#emperor-notebook-0x9cb72f54');

  var data = {"plot": {"decomposition": {"axes_names": [0, 1, 2, 3, 4], "ci": null, "coordinates": [[-0.651995810831719, -0.3417784983371589, 0.15713116241738878, -0.15964022322388774, 0.41511600449567154], [-0.5603276951316744, 0.10857735915373172, -0.32567898978232684, 0.3750137797216106, -0.583487828830988], [0.5394835270542403, -0.3068324227225251, -0.6770043110217822, 0.203820501907719, 0.1044335488558445], [0.09964194790906594, -0.03293232371368659, 0.14978636968698092, -0.8160388524355932, -0.301343079001781], [0.661089243947507, -0.014176279685000464, 0.05537095913733857, -0.11036487613740434, -0.3456924105084198], [0.5490376828031979, 0.32957520954888647, 0.7612242145083941, 0.4322721667939822, 0.04825249860931067], [0.40202458647314415, -0.4576554852461752, -0.0728438902229666, 0.04670222577076932, 0.36567512814466946], [-0.21532604614952783, 1.0, -0.31976501999316115, -0.13561208920603846, 0.35686551552017187], [-0.8236274360749414, -0.2847775589983077, 0.27177950526966277, 0.16384736680860681, -0.05981937728235736]], "edges": [], "percents_explained": [26.6887048633, 16.256370402199998, 13.775412916099999, 11.217215823, 10.024774995000001], "sample_ids": ["PC.636", "PC.635", "PC.356", "PC.481", "PC.354", "PC.593", "PC.355", "PC.607", "PC.634"]}, "metadata": [["PC.636", "Fast", "20080116", "Fasting_mouse_I.D._636"], ["PC.635", "Fast", "20080116", "Fasting_mouse_I.D._635"], ["PC.356", "Control", "20061126", "Control_mouse_I.D._356"], ["PC.481", "Control", "20070314", "Control_mouse_I.D._481"], ["PC.354", "Control", "20061218", "Ctrol_mouse_I.D._354"], ["PC.593", "Control", "20071210", "Control_mouse_I.D._593"], ["PC.355", "Control", "20061218", "Control_mouse_I.D._355"], ["PC.607", "Fast", "20071112", "Fasting_mouse_I.D._607"], ["PC.634", "Fast", "20080116", "Fasting_mouse_I.D._634"]], "metadata_headers": ["SampleID", "Treatment", "DOB", "Description"], "settings": {}, "type": "scatter"}};

  var plot, biplot = null, ec;

  function init() {
    // Initialize the DecompositionModel for the scatter plot, and optionally
    // add one for the biplot arrows
    plot = new DecompositionModel(data.plot.decomposition,
                                  data.plot.metadata_headers,
                                  data.plot.metadata,
                                  data.plot.type);

    if (data.biplot) {
      biplot = new DecompositionModel(data.biplot.decomposition,
                                      data.biplot.metadata_headers,
                                      data.biplot.metadata,
                                      data.biplot.type);
    }

    ec = new EmperorController(plot, biplot, "emperor-notebook-0x9cb72f54");
  }

  function animate() {
    requestAnimationFrame(animate);
    ec.render();
  }
  $(window).resize(function() {
    ec.resize(div.innerWidth(), div.innerHeight());
  });

  $(function(){
    init();
    animate();

    ec.ready = function () {
      // any other code that needs to be executed when emperor is loaded should
      // go here
      ec.loadConfig(data.plot.settings);
    }
  });

}); // END REQUIRE.JS block
</script>"""

STANDALONE_HTML_STRING = """<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Emperor</title>
    <!-- core dependencies that are otherwise included via the jupyter notebook -->
    <script src="./some-local-path//vendor/js/require-2.1.22.min.js"></script>
    <script src="./some-local-path//vendor/js/jquery-2.1.4.min.js"></script>
    <meta charset="utf-8">

    <script type="text/javascript">

if ($("#emperor-css").length == 0){{
    $("head").append([

        '<link id="emperor-css" rel="stylesheet" type="text/css" href="./some-local-path//css/emperor.css">',
        '<link rel="stylesheet" type="text/css" href="./some-local-path//vendor/css/jquery-ui.min.css">',
        '<link rel="stylesheet" type="text/css" href="./some-local-path//vendor/css/slick.grid.min.css">',
        '<link rel="stylesheet" type="text/css" href="./some-local-path//vendor/css/spectrum.min.css">',
        '<link rel="stylesheet" type="text/css" href="./some-local-path//vendor/css/chosen.min.css">',
        '<link rel="stylesheet" type="text/css" href="./some-local-path//vendor/css/jquery.contextMenu.min.css">'
    ]);
}}
</script>


    <style>
      #emperor-notebook-0x9cb72f54 {
        height:100vh !important;
        padding: 0px !important;
      }
      body {
        margin: 0;
        padding: 0;
        border: 0;
        outline: 0;
      }
    </style>
  </head>
  <body>
    <div id='emperor-notebook-0x9cb72f54' style="position: relative; width:100%; height:500px;">
  <div class='loading' style="position: absolute;top: 50%;left: 50%;margin-left: -229px; margin-top: -59px; z-index: 10000;height:118px;width:458px;padding:0px"><img src='./some-local-path//img/emperor.png' alt='Emperor resources missing. Expected them to be found in ./some-local-path/'></div>
</div>
</div>

<script type="text/javascript">
// When running in the Jupyter notebook we've encountered version conflicts
// with some dependencies. So instead of polluting the global require context,
// we define a new context.
var emperorRequire = require.config({
'context': 'emperor',
// the left side is the module name, and the right side is the path
// relative to the baseUrl attribute, do NOT include the .js extension
'paths': {
  /* jQuery */
  'jquery': './some-local-path//vendor/js/jquery-2.1.4.min',
  'jqueryui': './some-local-path//vendor/js/jquery-ui.min',
  'jquery_drag': './some-local-path//vendor/js/jquery.event.drag-2.2.min',

  /* jQuery plugins */
  'chosen': './some-local-path//vendor/js/chosen.jquery.min',
  'spectrum': './some-local-path//vendor/js/spectrum.min',
  'position': './some-local-path//vendor/js/jquery.ui.position.min',
  'contextmenu': './some-local-path//vendor/js/jquery.contextMenu.min',

  /* other libraries */
  'underscore': './some-local-path//vendor/js/underscore-min',
  'chroma': './some-local-path//vendor/js/chroma.min',
  'filesaver': './some-local-path//vendor/js/FileSaver.min',
  'blob': './some-local-path//vendor/js/Blob',
  'canvastoblob': './some-local-path//vendor/js/canvas-toBlob',
  'd3': './some-local-path//vendor/js/d3.min',

  /* THREE.js and plugins */
  'three': './some-local-path//vendor/js/three.min',
  'orbitcontrols': './some-local-path//vendor/js/three.js-plugins/OrbitControls',
  'projector': './some-local-path//vendor/js/three.js-plugins/Projector',
  'svgrenderer': './some-local-path//vendor/js/three.js-plugins/SVGRenderer',
  'canvasrenderer': './some-local-path//vendor/js/three.js-plugins/CanvasRenderer',

  /* SlickGrid */
  'slickcore': './some-local-path//vendor/js/slick.core.min',
  'slickgrid': './some-local-path//vendor/js/slick.grid.min',
  'slickformatters': './some-local-path//vendor/js/slick.editors.min',
  'slickeditors': './some-local-path//vendor/js/slick.formatters.min',

  /* Emperor's objects */
  'util': './some-local-path//js/util',
  'model': './some-local-path//js/model',
  'view': './some-local-path//js/view',
  'controller': './some-local-path//js/controller',
  'draw': './some-local-path//js/draw',
  'scene3d': './some-local-path//js/sceneplotview3d',
  'shapes': './some-local-path//js/shapes',
  'animationdirector': './some-local-path//js/animate',
  'trajectory': './some-local-path//js/trajectory',

  /* controllers */
  'abcviewcontroller': './some-local-path//js/abc-view-controller',
  'viewcontroller': './some-local-path//js/view-controller',
  'colorviewcontroller': './some-local-path//js/color-view-controller',
  'visibilitycontroller': './some-local-path//js/visibility-controller',
  'opacityviewcontroller': './some-local-path//js/opacity-view-controller',
  'scaleviewcontroller': './some-local-path//js/scale-view-controller',
  'shapecontroller': './some-local-path//js/shape-controller',
  'axescontroller': './some-local-path//js/axes-controller',
  'animationscontroller': './some-local-path//js/animations-controller',

  /* editors */
  'shape-editor': './some-local-path//js/shape-editor',
  'color-editor': './some-local-path//js/color-editor',
  'scale-editor': './some-local-path//js/scale-editor'

},
/*
   Libraries that are not AMD compatible need shim to declare their
   dependencies.
 */
'shim': {
  'jquery_drag': {
    'deps': ['jquery', 'jqueryui']
  },
  'chosen': {
    'deps': ['jquery'],
    'exports': 'jQuery.fn.chosen'
  },
  'contextmenu' : {
    'deps': ['jquery', 'jqueryui', 'position']
  },
  'filesaver' : {
    'deps': ['blob']
  },
  'canvastoblob' : {
    'deps': ['blob']
  },
  'slickcore': ['jqueryui'],
  'slickgrid': ['slickcore', 'jquery_drag', 'slickformatters', 'slickeditors']
}
});

emperorRequire(
["jquery", "model", "controller"],
function($, model, EmperorController) {
  var DecompositionModel = model.DecompositionModel;

  var div = $('#emperor-notebook-0x9cb72f54');

  var data = {"plot": {"decomposition": {"axes_names": [0, 1, 2, 3, 4], "ci": null, "coordinates": [[-0.651995810831719, -0.3417784983371589, 0.15713116241738878, -0.15964022322388774, 0.41511600449567154], [-0.5603276951316744, 0.10857735915373172, -0.32567898978232684, 0.3750137797216106, -0.583487828830988], [0.5394835270542403, -0.3068324227225251, -0.6770043110217822, 0.203820501907719, 0.1044335488558445], [0.09964194790906594, -0.03293232371368659, 0.14978636968698092, -0.8160388524355932, -0.301343079001781], [0.661089243947507, -0.014176279685000464, 0.05537095913733857, -0.11036487613740434, -0.3456924105084198], [0.5490376828031979, 0.32957520954888647, 0.7612242145083941, 0.4322721667939822, 0.04825249860931067], [0.40202458647314415, -0.4576554852461752, -0.0728438902229666, 0.04670222577076932, 0.36567512814466946], [-0.21532604614952783, 1.0, -0.31976501999316115, -0.13561208920603846, 0.35686551552017187], [-0.8236274360749414, -0.2847775589983077, 0.27177950526966277, 0.16384736680860681, -0.05981937728235736]], "edges": [], "percents_explained": [26.6887048633, 16.256370402199998, 13.775412916099999, 11.217215823, 10.024774995000001], "sample_ids": ["PC.636", "PC.635", "PC.356", "PC.481", "PC.354", "PC.593", "PC.355", "PC.607", "PC.634"]}, "metadata": [["PC.636", "Fast", "20080116", "Fasting_mouse_I.D._636"], ["PC.635", "Fast", "20080116", "Fasting_mouse_I.D._635"], ["PC.356", "Control", "20061126", "Control_mouse_I.D._356"], ["PC.481", "Control", "20070314", "Control_mouse_I.D._481"], ["PC.354", "Control", "20061218", "Ctrol_mouse_I.D._354"], ["PC.593", "Control", "20071210", "Control_mouse_I.D._593"], ["PC.355", "Control", "20061218", "Control_mouse_I.D._355"], ["PC.607", "Fast", "20071112", "Fasting_mouse_I.D._607"], ["PC.634", "Fast", "20080116", "Fasting_mouse_I.D._634"]], "metadata_headers": ["SampleID", "Treatment", "DOB", "Description"], "settings": {}, "type": "scatter"}};

  var plot, biplot = null, ec;

  function init() {
    // Initialize the DecompositionModel for the scatter plot, and optionally
    // add one for the biplot arrows
    plot = new DecompositionModel(data.plot.decomposition,
                                  data.plot.metadata_headers,
                                  data.plot.metadata,
                                  data.plot.type);

    if (data.biplot) {
      biplot = new DecompositionModel(data.biplot.decomposition,
                                      data.biplot.metadata_headers,
                                      data.biplot.metadata,
                                      data.biplot.type);
    }

    ec = new EmperorController(plot, biplot, "emperor-notebook-0x9cb72f54");
  }

  function animate() {
    requestAnimationFrame(animate);
    ec.render();
  }
  $(window).resize(function() {
    ec.resize(div.innerWidth(), div.innerHeight());
  });

  $(function(){
    init();
    animate();

    ec.ready = function () {
      // any other code that needs to be executed when emperor is loaded should
      // go here
      ec.loadConfig(data.plot.settings);
    }
  });

}); // END REQUIRE.JS block
</script>
  </body>
</html>"""

MAP_PANDAS = """#SampleID	cat_a	cat_b	cat_c	num_1	num_2	num_3	num_4
s1	foo	a	o	21	18	75	51
s2	foo	b	p	3	42	44	36
s3	bar	c	q	53	70	5	78
s4	baz	d	r	47	13	72	72
s5	FOO	e	s	13	50	1	56
s6	FOO	f	o	13	56	39	5
s7	foo	g	o	77	17	26	64
s8	barosaurus	h	o	63	20	74	69
s9	baz	i	p	20	32	39	16
s10	baz	j	p	19	44	61	17
s11	baz	k	q	47	25	37	42
s12	baz	l	r	50	73	27	58
s13	asdf	m	s	11	36	41	32
s14	1234	n	s	9	32	42	25
"""

PROCRUSTES_COORDS = [[-0.651995810831719, -0.3417784983371589, 0.15713116241738878, -0.15964022322388774, 0.41511600449567154],
                     [-0.5603276951316744, 0.10857735915373172, -0.32567898978232684, 0.3750137797216106, -0.583487828830988],
                     [0.5394835270542403, -0.3068324227225251, -0.6770043110217822, 0.203820501907719, 0.1044335488558445],
                     [0.09964194790906594, -0.03293232371368659, 0.14978636968698092, -0.8160388524355932, -0.301343079001781],
                     [0.661089243947507, -0.014176279685000464, 0.05537095913733857, -0.11036487613740434, -0.3456924105084198],
                     [0.5490376828031979, 0.32957520954888647, 0.7612242145083941, 0.4322721667939822, 0.04825249860931067],
                     [0.40202458647314415, -0.4576554852461752, -0.0728438902229666, 0.04670222577076932, 0.36567512814466946],
                     [-0.21532604614952783, 1.0, -0.31976501999316115, -0.13561208920603846, 0.35686551552017187],
                     [-0.8236274360749414, -0.2847775589983077, 0.27177950526966277, 0.16384736680860681, -0.05981937728235736],
                     [-0.6634310362798682, -0.3510130178200738, 0.161823434317824, -0.1644035019392208, 0.42562182667156767],
                     [-0.5720666595928215, 0.11186298295493931, -0.33458644519808095, 0.38487085063789367, -0.5952371563006809],
                     [0.5511659026978382, -0.3153372408552198, -0.6881883423282821, 0.20980093595189256, 0.1075966261458557],
                     [0.10266290780155124, -0.03393977028392673, 0.15426974010191444, -0.8243378024371981, -0.30972677917347763],
                     [0.6724419148088799, -0.014610339283797295, 0.057061445273222926, -0.11370325696164885, -0.35500399773440483],
                     [0.5607514429485241, 0.3385632773527147, 0.7709767609590733, 0.44301860965314516, 0.04972675659239302],
                     [0.41233158821549615, -0.4687146382667654, -0.07506278582541291, 0.04812933072285593, 0.375364706432626],
                     [-0.22161200875026232, 1.0, -0.32854837346785326, -0.13968814465616122, 0.36639168894586727],
                     [-0.8316906868062783, -0.2927856996591091, 0.27948280281041427, 0.1687292890141334, -0.0616447273352526],
                     [0.9620226739562296, 0.9895289404424465, 0.9977979655270016, 0.9977265255415432, 0.9845574301635451],
                     [0.9719087801715631, 0.9989578164186853, 0.9904923148126306, 0.9873942930501959, 0.969549178080792],
                     [0.9739522460622455, 0.9915613875240664, 0.9590724401081091, 0.9962835452282494, 0.9990371879740821],
                     [0.9991251199437706, 0.9999205225250398, 0.9980005962650546, 0.9407129001194223, 0.9918608589806137],
                     [0.9609624346908685, 1.0, 0.9997423022019966, 0.9989226251754129, 0.9892877630162716],
                     [0.9730250411393899, 0.9902634044107544, 0.9483455045565042, 0.9832567443082347, 0.9998086490045004],
                     [0.9855148843316903, 0.9812368404519857, 0.9995408089355806, 0.9998218895632658, 0.9880139384513328],
                     [0.9958503222204244, 0.9114065255759745, 0.9908346026547953, 0.9983642581258675, 0.9885842720139109],
                     [0.939616070382295, 0.9927319894788387, 0.9933812060303758, 0.99760420056383, 0.9996962140443878]]

PROCRUSTES_MAP = [['PC.636_0', 'Fast', '20080116', 'Fasting_mouse_I.D._636', 'Ordination 0'],
                  ['PC.635_0', 'Fast', '20080116', 'Fasting_mouse_I.D._635', 'Ordination 0'],
                  ['PC.356_0', 'Control', '20061126', 'Control_mouse_I.D._356', 'Ordination 0'],
                  ['PC.481_0', 'Control', '20070314', 'Control_mouse_I.D._481', 'Ordination 0'],
                  ['PC.354_0', 'Control', '20061218', 'Ctrol_mouse_I.D._354', 'Ordination 0'],
                  ['PC.593_0', 'Control', '20071210', 'Control_mouse_I.D._593', 'Ordination 0'],
                  ['PC.355_0', 'Control', '20061218', 'Control_mouse_I.D._355', 'Ordination 0'],
                  ['PC.607_0', 'Fast', '20071112', 'Fasting_mouse_I.D._607', 'Ordination 0'],
                  ['PC.634_0', 'Fast', '20080116', 'Fasting_mouse_I.D._634', 'Ordination 0'],
                  ['PC.636_1', 'Fast', '20080116', 'Fasting_mouse_I.D._636', 'Ordination 1'],
                  ['PC.635_1', 'Fast', '20080116', 'Fasting_mouse_I.D._635', 'Ordination 1'],
                  ['PC.356_1', 'Control', '20061126', 'Control_mouse_I.D._356', 'Ordination 1'],
                  ['PC.481_1', 'Control', '20070314', 'Control_mouse_I.D._481', 'Ordination 1'],
                  ['PC.354_1', 'Control', '20061218', 'Ctrol_mouse_I.D._354', 'Ordination 1'],
                  ['PC.593_1', 'Control', '20071210', 'Control_mouse_I.D._593', 'Ordination 1'],
                  ['PC.355_1', 'Control', '20061218', 'Control_mouse_I.D._355', 'Ordination 1'],
                  ['PC.607_1', 'Fast', '20071112', 'Fasting_mouse_I.D._607', 'Ordination 1'],
                  ['PC.634_1', 'Fast', '20080116', 'Fasting_mouse_I.D._634', 'Ordination 1'],
                  ['PC.636_2', 'Fast', '20080116', 'Fasting_mouse_I.D._636', 'Ordination 2'],
                  ['PC.635_2', 'Fast', '20080116', 'Fasting_mouse_I.D._635', 'Ordination 2'],
                  ['PC.356_2', 'Control', '20061126', 'Control_mouse_I.D._356', 'Ordination 2'],
                  ['PC.481_2', 'Control', '20070314', 'Control_mouse_I.D._481', 'Ordination 2'],
                  ['PC.354_2', 'Control', '20061218', 'Ctrol_mouse_I.D._354', 'Ordination 2'],
                  ['PC.593_2', 'Control', '20071210', 'Control_mouse_I.D._593', 'Ordination 2'],
                  ['PC.355_2', 'Control', '20061218', 'Control_mouse_I.D._355', 'Ordination 2'],
                  ['PC.607_2', 'Fast', '20071112', 'Fasting_mouse_I.D._607', 'Ordination 2'],
                  ['PC.634_2', 'Fast', '20080116', 'Fasting_mouse_I.D._634', 'Ordination 2']]

JACKKNIFED_SDEV = {'plot': {'decomposition': {'axes_names': [0, 1, 2, 3, 4],
                            'ci': [[0.15320242779027135, 0.32236552837806803, 0.5466426785698062, 0.41825529878880174, 0.2830130780228252],
                                   [0.2039091519703831, 0.5282908986822961, 0.3309487258366068, 0.6617111925195454, 0.8042017991635314],
                                   [0.7723912455913174, 0.34097058412680936, 0.1392698873994429, 0.5671696411542587, 0.446777128222758],
                                   [0.5252734491219532, 0.48332642496887657, 0.5436622163727768, 0.06107928238127947, 0.6177937137186658],
                                   [0.8619539593286029, 0.49283955936772467, 0.5120907361250878, 0.44372526843615145, 0.6437250003177745],
                                   [0.779233017307759, 0.6341156772712444, 0.9389398372025733, 0.698525460180768, 0.47553287337053074],
                                   [0.6788150679433408, 0.25999975777266915, 0.4629798250204843, 0.5098668968373103, 0.30958817362421626],
                                   [0.38922575751620364, 1.1297049251810314, 0.3340965570902247, 0.43070102800078963, 0.3143037650900199],
                                   [0.05677781772085612, 0.35266273082319943, 0.601451667218675, 0.5494291669314351, 0.5132784041987718]],
                            'coordinates': [[-0.7323613329748839, -0.5060247387342096, -0.2089936328022944, -0.37035261848213485, 0.560102816456614],
                                            [-0.6661577075069334, -0.2217737083659365, -0.4941091848938413, -0.15063086060307557, 0.09357800544502778],
                                            [-0.10569658584110184, -0.48014086845608406, -0.7503173511199889, -0.1966206523190892, 0.3288752279579067],
                                            [-0.22411555303555486, -0.27493123505908496, -0.21093271404078504, -0.8492821018569516, 0.170533519951784],
                                            [-0.07213012997049714, -0.26074072466344955, -0.23567021423219342, -0.3333389086029676, 0.1585709413204667],
                                            [-0.10306839954771646, -0.16292503176450995, -0.04434218589935773, -0.13505953366377238, 0.28651010070387867],
                                            [-0.14329582402904856, -0.5913156123027754, -0.30507284380173166, -0.23792313971010245, 0.5236822252933244],
                                            [-0.4120286058174356, 0.022148368606006386, -0.48972825402724274, -0.35231914529852637, 0.5171767480000304],
                                            [-0.854640407334614, -0.4637682017836408, -0.1784746008049904, -0.20721872788742415, 0.2345128716772838]],
                            'edges': [],
                            'percents_explained': [26.6887048633,
                                                   16.256370402199998,
                                                   13.775412916099999,
                                                   11.217215823,
                                                   10.024774995000001],
                            'sample_ids': ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354', 'PC.593', 'PC.355', 'PC.607', 'PC.634']},
          'metadata': [['PC.636', 'Fast', '20080116', 'Fasting_mouse_I.D._636'],
                       ['PC.635', 'Fast', '20080116', 'Fasting_mouse_I.D._635'],
                       ['PC.356', 'Control', '20061126', 'Control_mouse_I.D._356'],
                       ['PC.481', 'Control', '20070314', 'Control_mouse_I.D._481'],
                       ['PC.354', 'Control', '20061218', 'Ctrol_mouse_I.D._354'],
                       ['PC.593', 'Control', '20071210', 'Control_mouse_I.D._593'],
                       ['PC.355', 'Control', '20061218', 'Control_mouse_I.D._355'],
                       ['PC.607', 'Fast', '20071112', 'Fasting_mouse_I.D._607'],
                       ['PC.634', 'Fast', '20080116', 'Fasting_mouse_I.D._634']],
          'metadata_headers': ['SampleID', 'Treatment', 'DOB', 'Description'],
          'settings': {},
          'type': 'scatter'}}

CUSTOM_AXES_JSON = '  var data = {"plot": {"decomposition": {"axes_names": ["DOB", 0, 1, 2, 3, 4], "ci": null, "coordinates": [[1.322178487895014, -0.651995810831719, -0.3417784983371589, 0.15713116241738878, -0.15964022322388774, 0.41511600449567154], [1.322178487895014, -0.5603276951316744, 0.10857735915373172, -0.32567898978232684, 0.3750137797216106, -0.583487828830988], [-0.8236274360749414, 0.5394835270542403, -0.3068324227225251, -0.6770043110217822, 0.203820501907719, 0.1044335488558445], [0.21458556178898447, 0.09964194790906594, -0.03293232371368659, 0.14978636968698092, -0.8160388524355932, -0.301343079001781], [-0.813231746501206, 0.661089243947507, -0.014176279685000464, 0.05537095913733857, -0.11036487613740434, -0.3456924105084198], [0.3158305385071034, 0.5490376828031979, 0.32957520954888647, 0.7612242145083941, 0.4322721667939822, 0.04825249860931067], [-0.813231746501206, 0.40202458647314415, -0.4576554852461752, -0.0728438902229666, 0.04670222577076932, 0.36567512814466946], [0.30475686917855915, -0.21532604614952783, 1.0, -0.31976501999316115, -0.13561208920603846, 0.35686551552017187], [1.322178487895014, -0.8236274360749414, -0.2847775589983077, 0.27177950526966277, 0.16384736680860681, -0.05981937728235736]], "edges": [], "percents_explained": [-1, 26.6887048633, 16.256370402199998, 13.775412916099999, 11.217215823, 10.024774995000001], "sample_ids": ["PC.636", "PC.635", "PC.356", "PC.481", "PC.354", "PC.593", "PC.355", "PC.607", "PC.634"]}, "metadata": [["PC.636", "Fast", "20080116", "Fasting_mouse_I.D._636"], ["PC.635", "Fast", "20080116", "Fasting_mouse_I.D._635"], ["PC.356", "Control", "20061126", "Control_mouse_I.D._356"], ["PC.481", "Control", "20070314", "Control_mouse_I.D._481"], ["PC.354", "Control", "20061218", "Ctrol_mouse_I.D._354"], ["PC.593", "Control", "20071210", "Control_mouse_I.D._593"], ["PC.355", "Control", "20061218", "Control_mouse_I.D._355"], ["PC.607", "Fast", "20071112", "Fasting_mouse_I.D._607"], ["PC.634", "Fast", "20080116", "Fasting_mouse_I.D._634"]], "metadata_headers": ["SampleID", "Treatment", "DOB", "Description"], "settings": {}, "type": "scatter"}};'
