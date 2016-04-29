define([
    "jquery",
    "underscore",
    "viewcontroller",
    "chroma",
    "slickformatters",
    "slickeditors"
], function ($, _, ViewControllers, chroma, slickformatters, slickeditors) {

  // we only use the base attribute class, no need to get the base class
  var EmperorAttributeABC = ViewControllers.EmperorAttributeABC;

  /**
   * @name VisibilityController
   *
   * @class Manipulates and displays the visibility of objects on screen.
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
   * metadata category to visualize by.
   **/

  /*
   * @name VisibilityController
   *
   * @param {Node} container, Container node to create the controller in.
   * @params {Object} [decompViewDict] This object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   *
   **/
  function VisibilityController(container, decompViewDict){
    var helpmenu = 'Change the visibility of the attributes on the plot, such as ' +
      'spheres, vectors and ellipsoids.';
    var title = 'Visibility';

    // Constant for width in slick-grid
    var SLICK_WIDTH = 25, scope = this;

    // Build the options dictionary
    var options = {'valueUpdatedCallback':function(e, args) {
      var visible = args.item.value;
      var group = args.item.plottables;
      var element = scope.decompViewDict[scope.getActiveDecompViewKey()];
      VisibilityController.setPlottableAttributes(element, visible, group);
    },
      'categorySelectionCallback':function(evt, params) {
        var category = scope.$select.val();

        var k = scope.getActiveDecompViewKey();
        var decompViewDict = scope.decompViewDict[k];

        // getting all unique values per categories
        var uniqueVals = decompViewDict.decomp.getUniqueValuesByCategory(category);
        // getting color for each uniqueVals
        var attributes = {};
        _.each(uniqueVals, function(value) {
          attributes[value] = true;
        });
        // fetch the slickgrid-formatted data
        var data = decompViewDict.setCategory(attributes, VisibilityController.setPlottableAttributes, category);

        scope.setSlickGridDataset(data);
      },
      'slickGridColumn':{id: 'title', name: '', field: 'value',
        sortable: false, maxWidth: SLICK_WIDTH,
        minWidth: SLICK_WIDTH,
        autoEdit: true,
        formatter: Slick.Formatters.Checkmark,
        editor: Slick.Editors.Checkbox}};

    EmperorAttributeABC.call(this, container, title, helpmenu,
        decompViewDict, options);
    return this;
  }
  VisibilityController.prototype = Object.create(EmperorAttributeABC.prototype);
  VisibilityController.prototype.constructor = EmperorAttributeABC;

  VisibilityController.prototype.toJSON = function() {
    var json = {};
    json.category = this.$select.val();

    //get visbility status to save
    var meta_pos = this.decompViewDict.scatter.decomp.md_headers.indexOf(json.category);
    var markers = this.decompViewDict.scatter.markers;
    var metadata = this.decompViewDict.scatter.decomp.plottable;

    var visible = {};
    for (var i = 0; i < markers.length; i++) {
      var name = metadata[i].metadata[meta_pos];
      visible[name] = markers[i].visible;
    }
    json.visible = visible;
    return json;
  }

  VisibilityController.prototype.fromJSON = function(json) {
    this.$select.val(json.category);
    this.$select.trigger('chosen:updated');

    // fetch and set the slickgrid-formatted data
    var k = this.getActiveDecompViewKey();
      var data = this.decompViewDict[k].setCategory(json.visible, VisibilityController.setPlottableAttributes, json.category);
    this.setSlickGridDataset(data);
  }


  /**
   * Helper function to set the visibility of plottable
   *
   * @param {scope} object, the scope where the plottables exist
   * @param {visible} bool, visibility of the plottables
   * @param {group} array of objects, list of object that should be changed in
   * scope
   */
  VisibilityController.setPlottableAttributes = function(scope, visible, group){
    var idx;

    _.each(group, function(element) {
      idx = element.idx;
      scope.markers[idx].visible = visible;
    });
  };

  return VisibilityController;
});
