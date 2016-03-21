TEMPLATE_HTML = """
<script type="text/javascript">
{% raw %}
requirejs('jquery', function($){
if ($("#emperor-css").length == 0){{
    $("head").append([
{% endraw %}
        '<link id="emperor-css" rel="stylesheet" type="text/css" href="{{ base_URL }}/emperor/support_files/css/emperor.css">',
        '<link rel="stylesheet" type="text/css" href="{{ base_URL }}/emperor/support_files/vendor/css/jquery-ui.min.css">',
        '<link rel="stylesheet" type="text/css" href="{{ base_URL }}/emperor/support_files/vendor/css/slick.grid.min.css">',
        '<link rel="stylesheet" type="text/css" href="{{ base_URL }}/emperor/support_files/vendor/css/spectrum.min.css">',
        '<link rel="stylesheet" type="text/css" href="{{ base_URL }}/emperor/support_files/vendor/css/chosen.min.css">'
    ]);
}}
});
</script>
<div id='python-penguin' style="position: relative; width:100%; height:500px;"></div>
</div>
"""

TEMPLATE_JS = """
<script type="text/javascript">
requirejs.config({
'baseUrl': '{{ base_URL }}/emperor/support_files/',

// the left side is the module name, and the right side is the path
// relative to the baseUrl attribute, do NOT include the .js extension
'paths': {
  /* jQuery */
  'jquery': './vendor/js/jquery-2.1.4.min',
  'jqueryui': './vendor/js/jquery-ui.min',
  'jquery_drag': './vendor/js/jquery.event.drag-2.2.min',

  /* jQuery plugins */
  'chosen': './vendor/js/chosen.jquery.min',
  'spectrum': './vendor/js/spectrum.min',

  /* other libraries */
  'underscore': './vendor/js/underscore-min',
  'chroma': './vendor/js/chroma.min',


  /* THREE.js and plugins */
  'three': './vendor/js/three.min',
  'orbitcontrols': './vendor/js/three.js-plugins/OrbitControls',

  /* SlickGrid */
  'slickcore': './vendor/js/slick.core.min',
  'slickgrid': './vendor/js/slick.grid.min',
  'slickformatters': './vendor/js/slick.editors.min',
  'slickeditors': './vendor/js/slick.formatters.min',

  /* Emperor's objects */
  'model': './js/model',
  'view': './js/view',
  'controller': './js/controller',
  'scene3d': './js/sceneplotview3d',
  'viewcontroller': './js/view-controller',
  'colorviewcontroller': './js/color-view-controller',
  'visibilitycontroller': './js/visibility-controller',
  'color-editor': './js/color-editor',
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

  var div = $('#python-penguin');
  console.log(div)

  var ids = {{ coords_ids }};
  var coords = {{ coords }};
  var pct_var = {{ pct_var }};
  var md_headers = {{ md_headers}};
  var metadata = {{  metadata }};

  var dm, ec;

  function init() {
    // Initialize the DecompositionModel
    dm = new DecompositionModel(name, ids, coords, pct_var,
                                md_headers, metadata);
    // Initialize the EmperorController
    ec = new EmperorController(dm, 'python-penguin');
    lol = ec
  }

  function animate() {
    requestAnimationFrame(animate);
    ec.render();
  }
  $(window).resize(function() {
    ec.resize(window.innerWidth, window.innerHeight);
  });

  $(function(){
    init();
    animate();

  });

}); // END REQUIRE.JS block
</script>
"""

TEMPLATE_STRING="""<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Emperor test</title>
    <meta charset="utf-8">

    <link rel="stylesheet" type="text/css" href="../emperor/support_files/css/emperor.css">
    <link rel="stylesheet" type="text/css" href="../emperor/support_files/vendor/css/jquery-ui.min.css">
    <link rel="stylesheet" type="text/css" href="../emperor/support_files/vendor/css/slick.grid.min.css">
    <link rel="stylesheet" type="text/css" href="../emperor/support_files/vendor/css/spectrum.min.css">
    <link rel="stylesheet" type="text/css" href="../emperor/support_files/vendor/css/chosen.min.css">

    <style>
      div.emperor-space{
        position: fixed;
        height: 100%;
        width: 100%;
        height: 100vh;
        width: 100vw;
        margin: 0;
      }
    </style>

    <script type="text/javascript" src="../emperor/support_files/vendor/js/require-2.1.22.min.js"></script>

  </head>
  <body>
    <script type="text/javascript">
      requirejs.config({
        'baseUrl': '../emperor/support_files/',

        // the left side is the module name, and the right side is the path
        // relative to the baseUrl attribute, do NOT include the .js extension
        'paths': {
          /* jQuery */
          'jquery': './vendor/js/jquery-2.1.4.min',
          'jqueryui': './vendor/js/jquery-ui.min',
          'jquery_drag': './vendor/js/jquery.event.drag-2.2.min',

          /* jQuery plugins */
          'chosen': './vendor/js/chosen.jquery.min',
          'spectrum': './vendor/js/spectrum.min',

          /* other libraries */
          'underscore': './vendor/js/underscore-min',
          'chroma': './vendor/js/chroma.min',

          /* THREE.js and plugins */
          'three': './vendor/js/three.min',
          'orbitcontrols': './vendor/js/three.js-plugins/OrbitControls',

          /* SlickGrid */
          'slickcore': './vendor/js/slick.core.min',
          'slickgrid': './vendor/js/slick.grid.min',
          'slickformatters': './vendor/js/slick.editors.min',
          'slickeditors': './vendor/js/slick.formatters.min',

          /* Emperor's objects */
          'model': './js/model',
          'view': './js/view',
          'controller': './js/controller',
          'draw': './js/draw',
          'scene3d': './js/sceneplotview3d',
          'viewcontroller': './js/view-controller',
          'colorviewcontroller': './js/color-view-controller',
          'visibilitycontroller': './js/visibility-controller',
          'color-editor': './js/color-editor',
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

          $("<div id='plots' class='emperor-space'></div>").appendTo(document.body);
          var div = $('#plots');

          var ids = {{ coords_ids }};
          var coords = {{ coords }};
          var pct_var = {{ pct_var }};
          var md_headers = {{ md_headers}};
          var metadata = {{  metadata }};

          var dm, ec;

          function init() {
            // Initialize the DecompositionModel
            dm = new DecompositionModel(name, ids, coords, pct_var,
                                        md_headers, metadata);
            // Initialize the EmperorController
            ec = new EmperorController(dm, 'plots');
          }

          $(window).resize(function() {
            ec.resize(window.innerWidth, window.innerHeight);
          });

          function animate() {
            requestAnimationFrame(animate);
            ec.render();
          }

          $(function () {
            init();
            animate();
          });

          $(document).ready(function(){
             ec.resize(window.innerWidth, window.innerHeight);
          });

      }); // END REQUIRE.JS block
    </script>
  </body>
</html>
"""
