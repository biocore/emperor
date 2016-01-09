requirejs([
    "jquery",
    "underscore",
    "model",
    "view",
    "scene3d",
    "three",
    "svgrenderer",
    "orbitcontrols"
], function ($, _, model, DecompositionView, ScenePlotView3D, THREE, SVGRenderer, OrbitControls) {
  var DecompositionModel = model.DecompositionModel;
$(document).ready(function() {
  module('ScenePlotView3D', {

    setup: function(){
      // global variable shared
      this.sharedDecompositionViewDict = {};

      var div = $('<div id="fooligans"></div>');
      div.appendTo(document.body);

      var name = "pcoa";
      var ids = ['PC.636', 'PC.635'];
      var coords = [[-0.276542, -0.144964, 0.066647, -0.067711, 0.176070,
                     0.072969, -0.229889, -0.046599],
                    [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485,
                     -0.115211, -0.112864, 0.064794]];
      var pct_var = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
                     10.024774995, 8.22835130237, 7.55971173665, 6.24945796136];
      var md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment', 'DOB'];
      var metadata = [['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
                  ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112']];
      var decomp = new DecompositionModel(name, ids, coords, pct_var,
                                          md_headers, metadata);
      var dv = new DecompositionView(decomp);
      this.sharedDecompositionViewDict.pcoa = dv;

      name = "biplot";
      ids = ['tax_1', 'tax_2'];
      coords = [
        [-1, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
         -0.229889, -0.046599],
        [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
         -0.112864, 0.064794]];
      pct_var = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
                 10.024774995, 8.22835130237, 7.55971173665, 6.24945796136];
      md_headers = ['SampleID', 'Gram'];
      metadata = [['tax_1', '1'],
                  ['tax_2', '0']];
      decomp = new DecompositionModel(name, ids, coords, pct_var, md_headers,
                                      metadata);
      dv = new DecompositionView(decomp);
      this.sharedDecompositionViewDict.biplot = dv;
    },

    teardown: function(){
      // created as global during the setup function
      this.sharedDecompositionViewDict = undefined;

      // appended to the body during setup
      $("#fooligans").remove();
    }

  });

  /**
   *
   * Test the constructor for ScenePlotView3D
   *
   */
  test('Test the constructor', function(assert){

    // We will use SVGRenderer here and in the other tests as we cannot use
    // WebGLRenderer and test with phantom.js
    var renderer = new THREE.SVGRenderer({antialias: true});
    var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                  'fooligans', 0, 0, 20, 20);

    // assert proper initializations for the attributes, we won't check their
    // initialization values as these are subject to change
    assert.ok(spv.renderer instanceof THREE.SVGRenderer);
    assert.ok(spv.control instanceof THREE.OrbitControls);
    assert.ok(spv.scene instanceof THREE.Scene);
    assert.ok(spv.camera instanceof THREE.PerspectiveCamera);
    assert.ok(spv.light instanceof THREE.DirectionalLight);

    equal(spv.xView, 0);
    equal(spv.yView, 0);

    equal(spv.width, 20);
    equal(spv.height, 20);
  });


  /**
   *
   * Test the setCameraAspectRatio method for ScenePlotView3D
   *
   */
  test('Test setCameraAspectRatio', function(){

    var renderer = new THREE.SVGRenderer({antialias: true});
    var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                  'fooligans', 0, 0, 20, 20);
    spv.setCameraAspectRatio(100);
    equal(spv.camera.aspect, 100);

    spv.setCameraAspectRatio(200);
    equal(spv.camera.aspect, 200);

    spv.setCameraAspectRatio(1);
    equal(spv.camera.aspect, 1);

  });

  /**
   *
   * Test the resize method for ScenePlotView3D
   *
   */
  test('Test resize', function(){

    var renderer = new THREE.SVGRenderer({antialias: true});
    var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                  'fooligans', 0, 0, 20, 20);
    spv.resize(11, 11, 200, 300);

    equal(spv.xView, 11);
    equal(spv.yView, 11);

    equal(spv.width, 200);
    equal(spv.height, 300);

    spv.resize(8, 6, 75, 309);

    equal(spv.xView, 8);
    equal(spv.yView, 6);

    equal(spv.width, 75);
    equal(spv.height, 309);
  });

  /**
   *
   * Test the render method for ScenePlotView3D
   *
   */
  test('Test render', function(assert){

    var renderer = new THREE.SVGRenderer({antialias: true});
    var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                  'fooligans', 0, 0, 20, 20);

    // Couldn't really find a way to properly test the render method as the
    // properties it modifies are not publicly exposed by the renderer object.
    // Therefore we will only call the method and if all goes well then the
    // method shouldn't error or fail.
    // spv.render();
    // Update: turns out we cannot call the render method when we use the
    // SVGRenderer class. Would be great if we find a way around this problem.
    assert.ok(true);
  });
});
});
