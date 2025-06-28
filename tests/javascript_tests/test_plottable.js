requirejs(['jquery', 'model'], function($, model) {
  $(document).ready(function() {
    var Plottable = model.Plottable;

    QUnit.module('Plottable', {

      beforeEach () {
      },

      afterEach () {
      }
    });

    /**
     *
     * Test that the Plottable object is initialized correctly, without
     * optional arguments.
     *
     */
   QUnit.test('Test constructor',  function(assert) {
      var plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2]);

     assert.equal(plot.name, 'foo', 'The name matches!');
     assert.deepEqual(plot.metadata, ['a', 'b', 'c'], 'The metadata match!');
     assert.deepEqual(plot.coordinates, [0.2, 0.3, 0.5, 0.2], 'The coordinates ' +
          'match!');

      // optional arguments get default values
     assert.equal(plot.idx, -1, 'The index value was set correctly!');
     assert.deepEqual(plot.ci, [], 'The confidence intervals were set correctly!');
    });

    /**
     *
     * Test that the Plottable object is initialized correctly, with optional
     * arguments.
     *
     */
   QUnit.test('Test constructor optional+',  function(assert) {
      var plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2], 1);

     assert.equal(plot.name, 'foo', 'The name matches!');
     assert.deepEqual(plot.metadata, ['a', 'b', 'c'], 'The metadata matches!');
     assert.deepEqual(plot.coordinates, [0.2, 0.3, 0.5, 0.2], 'The coordinates ' +
          'match!');

     assert.equal(plot.idx, 1, 'The index value was set correctly!');
     assert.deepEqual(plot.ci, [], 'The confidence intervals were set correctly!');

      plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2], 1,
          [3, 2, 3, 4]);

     assert.equal(plot.name, 'foo', 'The name matches!');
     assert.deepEqual(plot.metadata, ['a', 'b', 'c'], 'The metadata matches!');
     assert.deepEqual(plot.coordinates, [0.2, 0.3, 0.5, 0.2], 'The coordinates ' +
          'match!');

     assert.equal(plot.idx, 1, 'The index value was set correctly');
     assert.deepEqual(plot.ci, [3, 2, 3, 4], 'The confidence intervals were set ' +
          'correctly');
    });

    /**
     *
     * Test that the Plottable object raises an exception with invalid
     * arguments.
     *
     */
   QUnit.test('Test constructor exceptions',  function(assert) {
      var result;

      // check this happens for all the properties
     assert.throws(
          function() {
            result = new Plottable('foo', ['x', 'y', 'z'],
                [0.2, 0.2, 0.5, 0, 111], 3, [0.2]);
          },
          Error,
          'An error is raised if the number of coordinates does not ' +
          'correspond to the number confidence intervals.'
          );
    });

   QUnit.test('Test toString method',  function(assert) {
      //check what happens with toString
      var plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2], 1);
     assert.equal(plot.toString(), 'Sample: foo located at: (0.2, 0.3, 0.5, 0.2) ' +
          'metadata: [a, b, c] at index: 1 and without confidence intervals.',
          'Test correctly converted Plottable to string type.');

      plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2], 1,
          [0.2, 0.05, 0.01, 0.2]);
     assert.equal(plot.toString(), 'Sample: foo located at: (0.2, 0.3, 0.5, 0.2) ' +
          'metadata: [a, b, c] at index: 1 and with confidence intervals at ' +
          '(0.2, 0.05, 0.01, 0.2).',
          'Test correctly converted Plottable to string type with confidence' +
          ' intervals.');

      plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2]);
     assert.equal(plot.toString(), 'Sample: foo located at: (0.2, 0.3, 0.5, 0.2) ' +
          'metadata: [a, b, c] without index and without confidence intervals.',
          'Test correctly converted Plottable to string type without index.');

    });
  });
});
