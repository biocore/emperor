requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'abcviewcontroller',
    'slickgrid',
    'axescontroller',
    'multi-model',
    'uistate'
], function($, _, model, DecompositionView, abc, SlickGrid,
            AxesController, MultiModel, UIState) {
  $(document).ready(function() {
    var EmperorViewControllerABC = abc.EmperorViewControllerABC;
    var DecompositionModel = model.DecompositionModel;

    module('AxesController', {
      setup: function() {
        var container = $('<div id="does-not-exist" style="height:1000px; ' +
                          'width:12px"></div>');

        var UIState1 = new UIState();
        this.sharedDecompositionViewDict = {};

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
                                         7.55971173665, 6.24945796136],
                    edges: [['PC.636', 'PC.635'], ['PC.636', 'PC.634']]};
        var md_headers = ['SampleID', 'Mixed', 'Treatment', 'DOB'];
        var metadata = [['PC.636', '14.2', 'Control', '20070314'],
        ['PC.635', 'StringValue', 'Fast', '20071112'],
        ['PC.634', '14.7', 'Fast', '20071112']];

        var decomp = new DecompositionModel(data, md_headers, metadata);
        var multiModel = new MultiModel({'scatter': decomp});
        var dv = new DecompositionView(multiModel, 'scatter', UIState1);
        this.controllerProcrustes = new AxesController(UIState1, container,
                                                       {'scatter': dv});

        // data without procrustes edges
        data = {name: 'pcoa', sample_ids: ['PC.636', 'PC.635', 'PC.634'],
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

        decomp = new DecompositionModel(data, md_headers, metadata);
        multiModel = new MultiModel({'scatter': decomp});
        dv = new DecompositionView(multiModel, 'scatter', UIState1);
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
        this.sharedDecompositionViewDict.biplot = dv;

        this.controller = new AxesController(UIState1, container,
                                             this.sharedDecompositionViewDict);
      },
      teardown: function() {
        // cleanup all the unwanted DOM elements
        this.controller._$backgroundColor.spectrum('destroy');
        this.controller._$axesColor.spectrum('destroy');
        this.controller._$referenceEdgeColor.spectrum('destroy');
        this.controller._$otherEdgeColor.spectrum('destroy');
        this.controllerProcrustes._$backgroundColor.spectrum('destroy');
        this.controllerProcrustes._$axesColor.spectrum('destroy');
        this.controllerProcrustes._$referenceEdgeColor.spectrum('destroy');
        this.controllerProcrustes._$otherEdgeColor.spectrum('destroy');

        this.controller = undefined;

        this.sharedDecompositionViewDict = undefined;
        this.decomp = undefined;
        this.multiModel = undefined;
      }
    });

    test('Constructor tests', function(assert) {
      assert.ok(AxesController.prototype instanceof EmperorViewControllerABC);

      equal(this.controller.title, 'Axes');

      deepEqual(this.controller._flippedAxes, [false, false, false]);
      equal(this.controller.$_screePlotContainer.attr('name'), 'scree-plot');

      equal(this.controller._$axesColor.length, 1);
      equal(this.controller._$backgroundColor.length, 1);

      equal(this.controller._$referenceEdgeColor.length, 0);
      equal(this.controller._$otherEdgeColor.length, 0);
    });

    test('Testing toJSON', function() {
      var obs = this.controller.toJSON();
      var exp = {'flippedAxes': [false, false, false],
                 'visibleDimensions': [0, 1, 2],
                 'referenceEdgeColor': null, 'viewType': 'scatter',
                 'otherEdgeColor': null, 'backgroundColor': '#000000',
                 'axesColor': '#ffffff'};
      deepEqual(obs, exp);

      // procrustes case
      obs = this.controllerProcrustes.toJSON();
      exp = {'flippedAxes': [false, false, false],
             'visibleDimensions': [0, 1, 2],
             'otherEdgeColor': '#ff0000', 'referenceEdgeColor': '#ffffff',
             'viewType': 'scatter',
             'backgroundColor': '#000000', 'axesColor': '#ffffff'};
      deepEqual(obs, exp);
    });

    test('Testing fromJSON', function() {
      var json = {'flippedAxes': [true, true, false],
                  'visibleDimensions': [0, 1, 0],
                  'backgroundColor': '#FF00FF', 'axesColor': '#FF000F'};

      this.controller.fromJSON(json);

      var decView = this.controller.getView();
      deepEqual(decView.visibleDimensions, [0, 1, 0]);
      deepEqual(this.controller._flippedAxes, [true, true, false]);

      deepEqual(decView.backgroundColor, '#FF00FF');
      deepEqual(decView.axesColor, '#FF000F');


      json = {'flippedAxes': [true, true, false],
              'visibleDimensions': [0, 2, 1],
              'backgroundColor': '#FF00FF', 'axesColor': '#FF000F',
              'referenceEdgeColor': '#f0f123', 'otherEdgeColor': '#f0000f'};
      this.controllerProcrustes.fromJSON(json);
      decView = this.controllerProcrustes.getView();

      deepEqual(decView.visibleDimensions, [0, 2, 1]);
      deepEqual(this.controller._flippedAxes, [true, true, false]);

      deepEqual(decView.backgroundColor, '#FF00FF');
      deepEqual(decView.axesColor, '#FF000F');

      deepEqual(this.controllerProcrustes.getBackgroundColor(), '#ff00ff');
      deepEqual(this.controllerProcrustes.getAxesColor(), '#ff000f');

      deepEqual(this.controllerProcrustes.getReferenceEdgeColor(), '#f0f123');
      deepEqual(this.controllerProcrustes.getOtherEdgeColor(), '#f0000f');
    });

    test('Test fromJSON issue #717', function() {
      // update the inversion of two axes before loading from JSON
      this.controller.flipAxis(0);
      this.controller.flipAxis(1);

      deepEqual(this.controller._flippedAxes, [true, true, false]);

      var json = {'flippedAxes': [false, true, true],
                  'visibleDimensions': [0, 1, 2],
                  'backgroundColor': '#FF00FF', 'axesColor': '#FF000F'};

      this.controller.fromJSON(json);

      var decView = this.controller.getView();
      deepEqual(decView.visibleDimensions, [0, 1, 2]);
      deepEqual(this.controller._flippedAxes, [false, true, true]);

      deepEqual(decView.backgroundColor, '#FF00FF');
      deepEqual(decView.axesColor, '#FF000F');
    });

    test('Testing _colorChanged', function() {
      this.controller._colorChanged('axes-color', '#f0f0f0');
      deepEqual(this.controller.getAxesColor(), '#f0f0f0');
      this.controller._colorChanged('background-color', '#101010');
      deepEqual(this.controller.getBackgroundColor(), '#101010');

      this.controller._colorChanged('reference-edge-color', '#ff00ff');
      deepEqual(this.controller.getReferenceEdgeColor(), null);
      this.controller._colorChanged('other-edge-color', '#ff0000');
      deepEqual(this.controller.getOtherEdgeColor(), null);
    });

    test('Testing background color', function(assert) {
      deepEqual(this.controller.getBackgroundColor(), '#000000');

      this.controller.setBackgroundColor('#f0f123');
      deepEqual(this.controller.getBackgroundColor(), '#f0f123');

      deepEqual(this.controllerProcrustes.getBackgroundColor(), '#000000');

      this.controllerProcrustes.setBackgroundColor('#f0f123');
      deepEqual(this.controllerProcrustes.getBackgroundColor(), '#f0f123');

    });

    test('Testing axes color', function(assert) {
      deepEqual(this.controller.getAxesColor(), '#ffffff');

      this.controller.setAxesColor('#f0f345');
      deepEqual(this.controller.getAxesColor(), '#f0f345');

      deepEqual(this.controllerProcrustes.getAxesColor(), '#ffffff');

      this.controllerProcrustes.setAxesColor('#f0f345');
      deepEqual(this.controllerProcrustes.getAxesColor(), '#f0f345');
    });

    test('Testing reference edge color', function(assert) {
      assert.ok(this.controller.getReferenceEdgeColor() === null);

      // we just check that the method doesn't raise an error
      this.controller.setReferenceEdgeColor('#f0f0f0');

      deepEqual(this.controllerProcrustes.getReferenceEdgeColor(), '#ffffff');
      this.controllerProcrustes.setReferenceEdgeColor('#f0f0f0');
      deepEqual(this.controllerProcrustes.getReferenceEdgeColor(), '#f0f0f0');
    });

    test('Testing other edge color', function(assert) {
      assert.ok(this.controller.getOtherEdgeColor() === null);

      // we just check that the method doesn't raise an error
      this.controller.setOtherEdgeColor('#f0f0f0');

      deepEqual(this.controllerProcrustes.getOtherEdgeColor(), '#ff0000');
      this.controllerProcrustes.setOtherEdgeColor('#0000ff');
      deepEqual(this.controllerProcrustes.getOtherEdgeColor(), '#0000ff');
    });

    test('Test flipAxis', function(assert) {
      var res;

      res = this.controller.$header.find(':checkbox');

      // verify the checkboxes change as expected
      deepEqual([res[0].checked, res[1].checked, res[2].checked],
                [false, false, false]);
      deepEqual(this.controller._flippedAxes, [false, false, false]);

      this.controller.flipAxis(1);

      res = this.controller.$header.find(':checkbox');
      deepEqual([res[0].checked, res[1].checked, res[2].checked],
                [false, true, false]);
      deepEqual(this.controller._flippedAxes, [false, true, false]);

      this.controller.flipAxis(1);

      res = this.controller.$header.find(':checkbox');
      deepEqual([res[0].checked, res[1].checked, res[2].checked],
                [false, false, false]);
      deepEqual(this.controller._flippedAxes, [false, false, false]);
    });

    test('Test updateVisibleAxes', function() {
      var res;

      // check that we can turn to a 2D plot
      this.controller.updateVisibleAxes(null, 2);

      res = this.controller.$header.find(':checkbox');
      deepEqual([res[0].disabled, res[1].disabled, res[2].disabled],
                [false, false, true]);
      deepEqual(this.controller._flippedAxes, [false, false, false]);

      this.controller.updateVisibleAxes(3, 2);

      res = this.controller.$header.find(':checkbox');
      deepEqual([res[0].disabled, res[1].disabled, res[2].disabled],
                [false, false, false]);
      deepEqual(this.controller._flippedAxes, [false, false, false]);
    });
  });
});
