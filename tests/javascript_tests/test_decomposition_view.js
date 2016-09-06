requirejs([
    'jquery',
    'underscore',
    'model',
    'view'
], function($, _, model, DecompositionView) {
  $(document).ready(function() {
    var DecompositionModel = model.DecompositionModel;

    module('Decomposition View', {
      setup: function() {
        // setup function
        name = 'pcoa';
        ids = ['PC.636', 'PC.635'];
        coords = [
          [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
          -0.229889, -0.046599],
          [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
          -0.112864, 0.064794]];
        pct_var = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
        10.024774995, 8.22835130237, 7.55971173665, 6.24945796136];
        md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment', 'DOB'];
        metadata = [['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
        ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112']];
        decomp = new DecompositionModel(name, ids, coords, pct_var, md_headers,
            metadata);
      },

      teardown: function() {
        // teardown function
        name = null;
        ids = null;
        coords = null;
        pct_var = null;
        md_headers = null;
        metadata = null;
        decomp = null;
      }
    });

    /**
     *
     * Test that the Decomposition View object is initialized correctly
     *
     */
    test('Test constructor', function() {
      var obs;
      var dv = new DecompositionView(decomp);
      var _name = 'pcoa';
      var _ids = ['PC.636', 'PC.635'];
      var _coords = [
        [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
        -0.229889, -0.046599],
        [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
        -0.112864, 0.064794]];
      var _pct_var = [26.6887048633, 16.2563704022, 13.7754129161,
                      11.217215823, 10.024774995, 8.22835130237, 7.55971173665,
                      6.24945796136];
      var _md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                         'DOB'];
      var _metadata = [
        ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
        ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112']];
      var exp = new DecompositionModel(_name, _ids, _coords, _pct_var,
          _md_headers, _metadata);

      deepEqual(dv.decomp, exp, 'decomp set correctly');
      equal(dv.count, 2, 'count set correctly');
      equal(dv.visibleCount, 2, 'visibleCount set correctly');
      deepEqual(dv.visibleDimensions, [0, 1, 2],
          'visibleDimensions set correctly');
      deepEqual(dv.tubes, [], 'tubes set correctly');

      equal(dv.axesColor, 0xFFFFFF);
      equal(dv.backgroundColor, 0x000000);

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

    /**
     *
     * Test that changeVisibleDimensions updates the meshes position
     *
     */
    test('Test changeVisibleDimensions', function() {
      var dv = new DecompositionView(decomp);
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
     * Test the changeVisibleDimensions throws an error if the number of
     * dimensions passes is different the 3
     *
     */
    test('Test changeVisibleDimensions excepts', function() {
      throws(
          function() {
            var dv = new DecompositionView(decomp);
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
      var dv = new DecompositionView(decomp);

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

    /**
     *
     * Test that changeVisibleDimensions and flip axis
     *
     */
    test('Test changing the orientations and then flipping a dimension',
         function() {
      var dv = new DecompositionView(decomp);

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
