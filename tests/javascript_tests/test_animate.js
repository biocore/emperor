requirejs([
    'underscore',
    'jquery',
    'animate'
], function(_, $, AnimationDirector) {
  $(document).ready(function() {

    // these variables are reused throughout this test suite
    var mappingFileHeaders, mappingFileData, coordinatesData;

    module('Animate', {

      setup: function() {
        // setup function
        mappingFileHeaders = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                              'DOB'];
        mappingFileData = {
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
        coordinatesData = new Array();
        coordinatesData['PC.636'] = { 'name': 'PC.636', 'color': 0, 'x':
        -0.276542, 'y': -0.144964, 'z': 0.066647, 'P1': -0.276542, 'P2':
        -0.144964, 'P3': 0.066647, 'P4': -0.067711, 'P5': 0.176070, 'P6':
        0.072969, 'P7': -0.229889, 'P8': -0.046599 };
        coordinatesData['PC.635'] = { 'name': 'PC.635', 'color': 0, 'x':
        -0.237661, 'y': 0.046053, 'z': -0.138136, 'P1': -0.237661, 'P2':
        0.046053, 'P3': -0.138136, 'P4': 0.159061, 'P5': -0.247485, 'P6':
        -0.115211, 'P7': -0.112864, 'P8': 0.064794 };
        coordinatesData['PC.356'] = { 'name': 'PC.356', 'color': 0, 'x':
        0.228820, 'y': -0.130142, 'z': -0.287149, 'P1': 0.228820, 'P2':
        -0.130142, 'P3': -0.287149, 'P4': 0.086450, 'P5': 0.044295, 'P6':
        0.206043, 'P7': 0.031000, 'P8': 0.071992 };

        coordinatesData['PC.481'] = { 'name': 'PC.481', 'color': 0, 'x':
        0.042263, 'y': -0.013968, 'z': 0.063531, 'P1': 0.042263, 'P2':
        -0.013968, 'P3': 0.063531, 'P4': -0.346121, 'P5': -0.127814, 'P6':
        0.013935, 'P7': 0.030021, 'P8': 0.140148 }; coordinatesData['PC.354'] =
        { 'name': 'PC.354', 'color': 0, 'x': 0.280399, 'y': -0.006013, 'z':
        0.023485, 'P1': 0.280399, 'P2': -0.006013, 'P3': 0.023485, 'P4':
        -0.046811, 'P5': -0.146624, 'P6': 0.005670, 'P7': -0.035430, 'P8':
        -0.255786 };
        coordinatesData['PC.593'] = { 'name': 'PC.593', 'color': 0,
        'x': 0.232873, 'y': 0.139788, 'z': 0.322871, 'P1': 0.232873, 'P2':
        0.139788, 'P3': 0.322871, 'P4': 0.183347, 'P5': 0.020466, 'P6':
        0.054059, 'P7': -0.036625, 'P8': 0.099824 };
        coordinatesData['PC.355'] = { 'name': 'PC.355', 'color': 0, 'x':
        0.170518, 'y': -0.194113, 'z': -0.030897, 'P1': 0.170518, 'P2':
        -0.194113, 'P3': -0.030897, 'P4': 0.019809, 'P5': 0.155100, 'P6':
        -0.279924, 'P7': 0.057609, 'P8': 0.024248 };
        coordinatesData['PC.607'] = { 'name': 'PC.607', 'color': 0,
        'x': -0.091330, 'y': 0.424147, 'z': -0.135627, 'P1': -0.091330, 'P2':
        0.424147, 'P3': -0.135627, 'P4': -0.057519, 'P5': 0.151363, 'P6':
        -0.025394, 'P7': 0.051731, 'P8': -0.038738 };
        coordinatesData['PC.634'] = { 'name': 'PC.634', 'color': 0,
        'x': -0.349339, 'y': -0.120788, 'z': 0.115275, 'P1': -0.349339,
        'P2': -0.120788, 'P3': 0.115275, 'P4': 0.069495, 'P5': -0.025372,
        'P6': 0.067853, 'P7': 0.244448, 'P8': -0.059883 };

        mappingFileDataShort = { 'PC.481': ['PC.481', 'YATGCTGCCTCCCGTAGGAGT',
        'Control', '20070314'], 'PC.635': ['PC.635', 'YATGCTGCCTCCCGTAGGAGT',
        'Fast', '20080116'], 'PC.636': ['PC.636', 'YATGCTGCCTCCCGTAGGAGT',
        'Fast', '20080116'], 'PC.356': ['PC.356', 'YATGCTGCCTCCCGTAGGAGT',
        'Fast', '20061126'] };
        coordinatesDataShort = new Array();
        coordinatesDataShort['PC.636'] = { 'name': 'PC.636', 'color': 0, 'x':
        -0.276542, 'y': -0.144964, 'z': 0.066647, 'P1': -0.276542, 'P2':
        -0.144964, 'P3': 0.066647, 'P4': -0.067711, 'P5': 0.176070, 'P6':
        0.072969, 'P7': -0.229889, 'P8': -0.046599 };
        coordinatesDataShort['PC.635'] = { 'name': 'PC.635', 'color': 0, 'x':
        -0.237661, 'y': 0.046053, 'z': -0.138136, 'P1': -0.237661, 'P2':
        0.046053, 'P3': -0.138136, 'P4': 0.159061, 'P5': -0.247485, 'P6':
        -0.115211, 'P7': -0.112864, 'P8': 0.064794 };
        coordinatesDataShort['PC.356'] = { 'name': 'PC.356', 'color': 0, 'x':
        0.228820, 'y': -0.130142, 'z': -0.287149, 'P1': 0.228820, 'P2':
        -0.130142, 'P3': -0.287149, 'P4': 0.086450, 'P5': 0.044295, 'P6':
        0.206043, 'P7': 0.031000, 'P8': 0.071992 };
        coordinatesDataShort['PC.481'] = { 'name': 'PC.481', 'color': 0, 'x':
        0.042263, 'y': -0.013968, 'z': 0.063531, 'P1': 0.042263, 'P2':
        -0.013968, 'P3': 0.063531, 'P4': -0.346121, 'P5': -0.127814, 'P6':
        0.013935, 'P7': 0.030021, 'P8': 0.140148 };

        // trajectories with only one unique timepoint in different cases
        // (1) all timepoints with the same value
        // (2) a single timepoint
        mappingFileHeadersUnique = ['SampleID', 'LinkerPrimerSequence',
                                    'Treatment', 'DOB'];
        mappingFileDataUnique = {
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

      teardown: function() {
        // teardown function
        mappingFileHeaders = null;
        mappingFileData = null;
        coordinatesData = null;
      }

    });

    /**
     *
     * Test that the animation object can be constructed without any problems
     * and check that the attributes are set correctly.
     *
     */
    test('Test constructor', function() {

      var director = new AnimationDirector(mappingFileHeaders, mappingFileData,
          coordinatesData, 'DOB',
          'Treatment', 1000, 10);

      // a quick run through all the properties
      equal(director.mappingFileHeaders, mappingFileHeaders, 'The mapping ' +
          'file headers are set correctly');
      equal(director.mappingFileData, mappingFileData, 'The mapping file ' +
          'data is set correctly');
      equal(director.coordinatesData, coordinatesData, 'The coordinates data' +
          ' is set correctly');
      equal(director.gradientCategory, 'DOB', 'The gradientCategory is set' +
          ' correctly');
      equal(director.trajectoryCategory, 'Treatment', 'The ' +
          'trajectoryCategory is set correctly');
      equal(director.minimumDelta, 92, 'The minimum delta is computed' +
          'correctly');
      equal(director.maximumTrajectoryLength, 26, 'The maximum trajectory ' +
          'length value is correct');
      equal(director.currentFrame, -1, 'The current frame is correct');
      equal(director.trajectories.length, 2, 'The number of trajectories is ' +
          'correct');
      equal(director.trajectories[0].metadataCategoryName, 'Control', 'The' +
          'metadata category name is set correctly for the trajectory 1');
      equal(director.trajectories[1].metadataCategoryName, 'Fast', 'The' +
          'metadata category name is set correctly for the trajectory 1');

      // check the trajectories are overall ok -- reason why I added this,
      // because they are not :P
      deepEqual(director.trajectories[0].representativeCoordinatesAtIndex(1000),
          [{'x': 0.22882, 'y': -0.130142, 'z': -0.287149},
          {'x': 0.170518, 'y': -0.194113, 'z': -0.030897},
          {'x': 0.280399, 'y': -0.006013, 'z': 0.023485},
          {'x': 0.042263, 'y': -0.013968, 'z': 0.063531},
          {'x': 0.232873, 'y': 0.139788, 'z': 0.322871}],
          'Control');
      deepEqual(director.trajectories[1].representativeCoordinatesAtIndex(1000),
          [{'x': -0.09133, 'y': 0.424147, 'z': -0.135627},
          {'x': -0.349339, 'y': -0.120788, 'z': 0.115275},
          {'x': -0.237661, 'y': 0.046053, 'z': -0.138136},
          {'x': -0.276542, 'y': -0.144964, 'z': 0.066647}],
          'Fast');
      equal(director.trajectories.length, 2, 'The number of trajectories is ' +
          'correct');
    });

    test('Test useless trajectories are removed', function() {
      var director = new AnimationDirector(mappingFileHeadersUnique,
          mappingFileDataUnique,
          coordinatesData, 'DOB',
          'Treatment', 1000, 10);
      equal(director.trajectories.length, 2, 'The number of trajectories is ' +
          'correct');
      equal(director.trajectories[0].metadataCategoryName, 'C', 'The ' +
          'category name (C) is assigned correctly');
      equal(director.trajectories[1].metadataCategoryName, 'D', 'The ' +
          'category name (D) is assigned correctly');
      deepEqual(director.trajectories[0].gradientPoints,
          ['0', '1', '2'], 'Correct time points (C)');
        deepEqual(director.trajectories[1].gradientPoints,
            ['-9999', '0', '100000'], 'Correct time points (D)');
    });

    /**
     *
     * Test that the animation object cannot be constructed when there are
     * missing arguments.
     *
     */
    test('Test constructor exceptions', function() {
      var result;

      // check this happens for all the properties
      throws(
          function() {
            result = new AnimationDirector(mappingFileData, coordinatesData,
                'DOB', 'Treatment', 1000);
          },
          Error,
          'An error is raised if mapping file headers are not passed'
          );

      throws(
          function() {
            result = new AnimationDirector(mappingFileHeaders,
                coordinatesData, 'DOB',
                'Treatment', 1000);
          },
          Error,
          'An error is raised if mapping file data is not passed'
          );

      throws(
          function() {
            result = new AnimationDirector(mappingFileHeaders,
                mappingFileData, coordinatesData,
                'Treatment', 1000);
          },
          Error,
          'An error is raised if no gradient category is passed'
          );

      throws(
          function() {
            result = new AnimationDirector(mappingFileHeaders,
                mappingFileData, 'DOB', 1000);
          },
          Error,
          'An error is raised if no trajectory category is passed'
          );

      throws(
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
    test('Test maximum trajectory length method', function() {

      var director = new AnimationDirector(mappingFileHeaders, mappingFileData,
          coordinatesData, 'DOB',
          'Treatment', 1000);
      equal(director.getMaximumTrajectoryLength(), 26,
          'Test for the correct getMaximumTrajectoryLength value to be ' +
          'returned');
      var director = new AnimationDirector(mappingFileHeaders, mappingFileData,
          coordinatesData, 'DOB',
          'Treatment', 10000);
      equal(director.getMaximumTrajectoryLength(), 26,
          'Test for the correct getMaximumTrajectoryLength value to be ' +
          'returned');
      var director = new AnimationDirector(mappingFileHeaders,
          mappingFileData, coordinatesData,
          'DOB', 'LinkerPrimerSequence',
          1000);
      equal(director.getMaximumTrajectoryLength(), 41,
          'Test for the correct getMaximumTrajectoryLength value to be ' +
          'returned');
    });

    /**
     *
     * Test that the animation object updateFrame method updates the value only
     * when needed.
     *
     */
    test('Test the current frame is updated correctly', function() {
      var director = new AnimationDirector(mappingFileHeaders,
          mappingFileData, coordinatesData,
          'DOB', 'Treatment', 1000);
      equal(director.currentFrame, -1, 'The current frame is set correctly');
      director.updateFrame();
      equal(director.currentFrame, 0, 'The current frame is set correctly');

      // make sure the value is topped at the maximum trajectory length
      for (var i = 1; i < 1000; i++) {
        director.updateFrame();
      }
      equal(director.currentFrame, 27, 'The current frame is stopped at the' +
          ' maximum trajectory length');
    });

    /**
     *
     * Test that the animation object gets the correct number of trajectories.
     *
     */
    test('Test the trajectories are initialized correctly', function() {
      var director = new AnimationDirector(mappingFileHeaders,
          mappingFileData, coordinatesData,
          'DOB', 'Treatment', 1000);
      equal(director.trajectories.length, 2, 'Correct number of trajectories');

      var director = new AnimationDirector(mappingFileHeaders, mappingFileData,
          coordinatesData, 'DOB',
          'LinkerPrimerSequence', 1000);
      equal(director.trajectories.length, 1, 'Correct number of trajectories');

    });

    /**
     *
     * Test that the animation object ignores one-sample trajectories
     *
     */
    test('Test that tricky trajectories are initialized correctly', function() {
      var director = new AnimationDirector(mappingFileHeaders,
          mappingFileDataShort,
          coordinatesDataShort,
          'DOB', 'Treatment', 1000);
      equal(director.trajectories.length, 1, 'Correct number of trajectories');

    });
  });
});
