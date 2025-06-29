requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'viewcontroller',
    'animationscontroller',
    'multi-model',
    'uistate'
], function($, _, model, DecompositionView, ViewControllers,
            AnimationsController, MultiModel, UIState) {
  $(document).ready(function() {
    var EmperorViewController = ViewControllers.EmperorViewController;
    var DecompositionModel = model.DecompositionModel;

    QUnit.module('AnimationsController', {
      beforeEach() {
        this.sharedDecompositionViewDict = {};

        var state = new UIState();
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
        var multiModel = new MultiModel({'scatter': decomp});
        var dv = new DecompositionView(multiModel, 'scatter', state);
        this.sharedDecompositionViewDict.scatter = dv;

      },
      afterEach() {
        this.sharedDecompositionViewDict = undefined;
        this.decomp = undefined;
      }
    });

   QUnit.test('Constructor tests', function(assert) {
     const done = assert.async();

     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                          'width:12px"></div>');
     var controller = new AnimationsController(
         new UIState(),
         container,
          this.sharedDecompositionViewDict
     );

      assert.ok(AnimationsController.prototype instanceof
                EmperorViewController);

     assert.equal(controller.title, 'Animations');
     assert.equal(controller.director, null);
     assert.equal(controller.playing, false);

     $(function() {
         assert.equal(controller.enabled, false);
         assert.equal(controller.$speed.slider('option', 'disabled'),
                      true);
         assert.equal(controller._grid.getOptions().editable, false);
         assert.equal(controller.$radius.slider('option', 'disabled'),
                      true);
         assert.equal(controller.$play.prop('disabled'),
                      true);
         assert.equal(controller.$pause.prop('disabled'),
                      true);
         assert.equal(controller.$rewind.prop('disabled'),
                      true);

         assert.equal(controller.getGradientCategory(), '');
         assert.equal(controller.getTrajectoryCategory(), '');
         assert.equal(controller.getSpeed(), 1);
         assert.equal(controller.getRadius(), 1);

         done();
     });
    });

   QUnit.test('Test speed setter/getter', function(assert) {
     const done = assert.async();
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                          'width:12px"></div>');
     var controller = new AnimationsController(
         new UIState(),
         container,
          this.sharedDecompositionViewDict
     );

     $(function() {
         assert.equal(controller.getSpeed(), 1);

         controller.setSpeed(1.11);
         assert.equal(controller.getSpeed(), 1.11);

         assert.throws(
             function() {
                 controller.setSpeed(-1);
             },
             Error,
             'An error is raised if an invalid speed is set'
         );

         controller.setSpeed(3.11);
         assert.equal(controller.getSpeed(), 3.11);

         assert.throws(
             function() {
                 controller.setSpeed(11);
             },
             Error,
             'An error is raised if an invalid speed is set'
         );
         done();
     });
    });

   QUnit.test('Test radius setter/getter', function(assert) {
     const done = assert.async();
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                          'width:12px"></div>');
     var controller = new AnimationsController(
         new UIState(),
         container,
          this.sharedDecompositionViewDict
     );

     $(function() {
         assert.equal(controller.getRadius(), 1);

         controller.setRadius(1.11);
         assert.equal(controller.getRadius(), 1.11);

         assert.throws(
             function() {
                 controller.setRadius(-1);
             },
             Error,
             'An error is raised if an invalid radius is set'
         );

         controller.setRadius(3.11);
         assert.equal(controller.getRadius(), 3.11);

         assert.throws(
             function() {
                 controller.setRadius(11);
             },
             Error,
             'An error is raised if an invalid radius is set'
         );
         done();
     });
    });

   QUnit.test('Test gradient category setter/getter', function(assert) {
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AnimationsController(
          new UIState(),
          container,
          this.sharedDecompositionViewDict
      );

     controller.setGradientCategory('Treatment');
     assert.deepEqual(controller.getGradientCategory(), 'Treatment');

      controller.setGradientCategory('Does not exist');
     assert.deepEqual(controller.getGradientCategory(), '');

      controller.setGradientCategory('DOB');
     assert.deepEqual(controller.getGradientCategory(), 'DOB');
    });

   QUnit.test('Test trajectory category setter/getter', function(assert) {
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AnimationsController(
          new UIState(),
          container,
          this.sharedDecompositionViewDict
      );

     controller.setTrajectoryCategory('DOB');
     assert.equal(controller.getTrajectoryCategory(), 'DOB');
     assert.deepEqual(controller.getColors(), {});

      controller.setGradientCategory('Does not exist either');
     assert.equal(controller.getGradientCategory(), '');

      controller.setTrajectoryCategory('Treatment');
     assert.equal(controller.getTrajectoryCategory(), 'Treatment');
     assert.deepEqual(controller.getColors(), {});
    });

   QUnit.test('Test trajectory and category methods together',
     function(assert) {
         const done = assert.async();

         var container = $('<div id="does-not-exist" style="height:1000px; ' +
                           'width:12px"></div>');
         var controller = new AnimationsController(
             new UIState(),
             container,
             this.sharedDecompositionViewDict
         );

         $(function() {
             assert.equal(controller.getTrajectoryCategory(), '');
             assert.equal(controller.getGradientCategory(), '');
             assert.equal(controller.enabled, false);

             controller.setTrajectoryCategory('Treatment');
             assert.equal(controller.enabled, false);
             assert.deepEqual(controller.getColors(), {});

             controller.setGradientCategory('DOB');
             assert.equal(controller.enabled, true);
             assert.deepEqual(controller.getColors(), {'Fast': '#ff0000'});

             controller.setTrajectoryCategory('');
             assert.equal(controller.enabled, false);
             assert.deepEqual(controller.getColors(), {});

             done();
         });
    });

   QUnit.test('Test colors setter/getter', function(assert) {
     const done = assert.async();
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                          'width:12px"></div>');
     var controller = new AnimationsController(
         new UIState(),
         container,
          this.sharedDecompositionViewDict
     );

       controller.setTrajectoryCategory('Treatment');
       controller.setGradientCategory('DOB');

      $(function() {
          assert.deepEqual(controller.getColors(), {'Fast': '#ff0000'});

          controller.setColors({'Fast': 'green'});
          assert.deepEqual(controller.getColors(), {'Fast': 'green'});

          done();
      });
    });


   QUnit.test('Test drawFrame', function(assert) {
      const done = assert.async();
      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                          'width:12px"></div>');
      var controller = new AnimationsController(
          new UIState(),
          container,
          this.sharedDecompositionViewDict
      );

      // 3 event tests
      assert.expect(3);

      controller.setGradientCategory('DOB');
      controller.setTrajectoryCategory('Treatment');

      controller.addEventListener('animation-new-frame-started',
                                       function(cont) {
       assert.equal(cont.message.frame, 0);
       assert.equal(cont.message.gradientPoint, 20070314);
       assert.equal(cont.type, 'animation-new-frame-started');
       done();
      });

      $(function() {
          controller._playButtonClicked();
          controller.drawFrame();
          controller.drawFrame();
      });
    });

   QUnit.test('Test _pauseButtonClicked', function(assert) {
     const done = assert.async();
     var container = $('<div id="does-not-exist" style="height:1000px; ' +
                       'width:12px"></div>');

     var controller = new AnimationsController(
          new UIState(),
          container,
          this.sharedDecompositionViewDict
      );

      // 7 UI tests + 3 event tests
      assert.expect(10);

      controller.setGradientCategory('DOB');
      controller.setTrajectoryCategory('Treatment');
      controller.playing = true;

      $(function() {
          controller._updateButtons();

          controller.addEventListener('animation-paused', function(cont) {
              assert.equal(cont.message.gradient, 'DOB');
              assert.equal(cont.message.trajectory, 'Treatment');
              assert.equal(cont.type, 'animation-paused');
          });

          controller._pauseButtonClicked();

          setTimeout(function() {
              assert.equal(controller.playing, false);
              assert.equal(controller.$speed.slider('option', 'disabled'),
                           false);
              assert.equal(controller._grid.getOptions().editable, true);
              assert.equal(controller.$radius.slider('option', 'disabled'),
                           false);
              assert.equal(controller.$play.prop('disabled'), false);
              assert.equal(controller.$pause.prop('disabled'), true);
              assert.equal(controller.$rewind.prop('disabled'), true);
              done();
          }, 0);
      });
    });

   QUnit.test('Test _playButtonClicked', function(assert) {
      const done = assert.async();
      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                        'width:12px"></div>');

      var controller = new AnimationsController(
          new UIState(),
          container,
          this.sharedDecompositionViewDict
      );

      // 9 UI tests + 3 event tests
      assert.expect(12);

      controller.setGradientCategory('DOB');
      controller.setTrajectoryCategory('Treatment');
     assert.equal(controller.playing, false);

      controller.addEventListener('animation-started', function(cont) {
       assert.equal(cont.message.gradient, 'DOB');
       assert.equal(cont.message.trajectory, 'Treatment');
       assert.equal(cont.type, 'animation-started');
      });

      $(function() {
          controller._playButtonClicked();

          setTimeout(function() {
              assert.equal(controller.playing, true);
              assert.ok(controller.director !== null);

              assert.equal(controller.$speed.slider('option', 'disabled'),
                           true);
              assert.equal(controller._grid.getOptions().editable, false);
              assert.equal(controller.$radius.slider('option', 'disabled'),
                           true);
              assert.equal(controller.$play.prop('disabled'), true);
              assert.equal(controller.$pause.prop('disabled'), false);
              assert.equal(controller.$rewind.prop('disabled'), false);
              done();
          }, 0);
      });
    });

   QUnit.test('Test _rewindButtonClicked', function(assert) {
      const done = assert.async();
      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                        'width:12px"></div>');

      var controller = new AnimationsController(
          new UIState(),
          container,
          this.sharedDecompositionViewDict
      );

      // 9 UI tests + 3 event tests
      assert.expect(12);

      controller.setGradientCategory('DOB');
      controller.setTrajectoryCategory('Treatment');
     assert.equal(controller.playing, false);
      $(function() {
          controller._playButtonClicked();

          new Promise(function(resolve) {
              setTimeout(function() {
                  controller.addEventListener('animation-cancelled',
                  function(cont) {
                      assert.equal(cont.message.gradient, 'DOB');
                      assert.equal(cont.message.trajectory, 'Treatment');
                      assert.equal(cont.type, 'animation-cancelled');
                  });
                  controller._rewindButtonClicked();
                  resolve();
              }, 0);
          }).then(function() {
              setTimeout(function() {
                  assert.equal(controller.playing, false);
                  assert.ok(controller.director === null);

                  assert.equal(controller.$speed.slider('option', 'disabled'),
                               false);
                  assert.equal(controller._grid.getOptions().editable, true);
                  assert.equal(controller.$radius.slider('option', 'disabled'),
                               false);
                  assert.equal(controller.$play.prop('disabled'), false);
                  assert.equal(controller.$pause.prop('disabled'), true);
                  assert.equal(controller.$rewind.prop('disabled'), true);
                  done();
              }, 0);
          });
      });
    });

   QUnit.test('Test _updateButtons', function(assert) {
      const done = assert.async();
      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                        'width:12px"></div>');

      var controller = new AnimationsController(
          new UIState(),
          container,
          this.sharedDecompositionViewDict
      );

     $(function() {
         controller._updateButtons();

         assert.equal(controller.$speed.slider('option', 'disabled'), true);
         assert.equal(controller._grid.getOptions().editable, false);
         assert.equal(controller.$radius.slider('option', 'disabled'), true);
         assert.equal(controller.$play.prop('disabled'), true);
         assert.equal(controller.$pause.prop('disabled'), true);
         assert.equal(controller.$rewind.prop('disabled'), true);

         controller.setGradientCategory('DOB');
         controller.setTrajectoryCategory('Treatment');

         assert.equal(controller.$speed.slider('option', 'disabled'), false);
         assert.equal(controller._grid.getOptions().editable, true);
         assert.equal(controller.$radius.slider('option', 'disabled'), false);
         assert.equal(controller.$play.prop('disabled'), false);
         assert.equal(controller.$pause.prop('disabled'), true);
         assert.equal(controller.$rewind.prop('disabled'), true);

         /**
          *
          * The next few tests use a "dummy" director and pretend that the
          * animation is running, but can't actually run because there's no
          * render loop in the test suite.
          *
          */
         controller.director = {'Dummy object': 'placeholder'};
         controller.playing = true;
         controller._updateButtons();

         assert.equal(controller.$speed.slider('option', 'disabled'), true);
         assert.equal(controller._grid.getOptions().editable, false);
         assert.equal(controller.$radius.slider('option', 'disabled'), true);
         assert.equal(controller.$play.prop('disabled'), true);
         assert.equal(controller.$pause.prop('disabled'), false);
         assert.equal(controller.$rewind.prop('disabled'), false);

         controller.playing = false;
         controller._updateButtons();

         assert.equal(controller.$speed.slider('option', 'disabled'), true);
         assert.equal(controller._grid.getOptions().editable, false);
         assert.equal(controller.$radius.slider('option', 'disabled'), true);
         assert.equal(controller.$play.prop('disabled'), false);
         assert.equal(controller.$pause.prop('disabled'), true);
         assert.equal(controller.$rewind.prop('disabled'), false);
         done();
     });
    });

   QUnit.test('Testing toJSON', function(assert) {
      const done = assert.async();
      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                        'width:12px"></div>');

      var controller = new AnimationsController(
          new UIState(),
          container,
          this.sharedDecompositionViewDict
      );

      controller.setGradientCategory('DOB');
      controller.setTrajectoryCategory('Treatment');

      $(function() {
          controller.setSpeed(1.11);
          controller.setRadius(0.5);
          controller.setColors({'Fast': 'black'});

          var obs = controller.toJSON();
          var exp = {'gradientCategory': 'DOB',
                     'trajectoryCategory': 'Treatment',
                     'speed': 1.11, 'radius': 0.5, 'colors': {'Fast': 'black'}};
          assert.deepEqual(obs, exp);
          done();
      });
    });

   QUnit.test('Testing fromJSON', function(assert) {
      const done = assert.async();
      var container = $('<div id="does-not-exist" style="height:1000px; ' +
                        'width:12px"></div>');

      var controller = new AnimationsController(
          new UIState(),
          container,
          this.sharedDecompositionViewDict
      );

      var json = {'gradientCategory': 'Treatment',
                  'trajectoryCategory': 'DOB',
                  'speed': 3.33, 'radius': 0.5, 'colors': {'Fast': 'blue'}};

     $(function() {
         controller.fromJSON(json);
         assert.equal(controller.getTrajectoryCategory(), 'DOB');
         assert.equal(controller.getGradientCategory(), 'Treatment');
         assert.equal(controller.getSpeed(), 3.33);
         assert.equal(controller.getRadius(), 0.5);
         assert.deepEqual(controller.getColors(), {'Fast': 'blue'});

         assert.equal(controller.$speed.slider('option', 'disabled'), false);
         assert.equal(controller._grid.getOptions().editable, true);
         assert.equal(controller.$radius.slider('option', 'disabled'), false);
         assert.equal(controller.$play.prop('disabled'), false);
         assert.equal(controller.$pause.prop('disabled'), true);
         assert.equal(controller.$rewind.prop('disabled'), true);

         assert.equal(controller.playing, false);
         assert.equal(controller.director, null);

         // let's add a dummy director and pretend there was something playing
         controller.director = {'This is a': 'dummy object'};
         controller.playing = true;

         controller.fromJSON(json);
         assert.equal(controller.getTrajectoryCategory(), 'DOB');
         assert.equal(controller.getGradientCategory(), 'Treatment');
         assert.equal(controller.getSpeed(), 3.33);
         assert.equal(controller.getRadius(), 0.5);
         assert.deepEqual(controller.getColors(), {'Fast': 'blue'});

         assert.equal(controller.$speed.slider('option', 'disabled'), false);
         assert.equal(controller._grid.getOptions().editable, true);
         assert.equal(controller.$radius.slider('option', 'disabled'), false);
         assert.equal(controller.$play.prop('disabled'), false);
         assert.equal(controller.$pause.prop('disabled'), true);
         assert.equal(controller.$rewind.prop('disabled'), true);

         assert.equal(controller.playing, false);
         assert.equal(controller.director, null);
         done();
     });
    });

  });
});
