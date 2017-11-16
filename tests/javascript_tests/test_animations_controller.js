requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'viewcontroller',
    'animationscontroller'
], function($, _, model, DecompositionView, ViewControllers,
            AnimationsController) {
  $(document).ready(function() {
    var EmperorViewController = ViewControllers.EmperorViewController;
    var DecompositionModel = model.DecompositionModel;

    module('AnimationsController', {
      setup: function() {
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
                                         7.55971173665, 6.24945796136]};
        var md_headers = ['SampleID', 'Mixed', 'Treatment', 'DOB'];
        var metadata = [['PC.636', '14.2', 'Control', '20070314'],
        ['PC.635', 'StringValue', 'Fast', '20071112'],
        ['PC.634', '14.7', 'Fast', '20071112']];
        var decomp = new DecompositionModel(data, md_headers, metadata);
        var dv = new DecompositionView(decomp);
        this.sharedDecompositionViewDict.scatter = dv;

        var container = $('<div id="does-not-exist" style="height:1000px; ' +
                          'width:12px"></div>');
        this.controller = new AnimationsController(container,
          this.sharedDecompositionViewDict);
      },
      teardown: function() {
        this.controller = undefined;
        this.sharedDecompositionViewDict = undefined;
        this.decomp = undefined;
      }
    });

    test('Constructor tests', function(assert) {
      assert.ok(AnimationsController.prototype instanceof
                EmperorViewController);

      equal(this.controller.title, 'Animations');
    });

    test('Testing toJSON', function() {
      var obs = this.controller.toJSON();
      var exp = {'flippedAxes': [false, false, false],
                 'visibleDimensions': [0, 1, 2],
                 'backgroundColor': '#000000', 'axesColor': '#FFFFFF'};
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
    });

    test('Testing colorChanged', function() {
      var decView = this.controller.getView();
      deepEqual({}, {});
    });

  });
});
