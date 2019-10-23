requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'multi-model',
    'uistate',
    'three'
], function($, _, model, DecompositionView, MultiModel, UIState, THREE,) {
  $(document).ready(function() {
    var DecompositionModel = model.DecompositionModel;

    module('Decomposition View', {
      setup: function() {
        // setup function
        var data = {
          name: 'pcoa',
          sample_ids: ['PC.636', 'PC.635'],
          coordinates: [
          [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
          -0.229889, -0.046599],
          [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
          -0.112864, 0.064794]],
          percents_explained: [26.6887048633, 16.2563704022, 13.7754129161,
                               11.217215823, 10.024774995, 8.22835130237,
                               7.55971173665, 6.24945796136]};
        var md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                          'DOB'];
        var metadata = [['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control',
                         '20070314'],
                        ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast',
                         '20071112']];

        this.decomp = new DecompositionModel(data, md_headers, metadata);

        data.edges = [['PC.636', 'PC.635']];
        this.decompWithEdges = new DecompositionModel(data, md_headers,
                                                      metadata);

        /* `this.expected`: this is the same as the object declared above,
         * except this object is not being passed anywhere and is only used to
         * check that nothing has changed between methods.
         */
        data = {name: 'pcoa',
                    sample_ids: ['PC.636', 'PC.635'],
                    coordinates: [
          [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
          -0.229889, -0.046599],
          [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
          -0.112864, 0.064794]],
                    percents_explained: [26.6887048633, 16.2563704022,
                                         13.7754129161, 11.217215823,
                                         10.024774995, 8.22835130237,
                                         7.55971173665, 6.24945796136]};
        md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                           'DOB'];
        metadata = [
          ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
          ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112']];
        this.expected = new DecompositionModel(data, md_headers, metadata);

        data.edges = [['PC.636', 'PC.635']];
        this.expectedWithEdges = new DecompositionModel(data, md_headers,
                                                        metadata);

        this.multiModel = new MultiModel({'scatter': this.decomp});
        this.multiModelWithEdges = new MultiModel(
                                      {'scatter': this.decompWithEdges});



      },

      teardown: function() {
        // teardown function
        this.decomp = null;
        this.expected = null;
      }
    });

    /**
     *
     * Test that the Decomposition View object is initialized correctly
     *
     */
    test('Test constructor', function() {
      var obs;

      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);

      deepEqual(dv.decomp, this.expected, 'decomp set correctly');
      equal(dv.count, 2, 'count set correctly');
      equal(dv.getVisibleCount(), 2, 'visibleCount set correctly');
      deepEqual(dv.visibleDimensions, [0, 1, 2],
          'visibleDimensions set correctly');
      deepEqual(dv.staticTubes, [], 'tubes set correctly');
      deepEqual(dv.dynamicTubes, [], 'tubes set correctly');

      equal(dv.axesColor, '#FFFFFF');
      equal(dv.backgroundColor, '#000000');

      deepEqual(dv.axesOrientation, [1, 1, 1]);

      /*
         I'm unsure on how to test this, so right now just testing what I think
         makes sense to test
       */
      obs = [dv.markers[0].position.x,
      dv.markers[0].position.y,
      dv.markers[0].position.z];
      exp = [-0.276542, -0.144964, 0.066647];
      deepEqual(obs, exp, 'First marker position set correctly');
      obs = [dv.markers[1].position.x,
      dv.markers[1].position.y,
      dv.markers[1].position.z];
      exp = [-0.237661, 0.046053, -0.138136];
      deepEqual(obs, exp, 'Second marker position set correctly');
      deepEqual(dv.lines, {'left': null, 'right': null});
      /*
         TODO: How do we test this?
         */
      // deepEqual(dv._genericSphere, undefined,
      //           "_genericSphere set correctly");
    });

    /**
     *
     * Test that the Decomposition View object is initialized correctly
     *
     */
    test('Test constructor with two dimensions', function() {

      var data = {
        name: 'pcoa',
        sample_ids: ['PC.636', 'PC.635'],
        coordinates: [[-0.276542, -0.144964], [-0.237661, 0.046053]],
        percents_explained: [80.0, 20.0]};
      var md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                        'DOB'];
      var metadata = [['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control',
                       '20070314'],
                      ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast',
                       '20071112']];
      decomp = new DecompositionModel(data, md_headers, metadata);
      var mm = new MultiModel({'scatter': decomp});
      var obs;

      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(mm, 'scatter', UIState1);

      equal(dv.count, 2, 'count set correctly');
      equal(dv.getVisibleCount(), 2, 'visibleCount set correctly');
      deepEqual(dv.visibleDimensions, [0, 1],
          'visibleDimensions set correctly');
      deepEqual(dv.staticTubes, [], 'tubes set correctly');
      deepEqual(dv.dynamicTubes, [], 'tubes set correctly');

      equal(dv.axesColor, '#FFFFFF');
      equal(dv.backgroundColor, '#000000');

      deepEqual(dv.axesOrientation, [1, 1]);

      deepEqual(dv.markers[0].position.toArray(), [-0.276542, -0.144964, 0]);
      deepEqual(dv.markers[1].position.toArray(), [-0.237661, 0.046053, 0]);
      deepEqual(dv.lines, {'left': null, 'right': null});
    });

    test('Test constructor (biplot)', function(assert) {
      // this test is pretty much the same as above except for arrow types
      this.decomp.type = 'arrow';

      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var view = new DecompositionView(this.multiModel, 'scatter', UIState1);

      this.expected.type = 'arrow';
      deepEqual(view.decomp, this.expected);
      equal(view.count, 2);
      equal(view.getVisibleCount(), 2);
      deepEqual(view.visibleDimensions, [0, 1, 2]);
      deepEqual(view.staticTubes, [], 'tubes set correctly');
      deepEqual(view.dynamicTubes, [], 'tubes set correctly');
      equal(view.axesColor, '#FFFFFF');
      equal(view.backgroundColor, '#000000');
      deepEqual(view.axesOrientation, [1, 1, 1]);

      // testing the markers
      assert.ok(view.markers.length === 2);

      equal(view.markers[0].line.name, 'PC.636');
      equal(view.markers[0].cone.name, 'PC.636');
      equal(view.markers[1].line.name, 'PC.635');
      equal(view.markers[1].cone.name, 'PC.635');

      var a = [0.19977209326971626, 0, 0.8289251461730293, 0.52246934148585];
      var b = [-0.3246511569372691, 0, 0.5585576432564162, 0.7632922018854449];

      deepEqual(view.markers[0].quaternion.toArray(), a);
      deepEqual(view.markers[1].quaternion.toArray(), b);

      deepEqual(view.markers[0].position.toArray(), [0, 0, 0]);
      deepEqual(view.markers[1].position.toArray(), [0, 0, 0]);

      // bulk checks
      view.markers.map(function(marker) {
        assert.ok(marker instanceof THREE.ArrowHelper);

        deepEqual(marker.line.material.color.getHex(), 0xc0c0c0);
        deepEqual(marker.cone.material.color.getHex(), 0xc0c0c0);
      });
    });

    test('Test constructor (with edges)', function(assert) {
      // this test is pretty much the same as above except checking for edges
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var view = new DecompositionView(this.multiModelWithEdges,
                                       'scatter',
                                       UIState1);

      deepEqual(view.decomp, this.expectedWithEdges);
      equal(view.count, 2);
      equal(view.getVisibleCount(), 2);
      deepEqual(view.visibleDimensions, [0, 1, 2]);
      deepEqual(view.staticTubes, [], 'tubes set correctly');
      deepEqual(view.dynamicTubes, [], 'tubes set correctly');
      equal(view.axesColor, '#FFFFFF');
      equal(view.backgroundColor, '#000000');
      deepEqual(view.axesOrientation, [1, 1, 1]);

      // testing the markers
      assert.ok(view.markers.length === 2);

      // check for the edges
      assert.ok(view.lines.left instanceof THREE.LineSegments);
      assert.ok(view.lines.right instanceof THREE.LineSegments);

      equal(view.lines.left.material.color.getHex(), 0xffffff);
      equal(view.lines.right.material.color.getHex(), 0xff0000);

      deepEqual(view.lines.left.geometry.attributes.position.array.length, 6);
      deepEqual(view.lines.right.geometry.attributes.position.array.length, 6);
    });

    test('Test constructor fails (biplot in fast mode)', function() {
      this.decomp.type = 'arrow';
      throws(function() {
        var UIState1 = new UIState();
        UIState.setProperty('view.usesPointCloud', true);
        var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
      }, Error, 'Biplots are not supported in fast mode');
    });

    test('Test constructor fails (jackknifed in fast mode)', function() {
      // setup function
      var data = {
        name: 'pcoa',
        sample_ids: ['PC.636', 'PC.635'],
        coordinates: [[-0.276542, -0.144964, 0.066647, -0.067711, 0.176070,
                       0.072969, -0.229889, -0.046599],
                      [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485,
                       -0.115211, -0.112864, 0.064794]],
        percents_explained: [26.6887048633, 16.2563704022, 13.7754129161,
                             11.217215823, 10.024774995, 8.22835130237,
                             7.55971173665, 6.24945796136],
        ci: [[0.3, 0.1, 0.06, 0.06, 0.1, 0.07, 0.2, 0.04],
             [0.3, 0.1, 0.06, 0.06, 0.1, 0.07, 0.2, 0.04]]};
      var md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                        'DOB'];
      var metadata = [['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control',
                       '20070314'],
                      ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast',
                       '20071112']];
      this.decomp = new DecompositionModel(data, md_headers, metadata);
      var multiModel = new MultiModel({'scatter': this.decomp});
      throws(function() {
        var UIState1 = new UIState();
        UIState1.setProperty('view.usesPointCloud', true);
        var dv = new DecompositionView(multiModel, 'scatter', UIState1);
      }, Error, 'Jaccknifed plots are not supported in fast mode');
    });

    test('Test getGeometryFactor', function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);

      equal(dv.getGeometryFactor(), 0.000466572);
    });

    /**
     *
     * Test that getVisibleCount is correctly updated
     *
     */
    test('Test getVisibleCount', function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
      dv.markers[0].visible = false;
      equal(dv.getVisibleCount(), 1);
      dv.markers[1].visible = false;
      equal(dv.getVisibleCount(), 0);
      dv.markers[0].visible = true;
      dv.markers[1].visible = true;
      equal(dv.getVisibleCount(), 2);
    });

    /**
     *
     * Test that changeVisibleDimensions updates the meshes position
     *
     */
    test('Test changeVisibleDimensions', function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
      dv.changeVisibleDimensions([2, 3, 4]);
      obs = [dv.markers[0].position.x,
      dv.markers[0].position.y,
      dv.markers[0].position.z];
      exp = [0.066647, -0.067711, 0.176070];
      deepEqual(obs, exp, 'First marker position updated correctly');
      obs = [dv.markers[1].position.x,
      dv.markers[1].position.y,
      dv.markers[1].position.z];
      exp = [-0.138136, 0.159061, -0.247485];
      deepEqual(obs, exp, 'Second marker position updated correctly');

      deepEqual(dv.axesOrientation, [1, 1, 1]);
    });

    /**
     *
     * Test that changeVisibleDimensions with edges
     *
     */
    test('Test changeVisibleDimensions with edges', function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModelWithEdges,
                                     'scatter',
                                     UIState1);
      dv.changeVisibleDimensions([2, 3, 4]);

      obs = [dv.markers[0].position.x, dv.markers[0].position.y,
             dv.markers[0].position.z];
      var exp = [0.066647, -0.067711, 0.176070];
      deepEqual(obs, exp);

      obs = [dv.markers[1].position.x,
      dv.markers[1].position.y,
      dv.markers[1].position.z];
      exp = [-0.138136, 0.159061, -0.247485];
      deepEqual(obs, exp);

      exp = [0.0666470006108284, -0.0677110031247139, 0.17607000470161438,
             -0.035744499415159225, 0.04567499831318855, -0.0357074998319149];
      exp = new Float32Array(exp);
      deepEqual(dv.lines.left.geometry.attributes.position.array, exp);

      exp = [-0.13813599944114685, 0.159060999751091, -0.2474849969148636,
             -0.035744499415159225, 0.04567499831318855, -0.0357074998319149];
      exp = new Float32Array(exp);
      deepEqual(dv.lines.right.geometry.attributes.position.array, exp);

      deepEqual(dv.axesOrientation, [1, 1, 1]);
    });

    test('Test changeVisibleDimensions (2D)', function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
      dv.changeVisibleDimensions([2, 3, null]);
      obs = [dv.markers[0].position.x,
      dv.markers[0].position.y,
      dv.markers[0].position.z];
      exp = [0.066647, -0.067711, 0];
      deepEqual(obs, exp);
      obs = [dv.markers[1].position.x,
      dv.markers[1].position.y,
      dv.markers[1].position.z];
      exp = [-0.138136, 0.159061, 0];
      deepEqual(obs, exp);

      deepEqual(dv.axesOrientation, [1, 1, 1]);
    });

    /**
     *
     * Test the changeVisibleDimensions throws an error if the number of
     * dimensions passes is different the 3
     *
     */
    test('Test changeVisibleDimensions excepts', function() {
      throws(
          function() {
            var UIState1 = new UIState();
            UIState1.setProperty('view.usesPointCloud', false);
            var dv = new DecompositionView(this.multiModel,
                                           'scatter',
                                           UIState1);
            dv.changeVisibleDimensions([2, 3, 4, 5]);
          },
          Error,
          'An error is raised if the number of dimensions is not 3'
          );
    });

    /**
     *
     * Test that changeVisibleDimensions updates the meshes position
     *
     */
    test('Test change flip axes', function(assert) {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);

      // copy the arrays
      expa = _.clone(dv.markers[0].position.toArray());
      expb = _.clone(dv.markers[1].position.toArray());

      // flip the orientation of the position
      expb[1] = expb[1] * -1;
      expa[1] = expa[1] * -1;

      // change the position of the decomposition view and ...
      dv.flipVisibleDimension(1);

      // ... Check for the following things:
      //
      // 1.- The position themselves
      // 2.- The ranges i.e. positions still fall within the dimensionRanges.
      // 3.- The axis orientation vector
      obs = dv.markers[0].position.toArray();
      deepEqual(obs, expa, 'First marker position updated correctly');

      assert.ok(obs[1] <= dv.decomp.dimensionRanges.max[1],
                'Falls within range (max)');
      assert.ok(obs[1] >= dv.decomp.dimensionRanges.min[1],
                'Falls within range (min)');

      obs = dv.markers[1].position.toArray();
      deepEqual(obs, expb, 'Second marker position updated correctly');

      assert.ok(obs[1] <= dv.decomp.dimensionRanges.max[1],
                'Falls within range (max)');
      assert.ok(obs[1] >= dv.decomp.dimensionRanges.min[1],
                'Falls within range (min)');

      deepEqual(dv.axesOrientation, [1, -1, 1]);
    });

    test('Test change flip axes (2D)', function(assert) {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);

      var expa = [-0.276542, 0.144964, 0], expb = [-0.237661, -0.046053, 0];

      dv.changeVisibleDimensions([0, 1, null]);

      // change the position of the decomposition view and ...
      dv.flipVisibleDimension(1);

      // ... Check for the following things:
      //
      // 1.- The position themselves
      // 2.- The ranges i.e. positions still fall within the dimensionRanges.
      // 3.- The axis orientation vector
      obs = dv.markers[0].position.toArray();
      deepEqual(obs, expa, 'First marker position updated correctly');
      obs = dv.markers[1].position.toArray();
      deepEqual(obs, expb, 'Second marker position updated correctly');

      deepEqual(dv.axesOrientation, [1, -1, 1]);
    });

    test('Test toggling label visibility errors', function(assert) {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);

      throws(
        function() {
          dv.toggleLabelVisibility();
        },
        Error, 'Scatter types cannot toggle label visibility'
      );
    });

    test('Test toggling label visibility', function(assert) {
      this.decomp.type = 'arrow';
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
      assert.equal(dv.markers[0].label.visible, true);
      assert.equal(dv.markers[1].label.visible, true);

      dv.toggleLabelVisibility();

      assert.equal(dv.markers[0].label.visible, false);
      assert.equal(dv.markers[1].label.visible, false);

      dv.toggleLabelVisibility();

      assert.equal(dv.markers[0].label.visible, true);
      assert.equal(dv.markers[1].label.visible, true);
    });

    /**
     *
     * Test that changeVisibleDimensions and flip axis
     *
     */
    test('Test changing the orientations and then flipping a dimension',
         function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);

      deepEqual(dv.axesOrientation, [1, 1, 1]);

      dv.changeVisibleDimensions([2, 3, 4]);
      obs = dv.markers[0].position.toArray();
      exp = [0.066647, -0.067711, 0.176070];
      deepEqual(obs, exp, 'First marker position updated correctly');

      obs = dv.markers[1].position.toArray();
      exp = [-0.138136, 0.159061, -0.247485];
      deepEqual(obs, exp, 'Second marker position updated correctly');

      deepEqual(dv.axesOrientation, [1, 1, 1]);

      dv.flipVisibleDimension(3);

      obs = dv.markers[0].position.toArray();
      exp = [0.066647, 0.067711, 0.176070];
      deepEqual(obs, exp, 'First marker position updated correctly');

      obs = dv.markers[1].position.toArray();
      exp = [-0.138136, -0.159061, -0.247485];
      deepEqual(obs, exp, 'Second marker position updated correctly');

      deepEqual(dv.axesOrientation, [1, -1, 1]);
    });

    test('Test showEdgesForPlottables', function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModelWithEdges,
                                     'scatter',
                                     UIState1);

      dv.hideEdgesForPlottables();

      dv.showEdgesForPlottables();

      exp = [-0.2765420079231262, -0.14496399462223053, 0.0666470006108284,
             -0.25710150599479675, -0.04945550113916397,
             -0.035744499415159225];
      exp = new Float32Array(exp);
      deepEqual(dv.lines.left.geometry.attributes.position.array, exp);

      exp = [-0.23766100406646729, 0.046052999794483185, -0.13813599944114685,
             -0.25710150599479675, -0.04945550113916397,
             -0.035744499415159225];

      exp = new Float32Array(exp);
      deepEqual(dv.lines.right.geometry.attributes.position.array, exp);

      // shouldn't error and work fine
      dv.showEdgesForPlottables('Not a plottable');

    });

    test('Test hideEdgesForPlottables', function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModelWithEdges,
                                     'scatter',
                                     UIState1);

      dv.hideEdgesForPlottables();

      exp = [0, 0, 0, 0, 0, 0];
      exp = new Float32Array(exp);
      deepEqual(dv.lines.left.geometry.attributes.position.array, exp);

      exp = [0, 0, 0, 0, 0, 0];
      exp = new Float32Array(exp);
      deepEqual(dv.lines.right.geometry.attributes.position.array, exp);

      dv.hideEdgesForPlottables('Not a plottable');
    });

    test('Test setters for attributes (scatter plot)', function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
      var plottables = [this.decomp.plottable[1]];

      // color
      dv.setColor(0x0f0f0f);
      deepEqual(dv.markers[0].material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);
      deepEqual(dv.markers[1].material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);

      dv.setColor(0xff00ff, plottables);
      deepEqual(dv.markers[0].material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);
      deepEqual(dv.markers[1].material.color.toArray(), [1, 0, 1]);

      // visibility
      dv.setVisibility(false);
      deepEqual(dv.markers[0].visible, false);
      deepEqual(dv.markers[1].visible, false);

      dv.setVisibility(true, plottables);
      deepEqual(dv.markers[0].visible, false);
      deepEqual(dv.markers[1].visible, true);

      // scale
      dv.setScale(3);
      deepEqual(dv.markers[0].scale.toArray(), [3, 3, 3]);
      deepEqual(dv.markers[1].scale.toArray(), [3, 3, 3]);

      dv.setScale(0.8, plottables);
      deepEqual(dv.markers[0].scale.toArray(), [3, 3, 3]);
      deepEqual(dv.markers[1].scale.toArray(), [0.8, 0.8, 0.8]);

      // opacity
      dv.setOpacity(0.5);
      deepEqual(dv.markers[0].material.transparent, true);
      deepEqual(dv.markers[0].material.opacity, 0.5);
      deepEqual(dv.markers[1].material.transparent, true);
      deepEqual(dv.markers[1].material.opacity, 0.5);

      dv.setOpacity(1.0, plottables);
      deepEqual(dv.markers[0].material.transparent, true);
      deepEqual(dv.markers[0].material.opacity, 0.5);
      deepEqual(dv.markers[1].material.transparent, false);
      deepEqual(dv.markers[1].material.opacity, 1.0);
    });

    test('Test setters for attributes (scatter plot with edges)', function() {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false, UIState1);
      var dv = new DecompositionView(this.multiModelWithEdges,
                                     'scatter',
                                     UIState1);

      plottables = [this.decomp.plottable[1]];

      // color
      dv.setColor(0x0f0f0f);
      deepEqual(dv.markers[0].material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);
      deepEqual(dv.markers[1].material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);

      dv.setColor(0xff00ff, plottables);
      deepEqual(dv.markers[0].material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);
      deepEqual(dv.markers[1].material.color.toArray(), [1, 0, 1]);

      // visibility
      dv.setVisibility(false);
      deepEqual(dv.markers[0].visible, false);
      deepEqual(dv.markers[1].visible, false);

      // also check for the edges' visibility since the two are tied
      deepEqual(dv.lines.left.geometry.attributes.position.array,
                new Float32Array([0, 0, 0, 0, 0, 0]));
      deepEqual(dv.lines.right.geometry.attributes.position.array,
                new Float32Array([0, 0, 0, 0, 0, 0]));

      dv.setVisibility(true, plottables);
      deepEqual(dv.markers[0].visible, false);
      deepEqual(dv.markers[1].visible, true);

      // scale
      dv.setScale(3);
      deepEqual(dv.markers[0].scale.toArray(), [3, 3, 3]);
      deepEqual(dv.markers[1].scale.toArray(), [3, 3, 3]);

      dv.setScale(0.8, plottables);
      deepEqual(dv.markers[0].scale.toArray(), [3, 3, 3]);
      deepEqual(dv.markers[1].scale.toArray(), [0.8, 0.8, 0.8]);

      // opacity
      dv.setOpacity(0.5);
      deepEqual(dv.markers[0].material.transparent, true);
      deepEqual(dv.markers[0].material.opacity, 0.5);
      deepEqual(dv.markers[1].material.transparent, true);
      deepEqual(dv.markers[1].material.opacity, 0.5);

      dv.setOpacity(1.0, plottables);
      deepEqual(dv.markers[0].material.transparent, true);
      deepEqual(dv.markers[0].material.opacity, 0.5);
      deepEqual(dv.markers[1].material.transparent, false);
      deepEqual(dv.markers[1].material.opacity, 1.0);
    });

    test('Test setters for attribures (biplot)', function(assert) {
      this.decomp.type = 'arrow';
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', false);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
      var plottables = [this.decomp.plottable[1]];

      // color
      dv.setColor(0x0f0f0f);
      deepEqual(dv.markers[0].line.material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);
      deepEqual(dv.markers[0].cone.material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);
      deepEqual(dv.markers[1].line.material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);
      deepEqual(dv.markers[1].cone.material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);

      dv.setColor(0xff00ff, plottables);
      deepEqual(dv.markers[0].line.material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);
      deepEqual(dv.markers[0].cone.material.color.toArray(),
                [15 / 255, 15 / 255, 15 / 255]);
      deepEqual(dv.markers[1].line.material.color.toArray(), [1, 0, 1]);
      deepEqual(dv.markers[1].cone.material.color.toArray(), [1, 0, 1]);

      // visibility
      dv.setVisibility(false);
      deepEqual(dv.markers[0].visible, false);
      deepEqual(dv.markers[1].visible, false);

      dv.setVisibility(true, plottables);
      deepEqual(dv.markers[0].visible, false);
      deepEqual(dv.markers[1].visible, true);

      throws(
        function() {
          dv.setScale(3);
        },
        Error, 'Arrow types cannot change scale');

      throws(
        function() {
          dv.setScale(0.8, plottables);
        },
        Error, 'Arrow types cannot change scale');

      // opacity
      dv.setOpacity(0.5);
      deepEqual(dv.markers[0].line.material.transparent, true);
      deepEqual(dv.markers[0].cone.material.transparent, true);
      deepEqual(dv.markers[0].line.material.opacity, 0.5);
      deepEqual(dv.markers[0].cone.material.opacity, 0.5);
      deepEqual(dv.markers[1].line.material.transparent, true);
      deepEqual(dv.markers[1].cone.material.transparent, true);
      deepEqual(dv.markers[1].line.material.opacity, 0.5);
      deepEqual(dv.markers[1].cone.material.opacity, 0.5);

      dv.setOpacity(1.0, plottables);
      deepEqual(dv.markers[0].line.material.transparent, true);
      deepEqual(dv.markers[0].cone.material.transparent, true);
      deepEqual(dv.markers[0].line.material.opacity, 0.5);
      deepEqual(dv.markers[0].cone.material.opacity, 0.5);
      deepEqual(dv.markers[1].line.material.transparent, false);
      deepEqual(dv.markers[1].cone.material.transparent, false);
      deepEqual(dv.markers[1].line.material.opacity, 1.0);
      deepEqual(dv.markers[1].cone.material.opacity, 1.0);
    });

    test('Test setters for attributes (using point cloud)', function(assert) {
      var UIState1 = new UIState();
      UIState1.setProperty('view.usesPointCloud', true);
      var dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
      var plottables;
      var observed;

      plottables = [this.decomp.plottable[1]];

      // point clouds are a single marker
      observed = dv.markers[0];

      // color
      dv.setColor(0x00ff00);
      equal(observed.geometry.attributes.color.getX(0), 0);
      equal(observed.geometry.attributes.color.getY(0), 1);
      equal(observed.geometry.attributes.color.getZ(0), 0);

      equal(observed.geometry.attributes.color.getX(1), 0);
      equal(observed.geometry.attributes.color.getY(1), 1);
      equal(observed.geometry.attributes.color.getZ(1), 0);

      dv.setColor(0x0000ff, plottables);
      equal(observed.geometry.attributes.color.getX(0), 0);
      equal(observed.geometry.attributes.color.getY(0), 1);
      equal(observed.geometry.attributes.color.getZ(0), 0);

      equal(observed.geometry.attributes.color.getX(1), 0);
      equal(observed.geometry.attributes.color.getY(1), 0);
      equal(observed.geometry.attributes.color.getZ(1), 1);

      // visibility
      dv.setVisibility(false);
      equal(observed.geometry.attributes.visible.getX(0), 0);
      equal(observed.geometry.attributes.visible.getX(1), 0);

      dv.setVisibility(true, plottables);
      equal(observed.geometry.attributes.visible.getX(0), 0);
      equal(observed.geometry.attributes.visible.getX(1), 1);

      // scale
      dv.setScale(3);
      equal(observed.geometry.attributes.scale.getX(0), 3);
      equal(observed.geometry.attributes.scale.getX(1), 3);

      dv.setScale(1, plottables);
      equal(observed.geometry.attributes.scale.getX(0), 3);
      equal(observed.geometry.attributes.scale.getX(1), 1);

      // opacity
      dv.setOpacity(0.5);
      equal(observed.geometry.attributes.opacity.getX(0), 0.5);
      equal(observed.geometry.attributes.opacity.getX(1), 0.5);

      dv.setOpacity(1.0, plottables);
      equal(observed.geometry.attributes.opacity.getX(0), 0.5);
      equal(observed.geometry.attributes.opacity.getX(1), 1.0);
    });

  });
});
