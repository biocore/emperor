define([
    'jquery',
    'underscore',
    'viewcontroller',
    'scale-editor'
], function($, _, ViewControllers, ScaleEditor) {

  // we only use the base attribute class, no need to get the base class
  var EmperorAttributeABC = ViewControllers.EmperorAttributeABC;

  /*
   * @name ScaleViewController
   *
   * @param {Node} container Container node to create the controller in.
   * @params {Object} decompViewDict This object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   *
   **/
  function ScaleViewController(container, decompViewDict) {
    var helpmenu = 'Change the scale of the attributes on the plot, allowing ' +
                   'highlighting of points using size.';
    var title = 'Scale';

    // Constant for width in slick-grid
    var SLICK_WIDTH = 150, scope = this;

    // Build the options dictionary
    var options = {'valueUpdatedCallback': function(e, args) {
      var scale = args.item.value;
      var group = args.item.plottables;
      var element = scope.decompViewDict[scope.getActiveDecompViewKey()];
      scope.setPlottableAttributes(element, scale, group);
    },
      'categorySelectionCallback': function(evt, params) {
        var category = scope.$select.val();

        var k = scope.getActiveDecompViewKey();
        var decompViewDict = scope.decompViewDict[k];

        // getting all unique values per categories
        var uniqueVals = decompViewDict.decomp.getUniqueValuesByCategory(
          category);
        // getting scale value for each point
        var attributes = {};
        _.each(uniqueVals, function(value) {
          attributes[value] = 1.0;
        });
        // fetch the slickgrid-formatted data
        var data = decompViewDict.setCategory(
          attributes, scope.setPlottableAttributes, category);

        scope.setSlickGridDataset(data);
      },
      'slickGridColumn': {id: 'title', name: '', field: 'value',
        sortable: false, maxWidth: SLICK_WIDTH,
        minWidth: SLICK_WIDTH,
        autoEdit: true,
        //formatter: Slick.Formatters.Checkmark,
        editor: ScaleEditor.ScaleEditor}};

    EmperorAttributeABC.call(this, container, title, helpmenu,
        decompViewDict, options);
    return this;
  }
  ScaleViewController.prototype = Object.create(EmperorAttributeABC.prototype);
  ScaleViewController.prototype.constructor = EmperorAttributeABC;

  /**
   * Helper function to set the scale of plottable
   *
   * @param {Object} scope The scope where the plottables exist
   * @param {Boolean} scale New scale of the plottables
   * @param {Object[]} group list of mesh objects that should be changed
   * scope
   */
  ScaleViewController.prototype.setPlottableAttributes = function(
      scope, scale, group) {
    var idx;

    _.each(group, function(element) {
      idx = element.idx;
      scope.markers[idx].scale.set(scale, scale, scale);
    });
    scope.needsUpdate = true;
  };

  return ScaleViewController;
});
