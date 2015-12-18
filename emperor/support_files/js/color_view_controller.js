/*
 * @name ColorViewController
 *
 * @param {Node} container, Container node to create the controller in.
 * @params {Object} [decompViewDict] This is object is keyed by unique
 * identifiers and the values are DecompositionView objects referring to a set
 * of objects presented on screen. This dictionary will usually be shared by
 * all the tabs in the application. This argument is passed by reference.
 *
 **/
function ColorViewController(container, decompViewDict){
  var helpmenu = 'Change the colors of the attributes on the plot, such as ' +
                 'spheres, vectors and ellipsoids.';
  var title = 'Color';

  // Constant for width in slick-grid
  var SLICK_WIDTH = 25;
  var scope = this;
  
  // Build the options dictionary
  var options = {'valueUpdatedCallback':function(e, args) {
                   var val = args.item.category, color = args.item.color, group = [];
                   group = args.item.plottables;
                   decompViewDict[this.getActiveDecompViewKey()].setGroupColor(color, group);
                 },
                 'categorySelectionCallback':function(evt, params) {
                   var newCategory = params.selected;

                   // fetch the slickgrid-formatted data
                   var data = decompViewDict[scope.getActiveDecompViewKey()].setCategoryColors(
                     'discrete-coloring-qiime', newCategory);
                   scope.setSlickGridDataset(data);
                 },
                 'slickGridColumn':{id: 'title', name: '', field: 'color',
                                    sortable: false, maxWidth: SLICK_WIDTH,
                                    minWidth: SLICK_WIDTH,
                                    editor: ColorEditor,
                                    formatter: ColorFormatter}};

  EmperorAttributeABC.call(this, container, title, helpmenu,
                           decompViewDict, options);
  return this;
};
ColorViewController.prototype = Object.create(EmperorAttributeABC.prototype);
ColorViewController.prototype.constructor = EmperorAttributeABC;

