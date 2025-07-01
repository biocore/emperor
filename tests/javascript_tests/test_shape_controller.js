requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'viewcontroller',
    'three',
    'shapecontroller',
    'shape-editor',
    'shapes',
    'multi-model',
    'uistate'
], function($, _, model, DecompositionView, viewcontroller, THREE,
            ShapeController, ShapeEditor, shapes, MultiModel, UIState) {
  $(document).ready(function() {
    var EmperorAttributeABC = viewcontroller.EmperorAttributeABC;
    var DecompositionModel = model.DecompositionModel;

    QUnit.module('Shape Controller', {
      beforeEach() {
        // setup function
        this.shapesAvailable = ['Sphere', 'Diamond', 'Cone', 'Cylinder',
                                'Ring', 'Square', 'Icosahedron', 'Star'];
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
        var metadata = [
          ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
          ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112']
        ];

        var decomp = new DecompositionModel(data, md_headers, metadata);
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
        this.decomp = new DecompositionModel(data, md_headers, metadata,
                                             'arrow');
        this.multiModel = new MultiModel({'scatter': this.decomp});
        this.dv = new DecompositionView(this.multiModel, 'scatter', UIState1);
        this.sharedDecompositionViewDict.biplot = this.dv;

      },

      afterEach() {
        // teardown function
        this.sharedDecompositionViewDict = undefined;
        this.controller = undefined;
      }
    });

   QUnit.test('Shapes dropdown', function(assert) {
      var values = [];
      shapes.$shapesDropdown.find('option').each(function() {
          values.push($(this).attr('value'));
      });
     assert.deepEqual(values, this.shapesAvailable);
    });

   QUnit.test('Constructor tests', function(assert) {
      const done = assert.async();
      assert.ok(ShapeController.prototype instanceof EmperorAttributeABC);

       var container = $('<div id="does-not-exist" style="height:11px; ' +
                         'width:12px"></div>');

      var controller = new ShapeController(new UIState(),
                                           container,
                                           this.sharedDecompositionViewDict);


     $(function() {
         assert.equal(controller.title, 'Shape');

         var testColumn = controller.bodyGrid.getColumns()[0];
         assert.equal(testColumn.field, 'value');

         // test filtering of the decompositon
         assert.ok(controller.decompViewDict.biplot === undefined);
         done();
     });

    });

   QUnit.test('Test getGeometry', function(assert) {
      var geom;

      geom = shapes.getGeometry('Sphere', 0.06);
     assert.equal(geom.parameters.radius, 0.06);

      geom = shapes.getGeometry('Square', 0.06);
     assert.equal(geom.parameters.width, 0.12);
     assert.equal(geom.parameters.height, 0.12);

      geom = shapes.getGeometry('Cone', 0.06);
     assert.equal(geom.parameters.radiusTop, 0.06);
     assert.equal(geom.parameters.radiusBottom, 0);
     assert.equal(geom.parameters.height, 0.12);

      geom = shapes.getGeometry('Icosahedron', 0.06);
     assert.equal(geom.parameters.radius, 0.06);

      geom = shapes.getGeometry('Diamond', 0.06);
     assert.equal(geom.parameters.radius, 0.06);

      geom = shapes.getGeometry('Ring', 0.06);
     assert.equal(geom.parameters.innerRadius, 0.06 / 1.618033);
     assert.equal(geom.parameters.outerRadius, 0.06);

      geom = shapes.getGeometry('Cylinder', 0.06);
     assert.equal(geom.parameters.radiusTop, 0.06);
     assert.equal(geom.parameters.radiusBottom, 0.06);
     assert.equal(geom.parameters.height, 0.12);
    });

   QUnit.test('Check getGeometry raises an exception with unknown shape',
         function(assert) {
     assert.throws(function() {
        shapes.getGeometry('Geometry McGeometryface', 0.06);
      }, Error, 'Throw error if unknown shape given');
    });

   QUnit.test('Testing setPlottableAttributes helper function',
     function(assert) {
      // testing with one plottable
      var idx = 0, view = this.sharedDecompositionViewDict.scatter;

       var container = $('<div id="does-not-exist" style="height:11px; ' +
                         'width:12px"></div>');

      var controller = new ShapeController(new UIState(),
                                           container,
                                           this.sharedDecompositionViewDict);


     var plottables = [{idx: idx}];
     assert.equal(view.markers[idx].geometry.type, 'SphereGeometry');
     assert.equal(view.markers[idx + 1].geometry.type, 'SphereGeometry');
     controller.setPlottableAttributes(view, 'Square', plottables);

     assert.equal(view.markers[idx].geometry.type, 'PlaneGeometry');
     assert.equal(view.markers[idx + 1].geometry.type, 'SphereGeometry');
     assert.equal(view.needsUpdate, true);

      // testing with multiple plottable
      plottables = [{idx: idx}, {idx: idx + 1}];
     controller.setPlottableAttributes(view, 'Cylinder', plottables);

     assert.equal(view.markers[idx].geometry.type, 'CylinderGeometry');
     assert.equal(view.markers[idx + 1].geometry.type, 'CylinderGeometry');
     assert.equal(view.needsUpdate, true);
    });

   QUnit.test('Testing setPlottableAttributes unknown shape', function(assert) {
      // testing with one plottable
      var plottables = [{0: 0}], view;
      view = this.sharedDecompositionViewDict.scatter;
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                         'width:12px"></div>');

      var controller = new ShapeController(new UIState(),
                                           container,
                                           this.sharedDecompositionViewDict);

     assert.throws(function() {
        controller.setPlottableAttributes(view, 'WEIRD', plottables);
      }, Error, 'Throw error if unknown shape given');

    });

   QUnit.test('Testing toJSON', function(assert) {
      const done = assert.async();
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                         'width:12px"></div>');

      var controller = new ShapeController(new UIState(),
                                           container,
                                           this.sharedDecompositionViewDict);

      $(function() {
          controller.setMetadataField('DOB');
          var obs = controller.toJSON();
          var exp = {category: 'DOB',
                     data: {'20070314': 'Sphere', '20071112': 'Sphere'}
                    };
          assert.deepEqual(obs, exp);
          done();
      });
    });

   QUnit.test('Testing fromJSON', function(assert) {
      const done = assert.async();

      var container = $('<div id="does-not-exist" style="height:11px; ' +
                         'width:12px"></div>');

      var controller = new ShapeController(new UIState(),
                                           container,
                                           this.sharedDecompositionViewDict);

      var json = {'category': 'SampleID',
                  'data': {'PC.636': 'Square', 'PC.635': 'Sphere'}
      };

      $(function() {
          controller.fromJSON(json);
          var idx = 0;
          assert.equal(
              controller.decompViewDict.scatter.markers[idx].geometry.type,
              'PlaneGeometry'
          );

          idx += 1;
          assert.equal(
              controller.decompViewDict.scatter.markers[idx].geometry.type,
              'SphereGeometry'
          );
          done();
      });
    });

   QUnit.test('Testing toJSON (null)', function(assert) {
      const done = assert.async();
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                         'width:12px"></div>');

      var controller = new ShapeController(new UIState(),
                                           container,
                                           this.sharedDecompositionViewDict);

      $(function() {
          controller.setMetadataField(null);
          var obs = controller.toJSON();
          var exp = {category: null, data: {}};
          assert.deepEqual(obs, exp);
          done();
      });
    });

   QUnit.test('Testing fromJSON (null)', function(assert) {
      const done = assert.async();

      var container = $('<div id="does-not-exist" style="height:11px; ' +
                         'width:12px"></div>');

      var controller = new ShapeController(new UIState(),
                                           container,
                                           this.sharedDecompositionViewDict);

      var json = {'category': null, 'data': {}};

      $(function() {
          controller.fromJSON(json);
          var idx = 0;
          assert.equal(
              controller.decompViewDict.scatter.markers[idx].geometry.type,
              'SphereGeometry'
          );

          idx += 1;
          assert.equal(
              controller.decompViewDict.scatter.markers[idx].geometry.type,
              'SphereGeometry'
          );
          done();
      });
    });

  });
});
