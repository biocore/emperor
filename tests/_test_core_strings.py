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

HTML_STRING = """<script type="text/javascript">

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
<div id='emperor-notebook-0x9cb72f54' style="position: relative; width:100%; height:500px;"><div class='loading' style="position: absolute;top: 50%;left: 50%;margin-left: -229px; margin-top: -59px; z-index: 10000;height:118px;width:458px;padding:0px"><img src='https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/img/emperor.png' alt='Emperor logo'></div></div>
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


  /* THREE.js and plugins */
  'three': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/three.min',
  'orbitcontrols': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/three.js-plugins/OrbitControls',

  /* SlickGrid */
  'slickcore': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/slick.core.min',
  'slickgrid': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/slick.grid.min',
  'slickformatters': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/slick.editors.min',
  'slickeditors': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/vendor/js/slick.formatters.min',

  /* Emperor's objects */
  'model': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/model',
  'view': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/view',
  'controller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/controller',
  'draw': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/draw',
  'scene3d': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/sceneplotview3d',
  'viewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/view-controller',
  'colorviewcontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/color-view-controller',
  'visibilitycontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/visibility-controller',
  'shapecontroller': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shape-controller',
  'shape-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/shape-editor',
  'color-editor': 'https://cdn.rawgit.com/biocore/emperor/new-api/emperor/support_files/js/color-editor',
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
  'orbitcontrols': {
    'deps': ['three']
  },
'slickcore': ['jqueryui'],
'slickgrid': ['slickcore', 'jquery_drag', 'slickformatters',
              'slickeditors']
}
});

requirejs(
["jquery", "model", "controller"],
function($, model, EmperorController) {
  var DecompositionModel = model.DecompositionModel;

  var div = $('#emperor-notebook-0x9cb72f54');

  var ids = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354', 'PC.593', 'PC.355', 'PC.607', 'PC.634'];
  var coords = [[-0.276542163845, -0.144964375408, 0.0666467344429, -0.0677109454288, 0.176070269506], [-0.237661393984, 0.0460527772512, -0.138135814766, 0.159061025229, -0.247484698646], [0.228820399536, -0.130142097093, -0.287149447883, 0.0864498846421, 0.0442951919304], [0.0422628480532, -0.0139681511889, 0.0635314615517, -0.346120552134, -0.127813807608], [0.280399117569, -0.0060128286014, 0.0234854344148, -0.0468109474823, -0.146624450094], [0.232872767451, 0.139788385269, 0.322871079774, 0.18334700682, 0.0204661596818], [0.170517581885, -0.194113268955, -0.0308965283066, 0.0198086158783, 0.155100062794], [-0.0913299284215, 0.424147148265, -0.135627421345, -0.057519480907, 0.151363490722], [-0.349339228244, -0.120787589539, 0.115274502117, 0.0694953933826, -0.0253722182853]];
  var pct_var = [0.266887048633, 0.162563704022, 0.137754129161, 0.11217215823, 0.10024774995];
  var md_headers = ['SampleID', 'Treatment', 'DOB', 'Description'];
  var metadata = [['PC.636', 'Fast', '20080116', 'Fasting_mouse_I.D._636'], ['PC.635', 'Fast', '20080116', 'Fasting_mouse_I.D._635'], ['PC.356', 'Control', '20061126', 'Control_mouse_I.D._356'], ['PC.481', 'Control', '20070314', 'Control_mouse_I.D._481'], ['PC.354', 'Control', '20061218', 'Ctrol_mouse_I.D._354'], ['PC.593', 'Control', '20071210', 'Control_mouse_I.D._593'], ['PC.355', 'Control', '20061218', 'Control_mouse_I.D._355'], ['PC.607', 'Fast', '20071112', 'Fasting_mouse_I.D._607'], ['PC.634', 'Fast', '20080116', 'Fasting_mouse_I.D._634']];

  var dm, ec;

  function init() {
    // Initialize the DecompositionModel
    dm = new DecompositionModel(name, ids, coords, pct_var,
                                md_headers, metadata);
    // Initialize the EmperorController
    ec = new EmperorController(dm, 'emperor-notebook-0x9cb72f54');
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

  });

}); // END REQUIRE.JS block
</script>"""
