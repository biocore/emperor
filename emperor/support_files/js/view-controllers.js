/**
 *
 * @author Yoshiki Vazquez-Baeza
 * @copyright Copyright 2013--, The Emperor Project
 * @credits Yoshiki Vazquez-Baeza
 * @license BSD
 * @version 0.9.51-dev
 * @maintainer Yoshiki Vazquez-Baeza
 * @email josenavas@gmail.com
 * @status Development
 *
 */

/*
 * @name AttributeViewController
 *
 * @param {Node} container, Container node to create the controller in.
 * @param {String} attrName, Attribute name to control, can be one of 'color',
 * 'opacity' or 'visibility'.
 * @param {Float} width, Width in pixels for the controller;
 * @param {Float} height, Height in pixels for the controller;
 * @param {ScenePlotView} sceneViews, SceneViews to controll; Maybe remove and
 * add a callback. FIXME
 * @param {Object} options, Options to set to the controller before
 * initializaiton.
 *
 * A few sections of this class are based on SlickGrid's slick.grid.js
 *
 **/
function AttributeViewController(container, attrName, width, height,
                                 sceneViews, options){
  var $container, $canvas;
  var scope = this;

  this.grid = null;
  this.attrName = attrName;

  this._categorySelectionCallback = null;
  this._valueUpdatedCallback = null;
  this._slickGridColumn = null;

  // verify we have a valid container
  $container = $(container);
  if ($container.length < 1) {
    throw new Error("Emperor requires a valid container, " + container +
        " does not exist in the DOM.");
  }

  /*
   *
   * Setup the needed properties to properly create the interface, mainly we
   * will be setting up the following few features:
   *
   * + Callback that responds to category selection change.
   * + Callback that responds to a value being updated.
   * + Column configuration for SlickGrid.
   *
   **/
  this._attrInit = function() {
    if (scope.attrName === 'color'){
      scope._categorySelectionCallback = function(evt, params) {
        var newCategory = params.selected;

        // fetch the slickgrid-formatted data
        data = sceneViews[0].decViews[0].setCategoryColors('discrete-coloring-qiime',
                                                           newCategory);
        scope.grid.setData(data);
        scope.grid.invalidate();
        scope.grid.render();
      }
;

      // properly respond to color changes
      scope._valueUpdatedCallback = function(e, args) {
        var val = args.item.category, color = args.item.color, group = [];

        group = args.item.plottables;
        sceneViews[0].decViews[0].setGroupColor(color, group);
      };

      // we use our homebrewed color editor
      scope._slickGridColumn = {id: 'title', name: '', field: 'color',
                                sortable: false, maxWidth: 25, minWidth: 25,
                                editor: ColorEditor,
                                formatter: ColorFormatter};
    }
    else{
      throw new Error("The attribute '" + scope.attrName +
                      "' is not supported.");
    }
  };

  /*
   *
   * Initialize the controller's interface and setup the base properties.
   *
   **/
  this.init = function() {
    var columns, gridOptions;

    // initialize the base attributes
    this._attrInit();

    $canvas = $('<div></div>');
    $container.append($canvas);
    $canvas.width(width);
    $canvas.height(height);

    // setup the columns for the main grid
    columns = [scope._slickGridColumn,
               {id: 'field1', name: 'Category Name', field: 'category'}];

    gridOptions = {editable: true, enableAddRow: false,
                   enableCellNavigation: true, forceFitColumns: true};

    $(function() {
      scope.grid = new Slick.Grid($canvas, [], columns, gridOptions);

      // subscribe to events when a cell is changed
      scope.grid.onCellChange.subscribe(scope._valueUpdatedCallback);

      // fire a callback to initialize the data grid
      scope._categorySelectionCallback(null, {selected: $select.val()});

      // setup chosen
      $select.chosen({width: "100%", search_contains: true});
      $select.chosen().change(scope._categorySelectionCallback);

      // make the columns fit the available spce whenever the window resizes
      // http://stackoverflow.com/a/29835739
      $(window).resize(function() {
        scope.grid.setColumns(scope.grid.getColumns());
      });
    });

  };

  this.resize = function(width, height) {
    scope.grid.width(gridWidth);
    scope.grid.height(gridHeight);
  };

  this.init();
}

/*
 *
 * coming soon ...
 *
 **/
function AnimationsViewController(){

}

/*
 *
 * coming soon ...
 *
 **/
function LabelsViewController(){

}

/*
 *
 * coming soon ...
 *
 **/
function VisibleDimensionsViewController(){

}

/*
 *
 * coming soon ...
 *
 **/
function OptionsViewController(){

}

/*
 *
 * coming soon ...
 *
 **/
function SearchViewController(){

}
