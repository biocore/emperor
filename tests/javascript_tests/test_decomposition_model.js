/**
 *
 * @author Jamie Morton, Jose Navas Molina, Andrew Hodges & Yoshiki
 *         Vazquez-Baeza
 * @copyright Copyright 2013--, The Emperor Project
 * @credits Jamie Morton, Jose Navas Molina, Andrew Hodges & Yoshiki
 *          Vazquez-Baeza
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
  test("Test constructor excepts num rows coord != num ids", function(){
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
  test("Test constructor excepts rows in coord different lengths", function(){
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
           0.057609, 0.024248],
          [-0.091330, 0.424147, -0.135627, -0.057519, 0.151363, -0.025394,
           0.051731, -0.038738],
          [-0.349339, -0.120788]];
        result = new DecompositionModel(name, ids, err_coords, pct_var,
                                          md_headers, metadata);
      },
      Error,
      'An error is raised if all rows in coords does not have the same length'
      );
  });

  /**
   *
   * Test the initializer raises an error if the number of elements in pct_var
   * does not correspond to the number of coords.
   *
   */
  test("Test constructor excepts num pct_var != num coords", function(){
    var result;
    throws(
      function(){
        err_pct_var = [26.6887048633, 16.2563704022, 13.7754129161,
                       11.217215823, 10.024774995, 8.22835130237];
        result = new DecompositionModel(name, ids, coords, err_pct_var,
                                        md_headers, metadata);
      },
      Error,
      'An error is raised if the number of percentage explained does not '+
      'correspond to the number of coords'
      );
  });

  /**
   *
   * Test the initializer raises an error if the number of rows in metadata is
   * not the same as the number of ids
   *
   */
  test("Test constructor excepts num rows metadata != num ids", function(){
    var result;

    throws(
      function(){
        err_metadata = [['YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
                        ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
                        ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
                        ['YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
                        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
                        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126']];
        result = new DecompositionModel(name, ids, coords, pct_var,
                                        md_headers, err_metadata);
      },
      Error,
      'An error is raised if the number of rows in the metadata parameter '+
      'does not correspond to the number of ids'
    );
  });

  /**
   *
   * Test the initializer raises an error if the number of columns in metadata
   * is not the same as the number of metadata headers
   *
   */
  test("Test constructor excepts metadata cols != num headers", function(){
    var result;

    throws(
      function(){
        err_metadata = [['YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
                        ['YATGCTGCCTCCCGTAGGAGT', '20071112'],
                        ['YATGCTGCCTCCCGTAGGAGT', '20080116'],
                        ['YATGCTGCCTCCCGTAGGAGT', '20080116'],
                        ['YATGCTGCCTCCCGTAGGAGT', '20071210'],
                        ['YATGCTGCCTCCCGTAGGAGT', '20080116'],
                        ['YATGCTGCCTCCCGTAGGAGT', '20061218'],
                        ['YATGCTGCCTCCCGTAGGAGT', '20061218'],
                        ['YATGCTGCCTCCCGTAGGAGT', '20061126']];
        result = new DecompositionModel(name, ids, coords, pct_var,
                                        md_headers, err_metadata);
      },
      Error,
      'An error is raised if the number of elements in each row in the '+
      'metadata parameter does not match the number of metadata columns'
    )
  });

  /* Jamie starts here */
  test('Test get plottable by id', function(){
    var dm = new DecompositionModel(name, ids, coords, pct_var, md_headers,
                                    metadata);
    var exp =
      new Plottable(
        'PC.636',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
        [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
         -0.229889, -0.046599],
         0);

    var obs = dm.getPlottableByID('PC.636');

    deepEqual(obs, exp,
	      "Metadata groups retrieved successfully");

  }

  test("Test getPlottableByID id not in DecompositionModel ids", function(){
    var result;
    throws(
      function(){
	var dm = new DecompositionModel(name, ids, coords, pct_var, md_headers,
					metadata);
	result = dm.getPlottableByID('PC.637');
      },
        Error,
        'An error is raised if the id is not found in the Decomposition Model ids';
    );
  }

  test('Test get plottables by ids', function(){
    var dm = new DecompositionModel(name, ids, coords, pct_var, md_headers,
                                    metadata);
    var exp = [
      new Plottable(
        'PC.636',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
        [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
         -0.229889, -0.046599],
         0),
      new Plottable(
        'PC.354',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
        [0.280399, -0.006013, 0.023485, -0.046811, -0.146624, 0.005670,
         -0.035430, -0.255786],
         4),
      new Plottable(
        'PC.355',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
        [0.170518, -0.194113, -0.030897, 0.019809, 0.155100, -0.279924,
         0.057609, 0.024248],
         6)];

    var obs = dm.getPlottableByIDs(['PC.636', 'PC.354', 'PC.355']);

    deepEqual(obs, exp,
	      "Metadata groups retrieved successfully");

  }

  test('Test get plottables by metadata category', function(){
    var exp = [
      new Plottable(
        'PC.636',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
        [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
         -0.229889, -0.046599],
         0),
      new Plottable(
        'PC.354',
        ['YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
        [0.280399, -0.006013, 0.023485, -0.046811, -0.146624, 0.005670,
         -0.035430, -0.255786],
         4),
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

    var dm = new DecompositionModel(name, ids, coords, pct_var, md_headers,
                                    metadata);
    var obs = dm.getPlottablesByMetadataCategoryValue('Treatment', 'Control');

    deepEqual(obs, exp,
	      "Metadata groups retrieved successfully");

  }

  test("Test getPlottablesByMetadataCategoryValue category not found in metadata headers", function(){
    var result;
    throws(
      function(){
	var dm = new DecompositionModel(name, ids, coords, pct_var, md_headers,
					metadata);
	result = dm.getPlottableByID('PC.637');
      },
        Error,
        'An error is raised if the metadata category is not found in the metadata headers';
    );
  }


  test('Test get unique values by category', function(){
    var dm;

    dm = new DecompositionModel(name, ids, coords, pct_var, md_headers,
                                metadata);
    var obs = dm.getUniqueValuesByCategory('foo');
    var exp = ['Fast', 'Control'];

    deepEqual(obs, exp,
	      "Unique metadata values retrieved successfully");
  }

  test("Test getUniqueValuesByCategory category not found in metadata headers", function(){
    var result;
    throws(
      function(){
	var dm = new DecompositionModel(name, ids, coords, pct_var, md_headers,
					metadata);
	result = dm.getUniqueValuesByCategory('foo');
      },
        Error,
        'An error is raised if the metadata category is not found in the metadata headers';
    );
  }

});
