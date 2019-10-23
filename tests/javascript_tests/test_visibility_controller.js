requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'viewcontroller',
    'slickgrid',
    'visibilitycontroller',
    'multi-model',
    'uistate'
], function($, _, model, DecompositionView, viewcontroller, SlickGrid,
            VisibilityController, MultiModel, UIState) {
  $(document).ready(function() {
    var EmperorAttributeABC = viewcontroller.EmperorAttributeABC;
    var DecompositionModel = model.DecompositionModel;

    module('VisibilityController', {
      setup: function() {
        this.sharedDecompositionViewDict = {};

        var UIState1 = new UIState();

        // setup function
        var data = {name: 'pcoa', sample_ids: ['PC.636', 'PC.635'],
                    coordinates: [[-0.276542, -0.144964, 0.066647, -0.067711,
                                   0.176070, 0.072969, -0.229889, -0.046599],
                                  [-0.237661, 0.046053, -0.138136, 0.159061,
                                   -0.247485, -0.115211, -0.112864, 0.064794]],
                    percents_explained: [26.6887048633, 16.2563704022,
                                         13.7754129161, 11.217215823,
                                         10.024774995, 8.22835130237,
                                         7.55971173665, 6.24945796136]};
        var md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                          'DOB'];
        var metadata = [['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control',
                         '20070314'],
                        ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast',
                         '20071112']];
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
        metadata = [['tax_1', '1'], ['tax_2', '0']];
        decomp = new DecompositionModel(data, md_headers, metadata);
        multiModel = new MultiModel({'scatter': decomp});
        this.dv = new DecompositionView(multiModel, 'scatter', UIState1);
        this.sharedDecompositionViewDict.biplot = this.dv;

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
        this.jackknifedDecView = new DecompositionView(multiModel, 'scatter',
                                                       UIState1);
      },
      teardown: function() {
        this.sharedDecompositionViewDict = undefined;
        $('#fooligans').remove();
        this.decomp = undefined;
      }
    });

    test('Constructor tests', function(assert) {
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                        'width:12px"></div>');

      assert.ok(VisibilityController.prototype instanceof EmperorAttributeABC);

      var controller = new VisibilityController(new UIState(), container,
          this.sharedDecompositionViewDict);
      equal(controller.title, 'Visibility');

      var testColumn = controller.bodyGrid.getColumns()[0];
      equal(testColumn.field, 'value');

      // verify the visibility value is set properly
      equal(controller.getMetadataField(), null);
    });

    test('Testing setPlottableAttributes helper function', function(assert) {
      // testing with one plottable
      var idx = 0;
      plottables = [{idx: idx}];
      equal(this.dv.markers[idx].visible, true);
      equal(this.dv.markers[idx + 1].visible, true);
      VisibilityController.prototype.setPlottableAttributes(this.dv, false,
                                                            plottables);
      equal(this.dv.needsUpdate, true);

      // testing with multiple plottable
      plottables = [{idx: idx}, {idx: idx + 1}];
      equal(this.dv.markers[idx].visible, false);
      equal(this.dv.markers[idx + 1].visible, true);
      VisibilityController.prototype.setPlottableAttributes(this.dv, true,
                                                            plottables);
      equal(this.dv.markers[idx].visible, true);
      equal(this.dv.markers[idx + 1].visible, true);
      equal(this.dv.needsUpdate, true);
    });

    test('Testing setPlottableAttributes (jackknifed)', function(assert) {
      // testing with one plottable
      var idx = 0, dv = this.jackknifedDecView;
      plottables = [{idx: idx}];

      // all should be visible
      equal(dv.markers[0].visible, true);
      equal(dv.markers[1].visible, true);
      equal(dv.ellipsoids[0].visible, true);
      equal(dv.ellipsoids[1].visible, true);

      VisibilityController.prototype.setPlottableAttributes(dv, false,
                                                            plottables);
      equal(dv.needsUpdate, true);

      // sample zero should be hidden
      equal(dv.markers[0].visible, false);
      equal(dv.markers[1].visible, true);
      equal(dv.ellipsoids[0].visible, false);
      equal(dv.ellipsoids[1].visible, true);


      // testing with multiple plottables
      plottables = [{idx: idx}, {idx: idx + 1}];
      VisibilityController.prototype.setPlottableAttributes(dv, true,
                                                            plottables);
      equal(dv.needsUpdate, true);

      // none should be visible
      equal(dv.markers[0].visible, true);
      equal(dv.markers[1].visible, true);
      equal(dv.ellipsoids[0].visible, true);
      equal(dv.ellipsoids[1].visible, true);
    });

    test('Testing toJSON', function() {
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                        'width:12px"></div>');
      var controller = new VisibilityController(new UIState(), container,
          this.sharedDecompositionViewDict);

      controller.setMetadataField('DOB');
      var obs = controller.toJSON();
      var exp = {category: 'DOB', data: {'20070314': true, '20071112': true}};
      deepEqual(obs, exp);
    });

    test('Testing fromJSON', function() {
      var json = {category: 'SampleID',
                  data: {'PC.636': false, 'PC.635': true}};
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                        'width:12px"></div>');
      var controller = new VisibilityController(new UIState(), container,
          this.sharedDecompositionViewDict);
      controller.fromJSON(json);

      var idx = 0;
      equal(controller.decompViewDict.scatter.markers[idx].visible, false);
      equal(controller.decompViewDict.scatter.markers[idx + 1].visible, true);
    });

    test('Testing toJSON', function() {
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                        'width:12px"></div>');
      var controller = new VisibilityController(new UIState(), container,
          this.sharedDecompositionViewDict);
      controller.setMetadataField(null);

      var obs = controller.toJSON();
      var exp = {category: null, data: {}};
      deepEqual(obs, exp);
    });

    test('Testing fromJSON', function() {
      var json = {category: null,
                  data: {}};
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                        'width:12px"></div>');
      var controller = new VisibilityController(new UIState(), container,
          this.sharedDecompositionViewDict);
      controller.fromJSON(json);

      equal(controller.decompViewDict.scatter.markers[0].visible, true);
      equal(controller.decompViewDict.scatter.markers[1].visible, true);
    });

  });

});
