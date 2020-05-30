requirejs([
    'jquery',
    'underscore',
    'chroma',
    'model',
    'view',
    'viewcontroller',
    'slickgrid',
    'colorviewcontroller',
    'multi-model',
    'uistate'
], function($, _, chroma, model, DecompositionView, viewcontroller, SlickGrid,
            ColorViewController, MultiModel, UIState) {
  $(document).ready(function() {
    var EmperorAttributeABC = viewcontroller.EmperorAttributeABC;
    var DecompositionModel = model.DecompositionModel;
    var Plottable = model.Plottable;

    module('ColorViewController', {
      setup: function() {
        this.sharedDecompositionViewDict = {};

        var UIState1 = new UIState();
        var UIState2 = new UIState();

        // setup function
        var data = {name: 'pcoa', sample_ids: ['PC.636', 'PC.635', 'PC.634'],
                    coordinates: [[-0.276542, -0.144964, 0.066647, -0.067711,
                                   0.176070, 0.072969,
                                   -0.229889, -0.046599],
                                  [-0.237661, 0.046053, -0.138136, 0.159061,
                                   -0.247485, -0.115211, -0.112864, 0.064794],
                                  [-0.237661, 0.046053, -0.138136, 0.159061,
                                    -0.247485, -0.115211, -0.112864, 0.064794]
                    ],
                    percents_explained: [26.6887048633, 16.2563704022,
                                         13.7754129161, 11.217215823,
                                         10.024774995, 8.22835130237,
                                         7.55971173665, 6.24945796136]};
        md_headers = ['SampleID', 'Mixed', 'Treatment', 'DOB'];
        metadata = [['PC.636', '14.2', 'Control', '20070314'],
        ['PC.635', 'StringValue', 'Fast', '20071112'],
        ['PC.634', '14.7', 'Fast', '20071112']];
        decomp = new DecompositionModel(data, md_headers, metadata);
        var multiModel = new MultiModel({'scatter': decomp});
        var dv = new DecompositionView(multiModel, 'scatter', UIState1);
        this.sharedDecompositionViewDict.scatter = dv;

        data = {name: 'biplot', sample_ids: ['tax_1', 'tax_2'],
                coordinates: [[-1, -0.144964, 0.066647, -0.067711, 0.176070,
                               0.072969, -0.229889, -0.046599],
                              [-0.237661, 0.046053, -0.138136, 0.159061,
                               -0.247485, -0.115211, -0.112864, 0.064794]],
                percents_explained: [26.6887048633, 16.2563704022,
                                     13.7754129161, 11.217215823, 10.024774995,
                                     8.22835130237, 7.55971173665,
                                     6.24945796136]};
        md_headers = ['SampleID', 'Gram'];
        metadata = [['tax_1', '1'],
        ['tax_2', '0']];
        this.decomp = new DecompositionModel(data, md_headers, metadata);
        this.multiModel = new MultiModel({'scatter': this.decomp});
        this.dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
        this.sharedDecompositionViewDict.biplot = dv;

        // jackknifed specific
        data = {name: 'pcoa', sample_ids: ['PC.636', 'PC.635', 'PC.634'],
                coordinates: [[-0.276542, -0.144964, 0.066647, -0.067711,
                               0.176070, 0.072969, -0.229889, -0.046599],
                              [-0.237661, 0.046053, -0.138136, 0.159061,
                               -0.247485, -0.115211, -0.112864, 0.064794],
                              [-0.237661, 0.046053, -0.138136, 0.159061,
                                -0.247485, -0.115211, -0.112864, 0.064794]
                ],
                percents_explained: [26.6887048633, 16.2563704022,
                                     13.7754129161, 11.217215823,
                                     10.024774995, 8.22835130237,
                                     7.55971173665, 6.24945796136],
                ci: [[0.5, 0.68, -1.64, 0.56, 1.87, 0.75, 0.61, 1.14],
                     [0.09, 0.8, -0.07, -1.52, 0.86, -0.2, -2.63, -0.57],
                     [0.21, -0.85, 0.19, -1.88, -1.19, -1.38, 1.55, -0.1]]
        };
        md_headers = ['SampleID', 'Mixed', 'Treatment', 'DOB'];
        metadata = [['PC.636', '14.2', 'Control', '20070314'],
        ['PC.635', 'StringValue', 'Fast', '20071112'],
        ['PC.634', '14.7', 'Fast', '20071112']];
        decomp = new DecompositionModel(data, md_headers, metadata);
        multiModel = new MultiModel({'scatter': decomp});
        this.jackknifedDecView = new DecompositionView(multiModel,
                                                       'scatter',
                                                       UIState2);
      },
      teardown: function() {
        this.sharedDecompositionViewDict = undefined;
        this.jackknifedDecView = undefined;
        $('#fooligans').remove();
        this.decomp = undefined;
        this.multiModel = undefined;
      }
    });

    test('Constructor tests', function(assert) {
      var container = $('<div id="no-exist" style="height:11px; ' +
                        'width:12px"></div>');

      assert.ok(ColorViewController.prototype instanceof EmperorAttributeABC);

      var controller = new ColorViewController(new UIState(),
        container, this.sharedDecompositionViewDict);
      equal(controller.title, 'Color');

      var testColumn = controller.bodyGrid.getColumns()[0];
      equal(testColumn.field, 'value');

      // verify the color value is set properly
      equal(controller.$colormapSelect.val(), 'discrete-coloring-qiime');
      equal(controller.$select.val(), null);
      equal(controller.$searchBar.val(), '');
      equal(controller.$searchBar.is(':hidden'), true);

      equal(controller.$colormapSelect.is(':disabled'), true);
      equal(controller.$scaled.is(':disabled'), true);
    });

    test('Is coloring continuous', function() {
      var container = $('<div id="no-exist" style="height:11px; ' +
                        'width:12px"></div>');

      var controller = new ColorViewController(new UIState(),
        container, this.sharedDecompositionViewDict);

      equal(controller.title, 'Color');

      equal(controller.isColoringContinuous(), false);

      controller.setMetadataField('Mixed');
      controller.$colormapSelect.val('Viridis').trigger('chosen:updated');
      controller.$scaled.prop('checked', true).trigger('change');
      equal(controller.$searchBar.is(':hidden'), true);

      equal(controller.isColoringContinuous(), true);

      controller.setMetadataField('DOB');
      controller.$colormapSelect.val('Dark2').trigger('chosen:updated');
      controller.$scaled.prop('checked', false).trigger('change');
      equal(controller.$searchBar.is(':hidden'), true);

      equal(controller.isColoringContinuous(), false);
    });

    test('Test _nonNumericPlottables', function() {
      var container = $('<div id="no-exist" style="height:11px; ' +
                        'width:12px"></div>');
      var controller = new ColorViewController(new UIState(),
        container, this.sharedDecompositionViewDict);
      controller.setMetadataField('DOB');
      var decompViewDict = controller.getView();

      var colors = {'14.7': '#f7fbff',
                    '14.2': '#f3f8fd',
                    'StringValue': '#e8f2fd'};
      var data = decompViewDict.setCategory(
        colors, ColorViewController.prototype.setPlottableAttributes, 'Mixed');
      var uniqueVars = ['14.7', '14.2', 'StringValue'];

      // Test all are string
      ColorViewController._nonNumericPlottables(uniqueVars, data);
      var plottables = ColorViewController._nonNumericPlottables(uniqueVars,
                                                                 data);
      var exp = [
        new Plottable(
            'PC.635',
            ['PC.635', 'StringValue', 'Fast', '20071112'],
            [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
            -0.112864, 0.064794],
            1)
        ];
      deepEqual(plottables, exp);

      // Test all are numeric
      var colors = {'20070314': '#f7fbff', '20071112': '#f3f8fd'};
      var data = decompViewDict.setCategory(
        colors, ColorViewController.prototype.setPlottableAttributes, 'DOB');
      var uniqueVars = ['20070314', '20071112'];
      var plottables = ColorViewController._nonNumericPlottables(uniqueVars,
                                                                 data);
      deepEqual(plottables, []);
    });

    test('Test discrete colors are retrieved correctly', function() {
      deepEqual(ColorViewController.getDiscreteColors([0, 1, 2]),
                {0: '#ff0000', 1: '#0000ff', 2: '#f27304'});
    });

    test('Test discrete colors are retrieved on roll-over', function() {
      var fifteen = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
      var obs = ColorViewController.getDiscreteColors(fifteen, 'Pastel1');
      var exp = {'0': '#fbb4ae', '1': '#b3cde3', '2': '#ccebc5',
                 '3': '#decbe4', '4': '#fed9a6', '5': '#ffffcc',
                 '6': '#e5d8bd', '7': '#fddaec', '8': '#f2f2f2',
                 '9': '#fbb4ae', '10': '#b3cde3', '11': '#ccebc5',
                 '12': '#decbe4', '13': '#fed9a6', '14': '#ffffcc'};
      deepEqual(obs, exp);
    });

    test('Test discrete colors with other maps', function() {
      deepEqual(ColorViewController.getDiscreteColors([0], 'Set1'),
                {0: '#e41a1c'});
    });


    test('Test getScaledColors', function() {
      var five = ['0', '1', '2', '3', '4'];
      var color = ColorViewController.getScaledColors(five, 'Viridis');
      deepEqual(color, [{0: '#440154', 1: '#3f4a8a', 2: '#26838f',
                         3: '#6cce5a', 4: '#fee825'},
        '<defs><linearGradient id="Gradient" x1="0" x2="0" y1="1" y2="0">' +
        '<stop offset="0%" stop-color="#440154"/>' +
        '<stop offset="1%" stop-color="#440457"/>' +
        '<stop offset="2%" stop-color="#45075a"/>' +
        '<stop offset="3%" stop-color="#450a5c"/>' +
        '<stop offset="4%" stop-color="#450d5f"/>' +
        '<stop offset="5%" stop-color="#461062"/>' +
        '<stop offset="6%" stop-color="#461365"/>' +
        '<stop offset="7%" stop-color="#461668"/>' +
        '<stop offset="8%" stop-color="#47196a"/>' +
        '<stop offset="9%" stop-color="#471c6d"/>' +
        '<stop offset="10%" stop-color="#471f70"/>' +
        '<stop offset="11%" stop-color="#482273"/>' +
        '<stop offset="12%" stop-color="#482576"/>' +
        '<stop offset="13%" stop-color="#482878"/>' +
        '<stop offset="14%" stop-color="#472b79"/>' +
        '<stop offset="15%" stop-color="#462e7b"/>' +
        '<stop offset="16%" stop-color="#45317c"/>' +
        '<stop offset="17%" stop-color="#45347e"/>' +
        '<stop offset="18%" stop-color="#44367f"/>' +
        '<stop offset="19%" stop-color="#433981"/>' +
        '<stop offset="20%" stop-color="#433c82"/>' +
        '<stop offset="21%" stop-color="#423f84"/>' +
        '<stop offset="22%" stop-color="#414285"/>' +
        '<stop offset="23%" stop-color="#404487"/>' +
        '<stop offset="24%" stop-color="#404788"/>' +
        '<stop offset="25%" stop-color="#3f4a8a"/>' +
        '<stop offset="26%" stop-color="#3e4c8a"/>' +
        '<stop offset="27%" stop-color="#3d4f8b"/>' +
        '<stop offset="28%" stop-color="#3c518b"/>' +
        '<stop offset="29%" stop-color="#3b538b"/>' +
        '<stop offset="30%" stop-color="#39568c"/>' +
        '<stop offset="31%" stop-color="#38588c"/>' +
        '<stop offset="32%" stop-color="#375a8c"/>' +
        '<stop offset="33%" stop-color="#365d8d"/>' +
        '<stop offset="34%" stop-color="#355f8d"/>' +
        '<stop offset="35%" stop-color="#34618d"/>' +
        '<stop offset="36%" stop-color="#33648e"/>' +
        '<stop offset="37%" stop-color="#32668e"/>' +
        '<stop offset="38%" stop-color="#31688e"/>' +
        '<stop offset="39%" stop-color="#306a8e"/>' +
        '<stop offset="40%" stop-color="#2f6d8e"/>' +
        '<stop offset="41%" stop-color="#2e6f8e"/>' +
        '<stop offset="42%" stop-color="#2d718e"/>' +
        '<stop offset="43%" stop-color="#2c738e"/>' +
        '<stop offset="44%" stop-color="#2b768f"/>' +
        '<stop offset="45%" stop-color="#2a788f"/>' +
        '<stop offset="46%" stop-color="#2a7a8f"/>' +
        '<stop offset="47%" stop-color="#297c8f"/>' +
        '<stop offset="48%" stop-color="#287f8f"/>' +
        '<stop offset="49%" stop-color="#27818f"/>' +
        '<stop offset="50%" stop-color="#26838f"/>' +
        '<stop offset="51%" stop-color="#25858f"/>' +
        '<stop offset="52%" stop-color="#25878e"/>' +
        '<stop offset="53%" stop-color="#24898e"/>' +
        '<stop offset="54%" stop-color="#248b8d"/>' +
        '<stop offset="55%" stop-color="#238d8d"/>' +
        '<stop offset="56%" stop-color="#238f8d"/>' +
        '<stop offset="57%" stop-color="#22928c"/>' +
        '<stop offset="58%" stop-color="#22948c"/>' +
        '<stop offset="59%" stop-color="#21968b"/>' +
        '<stop offset="60%" stop-color="#20988b"/>' +
        '<stop offset="61%" stop-color="#209a8b"/>' +
        '<stop offset="62%" stop-color="#1f9c8a"/>' +
        '<stop offset="63%" stop-color="#229f88"/>' +
        '<stop offset="64%" stop-color="#28a384"/>' +
        '<stop offset="65%" stop-color="#2ea780"/>' +
        '<stop offset="66%" stop-color="#35ab7d"/>' +
        '<stop offset="67%" stop-color="#3baf79"/>' +
        '<stop offset="68%" stop-color="#41b375"/>' +
        '<stop offset="69%" stop-color="#47b671"/>' +
        '<stop offset="70%" stop-color="#4dba6d"/>' +
        '<stop offset="71%" stop-color="#53be69"/>' +
        '<stop offset="72%" stop-color="#5ac266"/>' +
        '<stop offset="73%" stop-color="#60c662"/>' +
        '<stop offset="74%" stop-color="#66ca5e"/>' +
        '<stop offset="75%" stop-color="#6cce5a"/>' +
        '<stop offset="76%" stop-color="#72cf56"/>' +
        '<stop offset="77%" stop-color="#78d152"/>' +
        '<stop offset="78%" stop-color="#7ed24f"/>' +
        '<stop offset="79%" stop-color="#84d34b"/>' +
        '<stop offset="80%" stop-color="#8ad447"/>' +
        '<stop offset="81%" stop-color="#90d643"/>' +
        '<stop offset="82%" stop-color="#95d740"/>' +
        '<stop offset="83%" stop-color="#9bd83c"/>' +
        '<stop offset="84%" stop-color="#a1da38"/>' +
        '<stop offset="85%" stop-color="#a7db34"/>' +
        '<stop offset="86%" stop-color="#addc31"/>' +
        '<stop offset="87%" stop-color="#b3dd2d"/>' +
        '<stop offset="88%" stop-color="#b9de2b"/>' +
        '<stop offset="89%" stop-color="#bfdf2a"/>' +
        '<stop offset="90%" stop-color="#c4e02a"/>' +
        '<stop offset="91%" stop-color="#cae129"/>' +
        '<stop offset="92%" stop-color="#d0e229"/>' +
        '<stop offset="93%" stop-color="#d6e228"/>' +
        '<stop offset="94%" stop-color="#dbe328"/>' +
        '<stop offset="95%" stop-color="#e1e427"/>' +
        '<stop offset="96%" stop-color="#e7e527"/>' +
        '<stop offset="97%" stop-color="#ede626"/>' +
        '<stop offset="98%" stop-color="#f2e626"/>' +
        '<stop offset="99%" stop-color="#f8e725"/></linearGradient></defs>' +
        '<rect id="gradientRect" width="20" height="95%" ' +
        'fill="url(#Gradient)"/><text x="25" y="12px" ' +
        'font-family="sans-serif" font-size="12px" text-anchor="start">4' +
        '</text><text x="25" y="50%" font-family="sans-serif" ' +
        'font-size="12px" text-anchor="start">2</text><text x="25" y="95%" ' +
        'font-family="sans-serif" font-size="12px" text-anchor="start">0</text>'
      ]);
    });

    test('Test getInterpolatedColors', function() {
      var five = ['0', '1', '2', '3', '4'];
      var color = ColorViewController.getInterpolatedColors(five, 'Viridis');
      deepEqual(color, {
        '0': '#440154', '1': '#3f4a8a', '2': '#26838f', '3': '#6cce5a',
        '4': '#fee825'
      });
    });

    test('Test ColorViewController.getScaledColors exceptions', function() {
      var five = ['0', 'string1', 'string2', 'string3', 'string4'];

      throws(
          function() {
            var color = ColorViewController.getScaledColors(five, 'Viridis');
          },
          Error,
          'An error is raised if there are not 2+ numeric values'
          );
    });

    test('Test ColorViewController.getColorList works', function() {
      var one, five, ten, twenty, scaled, colors;

      one = [0];
      five = [0, 1, 2, 3, 4];
      ten = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
      twenty = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                18, 19];
      scaled = [0, 1, 2, 3, 7, 20, 50];

      colors = ColorViewController.getColorList(scaled, 'Blues', false, true);
      deepEqual(colors[0], {'0': '#f7fbff', '1': '#f3f8fe', '2': '#eff6fc',
                            '20': '#94c4df', '3': '#ebf3fb', '50': '#08306b',
                            '7': '#dbe9f6'});
      equal(colors[1],
        '<defs><linearGradient id="Gradient" x1="0" x2="0" y1="1" y2="0">' +
        '<stop offset="0%" stop-color="#f7fbff"/>' +
        '<stop offset="1%" stop-color="#f5fafe"/>' +
        '<stop offset="2%" stop-color="#f3f8fe"/>' +
        '<stop offset="3%" stop-color="#f1f7fd"/>' +
        '<stop offset="4%" stop-color="#eff6fc"/>' +
        '<stop offset="5%" stop-color="#edf5fc"/>' +
        '<stop offset="6%" stop-color="#ebf3fb"/>' +
        '<stop offset="7%" stop-color="#e9f2fb"/>' +
        '<stop offset="8%" stop-color="#e7f1fa"/>' +
        '<stop offset="9%" stop-color="#e5eff9"/>' +
        '<stop offset="10%" stop-color="#e3eef9"/>' +
        '<stop offset="11%" stop-color="#e1edf8"/>' +
        '<stop offset="12%" stop-color="#dfecf7"/>' +
        '<stop offset="13%" stop-color="#ddeaf7"/>' +
        '<stop offset="14%" stop-color="#dbe9f6"/>' +
        '<stop offset="15%" stop-color="#d9e8f5"/>' +
        '<stop offset="16%" stop-color="#d7e7f5"/>' +
        '<stop offset="17%" stop-color="#d5e5f4"/>' +
        '<stop offset="18%" stop-color="#d3e4f3"/>' +
        '<stop offset="19%" stop-color="#d2e3f3"/>' +
        '<stop offset="20%" stop-color="#d0e1f2"/>' +
        '<stop offset="21%" stop-color="#cee0f2"/>' +
        '<stop offset="22%" stop-color="#ccdff1"/>' +
        '<stop offset="23%" stop-color="#cadef0"/>' +
        '<stop offset="24%" stop-color="#c8dcf0"/>' +
        '<stop offset="25%" stop-color="#c6dbef"/>' +
        '<stop offset="26%" stop-color="#c3daee"/>' +
        '<stop offset="27%" stop-color="#c0d8ed"/>' +
        '<stop offset="28%" stop-color="#bcd7ec"/>' +
        '<stop offset="29%" stop-color="#b9d6eb"/>' +
        '<stop offset="30%" stop-color="#b6d4e9"/>' +
        '<stop offset="31%" stop-color="#b3d3e8"/>' +
        '<stop offset="32%" stop-color="#b0d1e7"/>' +
        '<stop offset="33%" stop-color="#acd0e6"/>' +
        '<stop offset="34%" stop-color="#a9cfe5"/>' +
        '<stop offset="35%" stop-color="#a6cde4"/>' +
        '<stop offset="36%" stop-color="#a3cce3"/>' +
        '<stop offset="37%" stop-color="#a0cbe2"/>' +
        '<stop offset="38%" stop-color="#9cc9e1"/>' +
        '<stop offset="39%" stop-color="#98c7e0"/>' +
        '<stop offset="40%" stop-color="#94c4df"/>' +
        '<stop offset="41%" stop-color="#90c2de"/>' +
        '<stop offset="42%" stop-color="#8cc0dd"/>' +
        '<stop offset="43%" stop-color="#88bedc"/>' +
        '<stop offset="44%" stop-color="#83bbdb"/>' +
        '<stop offset="45%" stop-color="#7fb9da"/>' +
        '<stop offset="46%" stop-color="#7bb7da"/>' +
        '<stop offset="47%" stop-color="#77b5d9"/>' +
        '<stop offset="48%" stop-color="#73b2d8"/>' +
        '<stop offset="49%" stop-color="#6fb0d7"/>' +
        '<stop offset="50%" stop-color="#6baed6"/>' +
        '<stop offset="51%" stop-color="#68acd5"/>' +
        '<stop offset="52%" stop-color="#64aad3"/>' +
        '<stop offset="53%" stop-color="#61a7d2"/>' +
        '<stop offset="54%" stop-color="#5ea5d1"/>' +
        '<stop offset="55%" stop-color="#5ba3d0"/>' +
        '<stop offset="56%" stop-color="#57a1ce"/>' +
        '<stop offset="57%" stop-color="#549ecd"/>' +
        '<stop offset="58%" stop-color="#519ccc"/>' +
        '<stop offset="59%" stop-color="#4d9aca"/>' +
        '<stop offset="60%" stop-color="#4a98c9"/>' +
        '<stop offset="61%" stop-color="#4795c8"/>' +
        '<stop offset="62%" stop-color="#4493c7"/>' +
        '<stop offset="63%" stop-color="#4191c5"/>' +
        '<stop offset="64%" stop-color="#3e8ec4"/>' +
        '<stop offset="65%" stop-color="#3b8bc3"/>' +
        '<stop offset="66%" stop-color="#3989c1"/>' +
        '<stop offset="67%" stop-color="#3686c0"/>' +
        '<stop offset="68%" stop-color="#3383bf"/>' +
        '<stop offset="69%" stop-color="#3181bd"/>' +
        '<stop offset="70%" stop-color="#2e7ebc"/>' +
        '<stop offset="71%" stop-color="#2c7cba"/>' +
        '<stop offset="72%" stop-color="#2979b9"/>' +
        '<stop offset="73%" stop-color="#2676b8"/>' +
        '<stop offset="74%" stop-color="#2474b6"/>' +
        '<stop offset="75%" stop-color="#2171b5"/>' +
        '<stop offset="76%" stop-color="#1f6eb3"/>' +
        '<stop offset="77%" stop-color="#1d6cb1"/>' +
        '<stop offset="78%" stop-color="#1b69af"/>' +
        '<stop offset="79%" stop-color="#1967ad"/>' +
        '<stop offset="80%" stop-color="#1764ab"/>' +
        '<stop offset="81%" stop-color="#1562a9"/>' +
        '<stop offset="82%" stop-color="#135fa7"/>' +
        '<stop offset="83%" stop-color="#115da5"/>' +
        '<stop offset="84%" stop-color="#0f5aa3"/>' +
        '<stop offset="85%" stop-color="#0d57a1"/>' +
        '<stop offset="86%" stop-color="#0b559f"/>' +
        '<stop offset="87%" stop-color="#09529d"/>' +
        '<stop offset="88%" stop-color="#08509a"/>' +
        '<stop offset="89%" stop-color="#084d96"/>' +
        '<stop offset="90%" stop-color="#084a92"/>' +
        '<stop offset="91%" stop-color="#08488e"/>' +
        '<stop offset="92%" stop-color="#08458a"/>' +
        '<stop offset="93%" stop-color="#084286"/>' +
        '<stop offset="94%" stop-color="#084083"/>' +
        '<stop offset="95%" stop-color="#083d7f"/>' +
        '<stop offset="96%" stop-color="#083b7b"/>' +
        '<stop offset="97%" stop-color="#083877"/>' +
        '<stop offset="98%" stop-color="#083573"/>' +
        '<stop offset="99%" stop-color="#08336f"/>' +
        '<stop offset="100%" stop-color="#08306b"/></linearGradient></defs>' +
        '<rect id="gradientRect" width="20" height="95%" ' +
        'fill="url(#Gradient)"/><text x="25" y="12px" ' +
        'font-family="sans-serif" font-size="12px" text-anchor="start">50' +
        '</text><text x="25" y="50%" font-family="sans-serif" ' +
        'font-size="12px" text-anchor="start">25</text><text x="25" y="95%" ' +
        'font-family="sans-serif" font-size="12px" text-anchor="start">0</text>'
      );

      deepEqual(ColorViewController.getColorList(five, 'Set1', true),
                [{'0': '#e41a1c', '1': '#377eb8', '2': '#4daf4a',
                  '3': '#984ea3', '4': '#ff7f00'}, undefined]);

      // Since the scaled parameter is false, this tests "equidistant colors"
      // (aka getInterpolatedColors()).
      var interpolatedColorList = ColorViewController.getColorList(
          twenty, 'BrBG', false
      );
      // Test that extreme values are correctly assigned to the colors at the
      // ends of the BrBG color map
      deepEqual(interpolatedColorList[0]['0'], '#543005');
      deepEqual(interpolatedColorList[0]['19'], '#003c30');
      // Now, check that all values (incl. intermediate ones) are correctly
      // assigned colors
      var interpolator = chroma.scale(chroma.brewer.BrBG).domain([0, 19]);
      for (var i = 0; i < 19; i++) {
          deepEqual(interpolatedColorList[0][String(i)], interpolator(i).hex());
      }
      // Lastly, check that the second element in interpolatedColorList is
      // undefined (since we're not drawing a gradient)
      deepEqual(interpolatedColorList[1], undefined);

      deepEqual(ColorViewController.getColorList(one, 'OrRd', false),
                [{'0': '#fff7ec'}, undefined]);
      deepEqual(ColorViewController.getColorList(one, 'RdGy', true),
                [{'0': '#67001f'}, undefined]);

    });

    test('Test ColorViewController.getColorList exceptions', function() {
      var five;
      five = [0, 1, 2, 3, 4];
      throws(
          function() {
            ColorViewController.getColorList(five, false, 'Non-existant');
          },
          Error,
          'An error is raised if the colormap does not exist'
          );

      five = [0, 'string1', 'string2', 'string3', 'string4'];
      throws(
          function() {
            ColorViewController.getColorList(five, 'Blues', false, true);
          },
          Error,
          'Error is raised if there are less than 2 numeric values when scaled'
          );
    });

    test('Testing setPlottableAttributes helper function', function(assert) {
      // testing with one plottable
      var idx = 0;
      plottables = [{idx: idx}];
      equal(this.dv.markers[idx].material.color.getHexString(), 'ff0000');
      equal(this.dv.markers[idx + 1].material.color.getHexString(), 'ff0000');
      ColorViewController.prototype.setPlottableAttributes(this.dv, '#00ff00',
                                                           plottables);
      equal(this.dv.markers[idx].material.color.getHexString(), '00ff00');
      equal(this.dv.markers[idx + 1].material.color.getHexString(), 'ff0000');
      equal(this.dv.needsUpdate, true);

      // testing with multiple plottable
      plottables = [{idx: idx}, {idx: idx + 1}];
      ColorViewController.prototype.setPlottableAttributes(this.dv, '#000000',
                                                           plottables);
      equal(this.dv.markers[idx].material.color.getHexString(), '000000');
      equal(this.dv.markers[idx + 1].material.color.getHexString(), '000000');
      equal(this.dv.needsUpdate, true);
    });

    test('Testing setPlottableAttributes (jackknifing)', function(assert) {
      // In this test we validate that ellipsoids can be changed in color
      // one by one and a few at a time.

      // testing with one plottable
      var idx = 0, dv = this.jackknifedDecView;
      plottables = [{idx: idx}];

      // assert initial state
      equal(dv.markers[0].material.color.getHexString(), 'ff0000');
      equal(dv.markers[1].material.color.getHexString(), 'ff0000');
      equal(dv.ellipsoids[0].material.color.getHexString(), 'ff0000');
      equal(dv.ellipsoids[1].material.color.getHexString(), 'ff0000');

      // change color to green (only one sample)
      ColorViewController.prototype.setPlottableAttributes(dv, '#00ff00',
                                                           plottables);
      equal(dv.needsUpdate, true);

      equal(dv.markers[0].material.color.getHexString(), '00ff00');
      equal(dv.markers[1].material.color.getHexString(), 'ff0000');
      equal(dv.ellipsoids[0].material.color.getHexString(), '00ff00');
      equal(dv.ellipsoids[1].material.color.getHexString(), 'ff0000');

      // change color to black (two samples)
      plottables = [{idx: idx}, {idx: idx + 1}];
      ColorViewController.prototype.setPlottableAttributes(dv, '#000000',
                                                           plottables);
      equal(dv.needsUpdate, true);

      equal(dv.markers[0].material.color.getHexString(), '000000');
      equal(dv.markers[1].material.color.getHexString(), '000000');
      equal(dv.ellipsoids[0].material.color.getHexString(), '000000');
      equal(dv.ellipsoids[1].material.color.getHexString(), '000000');
    });

    test('Testing toJSON', function() {
      var container = $('<div style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(new UIState(),
        container, this.sharedDecompositionViewDict);
      // Change color on one point
      var idx = 0;
      plottables = [{idx: idx}];
      ColorViewController.prototype.setPlottableAttributes(this.dv, '#00ff00',
                                                           plottables);

      controller.setMetadataField('DOB');
      var obs = controller.toJSON();
      var exp = {'category': 'DOB',
                 'colormap': 'discrete-coloring-qiime',
                 'continuous': false,
                 'data': { '20070314': '#ff0000', '20071112': '#0000ff'}};
      deepEqual(obs, exp);
    });

    test('Testing fromJSON', function(assert) {
      var json = {category: 'DOB',
                  colormap: 'discrete-coloring-qiime',
                  continuous: false,
                  data: {20070314: '#ff0000', 20071112: '#0000ff'}};

      var container = $('<div style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(new UIState(),
        container, this.sharedDecompositionViewDict);

      controller.setMetadataField('Treatment');

      controller.fromJSON(json);

      // check the data is rendered
      assert.ok(controller.$gridDiv.find(':contains(20070314)').length > 0);
      assert.ok(controller.$gridDiv.find(':contains(20071112)').length > 0);

      var idx = 0;
      var markers = controller.decompViewDict.scatter.markers;
      equal(markers[idx].material.color.getHexString(), 'ff0000');
      equal(markers[idx + 1].material.color.getHexString(), '0000ff');
      equal(markers[idx + 2].material.color.getHexString(), '0000ff');
      equal(controller.$select.val(), 'DOB');
      equal(controller.$colormapSelect.val(), 'discrete-coloring-qiime');
      equal(controller.$scaled.is(':checked'), false);
      equal(controller.$searchBar.val(), '');
      equal(controller.$searchBar.prop('hidden'), false);
    });

    test('Testing fromJSON scaled', function(assert) {
      var json = {category: 'Mixed', colormap: 'Viridis',
                  continuous: true, data: {'Non-numeric values': '#ae1221'}};

      var container = $('<div style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(new UIState(),
        container, this.sharedDecompositionViewDict);

      controller.setMetadataField('Treatment');

      controller.fromJSON(json);

      // no grid data should be rendered (continuous is set to true)
      assert.ok(controller.$gridDiv.find(':contains(14.2)').length <= 0);
      assert.ok(controller.$gridDiv.find(':contains(StringValue)').length <= 0);
      assert.ok(controller.$gridDiv.find(':contains(14.7)').length <= 0);

      var idx = 0;
      var markers = controller.decompViewDict.scatter.markers;
      equal(markers[idx].material.color.getHexString(), '440154');
      equal(markers[idx + 1].material.color.getHexString(), 'ae1221');
      equal(markers[idx + 2].material.color.getHexString(), 'fee825');
      equal(controller.$select.val(), 'Mixed');
      equal(controller.$colormapSelect.val(), 'Viridis');
      equal(controller.$scaled.is(':checked'), true);
      equal(controller.isColoringContinuous(), true);
      equal(controller.$searchBar.val(), '');
      equal(controller.$searchBar.prop('hidden'), true);
    });

    test('Testing toJSON (null)', function() {
      var container = $('<div style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(new UIState(),
        container, this.sharedDecompositionViewDict);
      controller.setMetadataField(null);

      var obs = controller.toJSON();
      var exp = {'category': null,
                 'colormap': 'discrete-coloring-qiime',
                 'continuous': false,
                 'data': {}};
      deepEqual(obs, exp);
    });

    test('Testing fromJSON (null)', function() {
      var json = {category: null,
                  colormap: 'discrete-coloring-qiime',
                  continuous: false,
                  data: {}};

      var container = $('<div style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(new UIState(),
        container, this.sharedDecompositionViewDict);

      controller.fromJSON(json);
      var markers = controller.decompViewDict.scatter.markers;
      equal(markers[0].material.color.getHexString(), 'ff0000');
      equal(markers[1].material.color.getHexString(), 'ff0000');
      equal(markers[2].material.color.getHexString(), 'ff0000');
      equal(controller.$select.val(), null);
      equal(controller.$colormapSelect.val(), 'discrete-coloring-qiime');
      equal(controller.$scaled.is(':checked'), false);
      equal(controller.isColoringContinuous(), false);
      equal(controller.$searchBar.val(), '');
      equal(controller.$searchBar.prop('hidden'), false);
    });

    test('Test getDiscretePaletteColor(map)', function() {
      deepEqual(ColorViewController.getPaletteColor('OrRd'),
      ['#fff7ec', '#fee8c8', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548',
      '#d7301f', '#b30000', '#7f0000']);
      deepEqual(ColorViewController.getPaletteColor('RdGy'),
      ['#67001f', '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#ffffff',
      '#e0e0e0', '#bababa', '#878787', '#4d4d4d', '#1a1a1a']);
      deepEqual(ColorViewController.getPaletteColor('Set2'),
      ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f',
      '#e5c494', '#b3b3b3']);
    });

    test('Test setEnabled', function() {
      var container = $('<div style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(new UIState(),
        container, this.sharedDecompositionViewDict);

      // disable
      controller.setEnabled(false);

      equal(controller.$colormapSelect.is(':disabled'), true);
      equal(controller.$scaled.is(':disabled'), true);
      equal(controller.$searchBar.prop('hidden'), true);
    });

    /**
     *
     * Test large dataset.
     *
     */
    asyncTest('Test large dataset', function() {
      var coords = [], metadata = [];
      for (var i = 0; i < 1001; i++) {
        coords.push([Math.random(), Math.random(), Math.random(),
                     Math.random()]);
        metadata.push([i, 'b ' + Math.random(), 'c ' + Math.random()]);
      }

      var data = {coordinates: coords, percents_explained: [45, 35, 15, 5],
                  sample_ids: _.range(1001), name: 'pcoa'};

      var d = new DecompositionModel(data, ['SampleID', 'foo', 'bar'],
                                     metadata);
      var mm = new MultiModel({'scatter': d});
      var state = new UIState();
      var dv = new DecompositionView(mm, 'scatter', state);
      var container = $('<div id="does-not-exist"></div>');
      // create a dummy category selection callback
      var options = {'categorySelectionCallback': function() {}};
      var attr = new ColorViewController(state, container, {'scatter': dv});
      $(function() {
        // Controllers should be enabled
        equal(attr.enabled, false);
        equal(attr.$select.val(), null);
        equal(attr.$select.is(':disabled'), false);
        equal(attr.$colormapSelect.is(':disabled'), true);
        equal(attr.$scaled.is(':disabled'), true);
        equal(attr.$searchBar.val(), '');
        equal(attr.$searchBar.is(':disabled'), true);

        start(); // qunit
      });
    });

    /**
     *
     * Test large dataset.
     *
     */
    asyncTest('Test large dataset', function() {
      var coords = [], metadata = [];
      for (var i = 0; i < 1001; i++) {
        coords.push([Math.random(), Math.random(), Math.random(),
                     Math.random()]);
        metadata.push([i, 'b ' + Math.random(), 'c ' + Math.random()]);
      }

      var data = {coordinates: coords, percents_explained: [45, 35, 15, 5],
                  sample_ids: _.range(1001), name: 'pcoa'};

      var d = new DecompositionModel(data, ['SampleID', 'foo', 'bar'],
                                     metadata);
      var mm = new MultiModel({'scatter': d});
      var state = new UIState();
      var dv = new DecompositionView(mm, 'scatter', state);
      var container = $('<div id="does-not-exist"></div>');
      // create a dummy category selection callback
      var options = {'categorySelectionCallback': function() {}};
      var attr = new ColorViewController(state, container, {'scatter': dv});
      $(function() {
        // Controllers should be enabled
        equal(attr.enabled, false);
        equal(attr.$select.val(), null);
        equal(attr.$select.is(':disabled'), false);
        equal(attr.$colormapSelect.is(':disabled'), true);
        equal(attr.$scaled.is(':disabled'), true);
        equal(attr.$searchBar.val(), '');
        equal(attr.$searchBar.is(':disabled'), true);

        start(); // qunit
      });
    });

  });
});
