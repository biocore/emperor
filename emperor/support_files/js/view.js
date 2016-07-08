define([
    'jquery',
    'underscore',
    'three',
    'shapes'
], function($, _, THREE, shapes) {
/**
 *
 * @class DecompositionView
 *
 * Contains all the information on how the model is being presented to the
 * user.
 *
 * @param {DecompositionModel} decomp a DecompositionModel object that will be
 * represented on screen.
 *
 * @return {DecompositionView}
 * @constructs DecompositionView
 *
 */
function DecompositionView(decomp) {
  /**
   * The decomposition model that the view represents.
   * @type {DecompositionModel}
   */
  this.decomp = decomp;
  /**
   * Number of samples represented in the view.
   * @type {integer}
   */
  this.count = decomp.length;
  /**
   * Number of visible samples.
   * @type {integer}
   */
  this.visibleCount = this.count;
  /**
   * Top visible dimensions
   * @type {integer[]}
   * @default [0, 1, 2]
   */
  this.visibleDimensions = [0, 1, 2]; // We default to the first three PCs
  /**
   * Axes color.
   * @type {integer}
   * @default 0xFFFFFF (white)
   */
  this.axesColor = 0xFFFFFF;
  /**
   * Background color.
   * @type {integer}
   * @default 0x000000 (black)
   */
  this.backgroundColor = 0x000000;
  /**
   * Tube objects on screen (used for animations)
   * @type {THREE.Mesh[]}
   */
  this.tubes = [];
  /**
   * Array of THREE.Mesh objects on screen (represent samples).
   * @type {THREE.Mesh[]}
   */
  this.markers = [];
  /**
   * Array of line objects shown on screen (used for procustes and vector
   * plots).
   * @type {THREE.Line[]}
   */
  this.lines = [];

  // setup this.markers and this.lines
  this._initBaseView();

  /**
   * True when changes have occured that require re-rendering of the canvas
   * @type {boolean}
   */
  this.needsUpdate = true;
}

/**
 *
 * Helper method to initialize the base THREE.js objects.
 * @private
 *
 */
DecompositionView.prototype._initBaseView = function() {
  var mesh, x = this.visibleDimensions[0], y = this.visibleDimensions[1],
      z = this.visibleDimensions[2];
  var scope = this;

  // get the correctly sized geometry
  var geometry = shapes.getGeometry('Sphere', this.decomp.dimensionRanges);

  this.decomp.apply(function(plottable) {
    mesh = new THREE.Mesh(geometry, new THREE.MeshPhongMaterial());
    mesh.name = plottable.name;

    mesh.material.color = new THREE.Color(0xff0000);
    mesh.material.transparent = false;
    mesh.material.depthWrite = true;
    mesh.material.opacity = 1;
    mesh.matrixAutoUpdate = true;

    mesh.position.set(plottable.coordinates[x], plottable.coordinates[y],
                      plottable.coordinates[z]);

    mesh.updateMatrix();

    scope.markers.push(mesh);
  });

  // apply but to the adjacency list NOT IMPLEMENTED
  // this.decomp.applyAJ( ... ); Blame Jamie and Jose - baby steps buddy...

};

/**
 *
 * Change the visible coordinates
 *
 * @param {integer[]} newDims An Array of integers in which each integer is the
 * index to the principal coordinate to show
 *
 */
DecompositionView.prototype.changeVisibleDimensions = function(newDims) {
  if (newDims.length !== 3) {
    throw new Error('Only three dimensions can be shown at the same time');
  }

  this.visibleDimensions = newDims;

  var x = newDims[0], y = newDims[1], z = newDims[2], scope = this;
  this.decomp.apply(function(plottable) {
    mesh = scope.markers[plottable.idx];
    mesh.position.set(plottable.coordinates[x],
                      plottable.coordinates[y],
                      plottable.coordinates[z]);
    mesh.updateMatrix();
  });

  this.needsUpdate = true;
};

/**
 *
 * Reorient one of the visible dimensions.
 *
 * @param {integer} index The index of the dimension to re-orient, if this
 * dimension is not visible i.e. not in `this.visibleDimensions`, then the
 * method will return right away.
 *
 */
DecompositionView.prototype.flipVisibleDimension = function(index) {
  var pos, scope = this;

  index = this.visibleDimensions.indexOf(index);

  if (index !== -1) {
    this.decomp.apply(function(plottable) {
      mesh = scope.markers[plottable.idx];
      pos = mesh.position.toArray();

      // flip the axis
      pos[index] = pos[index] * -1;

      mesh.position.set(pos[0], pos[1], pos[2]);
      mesh.updateMatrix();
    });

    this.needsUpdate = true;
  }
};

/**
 * Change the plottables attributes based on the metadata category using the
 * provided setPlottableAttributes function
 *
 * @param {object} attributes Key:value pairs of elements and values to change
 * in plottables.
 * @param {function} setPlottableAttributes Helper function to change the
 * values of plottables, in general this should be implemented in the
 * controller but it can be nullable if not needed. setPlottableAttributes
 * should receive: the scope where the plottables exist, the value to be
 * applied to the plottables and the plotables to change. For more info
 * see ColorViewController.setPlottableAttribute
 * @see ColorViewController.setPlottableAttribute
 * @param {string} category The category/column in the mapping file
 *
 * @return {object[]} Array of objects to be consumed by Slick grid.
 *
 */
DecompositionView.prototype.setCategory = function(attributes,
                                                   setPlottableAttributes,
                                                   category) {
  var scope = this, dataView = [], plottables;

  _.each(attributes, function(value, key) {
    /*
     *
     * WARNING: This is mixing attributes of the view with the model ...
     * it's a bit of a gray area though.
     *
     **/
    plottables = scope.decomp.getPlottablesByMetadataCategoryValue(category,
                                                                   key);
    if (setPlottableAttributes !== null) {
      setPlottableAttributes(scope, value, plottables);
    }

    dataView.push({category: key, value: value, plottables: plottables});
  });
  this.needsUpdate = true;

  return dataView;
};

/**
 *
 * Change the color for a set of plottables.
 *
 * @param {integer} color An RGB color in hexadecimal format.
 * @param {Plottable[]} group Array of Plottables that will change in color.
 *
 */
DecompositionView.prototype.setGroupColor = function(color, group) {
  var idx;
  var scope = this;

  _.each(group, function(element) {
    idx = element.idx;
    scope.markers[idx].material.color = new THREE.Color(color);
  });
};
this.needsUpdate = true;

  return DecompositionView;
});
