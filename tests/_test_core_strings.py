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
requirejs.config({
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
  'abcviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/abc-view-controller',
  'viewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/view-controller',
  'colorviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/color-view-controller',
  'visibilitycontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/visibility-controller',
  'scaleviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/scale-view-controller',
  'shapecontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shape-controller',
  'axescontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/axes-controller',
  'shape-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shape-editor',
  'color-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/color-editor',
  'scale-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/scale-editor',
  'shapes': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shapes'
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

requirejs(
["jquery", "model", "controller"],
function($, model, EmperorController) {
  var DecompositionModel = model.DecompositionModel;

  var div = $('#emperor-notebook-0x9cb72f54');

  var data = {
    // coordinates information
    'sample_ids': ["PC.636", "PC.635", "PC.356", "PC.481", "PC.354", "PC.593", "PC.355", "PC.607", "PC.634"],
    'coordinates': [[-0.651995810831719, -0.3417784983371589, 0.15713116241738878, -0.15964022322388774, 0.41511600449567154], [-0.5603276951316744, 0.10857735915373172, -0.32567898978232684, 0.3750137797216106, -0.583487828830988], [0.5394835270542403, -0.3068324227225251, -0.6770043110217822, 0.203820501907719, 0.1044335488558445], [0.09964194790906594, -0.03293232371368659, 0.14978636968698092, -0.8160388524355932, -0.301343079001781], [0.661089243947507, -0.014176279685000464, 0.05537095913733857, -0.11036487613740434, -0.3456924105084198], [0.5490376828031979, 0.32957520954888647, 0.7612242145083941, 0.4322721667939822, 0.04825249860931067], [0.40202458647314415, -0.4576554852461752, -0.0728438902229666, 0.04670222577076932, 0.36567512814466946], [-0.21532604614952783, 1.0, -0.31976501999316115, -0.13561208920603846, 0.35686551552017187], [-0.8236274360749414, -0.2847775589983077, 0.27177950526966277, 0.16384736680860681, -0.05981937728235736]],
    'axes_names': [0, 1, 2, 3, 4],
    'percents_explained': [26.6887048633, 16.256370402199998, 13.775412916099999, 11.217215823, 10.024774995000001],

    // sample information
    'metadata_headers': ["SampleID", "Treatment", "DOB", "Description"],
    'metadata': [["PC.636", "Fast", "20080116", "Fasting_mouse_I.D._636"], ["PC.635", "Fast", "20080116", "Fasting_mouse_I.D._635"], ["PC.356", "Control", "20061126", "Control_mouse_I.D._356"], ["PC.481", "Control", "20070314", "Control_mouse_I.D._481"], ["PC.354", "Control", "20061218", "Ctrol_mouse_I.D._354"], ["PC.593", "Control", "20071210", "Control_mouse_I.D._593"], ["PC.355", "Control", "20061218", "Control_mouse_I.D._355"], ["PC.607", "Fast", "20071112", "Fasting_mouse_I.D._607"], ["PC.634", "Fast", "20080116", "Fasting_mouse_I.D._634"]],
    'settings': {}
  }

  var dm, ec;

  function init() {
    // Initialize the DecompositionModel
    dm = new DecompositionModel('', data['sample_ids'],
                                data['coordinates'],
                                data['percents_explained'],
                                data['metadata_headers'], data['metadata'],
                                data['axes_names']);
    // Initialize the EmperorController
    ec = new EmperorController(dm, "emperor-notebook-0x9cb72f54");
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
      ec.loadConfig(data['settings']);
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
requirejs.config({
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
  'abcviewcontroller': './some-local-path//js/abc-view-controller',
  'viewcontroller': './some-local-path//js/view-controller',
  'colorviewcontroller': './some-local-path//js/color-view-controller',
  'visibilitycontroller': './some-local-path//js/visibility-controller',
  'scaleviewcontroller': './some-local-path//js/scale-view-controller',
  'shapecontroller': './some-local-path//js/shape-controller',
  'axescontroller': './some-local-path//js/axes-controller',
  'shape-editor': './some-local-path//js/shape-editor',
  'color-editor': './some-local-path//js/color-editor',
  'scale-editor': './some-local-path//js/scale-editor',
  'shapes': './some-local-path//js/shapes'
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

requirejs(
["jquery", "model", "controller"],
function($, model, EmperorController) {
  var DecompositionModel = model.DecompositionModel;

  var div = $('#emperor-notebook-0x9cb72f54');

  var data = {
    // coordinates information
    'sample_ids': ["PC.636", "PC.635", "PC.356", "PC.481", "PC.354", "PC.593", "PC.355", "PC.607", "PC.634"],
    'coordinates': [[-0.651995810831719, -0.3417784983371589, 0.15713116241738878, -0.15964022322388774, 0.41511600449567154], [-0.5603276951316744, 0.10857735915373172, -0.32567898978232684, 0.3750137797216106, -0.583487828830988], [0.5394835270542403, -0.3068324227225251, -0.6770043110217822, 0.203820501907719, 0.1044335488558445], [0.09964194790906594, -0.03293232371368659, 0.14978636968698092, -0.8160388524355932, -0.301343079001781], [0.661089243947507, -0.014176279685000464, 0.05537095913733857, -0.11036487613740434, -0.3456924105084198], [0.5490376828031979, 0.32957520954888647, 0.7612242145083941, 0.4322721667939822, 0.04825249860931067], [0.40202458647314415, -0.4576554852461752, -0.0728438902229666, 0.04670222577076932, 0.36567512814466946], [-0.21532604614952783, 1.0, -0.31976501999316115, -0.13561208920603846, 0.35686551552017187], [-0.8236274360749414, -0.2847775589983077, 0.27177950526966277, 0.16384736680860681, -0.05981937728235736]],
    'axes_names': [0, 1, 2, 3, 4],
    'percents_explained': [26.6887048633, 16.256370402199998, 13.775412916099999, 11.217215823, 10.024774995000001],

    // sample information
    'metadata_headers': ["SampleID", "Treatment", "DOB", "Description"],
    'metadata': [["PC.636", "Fast", "20080116", "Fasting_mouse_I.D._636"], ["PC.635", "Fast", "20080116", "Fasting_mouse_I.D._635"], ["PC.356", "Control", "20061126", "Control_mouse_I.D._356"], ["PC.481", "Control", "20070314", "Control_mouse_I.D._481"], ["PC.354", "Control", "20061218", "Ctrol_mouse_I.D._354"], ["PC.593", "Control", "20071210", "Control_mouse_I.D._593"], ["PC.355", "Control", "20061218", "Control_mouse_I.D._355"], ["PC.607", "Fast", "20071112", "Fasting_mouse_I.D._607"], ["PC.634", "Fast", "20080116", "Fasting_mouse_I.D._634"]],
    'settings': {}
  }

  var dm, ec;

  function init() {
    // Initialize the DecompositionModel
    dm = new DecompositionModel('', data['sample_ids'],
                                data['coordinates'],
                                data['percents_explained'],
                                data['metadata_headers'], data['metadata'],
                                data['axes_names']);
    // Initialize the EmperorController
    ec = new EmperorController(dm, "emperor-notebook-0x9cb72f54");
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
      ec.loadConfig(data['settings']);
    }
  });

}); // END REQUIRE.JS block
</script>
  </body>
</html>"""

HTML_STRING_CUSTOM_AXES = u"""
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
requirejs.config({
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
  'abcviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/abc-view-controller',
  'viewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/view-controller',
  'colorviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/color-view-controller',
  'visibilitycontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/visibility-controller',
  'scaleviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/scale-view-controller',
  'shapecontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shape-controller',
  'axescontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/axes-controller',
  'shape-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shape-editor',
  'color-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/color-editor',
  'scale-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/scale-editor',
  'shapes': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shapes'
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

requirejs(
["jquery", "model", "controller"],
function($, model, EmperorController) {
  var DecompositionModel = model.DecompositionModel;

  var div = $('#emperor-notebook-0x9cb72f54');

  var data = {
    // coordinates information
    'sample_ids': ["PC.636", "PC.635", "PC.356", "PC.481", "PC.354", "PC.593", "PC.355", "PC.607", "PC.634"],
    'coordinates': [[1.322178487895014, -0.651995810831719, -0.3417784983371589, 0.15713116241738878, -0.15964022322388774, 0.41511600449567154], [1.322178487895014, -0.5603276951316744, 0.10857735915373172, -0.32567898978232684, 0.3750137797216106, -0.583487828830988], [-0.8236274360749414, 0.5394835270542403, -0.3068324227225251, -0.6770043110217822, 0.203820501907719, 0.1044335488558445], [0.21458556178898447, 0.09964194790906594, -0.03293232371368659, 0.14978636968698092, -0.8160388524355932, -0.301343079001781], [-0.813231746501206, 0.661089243947507, -0.014176279685000464, 0.05537095913733857, -0.11036487613740434, -0.3456924105084198], [0.3158305385071034, 0.5490376828031979, 0.32957520954888647, 0.7612242145083941, 0.4322721667939822, 0.04825249860931067], [-0.813231746501206, 0.40202458647314415, -0.4576554852461752, -0.0728438902229666, 0.04670222577076932, 0.36567512814466946], [0.30475686917855915, -0.21532604614952783, 1.0, -0.31976501999316115, -0.13561208920603846, 0.35686551552017187], [1.322178487895014, -0.8236274360749414, -0.2847775589983077, 0.27177950526966277, 0.16384736680860681, -0.05981937728235736]],
    'axes_names': ["DOB", 0, 1, 2, 3, 4],
    'percents_explained': [-1, 26.6887048633, 16.256370402199998, 13.775412916099999, 11.217215823, 10.024774995000001],

    // sample information
    'metadata_headers': ["SampleID", "Treatment", "DOB", "Description"],
    'metadata': [["PC.636", "Fast", "20080116", "Fasting_mouse_I.D._636"], ["PC.635", "Fast", "20080116", "Fasting_mouse_I.D._635"], ["PC.356", "Control", "20061126", "Control_mouse_I.D._356"], ["PC.481", "Control", "20070314", "Control_mouse_I.D._481"], ["PC.354", "Control", "20061218", "Ctrol_mouse_I.D._354"], ["PC.593", "Control", "20071210", "Control_mouse_I.D._593"], ["PC.355", "Control", "20061218", "Control_mouse_I.D._355"], ["PC.607", "Fast", "20071112", "Fasting_mouse_I.D._607"], ["PC.634", "Fast", "20080116", "Fasting_mouse_I.D._634"]],
    'settings': {}
  }

  var dm, ec;

  function init() {
    // Initialize the DecompositionModel
    dm = new DecompositionModel('', data['sample_ids'],
                                data['coordinates'],
                                data['percents_explained'],
                                data['metadata_headers'], data['metadata'],
                                data['axes_names']);
    // Initialize the EmperorController
    ec = new EmperorController(dm, "emperor-notebook-0x9cb72f54");
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
      ec.loadConfig(data['settings']);
    }
  });

}); // END REQUIRE.JS block
</script>"""


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
