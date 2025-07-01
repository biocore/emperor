requirejs([
    'underscore',
    'jquery',
    'animationdirector'
], function(_, $, AnimationDirector) {
  $(document).ready(function() {

    QUnit.module('Animate', {

      beforeEach() {
        // setup function
        this.mappingFileHeaders = ['SampleID', 'LinkerPrimerSequence',
                                   'Treatment', 'DOB'];
        this.mappingFileData = {
          'PC.481': ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
          'PC.607': ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
          'PC.634': ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
          'PC.635': ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
          'PC.593': ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
          'PC.636': ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
          'PC.355': ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
          'PC.354': ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
          'PC.356': ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126']
        };
        this.coordinatesData = new Array();
        this.coordinatesData['PC.636'] = { 'name': 'PC.636', 'color': 0, 'x':
        -0.276542, 'y': -0.144964, 'z': 0.066647, 'P1': -0.276542, 'P2':
        -0.144964, 'P3': 0.066647, 'P4': -0.067711, 'P5': 0.176070, 'P6':
        0.072969, 'P7': -0.229889, 'P8': -0.046599 };
        this.coordinatesData['PC.635'] = { 'name': 'PC.635', 'color': 0, 'x':
        -0.237661, 'y': 0.046053, 'z': -0.138136, 'P1': -0.237661, 'P2':
        0.046053, 'P3': -0.138136, 'P4': 0.159061, 'P5': -0.247485, 'P6':
        -0.115211, 'P7': -0.112864, 'P8': 0.064794 };
        this.coordinatesData['PC.356'] = { 'name': 'PC.356', 'color': 0, 'x':
        0.228820, 'y': -0.130142, 'z': -0.287149, 'P1': 0.228820, 'P2':
        -0.130142, 'P3': -0.287149, 'P4': 0.086450, 'P5': 0.044295, 'P6':
        0.206043, 'P7': 0.031000, 'P8': 0.071992 };

        this.coordinatesData['PC.481'] = { 'name': 'PC.481', 'color': 0, 'x':
        0.042263, 'y': -0.013968, 'z': 0.063531, 'P1': 0.042263, 'P2':
        -0.013968, 'P3': 0.063531, 'P4': -0.346121, 'P5': -0.127814, 'P6':
        0.013935, 'P7': 0.030021, 'P8': 0.140148 };

        this.coordinatesData['PC.354'] = { 'name': 'PC.354', 'color': 0, 'x':
        0.280399, 'y': -0.006013, 'z': 0.023485, 'P1': 0.280399, 'P2':
        -0.006013, 'P3': 0.023485, 'P4': -0.046811, 'P5': -0.146624, 'P6':
        0.005670, 'P7': -0.035430, 'P8': -0.255786 };

        this.coordinatesData['PC.593'] = { 'name': 'PC.593', 'color': 0,
        'x': 0.232873, 'y': 0.139788, 'z': 0.322871, 'P1': 0.232873, 'P2':
        0.139788, 'P3': 0.322871, 'P4': 0.183347, 'P5': 0.020466, 'P6':
        0.054059, 'P7': -0.036625, 'P8': 0.099824 };

        this.coordinatesData['PC.355'] = { 'name': 'PC.355', 'color': 0, 'x':
        0.170518, 'y': -0.194113, 'z': -0.030897, 'P1': 0.170518, 'P2':
        -0.194113, 'P3': -0.030897, 'P4': 0.019809, 'P5': 0.155100, 'P6':
        -0.279924, 'P7': 0.057609, 'P8': 0.024248 };

        this.coordinatesData['PC.607'] = { 'name': 'PC.607', 'color': 0,
        'x': -0.091330, 'y': 0.424147, 'z': -0.135627, 'P1': -0.091330, 'P2':
        0.424147, 'P3': -0.135627, 'P4': -0.057519, 'P5': 0.151363, 'P6':
        -0.025394, 'P7': 0.051731, 'P8': -0.038738 };

        this.coordinatesData['PC.634'] = { 'name': 'PC.634', 'color': 0,
        'x': -0.349339, 'y': -0.120788, 'z': 0.115275, 'P1': -0.349339,
        'P2': -0.120788, 'P3': 0.115275, 'P4': 0.069495, 'P5': -0.025372,
        'P6': 0.067853, 'P7': 0.244448, 'P8': -0.059883 };

        this.mappingFileDataShort = { 'PC.481': ['PC.481',
        'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126'], 'PC.635': ['PC.635',
        'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'], 'PC.636': ['PC.636',
        'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'], 'PC.356': ['PC.356',
        'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20061126'] };
        this.coordinatesDataShort = new Array();
        this.coordinatesDataShort['PC.636'] = { 'name': 'PC.636', 'color': 0,
        'x': -0.276542, 'y': -0.144964, 'z': 0.066647, 'P1': -0.276542, 'P2':
        -0.144964, 'P3': 0.066647, 'P4': -0.067711, 'P5': 0.176070, 'P6':
        0.072969, 'P7': -0.229889, 'P8': -0.046599 };

        this.coordinatesDataShort['PC.635'] = { 'name': 'PC.635', 'color': 0,
        'x': -0.237661, 'y': 0.046053, 'z': -0.138136, 'P1': -0.237661, 'P2':
        0.046053, 'P3': -0.138136, 'P4': 0.159061, 'P5': -0.247485, 'P6':
        -0.115211, 'P7': -0.112864, 'P8': 0.064794 };

        this.coordinatesDataShort['PC.356'] = { 'name': 'PC.356', 'color': 0,
        'x': 0.228820, 'y': -0.130142, 'z': -0.287149, 'P1': 0.228820, 'P2':
        -0.130142, 'P3': -0.287149, 'P4': 0.086450, 'P5': 0.044295, 'P6':
        0.206043, 'P7': 0.031000, 'P8': 0.071992 };

        this.coordinatesDataShort['PC.481'] = { 'name': 'PC.481', 'color': 0,
        'x': 0.042263, 'y': -0.013968, 'z': 0.063531, 'P1': 0.042263, 'P2':
        -0.013968, 'P3': 0.063531, 'P4': -0.346121, 'P5': -0.127814, 'P6':
        0.013935, 'P7': 0.030021, 'P8': 0.140148 };

        // trajectories with only one unique timepoint in different cases
        // (1) all timepoints with the same value
        // (2) a single timepoint
        this.mappingFileHeadersUnique = ['SampleID', 'LinkerPrimerSequence',
                                         'Treatment', 'DOB'];
        this.mappingFileDataUnique = {
          'PC.481': ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'A', '0'],
          'PC.607': ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'B', '0'],
          'PC.634': ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'B', '0'],
          'PC.635': ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'C', '0'],
          'PC.593': ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', 'C', '1'],
          'PC.636': ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'C', '2'],
          'PC.355': ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'D', '-9999'],
          'PC.354': ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'D', '0'],
          'PC.356': ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'D', '100000'] };
      },

      afterEach() {
        // teardown function
        this.mappingFileHeaders = null;
        this.mappingFileData = null;
        this.coordinatesData = null;
      }

    });

    /**
     *
     * Test that the animation object can be constructed without any problems
     * and check that the attributes are set correctly.
     *
     */
   QUnit.test('Test constructor', function(assert) {

      var director = new AnimationDirector(this.mappingFileHeaders,
                                           this.mappingFileData,
                                           this.coordinatesData, 'DOB',
                                           'Treatment', 10);

      // a quick run through all the properties
     assert.equal(director.mappingFileHeaders,
                  this.mappingFileHeaders,
                  'The  mapping file headers are set correctly');

     assert.equal(director.mappingFileData,
                  this.mappingFileData,
                  'The mapping file data is set correctly');

     assert.equal(director.coordinatesData,
                  this.coordinatesData,
                  'The coordinates data is set correctly');

     assert.equal(director.gradientCategory,
                  'DOB',
                  'The gradientCategory is set correctly');

     assert.equal(director.trajectoryCategory,
                  'Treatment',
                  'The trajectoryCategory is set correctly');

     assert.equal(director.minimumDelta,
                  92,
                  'The minimum delta is computed correctly');

     assert.equal(director.maximumTrajectoryLength,
                  206,
                  'The maximum trajectory length value is correct');

     assert.equal(director.currentFrame,
                  -1,
                  'The current frame is correct');
     assert.equal(director.trajectories.length,
                  2,
                  'The number of trajectories is correct');

     assert.equal(director.trajectories[0].metadataCategoryName,
                  'Control',
                  'The metadata category name is set correctly for the ' +
                  'trajectory 1');

     assert.equal(director.trajectories[1].metadataCategoryName, 'Fast', 'The' +
          'metadata category name is set correctly for the trajectory 1');

      // check the trajectories are overall ok -- reason why I added this,
      // because they are not :P
     assert.deepEqual(
       director.trajectories[0].representativeCoordinatesAtIndex(1000),
       [{'x': 0.22882, 'y': -0.130142, 'z': -0.287149},
        {'x': 0.170518, 'y': -0.194113, 'z': -0.030897},
        {'x': 0.280399, 'y': -0.006013, 'z': 0.023485},
        {'x': 0.042263, 'y': -0.013968, 'z': 0.063531},
        {'x': 0.232873, 'y': 0.139788, 'z': 0.322871}],
       'Control');

     assert.deepEqual(
       director.trajectories[1].representativeCoordinatesAtIndex(1000),
       [{'x': -0.09133, 'y': 0.424147, 'z': -0.135527},
        {'x': -0.09133, 'y': 0.424147, 'z': -0.135627},
        {'x': -0.349339, 'y': -0.120788, 'z': 0.115275},
        {'x': -0.237661, 'y': 0.046053, 'z': -0.138136},
        {'x': -0.276542, 'y': -0.144964, 'z': 0.066647}],
       'Fast');

     assert.equal(director.trajectories.length,
                  2,
                  'The number of trajectories is correct');
    });

   QUnit.test('Test useless trajectories are removed', function(assert) {
      var director = new AnimationDirector(this.mappingFileHeadersUnique,
                                           this.mappingFileDataUnique,
                                           this.coordinatesData, 'DOB',
                                           'Treatment', 2);
     assert.equal(director.trajectories.length,
                  2,
                  'The number of trajectories is correct');
     assert.equal(director.trajectories[0].metadataCategoryName, 'C', 'The ' +
          'category name (C) is assigned correctly');
     assert.equal(director.trajectories[1].metadataCategoryName, 'D', 'The ' +
          'category name (D) is assigned correctly');
     assert.deepEqual(director.trajectories[0].gradientPoints,
          ['-9999', '0', '1', '2'], 'Correct time points (C)');
       assert.deepEqual(director.trajectories[1].gradientPoints,
            ['-9999', '0', '100000'], 'Correct time points (D)');
    });

    /**
     *
     * Test that the animation object cannot be constructed when there are
     * missing arguments.
     *
     */
   QUnit.test('Test constructor exceptions', function(assert) {
      var result;

      // check this happens for all the properties
     assert.throws(
          function() {
            result = new AnimationDirector(mappingFileData, coordinatesData,
                'DOB', 'Treatment', 1);
          },
          Error,
          'An error is raised if mapping file headers are not passed'
          );

     assert.throws(
          function() {
            result = new AnimationDirector(mappingFileHeaders,
                coordinatesData, 'DOB',
                'Treatment', 1);
          },
          Error,
          'An error is raised if mapping file data is not passed'
          );

     assert.throws(
          function() {
            result = new AnimationDirector(mappingFileHeaders,
                mappingFileData, coordinatesData,
                'Treatment', 1);
          },
          Error,
          'An error is raised if no gradient category is passed'
          );

     assert.throws(
          function() {
            result = new AnimationDirector(mappingFileHeaders,
                mappingFileData, 'DOB', 1);
          },
          Error,
          'An error is raised if no trajectory category is passed'
          );

     assert.throws(
          function() {
            result = new AnimationDirector(mappingFileHeaders, mappingFileData,
                'DOB', 'Treatment');
          },
          Error,
          'An error is raised if no the number of frames is not passed'
          );
    });

    /**
     *
     * Test that the animation object getMaximumTrajectoryLength method returns
     * the correct value for different cases.
     *
     */
   QUnit.test('Test maximum trajectory length method', function(assert) {

      var director = new AnimationDirector(this.mappingFileHeaders,
                                           this.mappingFileData,
                                           this.coordinatesData, 'DOB',
                                           'Treatment', 1);
     assert.equal(director.getMaximumTrajectoryLength(), 2064,
          'Test for the correct getMaximumTrajectoryLength value to be ' +
          'returned');
      var director = new AnimationDirector(this.mappingFileHeaders,
                                           this.mappingFileData,
                                           this.coordinatesData, 'DOB',
          'Treatment', 10);
     assert.equal(director.getMaximumTrajectoryLength(), 206,
          'Test for the correct getMaximumTrajectoryLength value to be ' +
          'returned');
      var director = new AnimationDirector(this.mappingFileHeaders,
                                           this.mappingFileData,
                                           this.coordinatesData,
                                           'DOB', 'LinkerPrimerSequence',
                                           100);
     assert.equal(director.getMaximumTrajectoryLength(), 1,
          'Test for the correct getMaximumTrajectoryLength value to be ' +
          'returned');
    });

    /**
     *
     * Test that the animation object updateFrame method updates the value only
     * when needed.
     *
     */
   QUnit.test('Test the current frame is updated correctly', function(assert) {
      var director = new AnimationDirector(this.mappingFileHeaders,
                                           this.mappingFileData,
                                           this.coordinatesData,
                                           'DOB', 'Treatment', 10);
     assert.equal(director.currentFrame,
                  -1,
                  'The current frame is set correctly');
      director.updateFrame();
     assert.equal(director.currentFrame,
                  0,
                  'The current frame is set correctly');

      // make sure the value is topped at the maximum trajectory length
      for (var i = 1; i < 1000; i++) {
        director.updateFrame();
      }
     assert.equal(director.currentFrame,
                  207,
                  'The current frame is stopped at the  maximum trajectory ' +
                  'length');
    });

    /**
     *
     * Test that the animation object gets the correct number of trajectories.
     *
     */
   QUnit.test('Test the trajectories are initialized correctly',
      function(assert) {
        var director = new AnimationDirector(this.mappingFileHeaders,
                                             this.mappingFileData,
                                             this.coordinatesData,
                                             'DOB', 'Treatment', 1000);
        assert.equal(director.trajectories.length,
                     2,
                     'Correct number of trajectories');

        var director = new AnimationDirector(this.mappingFileHeaders,
                                             this.mappingFileData,
                                             this.coordinatesData, 'DOB',
                                             'LinkerPrimerSequence', 1000);
        assert.equal(director.trajectories.length,
                     1,
                     'Correct number of trajectories');

        var gradientPoints = director.gradientPoints;
        assert.deepEqual(gradientPoints,
                         [20061126, 20061218, 20070314, 20071112, 20071210,
                          20080116]);
    });

    /**
     *
     * Test that the animation object ignores one-sample trajectories
     *
     */
   QUnit.test('Test that tricky trajectories are initialized correctly',
   function(assert) {
      var director = new AnimationDirector(this.mappingFileHeaders,
                                           this.mappingFileDataShort,
                                           this.coordinatesDataShort,
                                           'DOB', 'Treatment', 1);
     assert.equal(director.trajectories.length,
                  1,
                  'Correct number of trajectories');

    });


   QUnit.test('Test currentFrameIsGradientPoint works', function(assert) {
      var director = new AnimationDirector(this.mappingFileHeaders,
                                           this.mappingFileDataShort,
                                           this.coordinatesDataShort,
                                           'DOB', 'Treatment', 1);

      director.currentFrame = 1;
      assert.ok(director.currentFrameIsGradientPoint());

      director.currentFrame = 2;
      assert.ok(!director.currentFrameIsGradientPoint());

      director.currentFrame = 11;
      assert.ok(director.currentFrameIsGradientPoint());
    });


  });
});
