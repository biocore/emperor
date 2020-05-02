requirejs([
    'jquery',
    'underscore',
    'model'
], function($, _, model) {

  $(document).ready(function() {
    var DecompositionModel = model.DecompositionModel;
    var Plottable = model.Plottable;

    // these variables are reused throughout this test suite
    var name, ids, coords, pct_var, md_headers, metadata;

    module('Decomposition Model', {
      setup: function() {
        // setup function
        var name = 'pcoa';
        this.data = {
          name: 'pcoa',
          sample_ids: ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354',
                       'PC.593', 'PC.355', 'PC.607', 'PC.634'],
          coordinates: [
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
          0.244448, -0.059883]],
          percents_explained: [26.6887048633, 16.2563704022, 13.7754129161,
                               11.217215823, 10.024774995, 8.22835130237,
                               7.55971173665, 6.24945796136],
          type: 'ordination',
          axes_names: []
        };
        this.md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                           'DOB'];
        this.metadata = [
        ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
        ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
        ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
        ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
        ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
        ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
        ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
        ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
        ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126']];
      },
      teardown: function() {
        // teardown function
        this.data = null;
        this.md_headers = null;
        this.metadata = null;
      }
    });

    /**
     *
     * Test that the Decomposition model object can be constructed without any
     * problems and check that the attributes are set correctly
     *
     */
    test('Test constructor', function(assert) {
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);

      equal(dm.type, 'scatter');
      equal(dm.abbreviatedName, 'pcoa', 'Abbreviated name set correctly');

      var exp = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
      10.024774995, 8.22835130237, 7.55971173665, 6.24945796136];
      deepEqual(dm.percExpl, exp, 'Percentage explained set correctly');

      exp = ['SampleID', 'LinkerPrimerSequence', 'Treatment', 'DOB'];
      deepEqual(dm.md_headers, exp, 'Metadata headers set correctly');

      exp = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354', 'PC.593',
      'PC.355', 'PC.607', 'PC.634'];
      deepEqual(dm.ids, exp, 'Ids set correctly');

      exp = [
        new Plottable(
            'PC.636',
            ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
            [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
            -0.229889, -0.046599],
            0),
        new Plottable(
            'PC.635',
            ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
            [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
            -0.112864, 0.064794],
            1),
        new Plottable(
            'PC.356',
            ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
            [0.228820, -0.130142, -0.287149, 0.086450, 0.044295, 0.206043,
            0.031000, 0.071992],
            2),
        new Plottable(
            'PC.481',
            ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
            [0.042263, -0.013968, 0.063531, -0.346121, -0.127814, 0.013935,
            0.030021, 0.140148],
            3),
        new Plottable(
            'PC.354',
            ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
            [0.280399, -0.006013, 0.023485, -0.046811, -0.146624, 0.005670,
            -0.035430, -0.255786],
            4),
        new Plottable(
            'PC.593',
            ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
            [0.232873, 0.139788, 0.322871, 0.183347, 0.020466, 0.054059,
            -0.036625, 0.099824],
            5),
        new Plottable(
            'PC.355',
            ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
            [0.170518, -0.194113, -0.030897, 0.019809, 0.155100, -0.279924,
            0.057609, 0.024248],
            6),
        new Plottable(
            'PC.607',
            ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
            [-0.091330, 0.424147, -0.135627, -0.057519, 0.151363, -0.025394,
            0.051731, -0.038738],
            7),
        new Plottable(
            'PC.634',
            ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126'],
            [-0.349339, -0.120788, 0.115275, 0.069495, -0.025372, 0.067853,
            0.244448, -0.059883],
            8)];
      deepEqual(dm.plottable, exp, 'Plottables set correctly');

      deepEqual(dm.dimensionRanges.min, [-0.349339, -0.194113, -0.287149,
                                         -0.346121, -0.247485, -0.279924,
                                         -0.229889, -0.255786]);
      deepEqual(dm.dimensionRanges.max, [0.280399, 0.424147, 0.322871,
                                         0.183347, 0.17607, 0.206043, 0.244448,
                                         0.140148]);

      equal(dm.length, 9, 'Length set correctly');
      deepEqual(dm.axesNames, ['pcoa 1', 'pcoa 2', 'pcoa 3', 'pcoa 4', 'pcoa 5',
                               'pcoa 6', 'pcoa 7', 'pcoa 8']);

      deepEqual(dm.edges, []);
    });

    test('Test add edges', function(assert) {
      this.data.edges = [['PC.607', 'PC.634'], ['PC.355', 'PC.634']];

      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata, 'scatter');

      // checking the names we assume the rest is fine
      equal(dm.edges[0][0].name, 'PC.607');
      equal(dm.edges[0][1].name, 'PC.634');
      equal(dm.edges[1][0].name, 'PC.355');
      equal(dm.edges[1][1].name, 'PC.634');
    });

    test('Test add edges error', function(assert) {
      this.data.edges = [['PC.607', 'PC.607'], ['PC.355', 'PC.634']];

      throws(function() {
            var dm = new DecompositionModel(this.data, this.md_headers,
                                            this.metadata, 'scatter');
          }, Error);
    });

    test('Test axesNames', function() {
      var names = ['PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PC 7',
                   'PC 8', 'PC 9'];
      this.data.axes_names = names;
      this.data.name = undefined;
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      deepEqual(dm.axesNames,
                ['PC 1', 'PC 2', 'PC 3', 'PC 4', 'PC 5', 'PC 6', 'PC 7',
                 'PC 8', 'PC 9'], 'Axes correctly renamed');
    });

    test('Test isArrowType', function(assert) {
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata, 'arrow');
      equal(dm.type, 'arrow');
      assert.ok(dm.isArrowType());
      assert.ok(dm.isScatterType() === false);
    });

    test('Test isScatterType', function(assert) {
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata, 'scatter');
      equal(dm.type, 'scatter');
      assert.ok(dm.isScatterType());
      assert.ok(dm.isArrowType() === false);
    });


    /**
     *
     * Test the initializer raises an error if the number of rows in coords is
     * not the same as the number of ids
     *
     */
    test('Test constructor excepts num rows coord != num ids', function() {
      var result;

      throws(
          function() {
            var err_coords = [
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
            this.data.coordinates = err_coords;
            result = new DecompositionModel(this.data, this.md_headers,
                                            this.metadata);
          },
          Error,
          'An error is raised if the number of rows in the coords parameter ' +
            'does not correspond to the number of ids'
            );
    });

    /**
     *
     * Test the initializer raises an error if all rows in coords does not have
     * the same number of elements
     *
     */
    test('Test constructor excepts rows in coord different lengths',
         function() {
      var result;

      throws(
          function() {
            var err_coords = [
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
            this.data.coordinates = err_coords;
            result = new DecompositionModel(this.data, this.md_headers,
                                            this.metadata);
          },
      Error,
      'An error is raised if all rows in coords does not have the same length'
        );
    });

    /**
     *
     * Test the initializer raises an error if the number of elements in
     * pct_var does not correspond to the number of coords.
     *
     */
    test('Test constructor excepts num pct_var != num coords', function() {
      var result;
      throws(
          function() {
            var err_pct_var = [26.6887048633, 16.2563704022, 13.7754129161,
            11.217215823, 10.024774995, 8.22835130237];
            this.data.percents_explained = err_pct_var;
            result = new DecompositionModel(this.data, this.md_headers,
                                            this.metadata);
          },
          Error,
          'An error is raised if the number of percentage explained does not ' +
          'correspond to the number of coords'
          );
    });

    /**
     *
     * Test the initializer raises an error if no coordinates are provided.
     *
     */
    test('Test constructor excepts when no coords are provided', function() {
      var result;
      throws(
          function() {
            this.data.coordinates = undefined;
            result = new DecompositionModel(this.data, this.md_headers,
                                            this.metadata);
          },
          Error,
          'An error is raised if no coordinates are provided'
          );
    });

    /**
     *
     * Test the initializer raises an error if the number of rows in metadata
     * is not the same as the number of ids
     *
     */
    test('Test constructor excepts num rows metadata != num ids', function() {
      var result;

      throws(
          function() {
            var err_metadata = [
              ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
              ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
              ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
              ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116']];
            result = new DecompositionModel(this.data, this.md_headers,
                                            err_metadata);
          },
          Error,
          'An error is raised if the number of rows in the metadata parameter' +
          ' does not correspond to the number of ids'
          );
    });

    /**
     *
     * Test the initializer raises an error if the number of columns in metadata
     * is not the same as the number of metadata headers
     *
     */
    test('Test constructor excepts metadata cols != num headers', function() {
      var result;

      throws(
          function() {
            err_metadata = [
              ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
              ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
              ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
              ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
              ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
              ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', '20080116'],
              ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
              ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
              ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126']];
            result = new DecompositionModel(this.data, this.md_headers,
                                            err_metadata);
          },
          Error,
          'An error is raised if the number of elements in each row in the ' +
          'metadata parameter does not match the number of metadata columns'
          );
    });

    /**
     *
     * Test hasConfidenceIntervals returns true
     *
     */
    test('Test hasConfidenceIntervals (true)', function() {
      this.data.ci = [[2, 1, 2, 0, 2, 2, 1, 1],
                      [0, 1, 1, 0, 0, 1, 2, 0],
                      [2, 1, 2, 1, 1, 1, 2, 0],
                      [2, 0, 2, 2, 0, 0, 0, 2],
                      [2, 1, 1, 0, 1, 2, 0, 2],
                      [0, 2, 2, 2, 1, 2, 2, 2],
                      [0, 0, 2, 0, 2, 0, 0, 2],
                      [1, 2, 0, 0, 2, 0, 0, 1],
                      [1, 0, 0, 1, 0, 0, 1, 1]];
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      equal(dm.hasConfidenceIntervals(), true);
    });

    /**
     *
     * Test hasConfidenceIntervals returns false
     *
     */
    test('Test hasConfidenceIntervals (false)', function() {
      this.data.ci = [];
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      equal(dm.hasConfidenceIntervals(), false);
    });

    /**
     *
     * Test getPlottableByID returns the correct plottable object
     *
     */
    test('Test getPlottableByID', function() {
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);

      var obs = dm.getPlottableByID('PC.636');
      var exp = new Plottable(
          'PC.636',
          ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
          [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
          -0.229889, -0.046599],
          0);

      deepEqual(obs, exp, 'Plottable retrieved successfully');

    });

    /**
     *
     * Test getPlottableByID throws an error if the id does not exist in the
     * DecompositionModel object
     *
     */
    test('Test getPlottableByID excepts unrecognized id', function() {
      var result;
      throws(
          function() {
            var dm = new DecompositionModel(this.data, this.md_headers,
                                            this.metadata);
            result = dm.getPlottableByID('Does_not_exist');
          },
          Error,
          'An error is raised if the id is not present in the Decomposition ' +
          'Model object'
          );
    });

    /**
     *
     * Test getPlottableByIDs returns the correct list of plottables
     *
     */
    test('Test getPlottableByIDs', function() {
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);

      var obs = dm.getPlottableByIDs(['PC.636', 'PC.354', 'PC.355']);
      var exp = [
        new Plottable(
            'PC.636',
            ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
            [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
            -0.229889, -0.046599],
            0),
        new Plottable(
            'PC.354',
            ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
            [0.280399, -0.006013, 0.023485, -0.046811, -0.146624, 0.005670,
            -0.035430, -0.255786],
            4),
        new Plottable(
            'PC.355',
            ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
            [0.170518, -0.194113, -0.030897, 0.019809, 0.155100, -0.279924,
            0.057609, 0.024248],
            6)];

      deepEqual(obs, exp, 'Plottable list retrieved successfully');
    });

    /**
     *
     * Test getPlottableByIDs throws an error if a passed id does not exist in
     * the DecompositionModel object
     *
     */

    test('Test getPlottableByIDs excepts unrecognized id', function() {
      var result;
      throws(
          function() {
            var dm = new DecompositionModel(this.data, this.md_headers,
                                            this.metadata);
            result = dm.getPlottableByIDs(['PC.636', 'PC.354',
                                           'Does_not_exist']);
          },
          Error,
          'An error is raised if one of the ids is not present in the ' +
          'Decomposition Model object'
          );
    });

    /**
     *
     * Test _getMetadataIndex returns the correct index of a category
     *
     */
    test('Test _getMetadataIndex', function() {
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      equal(dm._getMetadataIndex('Treatment'), 2,
          'Header index retrieved successfully');
    });

    /**
     *
     * Test _getMetadataIndex throws an error if the passed columns does not
     * exists in the DecompositionModel
     *
     */
    test('Test _getMetadataIndex excepts unrecognized header', function() {
      var result;
      throws(
          function() {
            var dm = new DecompositionModel(this.data, this.md_headers,
                                            this.metadata);
            result = dm._getMetadataIndex('Does_not_exist');
          },
          Error,
          'An error is raised if the metadata header does not exist in the ' +
          'Decomposition Model object'
          );
    });

    /**
     *
     * Test getPlottablesByMetadataCategoryValue retrieves all the plottables
     * with the metadata category value associated.
     *
     */
    test('Test getPlottablesByMetadataCategoryValue', function() {
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      var obs = dm.getPlottablesByMetadataCategoryValue('Treatment',
                                                        'Control');
      var exp = [
        new Plottable(
            'PC.636',
            ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
            [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
            -0.229889, -0.046599],
            0),
        new Plottable(
            'PC.354',
            ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
            [0.280399, -0.006013, 0.023485, -0.046811, -0.146624, 0.005670,
            -0.035430, -0.255786],
            4),
        new Plottable(
            'PC.355',
            ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
            [0.170518, -0.194113, -0.030897, 0.019809, 0.155100, -0.279924,
            0.057609, 0.024248],
            6),
        new Plottable(
            'PC.607',
            ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
            [-0.091330, 0.424147, -0.135627, -0.057519, 0.151363, -0.025394,
            0.051731, -0.038738],
            7),
        new Plottable(
            'PC.634',
            ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126'],
            [-0.349339, -0.120788, 0.115275, 0.069495, -0.025372, 0.067853,
            0.244448, -0.059883],
            8)];

      deepEqual(obs, exp,
          'Plottables for the given metadata category value retrieved ' +
          'successfully');
    });

    /**
     *
     * Test getPlottablesByMetadataCategoryValue throws an error if the
     * metadata header does not exist in the Decomposition Model object.
     *
     */
    test('Test getPlottablesByMetadataCategoryValue excepts unrecognized ' +
        'header', function() {
          var result;
          throws(
              function() {
                var dm = new DecompositionModel(this.data,
                                                this.md_headers,
                                                this.metadata);
                result = dm.getPlottablesByMetadataCategoryValue('foo',
                                                                 'Control');
              },
              Error,
              'An error is raised if the metadata header does not exist in ' +
              'the Decomposition Model object'
              );
        });

    /**
     *
     * Test getPlottablesByMetadataCategoryValue throws an error if the metadata
     * values is not found in the given category
     *
     */
    test('Tests getPlottablesByMetadataCategoryValue excepts unrecognized ' +
        'metadata category value', function() {
          var result;
          throws(
              function() {
                var dm = new DecompositionModel(this.data,
                                                this.md_headers,
                                                this.metadata);
                result = dm.getPlottablesByMetadataCategoryValue('Treatment',
                                                                 'foo');
              },
              Error,
              'An error is raised if the metadata category value does not ' +
              'exist in the Decomposition Model object'
              );
        });

    /**
     *
     * Test the function used to find minimum and maximum values works.
     *
     */
    test('Test the _minMaxReduce function', function() {
        var p = new Plottable('PC.635', ['PC.635', 'YATGCTGCCTCCCGTAGGAGT',
                              'Fast', '20071112'], [-0.237661, 0.046053,
                              -0.138136, 0.159061, -0.247485, -0.115211,
                              -0.112864, 0.064794], 1);
        var accumulator = {'min': [-5, -5, -5, -5, -5, -6, -0.01, -8],
                           'max': [0, 0, 0, 0, 0, 0, 0, 0]};

        var val = DecompositionModel._minMaxReduce(accumulator, p);

        deepEqual(val.min, [-5, -5, -5, -5, -5, -6, -0.112864, -8]);
        deepEqual(val.max, [0, 0.046053, 0, 0.159061, 0, 0, 0, 0.064794]);
    });

    /**
     *
     * Tests if a unique set of metadata category values can be obtained from a
     * metadata category of mixed types.
     *
     */
    test('Test getUniqueValuesByCategory mixed types', function() {
      var mixedValues = ['b', '-1', '3', '0', '-5', '100', 'b', 'a', 'A'];

      this.metadata = _.map(this.metadata, function(row, index) {
        row.push(mixedValues[index]);
        return row;
      });
      this.md_headers.push('Mixed');

      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      var obs = dm.getUniqueValuesByCategory('Mixed');
      var exp = ['a', 'A', 'b', '-5', '-1', '0', '3', '100'];

      deepEqual(obs, exp, 'Unique metadata values retrieved successfully');
    });

    /**
     *
     * Tests if a unique set of metadata category values can be obtained from a
     * metadata category
     *
     */
    test('Test getUniqueValuesByCategory', function() {
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      var obs = dm.getUniqueValuesByCategory('Treatment').sort();
      var exp = ['Control', 'Fast'];

      deepEqual(obs, exp, 'Unique metadata values retrieved successfully');
    });

    /**
     *
     * Tests getUniqueValuesByCategory throws an error if the metadata header
     * does not exists
     *
     */
    test('Test getUniqueValuesByCategory excepts unrecognized headers',
        function() {
          var result;
          throws(
              function() {
                var dm = new DecompositionModel(this.data,
                                                this.md_headers,
                                                this.metadata);
                result = dm.getUniqueValuesByCategory('Does_not_exist');
              },
              Error,
              'An error is raised if the metadata category value does not ' +
              'exist in the Decomposition Model object'
              );
        });

    /**
     *
     * Tests apply executes the provided function for all the plottables
     * in the decomposition object
     *
     */
    test('Test apply', function() {
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      var obs = dm.apply(function(pl) {return pl.name;});
      var exp = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354', 'PC.593',
      'PC.355', 'PC.607', 'PC.634'];
      deepEqual(obs, exp, 'Apply works as expected');
    });

    /**
     *
     * Test axes names are fixed appropriately.
     *
     */
    test('Fix axes names for scikit-bio', function() {
      this.data.axes_names = [0, 1, 2, 3, 4, 5, 6, 7, 8];
      var expected = ['pcoa 1', 'pcoa 2', 'pcoa 3', 'pcoa 4', 'pcoa 5',
                      'pcoa 6', 'pcoa 7', 'pcoa 8', 'pcoa 9'];
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      deepEqual(dm.axesNames, expected, 'Integer names replaced correctly');
    });

    /**
     *
     * Test axes names are fixed appropriately with custom axes.
     *
     */
    test('Fix axes names for scikit-bio (custom axes)', function() {
      this.data.axes_names = ['days', 'ph', 0, 1, 2, 3, 4, 5, 6];
      this.data.name = undefined;
      var expected = ['days', 'ph', 'Axis 1', 'Axis 2', 'Axis 3', 'Axis 4',
                      'Axis 5', 'Axis 6', 'Axis 7'];
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      deepEqual(dm.axesNames, expected, 'Custon axes fixed correctly');
    });

    /**
     *
     * Test axes names are not modified because they don't match scikit-bio
     *
     */
    test('Do not fix axes names for scikit-bio', function() {
      this.data.axes_names = ['days', 'ph', 0, 1, 20, 3, 4, 5, 6];
      var expected = ['days', 'ph', 0, 1, 20, 3, 4, 5, 6];
      var dm = new DecompositionModel(this.data, this.md_headers,
                                      this.metadata);
      deepEqual(dm.axesNames, expected, 'No changes are made');
    });

    /**
     *
     * Tests the toString method
     *
     */
    test('Test toString', function() {
      var data = {sample_ids: ['samp1', 'samp2'],
                  coordinates: [[1, 2, 3], [4, 5, 6]],
                  percents_explained: [0.5, 0.4, 0.1],
                  name: 'pcoa'};
      var _md_headers = ['foo1', 'foo2', 'foo3'];
      var _metadata = [['a', 'b', 'c'], ['d', 'f', 'g']];
      var dm = new DecompositionModel(data, _md_headers, _metadata);
      var exp = 'name: pcoa\n' +
        'Metadata headers: [foo1, foo2, foo3]\n' +
        'Plottables:\n' +
        'Sample: samp1 located at: (1, 2, 3) ' +
        'metadata: [a, b, c] at index: 0 and without confidence intervals.\n' +
        'Sample: samp2 located at: (4, 5, 6) ' +
        'metadata: [d, f, g] at index: 1 and without confidence intervals.';

      equal(dm.toString(), exp,
          'Test correctly converted DecompositionModel to string type');

    });

  });

});
