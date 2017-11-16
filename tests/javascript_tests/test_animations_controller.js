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
        var metadata = [['PC.636', '14.2', 'Fast', '20070314'],
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
      equal(this.controller.director, null);
      equal(this.controller.playing, false);
      equal(this.controller.enabled, false);

      equal(this.controller.$speed.slider('option', 'disabled'), true);
      equal(this.controller.$play.prop('disabled'), true);
      equal(this.controller.$pause.prop('disabled'), true);
      equal(this.controller.$rewind.prop('disabled'), true);

      equal(this.controller.getGradientCategory(), '');
      equal(this.controller.getTrajectoryCategory(), '');
      equal(this.controller.getSpeed(), 1);
    });

    test('Test speed setter/getter', function(assert) {
      equal(this.controller.getSpeed(), 1);

      this.controller.setSpeed(1.11);
      equal(this.controller.getSpeed(), 1.11);

      throws(
          function() {
            this.controller.setSpeed(-1);
          },
          Error,
          'An error is raised if an invalid speed is set'
      );

      this.controller.setSpeed(3.11);
      equal(this.controller.getSpeed(), 3.11);

      throws(
          function() {
            this.controller.setSpeed(6);
          },
          Error,
          'An error is raised if an invalid speed is set'
      );
    });

    test('Test gradient category setter/getter', function(assert) {
      this.controller.setGradientCategory('Treatment');
      equal(this.controller.getGradientCategory(), 'Treatment');

      this.controller.setGradientCategory('Does not exist');
      equal(this.controller.getGradientCategory(), '');

      this.controller.setGradientCategory('DOB');
      equal(this.controller.getGradientCategory(), 'DOB');
    });

    test('Test trajectory category setter/getter', function(assert) {
      this.controller.setTrajectoryCategory('DOB');
      equal(this.controller.getTrajectoryCategory(), 'DOB');

      this.controller.setGradientCategory('Does not exist either');
      equal(this.controller.getGradientCategory(), '');

      this.controller.setTrajectoryCategory('Treatment');
      equal(this.controller.getTrajectoryCategory(), 'Treatment');
    });

    test('Test trajectory and category methods together', function(assert) {
      equal(this.controller.getTrajectoryCategory(), '');
      equal(this.controller.getGradientCategory(), '');
      equal(this.controller.enabled, false);

      this.controller.setTrajectoryCategory('Treatment');
      equal(this.controller.enabled, false);

      this.controller.setGradientCategory('DOB');
      equal(this.controller.enabled, true);

      this.controller.setTrajectoryCategory('');
      equal(this.controller.enabled, false);
    });

    test('Test _pauseButtonClicked', function(assert) {
      this.controller.setGradientCategory('DOB');
      this.controller.setTrajectoryCategory('Treatment');
      this.controller.playing = true;
      this.controller._updateButtons();

      this.controller._pauseButtonClicked();

      equal(this.controller.playing, false);
      equal(this.controller.$speed.slider('option', 'disabled'), false);
      equal(this.controller.$play.prop('disabled'), false);
      equal(this.controller.$pause.prop('disabled'), true);
      equal(this.controller.$rewind.prop('disabled'), true);
    });

    test('Test _playButtonClicked', function(assert) {
      this.controller.setGradientCategory('DOB');
      this.controller.setTrajectoryCategory('Treatment');
      equal(this.controller.playing, false);

      this.controller._playButtonClicked();

      equal(this.controller.playing, true);
      assert.ok(this.controller.director !== null);

      equal(this.controller.$speed.slider('option', 'disabled'), true);
      equal(this.controller.$play.prop('disabled'), true);
      equal(this.controller.$pause.prop('disabled'), false);
      equal(this.controller.$rewind.prop('disabled'), false);
    });

    test('Test _rewindButtonClicked', function(assert) {
      this.controller.setGradientCategory('DOB');
      this.controller.setTrajectoryCategory('Treatment');
      equal(this.controller.playing, false);

      this.controller._playButtonClicked();
      this.controller._rewindButtonClicked();

      equal(this.controller.playing, false);
      assert.ok(this.controller.director === null);

      equal(this.controller.$speed.slider('option', 'disabled'), false);
      equal(this.controller.$play.prop('disabled'), false);
      equal(this.controller.$pause.prop('disabled'), true);
      equal(this.controller.$rewind.prop('disabled'), true);
    });

    test('Test _updateButtons', function(assert) {
      this.controller._updateButtons();

      equal(this.controller.$speed.slider('option', 'disabled'), true);
      equal(this.controller.$play.prop('disabled'), true);
      equal(this.controller.$pause.prop('disabled'), true);
      equal(this.controller.$rewind.prop('disabled'), true);

      this.controller.setGradientCategory('DOB');
      this.controller.setTrajectoryCategory('Treatment');

      equal(this.controller.$speed.slider('option', 'disabled'), false);
      equal(this.controller.$play.prop('disabled'), false);
      equal(this.controller.$pause.prop('disabled'), true);
      equal(this.controller.$rewind.prop('disabled'), true);

      /**
       *
       * The next few tests use a "dummy" director and pretend that the
       * animation is running, but can't actually run because there's no
       * render loop in the test suite.
       *
       */
      this.controller.director = {'Dummy object': 'placeholder'};
      this.controller.playing = true;
      this.controller._updateButtons();

      equal(this.controller.$speed.slider('option', 'disabled'), true);
      equal(this.controller.$play.prop('disabled'), true);
      equal(this.controller.$pause.prop('disabled'), false);
      equal(this.controller.$rewind.prop('disabled'), false);

      this.controller.playing = false;
      this.controller._updateButtons();

      equal(this.controller.$speed.slider('option', 'disabled'), true);
      equal(this.controller.$play.prop('disabled'), false);
      equal(this.controller.$pause.prop('disabled'), true);
      equal(this.controller.$rewind.prop('disabled'), false);
    });

    test('Testing toJSON', function() {
      this.controller.setGradientCategory('DOB');
      this.controller.setTrajectoryCategory('Treatment');
      this.controller.setSpeed(1.11);

      var obs = this.controller.toJSON();
      var exp = {'gradientCategory': 'DOB',
                 'trajectoryCategory': 'Treatment',
                 'speed': 1.11};
      deepEqual(obs, exp);
    });

    test('Testing fromJSON', function() {
      var json = {'gradientCategory': 'Treatment',
                  'trajectoryCategory': 'DOB',
                  'speed': 3.33};

      this.controller.fromJSON(json);
      equal(this.controller.getTrajectoryCategory(), 'DOB');
      equal(this.controller.getGradientCategory(), 'Treatment');
      equal(this.controller.getSpeed(), 3.33);

      equal(this.controller.$speed.slider('option', 'disabled'), false);
      equal(this.controller.$play.prop('disabled'), false);
      equal(this.controller.$pause.prop('disabled'), true);
      equal(this.controller.$rewind.prop('disabled'), true);

      equal(this.controller.playing, false);
      equal(this.controller.director, null);

      // let's add a dummy director and pretend there was something playing
      this.controller.director = {'This is a': 'dummy object'};
      this.controller.playing = true;

      this.controller.fromJSON(json);
      equal(this.controller.getTrajectoryCategory(), 'DOB');
      equal(this.controller.getGradientCategory(), 'Treatment');
      equal(this.controller.getSpeed(), 3.33);

      equal(this.controller.$speed.slider('option', 'disabled'), false);
      equal(this.controller.$play.prop('disabled'), false);
      equal(this.controller.$pause.prop('disabled'), true);
      equal(this.controller.$rewind.prop('disabled'), true);

      equal(this.controller.playing, false);
      equal(this.controller.director, null);
    });

  });
});
