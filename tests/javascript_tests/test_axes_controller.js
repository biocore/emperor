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

    QUnit.module('AxesController', {
      beforeEach () {

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
        this.dv = new DecompositionView(multiModel, 'scatter', UIState1);

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
        var dv = new DecompositionView(multiModel, 'scatter', UIState1);
        this.sharedDecompositionViewDict.biplot = dv;

      },
      afterEach () {
        // cleanup all the unwanted DOM elements
        // if (this.controller !== undefined) {
        //     this.controller._$backgroundColor.spectrum('destroy');
        //     this.controller._$axesColor.spectrum('destroy');
        //     this.controller._$referenceEdgeColor.spectrum('destroy');
        //     this.controller._$otherEdgeColor.spectrum('destroy');
        // }
        // if (this.controllerProcrustes !== undefined) {
        //     this.controllerProcrustes._$backgroundColor.spectrum('destroy');
        //     this.controllerProcrustes._$axesColor.spectrum('destroy');
        //     this.controllerProcrustes._$referenceEdgeColor.spectrum('destroy');
        //     this.controllerProcrustes._$otherEdgeColor.spectrum('destroy');
        // }

        // this.controller = undefined;

        this.sharedDecompositionViewDict = undefined;
        this.decomp = undefined;
        this.multiModel = undefined;
      }
    });

   QUnit.test('Constructor tests', function(assert) {
     const done = assert.async();
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     $("#qunit-fixture").append(container);

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);

     assert.ok(AxesController.prototype instanceof EmperorViewControllerABC);

     $(function() {
         assert.equal(controller.title, 'Axes');

         assert.deepEqual(controller._flippedAxes, [false, false, false]);
         assert.equal(controller.$_screePlotContainer.attr('name'),
                      'scree-plot');

         assert.equal(controller._$axesColor.length, 1);
         assert.equal(controller._$backgroundColor.length, 1);

         assert.equal(controller._$referenceEdgeColor.length, 0);
         assert.equal(controller._$otherEdgeColor.length, 0);
         done();
     });
    });

   QUnit.test('Testing toJSON',  function(assert) {
     const done = assert.async();
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);

     var controllerProcrustes = new AxesController(new  UIState(),
                                                   container,
                                                   {'scatter': this.dv},
                                                  QUnit.config.fixture);


     $(function() {
         var obs = controller.toJSON();
         var exp = {'flippedAxes': [false, false, false],
                    'visibleDimensions': [0, 1, 2],
                    'referenceEdgeColor': null, 'viewType': 'scatter',
                    'otherEdgeColor': null, 'backgroundColor': '#000000',
                    'axesColor': '#ffffff'};
         assert.deepEqual(obs, exp);

         // procrustes case
         obs = controllerProcrustes.toJSON();
         exp = {'flippedAxes': [false, false, false],
                'visibleDimensions': [0, 1, 2],
                'otherEdgeColor': '#ff0000', 'referenceEdgeColor': '#ffffff',
                'viewType': 'scatter',
                'backgroundColor': '#000000', 'axesColor': '#ffffff'};
         assert.deepEqual(obs, exp);
         done();
     });
    });

   QUnit.test('Testing fromJSON',  function(assert) {
     const done = assert.async();
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);

     var controllerProcrustes = new AxesController(new  UIState(),
                                                   container,
                                                   {'scatter': this.dv},
                                                  QUnit.config.fixture);

      var json = {'flippedAxes': [true, true, false],
                  'visibleDimensions': [0, 1, 0],
                  'backgroundColor': '#FF00FF', 'axesColor': '#FF000F'};

      $(function() {
          controller.fromJSON(json);

          var decView = controller.getView();
          assert.deepEqual(decView.visibleDimensions, [0, 1, 0]);
          assert.deepEqual(controller._flippedAxes, [true, true, false]);

          assert.deepEqual(decView.backgroundColor, '#FF00FF');
          assert.deepEqual(decView.axesColor, '#FF000F');


          json = {'flippedAxes': [true, true, false],
                  'visibleDimensions': [0, 2, 1],
                  'backgroundColor': '#FF00FF', 'axesColor': '#FF000F',
                  'referenceEdgeColor': '#f0f123', 'otherEdgeColor': '#f0000f'};
          controllerProcrustes.fromJSON(json);
          decView = controllerProcrustes.getView();

          assert.deepEqual(decView.visibleDimensions, [0, 2, 1]);
          assert.deepEqual(controller._flippedAxes, [true, true, false]);

          assert.deepEqual(decView.backgroundColor, '#FF00FF');
          assert.deepEqual(decView.axesColor, '#FF000F');

          assert.deepEqual(controllerProcrustes.getBackgroundColor(),
                           '#ff00ff');
          assert.deepEqual(controllerProcrustes.getAxesColor(), '#ff000f');

          assert.deepEqual(controllerProcrustes.getReferenceEdgeColor(),
                           '#f0f123');
          assert.deepEqual(controllerProcrustes.getOtherEdgeColor(), '#f0000f');
          done();
      });
    });

   QUnit.test('Test fromJSON issue #717',  function(assert) {
     const done = assert.async();
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);
     
     // update the inversion of two axes before loading from JSON
     controller.flipAxis(0);
     controller.flipAxis(1);

     assert.deepEqual(controller._flippedAxes, [true, true, false]);

      var json = {'flippedAxes': [false, true, true],
                  'visibleDimensions': [0, 1, 2],
                  'backgroundColor': '#FF00FF', 'axesColor': '#FF000F'};

     $(function() {
         controller.fromJSON(json);

         var decView = controller.getView();
         assert.deepEqual(decView.visibleDimensions, [0, 1, 2]);
         assert.deepEqual(controller._flippedAxes, [false, true, true]);

         assert.deepEqual(decView.backgroundColor, '#FF00FF');
         assert.deepEqual(decView.axesColor, '#FF000F');

         done();
     });
    });

   QUnit.test('Testing _colorChanged',  function(assert) {
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);


     controller._colorChanged('axes-color', '#f0f0f0');
     assert.deepEqual(controller.getAxesColor(), '#f0f0f0');
     controller._colorChanged('background-color', '#101010');
     assert.deepEqual(controller.getBackgroundColor(), '#101010');

     controller._colorChanged('reference-edge-color', '#ff00ff');
     assert.deepEqual(controller.getReferenceEdgeColor(), null);
     controller._colorChanged('other-edge-color', '#ff0000');
     assert.deepEqual(controller.getOtherEdgeColor(), null);
    });

   QUnit.test('Testing background color', function(assert) {
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);

     var controllerProcrustes = new AxesController(new  UIState(),
                                                   container,
                                                   {'scatter': this.dv},
                                                  QUnit.config.fixture);


     assert.deepEqual(controller.getBackgroundColor(), '#000000');

     controller.setBackgroundColor('#f0f123');
     assert.deepEqual(controller.getBackgroundColor(), '#f0f123');

     assert.deepEqual(controllerProcrustes.getBackgroundColor(), '#000000');

     controllerProcrustes.setBackgroundColor('#f0f123');
     assert.deepEqual(controllerProcrustes.getBackgroundColor(), '#f0f123');

    });

   QUnit.test('Testing axes color', function(assert) {
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);

     var controllerProcrustes = new AxesController(new  UIState(),
                                                   container,
                                                   {'scatter': this.dv},
                                                  QUnit.config.fixture);

     assert.deepEqual(controller.getAxesColor(), '#ffffff');

     controller.setAxesColor('#f0f345');
     assert.deepEqual(controller.getAxesColor(), '#f0f345');

     assert.deepEqual(controllerProcrustes.getAxesColor(), '#ffffff');

     controllerProcrustes.setAxesColor('#f0f345');
     assert.deepEqual(controllerProcrustes.getAxesColor(), '#f0f345');
    });

   QUnit.test('Testing reference edge color', function(assert) {
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);

     var controllerProcrustes = new AxesController(new  UIState(),
                                                   container,
                                                   {'scatter': this.dv},
                                                   QUnit.config.fixture);

      assert.ok(controller.getReferenceEdgeColor() === null);

      // we just check that the method doesn't raise an error
      controller.setReferenceEdgeColor('#f0f0f0');

     assert.deepEqual(controllerProcrustes.getReferenceEdgeColor(), '#ffffff');
     controllerProcrustes.setReferenceEdgeColor('#f0f0f0');
     assert.deepEqual(controllerProcrustes.getReferenceEdgeColor(), '#f0f0f0');
    });

   QUnit.test('Testing other edge color', function(assert) {
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                         QUnit.config.fixture);

     var controllerProcrustes = new AxesController(new  UIState(),
                                                   container,
                                                   {'scatter': this.dv},
                                                   QUnit.config.fixture);

      assert.ok(controller.getOtherEdgeColor() === null);

      // we just check that the method doesn't raise an error
      controller.setOtherEdgeColor('#f0f0f0');

     assert.deepEqual(controllerProcrustes.getOtherEdgeColor(), '#ff0000');
     controllerProcrustes.setOtherEdgeColor('#0000ff');
     assert.deepEqual(controllerProcrustes.getOtherEdgeColor(), '#0000ff');
    });

   QUnit.test('Test flipAxis', function(assert) {
     const done = assert.async();

     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);

      var res;

      $(function() {
	  res = controller.$header.find(':checkbox');

	  // verify the checkboxes change as expected
	  assert.deepEqual([res[0].checked, res[1].checked, res[2].checked],
			   [false, false, false]);
	  assert.deepEqual(controller._flippedAxes, [false, false, false]);

	  controller.flipAxis(1);

	  res = controller.$header.find(':checkbox');
	  assert.deepEqual([res[0].checked, res[1].checked, res[2].checked],
			   [false, true, false]);
	  assert.deepEqual(controller._flippedAxes, [false, true, false]);

	  controller.flipAxis(1);

	  res = controller.$header.find(':checkbox');
	  assert.deepEqual([res[0].checked, res[1].checked, res[2].checked],
			   [false, false, false]);
	  assert.deepEqual(controller._flippedAxes, [false, false, false]);

	  done();
      });
    });

   QUnit.test('Test updateVisibleAxes',  function(assert) {
     const done = assert.async();

     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AxesController(new UIState(),
                                         container,
                                         this.sharedDecompositionViewDict,
                                        QUnit.config.fixture);

      var res;
       
      $(function() {
          // check that we can turn to a 2D plot
          controller.updateVisibleAxes(null, 2);

          new Promise(function(resolve) {
              setTimeout(
                  function() {
                      res = controller.$header.find(':checkbox');
                      assert.deepEqual(
                          [res[0].disabled, res[1].disabled, res[2].disabled],
                          [false, false, true]
                      );

                      assert.deepEqual(controller._flippedAxes,
                                       [false, false, false]);
                      controller.updateVisibleAxes(3, 2);
                      resolve();
                  }, 0);
          }).then(function() {
              setTimeout(
                  function() {
                      res = controller.$header.find(':checkbox');
                      assert.deepEqual([res[0].disabled,
                                        res[1].disabled, res[2].disabled],
                                       [false, false, false]);
                      assert.deepEqual(controller._flippedAxes,
                                       [false, false, false]);
                      done();
                  }, 0);
          });
      });
    });
  });
});
