define([
    'jquery',
    'underscore',
    'three',
    'shapes',
    'draw'
], function($, _, THREE, shapes, draw) {
  var makeArrow = draw.makeArrow;
  var makeLineCollection = draw.makeLineCollection;
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
   * Top visible dimensions
   * @type {integer[]}
   * @default [0, 1, 2]
   */
  this.visibleDimensions = [0, 1, 2]; // We default to the first three PCs
  /**
   * Orientation of the axes, `-1` means the axis is flipped, `1` means the
   * axis is not flipped.
   * @type {integer[]}
   * @default [1, 1, 1]
   */
  this.axesOrientation = [1, 1, 1];
  /**
   * Axes color.
   * @type {integer}
   * @default '#FFFFFF' (white)
   */
  this.axesColor = '#FFFFFF';
  /**
   * Background color.
   * @type {integer}
   * @default '#000000' (black)
   */
  this.backgroundColor = '#000000';
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
   * Array of THREE.Mesh objects on screen (represent confidence intervals).
   * @type {THREE.Mesh[]}
   */
  this.ellipsoids = [];
  /**
   * Object with THREE.LineSegments for the procrustes edges. Has a left and
   * a right attribute.
   * @type {Object}
   */
  this.lines = {'left': null, 'right': null};

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
  var radius = geometry.parameters.radius, hasConfidenceIntervals;

  hasConfidenceIntervals = this.decomp.hasConfidenceIntervals();

  if (this.decomp.isScatterType()) {
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

      scope.markers.push(mesh);

      if (hasConfidenceIntervals) {
        // copy the current sphere and make it an ellipsoid
        mesh = mesh.clone();

        mesh.name = plottable.name + '_ci';
        mesh.material.transparent = true;
        mesh.material.opacity = 0.5;

        mesh.scale.set(plottable.ci[x] / geometry.parameters.radius,
                       plottable.ci[y] / geometry.parameters.radius,
                       plottable.ci[z] / geometry.parameters.radius);

        scope.ellipsoids.push(mesh);
      }
    });
  }
  else if (this.decomp.isArrowType()) {
    var arrow, zero = [0, 0, 0], point;

    this.decomp.apply(function(plottable) {
      point = [plottable.coordinates[x],
               plottable.coordinates[y],
               plottable.coordinates[z]];
      arrow = makeArrow(zero, point, 0xc0c0c0, plottable.name);

      scope.markers.push(arrow);
    });
  }
  else {
    throw 'Unsupported decomposition type';
  }

  if (this.decomp.edges.length) {
    var left, center, right, u, v, verticesLeft = [], verticesRight = [];
    this.decomp.edges.forEach(function(edge) {
      u = edge[0];
      v = edge[1];

      // remember x, y and z
      center = [(u.coordinates[x] + v.coordinates[x]) / 2,
                (u.coordinates[y] + v.coordinates[y]) / 2,
                (u.coordinates[z] + v.coordinates[z]) / 2];

      left = [u.coordinates[x], u.coordinates[y], u.coordinates[z]];
      right = [v.coordinates[x], v.coordinates[y], v.coordinates[z]];

      verticesLeft.push(left, center);
      verticesRight.push(right, center);
    });

    this.lines.left = makeLineCollection(verticesLeft, 0xffffff);
    this.lines.right = makeLineCollection(verticesRight, 0xff0000);
  }
};

/**
 *
 * Get the number of visible elements
 *
 * @return {Number} The number of visible elements in this view.
 *
 */
DecompositionView.prototype.getVisibleCount = function() {
  var visible = 0;
  visible = _.reduce(this.markers, function(acc, marker) {
    return acc + (marker.visible + 0);
  }, 0);

  return visible;
};

/**
 *
 * Update the position of the markers, arrows and lines.
 *
 * This method is called by flipVisibleDimension and by changeVisibleDimensions
 * and will naively change the positions even if they haven't changed.
 *
 */
DecompositionView.prototype.updatePositions = function() {
  var x = this.visibleDimensions[0], y = this.visibleDimensions[1],
      z = this.visibleDimensions[2], scope = this, hasConfidenceIntervals,
      radius = 0, is2D = (z === null);

  hasConfidenceIntervals = this.decomp.hasConfidenceIntervals();

  // we need the original radius to scale confidence intervals (if they exist)
  if (hasConfidenceIntervals) {
    radius = scope.ellipsoids[0].geometry.parameters.radius;
  }

  if (this.decomp.isScatterType()) {
    this.decomp.apply(function(plottable) {
      mesh = scope.markers[plottable.idx];

      // always use the original data plus the axis orientation
      mesh.position.set(
        plottable.coordinates[x] * scope.axesOrientation[0],
        plottable.coordinates[y] * scope.axesOrientation[1],
        (is2D ? 0 : plottable.coordinates[z]) * scope.axesOrientation[2]);
      mesh.updateMatrix();

      if (hasConfidenceIntervals) {
        mesh = scope.ellipsoids[plottable.idx];

        mesh.position.set(
          plottable.coordinates[x] * scope.axesOrientation[0],
          plottable.coordinates[y] * scope.axesOrientation[1],
          (is2D ? 0 : plottable.coordinates[z]) * scope.axesOrientation[2]);

        // flatten the ellipsoids ever so slightly
        mesh.scale.set(plottable.ci[x] / radius, plottable.ci[y] / radius,
                       is2D ? 0.01 : plottable.ci[z] / radius);

        mesh.updateMatrix();
      }
    });
  }
  else if (this.decomp.isArrowType()) {
    var target, arrow;

    this.decomp.apply(function(plottable) {
      arrow = scope.markers[plottable.idx];

      target = new THREE.Vector3(
        plottable.coordinates[x] * scope.axesOrientation[0],
        plottable.coordinates[y] * scope.axesOrientation[1],
        (is2D ? 0 : plottable.coordinates[z]) * scope.axesOrientation[2]);

      arrow.setPointsTo(target);
    });
  }

  // edges are made using THREE.LineSegments and a buffer geometry so updating
  // the position takes a bit more work but these objects will render faster
  if (this.decomp.edges.length) {
    var left, center, right, u, v, positionsLeft, positionsRight, j = 0;
    positionsLeft = this.lines.left.geometry.attributes.position.array;
    positionsRight = this.lines.right.geometry.attributes.position.array;

    this.decomp.edges.forEach(function(edge) {
      u = edge[0];
      v = edge[1];

      // x, y and z are the visible dimensions (see above)
      center = [(u.coordinates[x] + v.coordinates[x]) / 2,
                (u.coordinates[y] + v.coordinates[y]) / 2,
                (u.coordinates[z] + v.coordinates[z]) / 2];

      left = [u.coordinates[x], u.coordinates[y], u.coordinates[z]];
      right = [v.coordinates[x], v.coordinates[y], v.coordinates[z]];

      positionsLeft[(j * 6)] = left[0] * scope.axesOrientation[0];
      positionsLeft[(j * 6) + 1] = left[1] * scope.axesOrientation[1];
      positionsLeft[(j * 6) + 2] = ((is2D ? 0 : left[2]) *
                                    scope.axesOrientation[2]);
      positionsLeft[(j * 6) + 3] = center[0] * scope.axesOrientation[0];
      positionsLeft[(j * 6) + 4] = center[1] * scope.axesOrientation[1];
      positionsLeft[(j * 6) + 5] = ((is2D ? 0 : center[2]) *
                                    scope.axesOrientation[2]);

      positionsRight[(j * 6)] = right[0] * scope.axesOrientation[0];
      positionsRight[(j * 6) + 1] = right[1] * scope.axesOrientation[1];
      positionsRight[(j * 6) + 2] = ((is2D ? 0 : right[2]) *
                                     scope.axesOrientation[2]);
      positionsRight[(j * 6) + 3] = center[0] * scope.axesOrientation[0];
      positionsRight[(j * 6) + 4] = center[1] * scope.axesOrientation[1];
      positionsRight[(j * 6) + 5] = ((is2D ? 0 : center[2]) *
                                     scope.axesOrientation[2]);

      j++;
    });

    // otherwise the geometry will remain unchanged
    this.lines.left.geometry.attributes.position.needsUpdate = true;
    this.lines.right.geometry.attributes.position.needsUpdate = true;
  }
  this.needsUpdate = true;
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

  // one by one, find and update the dimensions that are changing
  for (var i = 0; i < 3; i++) {
    if (this.visibleDimensions[i] !== newDims[i]) {
      // index represents the global position of the dimension
      var index = this.visibleDimensions[i],
          orientation = this.axesOrientation[i];

      // 1.- Correct the limits of the ranges for the dimension that we are
      // moving out of the scene i.e. the old dimension
      if (this.axesOrientation[i] === -1) {
        var max = this.decomp.dimensionRanges.max[index];
        var min = this.decomp.dimensionRanges.min[index];
        this.decomp.dimensionRanges.max[index] = min * (-1);
        this.decomp.dimensionRanges.min[index] = max * (-1);
      }

      // 2.- Set the orientation of the new dimension to be 1
      this.axesOrientation[i] = 1;

      // 3.- Update the visible dimensions to include the new value
      this.visibleDimensions[i] = newDims[i];
    }
  }

  this.updatePositions();
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
  var scope = this, newMin, newMax;

  // the index in the visible dimensions
  var localIndex = this.visibleDimensions.indexOf(index);

  if (localIndex !== -1) {
    // update the ranges for this decomposition
    var max = this.decomp.dimensionRanges.max[index];
    var min = this.decomp.dimensionRanges.min[index];
    this.decomp.dimensionRanges.max[index] = min * (-1);
    this.decomp.dimensionRanges.min[index] = max * (-1);

    // and update the state of the orientation
    this.axesOrientation[localIndex] *= -1;

    this.updatePositions();
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

  return DecompositionView;
});
