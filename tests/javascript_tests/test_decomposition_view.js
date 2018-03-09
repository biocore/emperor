requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'three'
], function($, _, model, DecompositionView, THREE) {
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
      var dv = new DecompositionView(this.decomp);

      deepEqual(dv.decomp, this.expected, 'decomp set correctly');
      equal(dv.count, 2, 'count set correctly');
      equal(dv.getVisibleCount(), 2, 'visibleCount set correctly');
      deepEqual(dv.visibleDimensions, [0, 1, 2],
          'visibleDimensions set correctly');
      deepEqual(dv.tubes, [], 'tubes set correctly');

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
      deepEqual(dv.lines, [], 'lines set correctly');
      /*
         TODO: How do we test this?
         */
      // deepEqual(dv._genericSphere, undefined,
      //           "_genericSphere set correctly");
    });

    test('Test constructor (biplot)', function(assert) {
      // this test is pretty much the same as above except for arrow types
      this.decomp.type = 'arrow';
      var view = new DecompositionView(this.decomp);

      this.expected.type = 'arrow';
      deepEqual(view.decomp, this.expected);
      equal(view.count, 2);
      equal(view.getVisibleCount(), 2);
      deepEqual(view.visibleDimensions, [0, 1, 2]);
      deepEqual(view.tubes, []);
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
      view.markers.map(function (marker) {
        assert.ok(marker instanceof THREE.ArrowHelper);

        deepEqual(marker.line.material.color.getHex(), 0x708090);
        deepEqual(marker.cone.material.color.getHex(), 0x708090);
      });
    });

    /**
     *
     * Test that getVisibleCount is correctly updated
     *
     */
    test('Test getVisibleCount', function() {
      var dv = new DecompositionView(this.decomp);
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
      var dv = new DecompositionView(this.decomp);
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

    test('Test changeVisibleDimensions (2D)', function() {
      var dv = new DecompositionView(this.decomp);
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
            var dv = new DecompositionView(this.decomp);
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
      var dv = new DecompositionView(this.decomp);

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
      var dv = new DecompositionView(this.decomp);

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


    /**
     *
     * Test that changeVisibleDimensions and flip axis
     *
     */
    test('Test changing the orientations and then flipping a dimension',
         function() {
      var dv = new DecompositionView(this.decomp);

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
  });
});
