/**
 *
 * @author Jose Antonio Navas Molina, Jamie Morton
 * @copyright Copyright 2013, The Emperor Project
 * @credits Jose Antonio Navas Molina, Jamie Morton
 * @license BSD
 * @version 0.9.51-dev
 * @maintainer Jose Antonio Navas Molina
 * @email josenavasmolina@gmail.com
 * @status Development
 *
 */

$(document).ready(function() {

  // these variables are reused throughout this test suite
  var name, ids, coords, pct_var, md_headers, metadata;

  module("Decomposition Model", {
    setup: function(){
      // setup function
      name = "pcoa";
      ids = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354', 'PC.593',
             'PC.355', 'PC.607', 'PC.634'];
      coords = [
        [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
         -0.229889, -0.046599],
        [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
         -0.112864, 0.064794],
        [0.228820, -0.130142, -0.287149, 0.086450, 0.044295, 0.206043,
         0.031000, 0.071992],
        [0.042263, -0.013968, 0.063531, -0.346121, -0.127814, 0.013935,
         0.030021, 0.140148],
        [0.280399, -0.006013, 0.023485, -0.046811, -0.146624, 0.005670,
         -0.035430, -0.255786],
        [0.232873, 0.139788, 0.322871, 0.183347, 0.020466, 0.054059,
         -0.036625, 0.099824],
        [0.170518, -0.194113, -0.030897, 0.019809, 0.155100, -0.279924,
         0.057609, 0.024248],
        [-0.091330, 0.424147, -0.135627, -0.057519, 0.151363, -0.025394,
         0.051731, -0.038738],
        [-0.349339, -0.120788, 0.115275, 0.069495, -0.025372, 0.067853,
         0.244448, -0.059883]];
      pct_var = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
                 10.024774995, 8.22835130237, 7.55971173665, 6.24945796136,
                 1.17437418531e-14];
      md_headers = ['LinkerPrimerSequence', 'Treatment', 'DOB'];
      metadata = [['YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
                  ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
                  ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
                  ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
                  ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
                  ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
                  ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
                  ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
                  ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126']];
    },
    teardown: function(){
      // teardown function
      name = null;
      ids = null;
      coords = null;
      pct_var = null;
      md_headers = null;
      metadata = null;
    }
  });

  /**
   *
   * Test that the Decomposition model object can be constructed without any
   * problems and check that the attributes are set correctly
   *
   */
  test("Test constructor", function(){
    var decompositionModel;

    dm = new DecompositionModel(name, ids, coords, pct_var, md_headers,
                                metadata);
    equal(dm.abbreviatedName, "pcoa", "Abbreviated name set correctly");

    var exp = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
               10.024774995, 8.22835130237, 7.55971173665, 6.24945796136,
               1.17437418531e-14];
    deepEqual(dm.percExpl, exp, "Percentage explained set correctly");

    exp = ['LinkerPrimerSequence', 'Treatment', 'DOB'];
    deepEqual(dm.md_headers, exp, "Metadata headers set correctly");

    exp = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354', 'PC.593',
           'PC.355', 'PC.607', 'PC.634'];
    deepEqual(dm.ids, exp, "Ids set correctly");

    exp = [
      new Plottable(
        'PC.636',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
        [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
         -0.229889, -0.046599],
         0),
      new Plottable(
        'PC.635',
        ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
        [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
         -0.112864, 0.064794],
         1),
      new Plottable(
        'PC.356',
        ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
        [0.228820, -0.130142, -0.287149, 0.086450, 0.044295, 0.206043,
         0.031000, 0.071992],
         2),
      new Plottable(
        'PC.481',
        ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
        [0.042263, -0.013968, 0.063531, -0.346121, -0.127814, 0.013935,
         0.030021, 0.140148],
         3),
      new Plottable(
        'PC.354',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
        [0.280399, -0.006013, 0.023485, -0.046811, -0.146624, 0.005670,
         -0.035430, -0.255786],
         4),
      new Plottable(
        'PC.593',
        ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
        [0.232873, 0.139788, 0.322871, 0.183347, 0.020466, 0.054059,
         -0.036625, 0.099824],
         5),
      new Plottable(
        'PC.355',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
        [0.170518, -0.194113, -0.030897, 0.019809, 0.155100, -0.279924,
         0.057609, 0.024248],
         6),
      new Plottable(
        'PC.607',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
        [-0.091330, 0.424147, -0.135627, -0.057519, 0.151363, -0.025394,
         0.051731, -0.038738],
         7),
      new Plottable(
        'PC.634',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126'],
        [-0.349339, -0.120788, 0.115275, 0.069495, -0.025372, 0.067853,
         0.244448, -0.059883],
         8)];
    deepEqual(dm.plottable, exp, "Plottables set correctly");
  });

  /**
   *
   * Test the initializer raises an error if the number of rows in coords is
   * not the same as the number of ids
   *
   */
  test("Test constructor num rows coord != num ids", function(){
    var result;

    throws(
        function(){
          err_coords = [
            [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
             -0.229889, -0.046599],
            [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
             -0.112864, 0.064794],
            [0.228820, -0.130142, -0.287149, 0.086450, 0.044295, 0.206043,
             0.031000, 0.071992],
            [0.042263, -0.013968, 0.063531, -0.346121, -0.127814, 0.013935,
             0.030021, 0.140148],
            [0.280399, -0.006013, 0.023485, -0.046811, -0.146624, 0.005670,
             -0.035430, -0.255786],
            [0.232873, 0.139788, 0.322871, 0.183347, 0.020466, 0.054059,
             -0.036625, 0.099824],
            [0.170518, -0.194113, -0.030897, 0.019809, 0.155100, -0.279924,
             0.057609, 0.024248]]; 
          result = new DecompositionModel(name, ids, err_coords, pct_var,
                                          md_headers, metadata);
        },
        Error,
        'An error is raised if the number of rows in the coords parameter '+
        'does not correspond to the number of ids'
      );
  });

  /**
   *
   * Test the initializer raises an error if all rows in coords does not have
   * the same number of elements
   *
   */
  test("Test")



  /**
   *
   * Test the trajectory object raises the appropriate errors when
   * constructing with bad arguments.
   *
   */
  test("Test constructor exceptions", function(){
      var result;
  
      // check this happens for all the properties
      throws(
          function (){
              result = new TrajectoryOfSamples(sampleNames, 'foo', [1, 2, 3],
                                               coordinates);
          },
          Error,
          'An error is raised if the number of coordinates does not '+
          'correspond to the number of gradient points'
      );
  });

  /**
   *
   * Test the trajectory object computes the interpolated coordinates
   * correctly
   *
   */
  test("Test _generateInterpolatedCoordinates", function(){

      var trajectory;
      var expectedInterpolatedCoordinates = [{ "x": 0, "y": 0, "z": 0},
      { "x": 0.1, "y": 0.1, "z": 0.1},
      { "x": 0.2, "y": 0.2, "z": 0.2},
      { "x": 0.30000000000000004, "y": 0.30000000000000004, "z": 0.30000000000000004},
      { "x": 0.4, "y": 0.4, "z": 0.4},
      { "x": 0.5, "y": 0.5, "z": 0.5},
      { "x": 0.6000000000000001, "y": 0.6000000000000001, "z": 0.6000000000000001},
      { "x": 0.7000000000000001, "y": 0.7000000000000001, "z": 0.7000000000000001},
      { "x": 0.8, "y": 0.8, "z": 0.8},
      { "x": 0.9, "y": 0.9, "z": 0.9},
      { "x": 1, "y": 1, "z": 1},
      { "x": 0, "y": 0, "z": 0},
      { "x": -1, "y": -1, "z": -1},
      { "x": -2, "y": -2, "z": -2},
      { "x": -3, "y": -3, "z": -3},
      { "x": -4, "y": -4, "z": -4},
      { "x": -5, "y": -5, "z": -5},
      { "x": -6, "y": -6, "z": -6},
      { "x": -7, "y": -7, "z": -7},
      { "x": -8, "y": -8, "z": -8},
      { "x": -9, "y": -9, "z": -9},
      { "x": -7.8, "y": -7.8, "z": -7.8},
      { "x": -6.6, "y": -6.6, "z": -6.6},
      { "x": -5.4, "y": -5.4, "z": -5.4},
      { "x": -4.2, "y": -4.2, "z": -4.2},
      { "x": -3, "y": -3, "z": -3},
      { "x": -1.8000000000000007, "y": -1.8000000000000007, "z": -1.8000000000000007},
      { "x": -0.5999999999999996, "y": -0.5999999999999996, "z": -0.5999999999999996},
      { "x": 0.5999999999999996, "y": 0.5999999999999996, "z": 0.5999999999999996},
      { "x": 1.799999999999999, "y": 1.799999999999999, "z": 1.799999999999999},
      { "x": 3, "y": 3, "z": 3},
      { "x": 3.5, "y": 3.5, "z": 3.5},
      { "x": 4, "y": 4, "z": 4},
      { "x": 4.5, "y": 4.5, "z": 4.5},
      { "x": 5, "y": 5, "z": 5},
      { "x": 5.5, "y": 5.5, "z": 5.5},
      { "x": 6, "y": 6, "z": 6},
      { "x": 6.5, "y": 6.5, "z": 6.5},
      { "x": 7, "y": 7, "z": 7},
      { "x": 7.5, "y": 7.5, "z": 7.5},
      { "x": 8, "y": 8, "z": 8}];
      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
                                           gradientPoints, coordinates, 2,
                                           10);

      // test the interpolated values and the interval values
      deepEqual(trajectory.interpolatedCoordinates,
                expectedInterpolatedCoordinates,
                'Check the interpolated coordinates are computed correctly');
      deepEqual(trajectory._intervalValues, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3,
              3, 3, 3, 3, 3, 3, 3, 3] , 'Check the intervals array is '+
              'created properyl');

      expectedInterpolatedCoordinates = [{"x": 0, "y": 0, "z": 0},
                                         {"x": 0.25, "y": 0.25, "z": 0.25},
                                         {"x": 0.5, "y": 0.5, "z": 0.5},
                                         {"x": 0.75, "y": 0.75, "z": 0.75},
                                         {"x": 1, "y": 1, "z": 1},
                                         {"x": -2.3333333333333335, "y": -2.3333333333333335, "z": -2.3333333333333335},
                                         {"x": -5.666666666666667, "y": -5.666666666666667, "z": -5.666666666666667},
                                         {"x": -9, "y": -9, "z": -9},
                                         {"x": -5, "y": -5, "z": -5},
                                         {"x": -1, "y": -1, "z": -1},
                                         {"x": 3, "y": 3, "z": 3},
                                         {"x": 4.25, "y": 4.25, "z": 4.25},
                                         {"x": 5.5, "y": 5.5, "z": 5.5},
                                         {"x": 6.75, "y": 6.75, "z": 6.75},
                                         {"x": 8, "y": 8, "z": 8 }];
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
  test('Test representativeCoordinatesAtIndex edge cases', function(){
      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
          gradientPoints, coordinates, 2,
          3);
      deepEqual(trajectory.representativeCoordinatesAtIndex(0),
                [{'x':0, 'y':0, 'z':0}],
                'Returns an empty array for index 0');

      var expectedCoordinates = [{'x':0, 'y':0, 'z':0},
                                 {'x':1, 'y':1, 'z':1},
                                 {'x':-9, 'y':-9, 'z':-9},
                                 {'x':3, 'y':3, 'z':3},
                                 {'x':8, 'y':8, 'z':8}];
      // the interpolated array is 18 samples long
      deepEqual(trajectory.representativeCoordinatesAtIndex(18),
                expectedCoordinates, 'Returns an array with only the '+
                'original coordinates');
      deepEqual(trajectory.representativeCoordinatesAtIndex(100),
                expectedCoordinates, 'Returns an array with only the '+
                'original coordinates');
  });

  /**
   *
   * Test the trajectory object retrieves only the needed points for a given
   * index.
   *
   */
  test('Test representativeCoordinatesAtIndex', function(){
      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
          gradientPoints, coordinates, 2,
          3);

      var expectedCoordinates = [{'x':0, 'y':0, 'z':0},
                                 {'x':1, 'y':1, 'z':1},
                                 {'x':-9, 'y':-9, 'z':-9},
                                 {'x':3, 'y':3, 'z':3},
                                 {'x':8, 'y':8, 'z':8}];

      var expectedInterpolatedCoordinates = [{'x': 0, 'y': 0, 'z': 0},
                                           {'x': 0.25, 'y': 0.25, 'z': 0.25},
                                           {'x': 0.5, 'y': 0.5, 'z': 0.5},
                                           {'x': 0.75, 'y': 0.75, 'z': 0.75},
                                           {'x': 1, 'y': 1, 'z': 1},
                                           {'x': -2.3333333333333335, 'y': -2.3333333333333335, 'z': -2.3333333333333335},
                                           {'x': -5.666666666666667, 'y': -5.666666666666667, 'z': -5.666666666666667},
                                           {'x': -9, 'y': -9, 'z': -9},
                                           {'x': -5, 'y': -5, 'z': -5},
                                           {'x': -1, 'y': -1, 'z': -1},
                                           {'x': 3, 'y': 3, 'z': 3},
                                           {'x': 4.25, 'y': 4.25, 'z': 4.25},
                                           {'x': 5.5, 'y': 5.5, 'z': 5.5},
                                           {'x': 6.75, 'y': 6.75, 'z': 6.75},
                                           {'x': 8, 'y': 8, 'z': 8}]

      deepEqual(trajectory.representativeCoordinatesAtIndex(3),
                [{"x": 0, "y": 0, "z": 0},
                {"x": 0.75, "y": 0.75, "z": 0.75}],
                'Coordinates are retrieved correctly at index 3');
      deepEqual(trajectory.representativeCoordinatesAtIndex(11),
                [{'x':0, 'y':0, 'z':0}, {'x':1, 'y':1, 'z':1},
                 {'x':-9, 'y':-9, 'z':-9}, {'x':3, 'y':3, 'z':3},
                 {'x': 4.25, 'y': 4.25, 'z': 4.25}],
                'Coordinates are retrieved correctly at index 11');

  });

  /**
   *
   * Test the trajectory object computes the number of points for a given
   * delta correctly.
   *
   */
  test('Test calculateNumberOfPointsForDelta', function(){
      var trajectory;

      trajectory = new TrajectoryOfSamples(sampleNames, 'Treatment',
                                           gradientPoints, coordinates, 2,
                                           10);
      equal(trajectory.calculateNumberOfPointsForDelta(3), 15, 'Number of '+
            'points for delta is calculated correctly');
      equal(trajectory.calculateNumberOfPointsForDelta(8), 40, 'Number of '+
            'points for delta is calculated correctly');
      equal(trajectory.calculateNumberOfPointsForDelta(7), 35, 'Number of '+
            'points for delta is calculated correctly');
      equal(trajectory.calculateNumberOfPointsForDelta(11), 55, 'Number of '+
            'points for delta is calculated correctly');
      equal(trajectory.calculateNumberOfPointsForDelta(1), 5, 'Number of '+
            'points for delta is calculated correctly');
  });

  /**
   *
   * Test linearInterpolation function.
   *
   */
  test('Test linearInterpolation', function(){
      var result;
      result = linearInterpolation(0, 0, 0, 1, 1, 1, 5);
      expectedResult = [{ "x": 0, "y": 0, "z": 0},
                        {"x": 0.2, "y": 0.2, "z": 0.2},
                        { "x": 0.4, "y": 0.4, "z": 0.4 },
                        { "x": 0.6000000000000001, "y": 0.6000000000000001,
                        "z": 0.6000000000000001 },
                        { "x": 0.8, "y": 0.8, "z": 0.8 },
                        { "x": 1, "y": 1, "z": 1}];
      deepEqual(result, expectedResult, 'Linear interpolation is computed '+
                'correctly')

      result = linearInterpolation(0, 0, 0, -1, -1, -1, 5);
      expectedResult = [{ "x": 0, "y": 0, "z": 0},
                        {"x": -0.2, "y": -0.2, "z": -0.2},
                        { "x": -0.4, "y": -0.4, "z": -0.4 },
                        { "x": -0.6000000000000001, "y": -0.6000000000000001,
                        "z": -0.6000000000000001 },
                        { "x": -0.8, "y": -0.8, "z": -0.8 },
                        { "x": -1, "y": -1, "z": -1}];
      deepEqual(result, expectedResult, 'Linear interpolation is computed '+
                'correctly')
  });

  /**
   *
   * Test distanceBetweenPoints function.
   *
   */
  test('Test distanceBetweenPoints', function(){
      var result;
      result = distanceBetweenPoints(0, 0, 0, 1, 1, 1);
      equal(result, Math.sqrt(3),'Distance between points is computed'+
            'correctly');

      result = distanceBetweenPoints(-4, -3, -2, 84, 2, 11);
      equal(result, 89.09545442950498, 'Distance between points is computed '+
            'correctly');

      result = distanceBetweenPoints(0, 0, 0, 0, 0, 0);
      equal(result, 0, 'Distance between points is computed correctly');

      result = distanceBetweenPoints(-3, 17, -8888, 11, 0, 1);
      equal(result, 8889.027280867125, 'Distance between points is computed '+
          'correctly');

  });

  /**
   *
   * Test getSampleNamesAndDataForSortedTrajectories function.
   *
   */
  test('Test getSampleNamesAndDataForSortedTrajectories', function(){
      var result, expectedResult;

      result = getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders,
                                                              mappingFileData,
                                                              coordinatesData,
                                                              'Treatment',
                                                              'DOB');
      deepEqual(result, crunchedDataTwoCategories, 'The data is computed '+
                'correctly for two trajectories');

      result = getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders,
                                                          mappingFileData,
                                                          coordinatesData,
                                                          'LinkerPrimerSequence',
                                                          'DOB');
      deepEqual(result, crunchedDataOneCategory, 'The data is computed '+
                'correctly for a single trajectory');
  });

  /**
   *
   * Test getSampleNamesAndDataForSortedTrajectories function raises the
   * appropriate errors.
   *
   */
  test('Test getSampleNamesAndDataForSortedTrajectories exceptions', function(){
      throws(function(){
          result = getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders,
                                                              mappingFileData,
                                                              coordinatesData,
                                                              'DOB',
                                                              'BAZ');
      }, Error, 'Error is thrown when a category is not found');

      throws(function(){
        result = getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders,
                                                            mappingFileData,
                                                            coordinatesData,
                                                            'SPAM',
                                                            'DOB');
      }, Error, 'Error is thrown when a category is not found');

      throws(function(){
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
  test('Test getMinimumDelta function', function(){
      var result;
      result = getMinimumDelta(crunchedDataOneCategory);
      equal(result, 92, 'The minimum delta is computed correctly for one '+
            'category');

      result = getMinimumDelta(crunchedDataTwoCategories);
      equal(result, 92, 'The minimum delta is computed correctly for one '+
            'category');
  });

});
