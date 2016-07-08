requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'viewcontroller',
    'slickgrid',
    'axescontroller'
], function($, _, model, DecompositionView, viewcontroller, SlickGrid,
            AxesController) {
  $(document).ready(function() {
    var EmperorViewControllerABC = viewcontroller.EmperorViewControllerABC;
    var DecompositionModel = model.DecompositionModel;

    module('AxesController', {
      setup: function() {
        this.sharedDecompositionViewDict = {};
        var $slickid = $('<div id="fooligans"></div>');
        $slickid.appendTo(document.body);

        // setup function
        name = 'pcoa';
        ids = ['PC.636', 'PC.635', 'PC.634'];
        coords = [
          [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
          -0.229889, -0.046599],
          [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
          -0.112864, 0.064794],
          [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
          -0.112864, 0.064794]];
        pct_var = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
        10.024774995, 8.22835130237, 7.55971173665, 6.24945796136];
        md_headers = ['SampleID', 'Mixed', 'Treatment', 'DOB'];
        metadata = [['PC.636', '14.2', 'Control', '20070314'],
        ['PC.635', 'StringValue', 'Fast', '20071112'],
        ['PC.634', '14.7', 'Fast', '20071112']];
        decomp = new DecompositionModel(name, ids, coords, pct_var, md_headers,
            metadata);
        var dv = new DecompositionView(decomp);
        this.sharedDecompositionViewDict.scatter = dv;

        name = 'biplot';
        ids = ['tax_1', 'tax_2'];
        coords = [
          [-1, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
          -0.229889, -0.046599],
          [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
          -0.112864, 0.064794]];
        pct_var = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
        10.024774995, 8.22835130237, 7.55971173665, 6.24945796136];
        md_headers = ['SampleID', 'Gram'];
        metadata = [['tax_1', '1'],
        ['tax_2', '0']];
        this.decomp = new DecompositionModel(name, ids, coords, pct_var,
            md_headers, metadata);
        this.dv = new DecompositionView(this.decomp);
        this.sharedDecompositionViewDict.biplot = dv;

        // Slickgrid
        var columns = [
        {id: 'pc1', name: 'pc1', field: 'pc1'},
        {id: 'pc2', name: 'pc2', field: 'pc2'},
        {id: 'pc3', name: 'pc3', field: 'pc3'}
        ];

        var options = {
          enableCellNavigation: true,
          enableColumnReorder: false
        };
        var data = [];
        data.push({'pc1': 1, 'pc2': 1, 'pc3': 1});
        data.push({'pc1': 1, 'pc2': 1, 'pc3': 2});
        data.push({'pc1': 2, 'pc2': 1, 'pc3': 2});

        grid = new Slick.Grid('#fooligans', data, columns, options);
      },
      teardown: function() {
        this.sharedDecompositionViewDict = undefined;
        $('#fooligans').remove();
        this.decomp = undefined;
      }
    });

    test('Constructor tests', function(assert) {
      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                        'width:12px"></div>');

      assert.ok(AxesController.prototype instanceof EmperorViewControllerABC);

      var controller = new AxesController(
        container, this.sharedDecompositionViewDict);
      equal(controller.title, 'Axes');

      deepEqual(controller._flippedAxes, [0, 0, 0]);
      equal(controller.$_screePlotContainer.attr('name'), 'scree-plot');

      equal(controller.$body.find('[name="axes-color"]').length, 1);
      equal(controller.$body.find('[name="background-color"]').length, 1);
    });

    test('Testing toJSON', function() {
      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                        'width:12px"></div>');
      var controller = new AxesController(
        container, this.sharedDecompositionViewDict);

      var obs = controller.toJSON();
      var exp = {'flippedAxes': [0, 0, 0], 'visibleDimensions': [0, 1, 2],
                 'backgroundColor': 0x000000, 'axesColor': 0xFFFFFF};
      deepEqual(obs, exp);
    });

    test('Testing fromJSON', function() {
      var json = {'flippedAxes': [1, 1, 0], 'visibleDimensions': [0, 1, 0],
                  'backgroundColor': 0xFF00FF, 'axesColor': 0xFF000F};

      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                        'width:12px"></div>');
      var controller = new AxesController(
        container, this.sharedDecompositionViewDict);

      controller.fromJSON(json);

      var decView = controller.decompViewDict[controller.activeViewKey];
      deepEqual(decView.visibleDimensions, [0, 1, 0]);
      deepEqual(controller._flippedAxes, [1, 1, 0]);

      deepEqual(decView.backgroundColor, 0xFF00FF);
      deepEqual(decView.axesColor, 0xFF000F);
    });

    test('Testing colorChanged', function() {
      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                        'width:12px"></div>');
      var controller = new AxesController(
        container, this.sharedDecompositionViewDict);

      var decView = controller.decompViewDict[controller.activeViewKey];
      controller.colorChanged('axes-color', 0xF0F0F0);
      deepEqual(decView.axesColor, 0xF0F0F0);
      controller.colorChanged('background-color', 0x101010);
      deepEqual(decView.backgroundColor, 0x101010);
    });

  });
});
