requirejs(['underscore', 'ui', 'util'], function(_, buildColorSelectorTable, util) {
  $(document).ready(function() {
    var cleanHTML = util.cleanHTML, convertXMLToString = util.convertXMLToString;

    // these variables are reused throughout this test suite
    var mappingFileHeaders, mappingFileData, coordinatesData;
    var sampleNames, gradientPoints, coordinates;

    // these are expected results needed for multiple tests
    var crunchedDataTwoCategories, crunchedDataOneCategory;

    module('User Interface', {

      setup: function() {
        // setup function
        mappingFileHeaders = ['SampleID', 'LinkerPrimerSequence', 'Treatment', 'DOB'];
        mappingFileData = { 'PC.481': ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'], 'PC.607': ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'], 'PC.634': ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'], 'PC.635': ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'], 'PC.593': ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'], 'PC.636': ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'], 'PC.355': ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'], 'PC.354': ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'], 'PC.356': ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126'] };
        coordinatesData = new Array();
        coordinatesData['PC.636'] = { 'name': 'PC.636', 'color': 0, 'x': -0.276542, 'y': -0.144964, 'z': 0.066647, 'P1': -0.276542, 'P2': -0.144964, 'P3': 0.066647, 'P4': -0.067711, 'P5': 0.176070, 'P6': 0.072969, 'P7': -0.229889, 'P8': -0.046599 };
        coordinatesData['PC.635'] = { 'name': 'PC.635', 'color': 0, 'x': -0.237661, 'y': 0.046053, 'z': -0.138136, 'P1': -0.237661, 'P2': 0.046053, 'P3': -0.138136, 'P4': 0.159061, 'P5': -0.247485, 'P6': -0.115211, 'P7': -0.112864, 'P8': 0.064794 };
        coordinatesData['PC.356'] = { 'name': 'PC.356', 'color': 0, 'x': 0.228820, 'y': -0.130142, 'z': -0.287149, 'P1': 0.228820, 'P2': -0.130142, 'P3': -0.287149, 'P4': 0.086450, 'P5': 0.044295, 'P6': 0.206043, 'P7': 0.031000, 'P8': 0.071992 };
        coordinatesData['PC.481'] = { 'name': 'PC.481', 'color': 0, 'x': 0.042263, 'y': -0.013968, 'z': 0.063531, 'P1': 0.042263, 'P2': -0.013968, 'P3': 0.063531, 'P4': -0.346121, 'P5': -0.127814, 'P6': 0.013935, 'P7': 0.030021, 'P8': 0.140148 };
        coordinatesData['PC.354'] = { 'name': 'PC.354', 'color': 0, 'x': 0.280399, 'y': -0.006013, 'z': 0.023485, 'P1': 0.280399, 'P2': -0.006013, 'P3': 0.023485, 'P4': -0.046811, 'P5': -0.146624, 'P6': 0.005670, 'P7': -0.035430, 'P8': -0.255786 };
        coordinatesData['PC.593'] = { 'name': 'PC.593', 'color': 0, 'x': 0.232873, 'y': 0.139788, 'z': 0.322871, 'P1': 0.232873, 'P2': 0.139788, 'P3': 0.322871, 'P4': 0.183347, 'P5': 0.020466, 'P6': 0.054059, 'P7': -0.036625, 'P8': 0.099824 };
        coordinatesData['PC.355'] = { 'name': 'PC.355', 'color': 0, 'x': 0.170518, 'y': -0.194113, 'z': -0.030897, 'P1': 0.170518, 'P2': -0.194113, 'P3': -0.030897, 'P4': 0.019809, 'P5': 0.155100, 'P6': -0.279924, 'P7': 0.057609, 'P8': 0.024248 };
        coordinatesData['PC.607'] = { 'name': 'PC.607', 'color': 0, 'x': -0.091330, 'y': 0.424147, 'z': -0.135627, 'P1': -0.091330, 'P2': 0.424147, 'P3': -0.135627, 'P4': -0.057519, 'P5': 0.151363, 'P6': -0.025394, 'P7': 0.051731, 'P8': -0.038738 };
        coordinatesData['PC.634'] = { 'name': 'PC.634', 'color': 0, 'x': -0.349339, 'y': -0.120788, 'z': 0.115275, 'P1': -0.349339, 'P2': -0.120788, 'P3': 0.115275, 'P4': 0.069495, 'P5': -0.025372, 'P6': 0.067853, 'P7': 0.244448, 'P8': -0.059883 };

        sampleNames = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354'];

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
     * Test the table construction is made correctly.
     *
     */
    test('Test color manager table construction with no extra parameters',
        function() {
          var table, crawfordTable;
          crawfordTable = '<table class=\"emperor-tab-table\"><tbody><tr><td><d' +
            'iv id=\"row-0-column-0\" class=\"colorbox\" name=\"PC.354\"></div></' +
            'td><td title=\"PC.354\">PC.354</td></tr><tr><td><div id=\"row-1-colu' +
            'mn-0\" class=\"colorbox\" name=\"PC.355\"></div></td><td title=\"PC.' +
            '355\">PC.355</td></tr><tr><td><div id=\"row-2-column-0\" class=\"col' +
            'orbox\" name=\"PC.356\"></div></td><td title=\"PC.356\">PC.356</td><' +
            '/tr><tr><td><div id=\"row-3-column-0\" class=\"colorbox\" name=\"PC.' +
            '481\"></div></td><td title=\"PC.481\">PC.481</td></tr><tr><td><div i' +
            'd=\"row-4-column-0\" class=\"colorbox\" name=\"PC.593\"></div></td><' +
            'td title=\"PC.593\">PC.593</td></tr><tr><td><div id=\"row-5-column-0' +
            '\" class=\"colorbox\" name=\"PC.607\"></div></td><td title=\"PC.607' +
            '\">PC.607</td></tr><tr><td><div id=\"row-6-column-0\" class=\"colorbo' +
            'x\" name=\"PC.634\"></div></td><td title=\"PC.634\">PC.634</td></tr>' +
            '<tr><td><div id=\"row-7-column-0\" class=\"colorbox\" name=\"PC.635' +
            '\"></div></td><td title=\"PC.635\">PC.635</td></tr><tr><td><div id=\"' +
            'row-8-column-0\" class=\"colorbox\" name=\"PC.636\"></div></td><td t' +
            'itle=\"PC.636\">PC.636</td></tr></tbody></table>';
            table = buildColorSelectorTable(mappingFileHeaders, mappingFileData,
                'SampleID');
          equal(cleanHTML(convertXMLToString(table)), cleanHTML(crawfordTable));
        }
    );

    /**
     *
     * Test the table construction is made correctly with an identifier.
     *
     */
    test('Test color manager table construction with an extra parameter',
        function() {
          var table, crawfordTable;
          crawfordTable = '<table class=\"emperor-tab-table\"><tbody><tr><td><d' +
            'iv id=\"foo-row-0-column-0\" class=\"colorbox\" name=\"PC.354\"></di' +
            'v></td><td title=\"PC.354\">PC.354</td></tr><tr><td><div id=\"foo-ro' +
            'w-1-column-0\" class=\"colorbox\" name=\"PC.355\"></div></td><td tit' +
            'le=\"PC.355\">PC.355</td></tr><tr><td><div id=\"foo-row-2-column-0\"' +
            ' class=\"colorbox\" name=\"PC.356\"></div></td><td title=\"PC.356\">P' +
            'C.356</td></tr><tr><td><div id=\"foo-row-3-column-0\" class=\"colorb' +
            'ox\" name=\"PC.481\"></div></td><td title=\"PC.481\">PC.481</td></tr' +
            '><tr><td><div id=\"foo-row-4-column-0\" class=\"colorbox\" name=\"PC' +
            '.593\"></div></td><td title=\"PC.593\">PC.593</td></tr><tr><td><div ' +
            'id=\"foo-row-5-column-0\" class=\"colorbox\" name=\"PC.607\"></div><' +
            '/td><td title=\"PC.607\">PC.607</td></tr><tr><td><div id=\"foo-row-6' +
            '-column-0\" class=\"colorbox\" name=\"PC.634\"></div></td><td title=' +
            '\"PC.634\">PC.634</td></tr><tr><td><div id=\"foo-row-7-column-0\" cl' +
            'ass=\"colorbox\" name=\"PC.635\"></div></td><td title=\"PC.635\">PC.' +
            '635</td></tr><tr><td><div id=\"foo-row-8-column-0\" class=\"colorbox' +
            '\" name=\"PC.636\"></div></td><td title=\"PC.636\">PC.636</td></tr><' +
            '/tbody></table>';
            table = buildColorSelectorTable(mappingFileHeaders, mappingFileData,
                'SampleID', 'foo');
          equal(cleanHTML(convertXMLToString(table)), cleanHTML(crawfordTable));
        }
    );

    /**
     *
     * Test the trajectory object raises the appropriate errors when constructing
     * with bad arguments.
     *
     */
    test('Test color manager table exceptions', function() {
      var result;

      // check this happens for all the properties
      throws(
          function() {
            result = buildColorSelectorTable(mappingFileHeaders, mappingFileData,
                'FOO', false);
          },
          Error,
          'An error is raised if the selected category does not exist in the ' +
          'mapping file'
          );
    });

  });
});
