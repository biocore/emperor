define([
    'jquery',
    'underscore',
    'viewcontroller',
    'scale-editor'
], function($, _, ViewControllers, ScaleEditor) {

  // we only use the base attribute class, no need to get the base class
  var EmperorAttributeABC = ViewControllers.EmperorAttributeABC;

  /**
   * @class ScaleViewController
   *
   * Alters the scale of points displayed on the screen.
   *
   * @param {Node} container Container node to create the controller in.
   * @param {Object} decompViewDict This object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   *
   * @return {ScaleViewController}
   * @constructs ScaleViewController
   * @extends EmperorAttributeABC
   *
   **/
  function ScaleViewController(container, decompViewDict) {
    var helpmenu = 'Change the scale of the attributes on the plot, allowing ' +
                   'highlighting of points using size.';
    var title = 'Scale';
    // Create checkbox for scaling by values
    /**
     * jQuery node for checkbox controlling whether to scale by values or not
     * @type {Node}
     */
    this.$scaledValue = $("<input type='checkbox'>");
    /**
     * jQuery node for label of $scaledValues
     * @type {Node}
     */
    this.$scaledLabel = $("<label for='scaledValue'>Scale by values</label>");

    //Create global scale bar
    /**
     * jQuery node for global scale bar container div
     * @type {Node}
     */
    this.$globalDiv = $('<div style="width:100%;padding:5px;">');
    this.$globalDiv.html('<p>Global Scaling</p>');
    var $sliderDiv = $('<div style="width:80%;display:inline-block;">');
    var $viewval = $('<input type="text" value="1.0" readonly ' +
                     'style="border:0;width:25px;' +
                     'background-color:rgb(238, 238, 238)">');
    /**
     * jQuery node for global scale bar
     * @type {Node}
     */
    this.$sliderGlobal = $sliderDiv.slider({
        range: 'max',
        min: 0.1,
        max: 5.0,
        value: 1.0,
        step: 0.1,
        slide: function(event, ui) {
          $viewval.val(ui.value);
          // Update the slickgrid values with the new scale
          var data = scope.getSlickGridDataset();
          _.each(data, function(element) {
            element.value = ui.value;
          });
          scope.setSlickGridDataset(data);

          //Update the scales for all meshes
          var dv = scope.decompViewDict[scope.getActiveDecompViewKey()];
          _.each(dv.markers, function(element) {
            element.scale.set(ui.value, ui.value, ui.value);
          });
          dv.needsUpdate = true;
        }
      });
    this.$globalDiv.append($sliderDiv);
    this.$globalDiv.append($viewval);

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
        var scaled = scope.$scaledValue.is(':checked');
        var attributes = ScaleViewController.getScale(uniqueVals, scaled);

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
    this.$header.append(this.$scaledValue);
    this.$header.append(this.$scaledLabel);
    this.$body.prepend(this.$globalDiv);
    return this;
  }
  ScaleViewController.prototype = Object.create(EmperorAttributeABC.prototype);
  ScaleViewController.prototype.constructor = EmperorAttributeABC;

  /**
   * Helper function to set the scale of plottable
   *
   * @param {Object} scope The scope where the plottables exist
   * @param {Boolean} scale New scaling factor of the plottables
   * (1.0 being standard scale)
   * @param {Object[]} group list of mesh objects that should be changed
   * in scope
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

  ScaleViewController.getScale = function(values, scaled) {
    var scale = {};
    _.each(values, function(element) {
      scale[element] = 1.0;
    });
    return scale;
  };

  return ScaleViewController;
});
