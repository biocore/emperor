requirejs(['underscore', 'trajectory'], function(_, trajectory) {
  $(document).ready(function() {
    var TrajectoryOfSamples = trajectory.TrajectoryOfSamples;
    var getMinimumDelta = trajectory.getMinimumDelta;
    var getSampleNamesAndDataForSortedTrajectories =
      trajectory.getSampleNamesAndDataForSortedTrajectories;
    var distanceBetweenPoints = trajectory.distanceBetweenPoints;
    var linearInterpolation = trajectory.linearInterpolation;

    // these variables are reused throughout this test suite
    var mappingFileHeaders, mappingFileData, coordinatesData;
    var sampleNames, gradientPoints, coordinates;

    // these are expected results needed for multiple tests
    var crunchedDataTwoCategories, crunchedDataOneCategory;

    module('Trajectory', {

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
          'PC.356': ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126']};

        coordinatesData = new Array();
        coordinatesData['PC.636'] = { 'name': 'PC.636', 'color': 0,
          'x': -0.276542, 'y': -0.144964, 'z': 0.066647, 'P1': -0.276542,
          'P2': -0.144964, 'P3': 0.066647, 'P4': -0.067711, 'P5': 0.176070,
          'P6': 0.072969, 'P7': -0.229889, 'P8': -0.046599 };

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
            0.013935, 'P7': 0.030021, 'P8': 0.140148 };
        coordinatesData['PC.354'] = { 'name': 'PC.354', 'color': 0, 'x':
          0.280399, 'y': -0.006013, 'z': 0.023485, 'P1': 0.280399, 'P2':
            -0.006013, 'P3': 0.023485, 'P4': -0.046811, 'P5': -0.146624, 'P6':
            0.005670, 'P7': -0.035430, 'P8': -0.255786 };
        coordinatesData['PC.593'] = { 'name': 'PC.593', 'color': 0, 'x':
          0.232873, 'y': 0.139788, 'z': 0.322871, 'P1': 0.232873, 'P2':
            0.139788, 'P3': 0.322871, 'P4': 0.183347, 'P5': 0.020466, 'P6':
            0.054059, 'P7': -0.036625, 'P8': 0.099824 };
        coordinatesData['PC.355'] = { 'name': 'PC.355', 'color': 0, 'x':
          0.170518, 'y': -0.194113, 'z': -0.030897, 'P1': 0.170518, 'P2':
            -0.194113, 'P3': -0.030897, 'P4': 0.019809, 'P5': 0.155100, 'P6':
            -0.279924, 'P7': 0.057609, 'P8': 0.024248 };
        coordinatesData['PC.607'] = { 'name': 'PC.607', 'color': 0, 'x':
          -0.091330, 'y': 0.424147, 'z': -0.135627, 'P1': -0.091330, 'P2':
            0.424147, 'P3': -0.135627, 'P4': -0.057519, 'P5': 0.151363, 'P6':
            -0.025394, 'P7': 0.051731, 'P8': -0.038738 };
        coordinatesData['PC.634'] = { 'name': 'PC.634', 'color': 0, 'x':
          -0.349339, 'y': -0.120788, 'z': 0.115275, 'P1': -0.349339, 'P2':
            -0.120788, 'P3': 0.115275, 'P4': 0.069495, 'P5': -0.025372, 'P6':
            0.067853, 'P7': 0.244448, 'P8': -0.059883 };

        sampleNames = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354'];
        gradientPoints = [1, 4, 6, 8, 11];
        coordinates = [{'x': 0, 'y': 0, 'z': 0}, {'x': 1, 'y': 1, 'z': 1},
        {'x': -9, 'y': -9, 'z': -9}, {'x': 3, 'y': 3, 'z': 3},
        {'x': 8, 'y': 8, 'z': 8}];

        crunchedDataOneCategory = {'YATGCTGCCTCCCGTAGGAGT': [
          { 'name': 'PC.356', 'value': '20061126', 'x': 0.22882, 'y':
            -0.130142, 'z': -0.287149},
          { 'name': 'PC.355', 'value': '20061218', 'x': 0.170518, 'y':
            -0.194113, 'z': -0.030897},
          { 'name': 'PC.354', 'value': '20061218', 'x': 0.280399, 'y':
            -0.006013, 'z': 0.023485},
          { 'name': 'PC.481', 'value': '20070314', 'x': 0.042263, 'y':
            -0.013968, 'z': 0.063531},
          { 'name': 'PC.607', 'value': '20071112', 'x': -0.09133, 'y':
            0.424147, 'z': -0.135627},
          { 'name': 'PC.593', 'value': '20071210', 'x': 0.232873, 'y':
            0.139788, 'z': 0.322871},
          { 'name': 'PC.634', 'value': '20080116', 'x': -0.349339, 'y':
            -0.120788, 'z': 0.115275},
          { 'name': 'PC.635', 'value': '20080116', 'x': -0.237661, 'y':
            0.046053, 'z': -0.138136},
          { 'name': 'PC.636', 'value': '20080116', 'x': -0.276542, 'y':
            -0.144964, 'z': 0.066647}
        ]
        };

        crunchedDataTwoCategories = expectedResult = {'Control': [
          {'name': 'PC.356', 'value': '20061126', 'x': 0.22882, 'y': -0.130142,
            'z': -0.287149},
          {'name': 'PC.355', 'value': '20061218', 'x': 0.170518, 'y':
            -0.194113, 'z': -0.030897},
          {'name': 'PC.354', 'value': '20061218', 'x': 0.280399, 'y':
            -0.006013, 'z': 0.023485},
          {'name': 'PC.481', 'value': '20070314', 'x': 0.042263, 'y':
            -0.013968, 'z': 0.063531},
          {'name': 'PC.593', 'value': '20071210', 'x': 0.232873, 'y': 0.139788,
            'z': 0.322871}
        ],
        'Fast': [
        {'name': 'PC.607', 'value': '20071112', 'x': -0.09133, 'y': 0.424147,
          'z': -0.135627},
        {'name': 'PC.634', 'value': '20080116', 'x': -0.349339, 'y': -0.120788,
          'z': 0.115275},
        {'name': 'PC.635', 'value': '20080116', 'x': -0.237661, 'y': 0.046053,
          'z': -0.138136},
        {'name': 'PC.636', 'value': '20080116', 'x': -0.276542, 'y': -0.144964,
          'z': 0.066647}
        ]
        };
      },

      teardown: function() {
        // teardown function
        mappingFileHeaders = null;
        mappingFileData = null;
        coordinatesData = null;

        sampleNames = null;
        gradientPoints = null;
        coordinates = null;
      }

    });

    /**
     *
     * Test that the trajectory object can be constructed without any problems
     * and check that the attributes are set correctly.
     *
     */
    test('Test constructor', function() {
      var trajectory;

      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
          gradientPoints, coordinates, 2,
          10);
      deepEqual(trajectory.sampleNames, ['PC.636', 'PC.635', 'PC.356',
          'PC.481', 'PC.354'], 'Sample names are set correctly');
      equal(trajectory.metadataCategoryName, 'Treatment', 'Metadata ' +
          'category name is set correctly');
      deepEqual(trajectory.gradientPoints, [1, 4, 6, 8, 11], 'Gradient ' +
          'point values are set correctly');
      deepEqual(trajectory.coordinates, [{'x': 0, 'y': 0, 'z': 0},
          {'x': 1, 'y': 1, 'z': 1}, {'x': -9, 'y': -9, 'z': -9},
          {'x': 3, 'y': 3, 'z': 3}, {'x': 8, 'y': 8, 'z': 8}], 'Coordinates' +
          ' values are set correctly');
      equal(trajectory.minimumDelta, 2, 'Minimum delta is set correctly');
      equal(trajectory.suppliedN, 10, 'Value of N is set correctly');

      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
          gradientPoints,
          coordinates, 2);
      deepEqual(trajectory.sampleNames, ['PC.636', 'PC.635', 'PC.356',
          'PC.481', 'PC.354'], 'Sample names are set correctly');
      equal(trajectory.metadataCategoryName, 'Treatment', 'Metadata ' +
          'category name is set correctly');
      deepEqual(trajectory.gradientPoints, [1, 4, 6, 8, 11], 'Gradient' +
          ' point values are set correctly');
      deepEqual(trajectory.coordinates, [{'x': 0, 'y': 0, 'z': 0},
          {'x': 1, 'y': 1, 'z': 1}, {'x': -9, 'y': -9, 'z': -9},
          {'x': 3, 'y': 3, 'z': 3}, {'x': 8, 'y': 8, 'z': 8}], 'Coordinates' +
          ' values are set correctly');
      equal(trajectory.minimumDelta, 2, 'Minimum delta is set correctly');
      equal(trajectory.suppliedN, 5, 'Default value of N is set to 5');
    });

    /**
     *
     * Test the trajectory object raises the appropriate errors when
     * constructing with bad arguments.
     *
     */
    test('Test constructor exceptions', function() {
      var result;

      // check this happens for all the properties
      throws(
          function() {
            result = new TrajectoryOfSamples(sampleNames, 'foo', [1, 2, 3],
                coordinates);
          },
          Error,
          'An error is raised if the number of coordinates does not ' +
          'correspond to the number of gradient points'
          );
    });

    /**
     *
     * Test the trajectory object computes the interpolated coordinates
     * correctly
     *
     */
    test('Test _generateInterpolatedCoordinates', function() {

      var trajectory;
      var expectedInterpolatedCoordinates = [{ 'x': 0, 'y': 0, 'z': 0},
      { 'x': 0.1, 'y': 0.1, 'z': 0.1},
      { 'x': 0.2, 'y': 0.2, 'z': 0.2},
      { 'x': 0.30000000000000004, 'y': 0.30000000000000004,
        'z': 0.30000000000000004},
      { 'x': 0.4, 'y': 0.4, 'z': 0.4},
      { 'x': 0.5, 'y': 0.5, 'z': 0.5},
      { 'x': 0.6000000000000001, 'y': 0.6000000000000001,
        'z': 0.6000000000000001},
      { 'x': 0.7000000000000001, 'y': 0.7000000000000001,
        'z': 0.7000000000000001},
      { 'x': 0.8, 'y': 0.8, 'z': 0.8},
      { 'x': 0.9, 'y': 0.9, 'z': 0.9},
      { 'x': 1, 'y': 1, 'z': 1},
      { 'x': 0, 'y': 0, 'z': 0},
      { 'x': -1, 'y': -1, 'z': -1},
      { 'x': -2, 'y': -2, 'z': -2},
      { 'x': -3, 'y': -3, 'z': -3},
      { 'x': -4, 'y': -4, 'z': -4},
      { 'x': -5, 'y': -5, 'z': -5},
      { 'x': -6, 'y': -6, 'z': -6},
      { 'x': -7, 'y': -7, 'z': -7},
      { 'x': -8, 'y': -8, 'z': -8},
      { 'x': -9, 'y': -9, 'z': -9},
      { 'x': -7.8, 'y': -7.8, 'z': -7.8},
      { 'x': -6.6, 'y': -6.6, 'z': -6.6},
      { 'x': -5.4, 'y': -5.4, 'z': -5.4},
      { 'x': -4.2, 'y': -4.2, 'z': -4.2},
      { 'x': -3, 'y': -3, 'z': -3},
      { 'x': -1.8000000000000007, 'y': -1.8000000000000007,
        'z': -1.8000000000000007},
      { 'x': -0.5999999999999996, 'y': -0.5999999999999996,
        'z': -0.5999999999999996},
      { 'x': 0.5999999999999996, 'y': 0.5999999999999996,
        'z': 0.5999999999999996},
      { 'x': 1.799999999999999, 'y': 1.799999999999999,
        'z': 1.799999999999999},
      { 'x': 3, 'y': 3, 'z': 3},
      { 'x': 3.5, 'y': 3.5, 'z': 3.5},
      { 'x': 4, 'y': 4, 'z': 4},
      { 'x': 4.5, 'y': 4.5, 'z': 4.5},
      { 'x': 5, 'y': 5, 'z': 5},
      { 'x': 5.5, 'y': 5.5, 'z': 5.5},
      { 'x': 6, 'y': 6, 'z': 6},
      { 'x': 6.5, 'y': 6.5, 'z': 6.5},
      { 'x': 7, 'y': 7, 'z': 7},
      { 'x': 7.5, 'y': 7.5, 'z': 7.5},
      { 'x': 8, 'y': 8, 'z': 8}];
      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
          gradientPoints, coordinates, 2,
          10);

      // test the interpolated values and the interval values
      deepEqual(trajectory.interpolatedCoordinates,
          expectedInterpolatedCoordinates,
          'Check the interpolated coordinates are computed correctly');
      deepEqual(trajectory._intervalValues, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3,
          3, 3, 3, 3, 3, 3, 3, 3] , 'Check the intervals array is ' +
          'created properyl');

      expectedInterpolatedCoordinates = [{'x': 0, 'y': 0, 'z': 0},
      {'x': 0.25, 'y': 0.25, 'z': 0.25},
      {'x': 0.5, 'y': 0.5, 'z': 0.5},
      {'x': 0.75, 'y': 0.75, 'z': 0.75},
      {'x': 1, 'y': 1, 'z': 1},
      {'x': -2.3333333333333335, 'y': -2.3333333333333335,
        'z': -2.3333333333333335},
      {'x': -5.666666666666667, 'y': -5.666666666666667,
        'z': -5.666666666666667},
      {'x': -9, 'y': -9, 'z': -9},
      {'x': -5, 'y': -5, 'z': -5},
      {'x': -1, 'y': -1, 'z': -1},
      {'x': 3, 'y': 3, 'z': 3},
      {'x': 4.25, 'y': 4.25, 'z': 4.25},
      {'x': 5.5, 'y': 5.5, 'z': 5.5},
      {'x': 6.75, 'y': 6.75, 'z': 6.75},
      {'x': 8, 'y': 8, 'z': 8 }];
      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
          gradientPoints, coordinates, 2,
          3);
      deepEqual(trajectory.interpolatedCoordinates,
          expectedInterpolatedCoordinates,
          'Check the interpolated coordinates are computed correctly');
      deepEqual(trajectory._intervalValues,
          [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3] ,
          'Check the interpolated coordinates are computed correctly');
    });

    /**
     *
     * Test the trajectory object retrieves only the needed points for a given
     * index (edge cases).
     *
     */
    test('Test representativeCoordinatesAtIndex edge cases', function() {
      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
          gradientPoints, coordinates, 2,
          3);
      deepEqual(trajectory.representativeCoordinatesAtIndex(0),
          [{'x': 0, 'y': 0, 'z': 0}],
          'Returns an empty array for index 0');

      var expectedCoordinates = [{'x': 0, 'y': 0, 'z': 0},
      {'x': 1, 'y': 1, 'z': 1},
      {'x': -9, 'y': -9, 'z': -9},
      {'x': 3, 'y': 3, 'z': 3},
      {'x': 8, 'y': 8, 'z': 8}];
      // the interpolated array is 18 samples long
      deepEqual(trajectory.representativeCoordinatesAtIndex(18),
          expectedCoordinates, 'Returns an array with only the ' +
          'original coordinates');
      deepEqual(trajectory.representativeCoordinatesAtIndex(100),
          expectedCoordinates, 'Returns an array with only the ' +
          'original coordinates');
    });

    /**
     *
     * Test the trajectory object retrieves only the needed points for a given
     * index.
     *
     */
    test('Test representativeCoordinatesAtIndex', function() {
      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
          gradientPoints, coordinates, 2,
          3);

      var expectedCoordinates = [{'x': 0, 'y': 0, 'z': 0},
      {'x': 1, 'y': 1, 'z': 1},
      {'x': -9, 'y': -9, 'z': -9},
      {'x': 3, 'y': 3, 'z': 3},
      {'x': 8, 'y': 8, 'z': 8}];

      var expectedInterpolatedCoordinates = [{'x': 0, 'y': 0, 'z': 0},
      {'x': 0.25, 'y': 0.25, 'z': 0.25},
      {'x': 0.5, 'y': 0.5, 'z': 0.5},
      {'x': 0.75, 'y': 0.75, 'z': 0.75},
      {'x': 1, 'y': 1, 'z': 1},
      {'x': -2.3333333333333335, 'y': -2.3333333333333335,
        'z': -2.3333333333333335},
      {'x': -5.666666666666667, 'y': -5.666666666666667,
        'z': -5.666666666666667},
      {'x': -9, 'y': -9, 'z': -9},
      {'x': -5, 'y': -5, 'z': -5},
      {'x': -1, 'y': -1, 'z': -1},
      {'x': 3, 'y': 3, 'z': 3},
      {'x': 4.25, 'y': 4.25, 'z': 4.25},
      {'x': 5.5, 'y': 5.5, 'z': 5.5},
      {'x': 6.75, 'y': 6.75, 'z': 6.75},
      {'x': 8, 'y': 8, 'z': 8}];

      deepEqual(trajectory.representativeCoordinatesAtIndex(3),
          [{'x': 0, 'y': 0, 'z': 0},
          {'x': 0.75, 'y': 0.75, 'z': 0.75}],
          'Coordinates are retrieved correctly at index 3');
      deepEqual(trajectory.representativeCoordinatesAtIndex(11),
          [{'x': 0, 'y': 0, 'z': 0}, {'x': 1, 'y': 1, 'z': 1},
          {'x': -9, 'y': -9, 'z': -9}, {'x': 3, 'y': 3, 'z': 3},
          {'x': 4.25, 'y': 4.25, 'z': 4.25}],
          'Coordinates are retrieved correctly at index 11');

    });

    /**
     *
     * Test the trajectory object computes the number of points for a given
     * delta correctly.
     *
     */
    test('Test calculateNumberOfPointsForDelta', function() {
      var trajectory;

      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
          gradientPoints, coordinates, 2,
          10);
      equal(trajectory.calculateNumberOfPointsForDelta(3), 15, 'Number of ' +
          'points for delta is calculated correctly');
      equal(trajectory.calculateNumberOfPointsForDelta(8), 40, 'Number of ' +
          'points for delta is calculated correctly');
      equal(trajectory.calculateNumberOfPointsForDelta(7), 35, 'Number of ' +
          'points for delta is calculated correctly');
      equal(trajectory.calculateNumberOfPointsForDelta(11), 55, 'Number of ' +
          'points for delta is calculated correctly');
      equal(trajectory.calculateNumberOfPointsForDelta(1), 5, 'Number of ' +
          'points for delta is calculated correctly');
    });

    /**
     *
     * Test linearInterpolation function.
     *
     */
    test('Test linearInterpolation', function() {
      var result;
      result = linearInterpolation(0, 0, 0, 1, 1, 1, 5);
      expectedResult = [{ 'x': 0, 'y': 0, 'z': 0},
      {'x': 0.2, 'y': 0.2, 'z': 0.2},
      { 'x': 0.4, 'y': 0.4, 'z': 0.4 },
      { 'x': 0.6000000000000001, 'y': 0.6000000000000001,
        'z': 0.6000000000000001 },
      { 'x': 0.8, 'y': 0.8, 'z': 0.8 },
      { 'x': 1, 'y': 1, 'z': 1}];
      deepEqual(result, expectedResult, 'Linear interpolation is computed ' +
          'correctly');

        result = linearInterpolation(0, 0, 0, -1, -1, -1, 5);
      expectedResult = [{ 'x': 0, 'y': 0, 'z': 0},
      {'x': -0.2, 'y': -0.2, 'z': -0.2},
      { 'x': -0.4, 'y': -0.4, 'z': -0.4 },
      { 'x': -0.6000000000000001, 'y': -0.6000000000000001,
        'z': -0.6000000000000001 },
      { 'x': -0.8, 'y': -0.8, 'z': -0.8 },
      { 'x': -1, 'y': -1, 'z': -1}];
      deepEqual(result, expectedResult, 'Linear interpolation is computed ' +
          'correctly');
    });

    /**
     *
     * Test distanceBetweenPoints function.
     *
     */
    test('Test distanceBetweenPoints', function() {
      var result;
      result = distanceBetweenPoints(0, 0, 0, 1, 1, 1);
      equal(result, Math.sqrt(3), 'Distance between points is computed' +
          'correctly');

      result = distanceBetweenPoints(-4, -3, -2, 84, 2, 11);
      equal(result, 89.09545442950498, 'Distance between points is computed ' +
          'correctly');

      result = distanceBetweenPoints(0, 0, 0, 0, 0, 0);
      equal(result, 0, 'Distance between points is computed correctly');

      result = distanceBetweenPoints(-3, 17, -8888, 11, 0, 1);
      equal(result, 8889.027280867125, 'Distance between points is computed ' +
          'correctly');

    });

    /**
     *
     * Test getSampleNamesAndDataForSortedTrajectories function.
     *
     */
    test('Test getSampleNamesAndDataForSortedTrajectories', function() {
      var result, expectedResult;

      result = getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders,
          mappingFileData,
          coordinatesData,
          'Treatment',
          'DOB');
      deepEqual(result, crunchedDataTwoCategories, 'The data is computed ' +
          'correctly for two trajectories');

      result = getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders,
          mappingFileData,
          coordinatesData,
          'LinkerPrimerSequence',
          'DOB');
      deepEqual(result, crunchedDataOneCategory, 'The data is computed ' +
          'correctly for a single trajectory');
    });

    /**
     *
     * Test getSampleNamesAndDataForSortedTrajectories function raises the
     * appropriate errors.
     *
     */
    test('Test getSampleNamesAndDataForSortedTrajectories errors', function() {
      throws(function() {
        result = getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders,
            mappingFileData,
            coordinatesData,
            'DOB',
            'BAZ');
      }, Error, 'Error is thrown when a category is not found');

      throws(function() {
        result = getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders,
            mappingFileData,
            coordinatesData,
            'SPAM',
            'DOB');
      }, Error, 'Error is thrown when a category is not found');

      throws(function() {
        result = getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders,
            mappingFileData,
            coordinatesData,
            'FOO',
            'BAR');
      }, Error, 'Error is thrown when a category is not found');

    });

    /**
     *
     * Test getMinimumDelta function computes data correctly.
     *
     */
    test('Test getMinimumDelta function', function() {
      var result;
      result = getMinimumDelta(crunchedDataOneCategory);
      equal(result, 92, 'The minimum delta is computed correctly for one ' +
          'category');

      result = getMinimumDelta(crunchedDataTwoCategories);
      equal(result, 92, 'The minimum delta is computed correctly for one ' +
          'category');
    });

  });
});
