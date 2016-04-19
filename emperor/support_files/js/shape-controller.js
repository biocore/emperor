define([
    "jquery",
    "underscore",
    "view",
    "viewcontroller",
    "three",
    "shape-editor",
    "shapes"
], function ($, _, DecompositionView, ViewControllers, three, Shape, shapes) {

  // we only use the base attribute class, no need to get the base class
  var EmperorAttributeABC = ViewControllers.EmperorAttributeABC;
  var ShapeEditor = Shape.ShapeEditor;
  var ShapeFormatter = Shape.ShapeFormatter;
  /**
   * @name ShapeController
   *
   * @class Manipulates and displays the shape of objects on screen.
   * @property {String} [title=""] Title of the controller.
   * @property {Node} [header=div node] jQuery element for the header
   * which contains the uppermost elements displayed in a tab.
   * @property {Node} [body=div node] jQuery element for the body,
   * which contains the lowermost elements displayed in tab.
   * This goes below the header.
   * @property {Node} [canvas=div node] jQuery element for the canvas,
   * which contains the header and the body.
   * @property {Node} [container=div node] jQuery element for the parent
   * container.
   * This only contains the canvas.
   * @property {Boolean} [active=false] Indicates whether the tab is front most
   * @property {String} [identifier="EMPtab-xxxxxxx"] Unique hash identifier
   * for the tab instance.
   * @property {Boolean} [enabled=true] Indicates if tab can be accessed.
   * @property {String} [description=""] Human-readable description of the tab.
   * @property {Node} [$select=chosen node] Drop-down menu to select the
   * metadata category to change shape for.
   **/

  /*
   * @name ShapeController
   *
   * @param {Node} container, Container node to create the controller in.
   * @params {Object} [decompViewDict] This is object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   *
   **/
  function ShapeController(container, decompViewDict) {
    var helpmenu = 'Change the shapes representing groups of data on the plot';
    var title = 'Shape';

    // Constant for width in slick-grid
    var SLICK_WIDTH = 100, scope = this;
    var name, value, shapeItem;

    // Build the options dictionary
    var options = {'valueUpdatedCallback': function(e, args) {
      var val = args.item.category, shape = args.item.value;
      var group = args.item.plottables;
      var element = scope.decompViewDict[scope.getActiveDecompViewKey()];
      ShapeController.setPlottableAttributes(element, shape, group);
    },
      'categorySelectionCallback': function(evt, params) {
        var category = scope.$select.val();

        var k = scope.getActiveDecompViewKey();
        var decompViewDict = scope.decompViewDict[k];

        // getting all unique values per categories
        var uniqueVals = decompViewDict.decomp.getUniqueValuesByCategory(category);

        // Reset all to shapes to default
        var attributes = {}
        for (var index in uniqueVals) {
          attributes[uniqueVals[index]] = 'sphere';
        }
        // fetch the slickgrid-formatted data

        var data = decompViewDict.setCategory(attributes, ShapeController.setPlottableAttributes, category);

        scope.setSlickGridDataset(data);
      },
      'slickGridColumn':{id: 'title', name: '', field: 'value',
        sortable: false, maxWidth: SLICK_WIDTH,
        minWidth: SLICK_WIDTH,
        autoEdit: true,
        editor: ShapeEditor,
        formatter: ShapeFormatter}};

    EmperorAttributeABC.call(this, container, title, helpmenu,
        decompViewDict, options);
    return this;
  }

  ShapeController.prototype = Object.create(EmperorAttributeABC.prototype);
  ShapeController.prototype.constructor = EmperorAttributeABC;

    /**
   * Helper function to set the shape of plottable
   *
   * @param {scope} object, the scope where the plottables exist
   * @param {shape} string, string representation of the shape to be applied
   * to the plottables.
   * @param {group} array of objects, list of object that should be changed in
   * scope
   */
  ShapeController.setPlottableAttributes = function(scope, shape, group) {
    var idx;
    var geometry = shapes.shapes[shape];
    if (geometry === undefined) {
      throw new Error('Unknown shape ' + shape);
    }

    _.each(group, function(element) {
      idx = element.idx;
      scope.markers[idx].geometry = geometry;
    });
  };
  return ShapeController;
});
