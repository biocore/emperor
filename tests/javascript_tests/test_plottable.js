requirejs(['jquery', 'model'], function($, model) {
  $(document).ready(function() {
    var Plottable = model.Plottable;

    module('Plottable', {

      setup: function() {
      },

      teardown: function() {
      }
    });

    /**
     *
     * Test that the Plottable object is initialized correctly, without
     * optional arguments.
     *
     */
    test('Test constructor', function() {
      var plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2]);

      equal(plot.name, 'foo', 'The name matches!');
      deepEqual(plot.metadata, ['a', 'b', 'c'], 'The metadata match!');
      deepEqual(plot.coordinates, [0.2, 0.3, 0.5, 0.2], 'The coordinates ' +
          'match!');

      // optional arguments get default values
      equal(plot.idx, -1, 'The index value was set correctly!');
      deepEqual(plot.ci, [], 'The confidence intervals were set correctly!');
    });

    /**
     *
     * Test that the Plottable object is initialized correctly, with optional
     * arguments.
     *
     */
    test('Test constructor optional+', function() {
      var plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2], 1);

      equal(plot.name, 'foo', 'The name matches!');
      deepEqual(plot.metadata, ['a', 'b', 'c'], 'The metadata matches!');
      deepEqual(plot.coordinates, [0.2, 0.3, 0.5, 0.2], 'The coordinates ' +
          'match!');

      equal(plot.idx, 1, 'The index value was set correctly!');
      deepEqual(plot.ci, [], 'The confidence intervals were set correctly!');

      plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2], 1,
          [3, 2, 3, 4]);

      equal(plot.name, 'foo', 'The name matches!');
      deepEqual(plot.metadata, ['a', 'b', 'c'], 'The metadata matches!');
      deepEqual(plot.coordinates, [0.2, 0.3, 0.5, 0.2], 'The coordinates ' +
          'match!');

      equal(plot.idx, 1, 'The index value was set correctly');
      deepEqual(plot.ci, [3, 2, 3, 4], 'The confidence intervals were set ' +
          'correctly');
    });

    /**
     *
     * Test that the Plottable object raises an exception with invalid
     * arguments.
     *
     */
    test('Test constructor exceptions', function() {
      var result;

      // check this happens for all the properties
      throws(
          function() {
            result = new Plottable('foo', ['x', 'y', 'z'],
                [0.2, 0.2, 0.5, 0, 111], 3, [0.2]);
          },
          Error,
          'An error is raised if the number of coordinates does not ' +
          'correspond to the number confidence intervals.'
          );
    });

    test('Test toString method', function() {
      //check what happens with toString
      var plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2], 1);
      equal(plot.toString(), 'Sample: foo located at: (0.2, 0.3, 0.5, 0.2) ' +
          'metadata: [a, b, c] at index: 1 and without confidence intervals.',
          'Test correctly converted Plottable to string type.');

      plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2], 1,
          [0.2, 0.05, 0.01, 0.2]);
      equal(plot.toString(), 'Sample: foo located at: (0.2, 0.3, 0.5, 0.2) ' +
          'metadata: [a, b, c] at index: 1 and with confidence intervals at ' +
          '(0.2, 0.05, 0.01, 0.2).',
          'Test correctly converted Plottable to string type with confidence' +
          ' intervals.');

      plot = new Plottable('foo', ['a', 'b', 'c'], [0.2, 0.3, 0.5, 0.2]);
      equal(plot.toString(), 'Sample: foo located at: (0.2, 0.3, 0.5, 0.2) ' +
          'metadata: [a, b, c] without index and without confidence intervals.',
          'Test correctly converted Plottable to string type without index.');

    });
  });
});
