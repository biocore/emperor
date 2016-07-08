requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'viewcontroller',
    'three',
    'shapecontroller',
    'shape-editor',
    'shapes'
], function($, _, model, DecompositionView, viewcontroller, THREE,
            ShapeController, ShapeEditor, shapes) {
  $(document).ready(function() {
    var EmperorAttributeABC = viewcontroller.EmperorAttributeABC;
    var DecompositionModel = model.DecompositionModel;

    module('Shape Controller', {
      setup: function() {
        // setup function
        this.shapesAvailable = ['Sphere', 'Cube', 'Cone', 'Icosahedron',
                                'Cylinder'];
        this.sharedDecompositionViewDict = {};

        // setup function
        var name = 'pcoa';
        var ids = ['PC.636', 'PC.635'];
        coords = [
          [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
          -0.229889, -0.046599],
          [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
          -0.112864, 0.064794]];
        var pct_var = [26.6887048633, 16.2563704022, 13.7754129161,
                       11.217215823, 10.024774995, 8.22835130237,
                       7.55971173665, 6.24945796136];
        var md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment',
                          'DOB'];
        var metadata = [
          ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
          ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112']
        ];
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
      },

      teardown: function() {
        // teardown function
      }
    });

    test('Shapes dropdown', function() {
      var values = [];
      shapes.$shapesDropdown.find('option').each(function() {
          values.push($(this).attr('value'));
      });
      deepEqual(values, this.shapesAvailable);
    });

    test('Constructor tests', function(assert) {
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                        'width:12px"></div>');

      assert.ok(ShapeController.prototype instanceof EmperorAttributeABC);

      var controller = new ShapeController(container,
                                           this.sharedDecompositionViewDict);
      equal(controller.title, 'Shape');

      var testColumn = controller.bodyGrid.getColumns()[0];
      equal(testColumn.field, 'value');
    });

    test('Test getGeometry', function() {
      var geom, range;

      range = {'min': [-2, -1, -3], 'max': [3, 8, 9]};

      geom = shapes.getGeometry('Sphere', range);
      equal(geom.parameters.radius, 0.06);

      geom = shapes.getGeometry('Cube', range);
      equal(geom.parameters.width, 0.06);
      equal(geom.parameters.height, 0.06);
      equal(geom.parameters.depth, 0.06);

      geom = shapes.getGeometry('Cone', range);
      equal(geom.parameters.radiusTop, 0.024);
      equal(geom.parameters.radiusBottom, 0);
      equal(geom.parameters.height, 0.09);

      geom = shapes.getGeometry('Icosahedron', range);
      equal(geom.parameters.radius, 0.06);

      geom = shapes.getGeometry('Cylinder', range);
      equal(geom.parameters.radiusTop, 0.024);
      equal(geom.parameters.radiusBottom, 0.024);
      equal(geom.parameters.height, 0.09);
    });

    test('Check getGeometry raises an exception with unknown shape',
         function() {
      var range = {'min': [-2, -1, -3], 'max': [3, 8, 9]};
      throws(function() {
        shapes.getGeometry('Geometry McGeometryface', range);
      }, Error, 'Throw error if unknown shape given');
    });

    test('Testing setPlottableAttributes helper function', function(assert) {
      // testing with one plottable
      var idx = 0;
      plottables = [{idx: idx}];
      equal(this.dv.markers[idx].geometry.type, 'SphereGeometry');
      equal(this.dv.markers[idx + 1].geometry.type, 'SphereGeometry');
      ShapeController.prototype.setPlottableAttributes(this.dv, 'Cube',
                                                       plottables);
      equal(this.dv.markers[idx].geometry.type, 'BoxGeometry');
      equal(this.dv.markers[idx + 1].geometry.type, 'SphereGeometry');
      equal(this.dv.needsUpdate, true);

      // testing with multiple plottable
      plottables = [{idx: idx}, {idx: idx + 1}];
      ShapeController.prototype.setPlottableAttributes(this.dv, 'Cylinder',
                                                       plottables);
      equal(this.dv.markers[idx].geometry.type, 'CylinderGeometry');
      equal(this.dv.markers[idx + 1].geometry.type, 'CylinderGeometry');
      equal(this.dv.needsUpdate, true);
    });

    test('Testing setPlottableAttributes unknown shape', function(assert) {
      // testing with one plottable
      plottables = [{idx: idx}];
      throws(function() {
        ShapeController.prototype.setPlottableAttributes(this.dv, 'WEIRD',
                                                         plottables);
      }, Error, 'Throw error if unknown shape given');

    });

    test('Testing toJSON', function() {
      var container = $('<div id="does-not-exist" style="height:11px; ' +
                        'width:12px"></div>');
      var controller = new ShapeController(container,
                                           this.sharedDecompositionViewDict);

      var obs = controller.toJSON();
      var exp = {category: 'SampleID',
                 data: {'PC.636': 'Sphere', 'PC.635': 'Sphere'}
      };
      deepEqual(obs, exp);
    });

    test('Testing fromJSON', function() {
      var json = {'category': 'SampleID',
                  'data': {'PC.636': 'Cube', 'PC.635': 'Sphere'}
      };

      var container = $('<div id="does-not-exist" style="height:11px; ' +
                        'width:12px"></div>');
      var controller = new ShapeController(container,
                                           this.sharedDecompositionViewDict);

      controller.fromJSON(json);
      var idx = 0;
      equal(controller.decompViewDict.scatter.markers[idx].geometry.type,
            'BoxGeometry');
      equal(controller.decompViewDict.scatter.markers[idx + 1].geometry.type,
            'SphereGeometry');
    });

  });
});
