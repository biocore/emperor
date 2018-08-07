requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'scene3d',
    'three',
    'svgrenderer',
    'orbitcontrols'
], function($, _, model, DecompositionView, ScenePlotView3D, THREE,
            SVGRenderer, OrbitControls) {
  var DecompositionModel = model.DecompositionModel;
  $(document).ready(function() {
    module('ScenePlotView3D', {

      setup: function() {
        // global variable shared
        this.sharedDecompositionViewDict = {};

        var div = $('<div id="fooligans"></div>');
        div.appendTo(document.body);

        var data = {name: 'PCOA',
                    sample_ids: ['PC.636', 'PC.635'],
                    coordinates: [[-0.276542, -0.144964, 0.066647, -0.067711,
                                   0.176070, 0.072969, -0.229889, -0.046599],
                                  [-0.237661, 0.046053, -0.138136, 0.159061,
                                   -0.247485, -0.115211, -0.112864, 0.064794]],
                    percents_explained: [26.6887048633, 16.2563704022,
                                         13.7754129161, 11.217215823,
                                         10.024774995, 8.22835130237,
                                         7.55971173665, 6.24945796136]};
        var md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                          'DOB'];
        var metadata = [
          ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
          ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112']
        ];
        var decomp = new DecompositionModel(data, md_headers, metadata);
        var dv = new DecompositionView(decomp);
        this.sharedDecompositionViewDict.scatter = dv;

        data = {name: 'biplot',
                sample_ids: ['tax_1', 'tax_2'],
                coordinates: [[-1, -0.144964, 0.066647, -0.067711, 0.176070,
                               0.072969, -0.229889, -0.046599],
                              [-0.237661, 0.046053, -0.138136, 0.159061,
                               -0.247485, -0.115211, -0.112864, 0.064794]],
                percents_explained: [26.6887048633, 16.2563704022,
                                     13.7754129161, 11.217215823,
                                     10.024774995, 8.22835130237,
                                     7.55971173665, 6.24945796136]};
        md_headers = ['SampleID', 'Gram'];
        metadata = [['tax_1', '1'],
        ['tax_2', '0']];
        decomp = new DecompositionModel(data, md_headers, metadata);
        dv = new DecompositionView(decomp);
        this.sharedDecompositionViewDict.biplot = dv;
      },

      teardown: function() {
        // created as global during the setup function
        this.sharedDecompositionViewDict = undefined;

        // appended to the body during setup
        $('#fooligans').remove();
      }

    });

    /**
     *
     * Test the constructor for ScenePlotView3D
     *
     */
    test('Test the constructor', function(assert) {

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
      assert.ok(spv.camera instanceof THREE.OrthographicCamera);
      assert.ok(spv.light instanceof THREE.DirectionalLight);

      deepEqual(spv.xView, 0);
      deepEqual(spv.yView, 0);

      equal(spv.width, 20);
      equal(spv.height, 20);
      equal(spv.checkUpdate(), true);

      equal(spv.axesColor, '#FFFFFF');
      equal(spv.backgroundColor, '#000000');

      deepEqual(spv.visibleDimensions, [0, 1, 2]);
      deepEqual(spv.dimensionRanges.max, [-0.237661, 0.046053, 0.066647,
                                          0.159061, 0.17607, 0.072969,
                                          -0.112864, 0.064794]);
      deepEqual(spv.dimensionRanges.min, [-1, -0.144964, -0.138136, -0.067711,
                                          -0.247485, -0.115211, -0.229889,
                                          -0.046599]);

      // raycasting properties
      assert.ok(spv._raycaster instanceof THREE.Raycaster);
      assert.ok(spv._mouse instanceof THREE.Vector2);

      // pub/sub
      deepEqual(spv.EVENTS, ['click', 'dblclick']);
      deepEqual(spv._subscribers.click.length, 1);
      deepEqual(spv._subscribers.dblclick.length, 1);

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test checkUpdate', function() {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);
      spv.needsUpdate = false;
      spv.decViews.scatter.needsUpdate = false;
      spv.decViews.biplot.needsUpdate = false;
      equal(spv.checkUpdate(), false);

      spv.needsUpdate = true;
      equal(spv.checkUpdate(), true);
      spv.needsUpdate = false;

      spv.decViews.scatter.needsUpdate = true;
      equal(spv.checkUpdate(), true);

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test checkUpdate background color', function() {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);
      spv.needsUpdate = false;

      spv.decViews.scatter.backgroundColor = 0x00FF00;
      equal(spv.checkUpdate(), true);

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test checkUpdate axes color', function() {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);
      spv.needsUpdate = false;

      spv.decViews.scatter.axesColor = 0x00FF00;
      equal(spv.checkUpdate(), true);

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test checkUpdate visible dimensions', function() {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);
      spv.needsUpdate = false;

      spv.decViews.scatter.visibleDimensions = [1, 2, 3];
      equal(spv.checkUpdate(), true);

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test draw axes', function(assert) {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      // color the axis lines
      spv.drawAxesWithColor(0x00FF0F);

      var line;

      for (var i = 0; i < 3; i++) {
        line = spv.scene.getObjectByName('emperor-axis-line-' + i);
        equal(line.material.color.r, 0);
        equal(line.material.color.g, 1);
        equal(line.material.color.b, 0.058823529411764705);
      }

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test draw axes 2D', function(assert) {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      spv.removeAxes();
      spv.visibleDimensions[2] = null;
      spv.drawAxesWithColor('#0000FF');

      var line;

      for (var i = 0; i < 3; i++) {
        line = spv.scene.getObjectByName('emperor-axis-line-' + i);

        if (i !== 2) {
          equal(line.material.color.r, 0);
          equal(line.material.color.g, 0);
          equal(line.material.color.b, 1);
        }
        else {
          equal(line, undefined);
        }
      }

      // release the control back to the main page
      spv.control.dispose();
    });


    test('Test axes color as null', function(assert) {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      // color the axis lines
      spv.drawAxesWithColor(null);

      var line;

      for (var i = 0; i < 3; i++) {
        line = spv.scene.getObjectByName('emperor-axis-line-' + i);
        equal(line, undefined);
      }

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test removing axes', function(assert) {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      // remove the axis lines
      spv.removeAxes();

      var line;

      for (var i = 0; i < 3; i++) {
        line = spv.scene.getObjectByName('emperor-axis-line-' + i);
        assert.equal(line, undefined);
      }

      // release the control back to the main page
      spv.control.dispose();
    });


    test('Test the draw axes labels', function(assert) {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      // color the axis lines
      spv.drawAxesLabelsWithColor('#00FF0F');

      var label, tolerance = 0.000001,
          positions = [[-0.25429727, -0.15511148, -0.147805522],
                       [-1.07, 0.04927671, -0.14780552000000002],
                       [-1.07, -0.15511148000000002, 0.07131229]];

      for (var i = 0; i < 3; i++) {
        label = spv.scene.getObjectByName('emperor-axis-label-' + i);

        assert.ok((label.position.x - positions[i][0]) < tolerance);
        assert.ok((label.position.y - positions[i][1]) < tolerance);
        assert.ok((label.position.z - positions[i][2]) < tolerance);

        equal(label.material.color.r, 0);
        equal(label.material.color.g, 1);
        equal(label.material.color.b, 0.058823529411764705);

        deepEqual(label.scale.toArray(), [0.390317568, 0.024394848, 1]);
      }

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test the draw axes labels as null', function(assert) {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      // color the axis lines
      spv.drawAxesLabelsWithColor(null);

      for (var i = 0; i < 3; i++) {
        label = spv.scene.getObjectByName('emperor-axis-label-' + i);
        equal(label, undefined);
      }

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test removing axes labels', function(assert) {
      // We will use SVGRenderer here and in the other tests as we cannot use
      // WebGLRenderer and test with phantom.js
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      // remove the axis lines
      spv.removeAxesLabels();

      var label;

      for (var i = 0; i < 3; i++) {
        label = spv.scene.getObjectByName('emperor-axis-label-' + i);
        assert.equal(label, undefined);
      }

      // release the control back to the main page
      spv.control.dispose();
    });

    test('Test getScalingConstant', function(assert) {
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      assert.equal(spv.getScalingConstant(), 0.000762339);

      // release the control back to the main page
      spv.control.dispose();
    });

    /**
     *
     * Test the updateCameraAspectRatio method for ScenePlotView3D
     *
     */
    test('Test updateCameraAspectRatio', function() {

      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      // same width and height
      spv.updateCameraAspectRatio();
      equal(spv.camera.left, -0.0955085);
      equal(spv.camera.right, 0.0955085);
      equal(spv.camera.top, 0.0955085);
      equal(spv.camera.bottom, -0.0955085);
      equal(spv.camera.aspect, 1);

      spv.width = 30;
      spv.updateCameraAspectRatio();
      equal(spv.camera.left, -0.14326275);
      equal(spv.camera.right, 0.14326275);
      equal(spv.camera.top, 0.0955085);
      equal(spv.camera.bottom, -0.0955085);
      equal(spv.camera.aspect, 1.5);

      // release the control back to the main page
      spv.control.dispose();
    });

    /**
     *
     * Test the addDecompositionsToScene method for ScenePlotView3D
     *
     */
    test('Test addDecompositionsToScene', function() {

      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      equal(spv.scene.children.length, 11);
      spv.addDecompositionsToScene();
      equal(spv.scene.children.length, 11);

      // release the control back to the main page
      spv.control.dispose();
    });

    /**
     *
     * Test the addDecompositionsToScene method for ScenePlotView3D
     *
     */
    test('Test addDecompositionsToScene new objects', function() {

      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      equal(spv.scene.children.length, 11);

      var data = {name: 'PCOA',
                  sample_ids: ['PC.636', 'PC.635'],
                  coordinates: [[-0.276542, -0.144964, 0.066647, -0.067711,
                                 0.176070, 0.072969, -0.229889, -0.046599],
                                [-0.237661, 0.046053, -0.138136, 0.159061,
                                 -0.247485, -0.115211, -0.112864, 0.064794]],
                  percents_explained: [26.6887048633, 16.2563704022,
                                       13.7754129161, 11.217215823,
                                       10.024774995, 8.22835130237,
                                       7.55971173665, 6.24945796136]};
      md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment', 'DOB'];
      metadata = [['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
      ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112']];

      decomp = new DecompositionModel(data, md_headers, metadata, 'arrow');
      dv = new DecompositionView(decomp);

      // the label is not scaled upon creation
      deepEqual(dv.markers[0].label.scale.toArray(), [128, 32, 1]);
      deepEqual(dv.markers[1].label.scale.toArray(), [128, 32, 1]);

      this.sharedDecompositionViewDict.pleep = dv;
      spv.addDecompositionsToScene();

      equal(spv.scene.children.length, 13);

      // after the labels are added to the scene, their scales change
      deepEqual(dv.markers[0].label.scale.toArray(),
                [0.097579392, 0.024394848, 1]);
      deepEqual(dv.markers[1].label.scale.toArray(),
                [0.097579392, 0.024394848, 1]);

      // release the control back to the main page
      spv.control.dispose();
    });

    /**
     *
     * Test the resize method for ScenePlotView3D
     *
     */
    test('Test resize', function() {

      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);
      spv.resize(11, 11, 200, 300);

      equal(spv.xView, 11);
      equal(spv.yView, 11);

      equal(spv.width, 200);
      equal(spv.height, 300);

      equal(spv.needsUpdate, true);

      spv.resize(8, 6, 75, 309);

      equal(spv.xView, 8);
      equal(spv.yView, 6);

      equal(spv.width, 75);
      equal(spv.height, 309);

      // release the control back to the main page
      spv.control.dispose();
    });

    /**
     *
     * Test the render method for ScenePlotView3D
     *
     */
    test('Test render', function(assert) {

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

      // release the control back to the main page
      spv.control.dispose();
    });

    /**
     *
     * Test exceptions are correctly raised on unknown events
     *
     */
    test('Test off exceptions', function() {
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      // check this happens for all the properties
      throws(
        function() {
          spv.off('does not exist', function(a, b) { return a;});
        }, Error, 'An error is raised if the event is unknown'
      );

      // release the control back to the main page
      spv.control.dispose();
    });

    /**
     *
     * Test exceptions are correctly raised on unknown events
     *
     */
    test('Test on exceptions', function() {
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      // check this happens for all the properties
      throws(
        function() {
          spv.on('does not exist', function(a, b) { return a;});
        }, Error, 'An error is raised if the event is unknown'
      );

      // release the control back to the main page
      spv.control.dispose();
    });

    /*
     *
     * Testing raycasting-involved methods
     *
     * We need to setup a few mock methods and objects, otherwise we can't
     * quite test the raycasting with the SVGRenderer.
     *
     * 1.- Setup a mock event that will be used to calculate the position of
     * the mouse.
     *
     * 2.- Overwrite the intersectObjects method with a new function that
     * returns a manufactured mock object.
     *
     * 3.- Finally, trigger the callback on 'click' and verify that the
     * received objects are correct.
     *
     */

    /**
     *
     * Test the 'click' callback is resolved
     *
     */
    test('Verifying click works', function() {
      // for the test to pass, two assertions should be made
      expect(2);

      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      spv.on('click', function(a, b) {
        equal(a, 'Meshy McMeshface');
        deepEqual(b, {'name': 'Meshy McMeshface'});
      });

      var mockEvent = {
        'clientX': -0.276542,
        'clientY': -0.144964,
        'offsetLeft': 0,
        'offsetTop': 0,
        'width': 20,
        'height': 20
      };
      mockEvent.preventDefault = function() {};

      var meshy = {'object': {'name': 'Meshy McMeshface'}};
      spv._raycaster.intersectObjects = function() { return [meshy]; };
      spv._eventCallback('click', mockEvent);

      // release the control back to the main page
      spv.control.dispose();
    });

    /**
     *
     * Test the 'dblclick' callback is resolved
     *
     */
    test('Verifying double click works', function() {
      // for the test to pass, two assertions should be made
      expect(2);

      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      spv.on('dblclick', function(a, b) {
        equal(a, 'Meshy McMeshface');
        deepEqual(b, {'name': 'Meshy McMeshface'});
      });

      var mockEvent = {
        'clientX': -0.276542,
        'clientY': -0.144964,
        'offsetLeft': 0,
        'offsetTop': 0,
        'width': 20,
        'height': 20
      };
      mockEvent.preventDefault = function() {};

      var meshy = {'object': {'name': 'Meshy McMeshface'}};
      spv._raycaster.intersectObjects = function() { return [meshy]; };
      spv._eventCallback('dblclick', mockEvent);

      // release the control back to the main page
      spv.control.dispose();
    });

    /*
     *
     * Check we can add/remove subscribers
     *
     */
    test('Check removal and addition of subscribers', function() {
      var renderer = new THREE.SVGRenderer({antialias: true});
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      var a = function() {
        return 42;
      };

      var b = function() {
        return 'forty two';
      };

      spv.on('click', a);
      spv.on('click', b);
      equal(spv._subscribers.click.length, 3);
      spv.off('click', a);
      equal(spv._subscribers.click.length, 2);
      spv.off('click', b);
      equal(spv._subscribers.click.length, 1);

      // release the control back to the main page
      spv.control.dispose();
    });

    /**
     *
     * Test the recenterCamera method for ScenePlotView3D
     *
     */
    test('Test recenterCamera', function(assert) {

      var renderer = new THREE.SVGRenderer({antialias: true}), max;
      var spv = new ScenePlotView3D(renderer, this.sharedDecompositionViewDict,
                                    'fooligans', 0, 0, 20, 20);

      spv.camera.rotation.set(1, 1, 1);
      spv.camera.updateProjectionMatrix();
      spv.camera.position.set(-1, 11, 0);
      spv.camera.updateProjectionMatrix();
      spv.needsUpdate = true;

      max = _.max(spv.dimensionRanges.max);

      spv.recenterCamera();

      // for some odd reason orbit controls makes the rotation close to zero
      // but not actually zero and there's no "close to zero" method in Qunit
      function closeToZero(x) {
        x = Math.abs(x);
        return x >= 0 && x < 0.0000001;
      }
      assert.ok(closeToZero(spv.camera.rotation.x));
      assert.ok(closeToZero(spv.camera.rotation.y));
      assert.ok(closeToZero(spv.camera.rotation.z));

      assert.ok(closeToZero(spv.camera.position.x));
      assert.ok(closeToZero(spv.camera.position.y));
      equal(spv.camera.position.z, max * 5);

      spv.control.dispose();
    });
  });
});
