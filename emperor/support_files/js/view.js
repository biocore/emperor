define([
    "jquery",
    "underscore",
    "three",
], function ($, _, THREE) {
/**
 *
 * @name DecompositionView
 *
 * @class Contains all the information on how the model is being presented to
 *        the user.
 *
 * @param {DecompositionModel} decomp a DecompositionModel object that will be
 * represented on screen.
 *
 **/
function DecompositionView(decomp) {
  /* The length of this list attributes is len(DecompositionModel.ids) */

  this.decomp = decomp; // The decomposition model seen by the view

  this.count = decomp.length;
  this.visibleCount = this.count;
  this.visibleDimensions = [0, 1, 2]; // We default to the first three PCs

  this.tubes = []; // Three.meshes
  this.labels = []; // Three.text

  this.markers = []; // Three.meshes
  this.lines = []; // Three.lines

  // these sizes should likely be changed but, they should be modified here
  this._genericSphere = new THREE.SphereGeometry(0.1, 8, 8);

  // setup this.markers and this.lines
  this._initBaseView();
  // this.elementOrdering = []; // list of ints - Not sure if needed
}

/*
 *
 * Helper method to initialize the base THREE.js objects.
 *
 **/
DecompositionView.prototype._initBaseView = function(){
  var mesh, x = this.visibleDimensions[0], y = this.visibleDimensions[1],
      z = this.visibleDimensions[2];

  var dv = this;
  this.decomp.apply(function(plottable) {
    mesh = new THREE.Mesh(dv._genericSphere, new THREE.MeshPhongMaterial());
    mesh.name = plottable.name;

    mesh.material.color = new THREE.Color(0xff0000);
    mesh.material.transparent = false;
    mesh.material.depthWrite = true;
    mesh.material.opacity = 1;
    mesh.matrixAutoUpdate = true;

    mesh.position.set(plottable.coordinates[x], plottable.coordinates[y],
                      plottable.coordinates[z]);

    mesh.updateMatrix();

    dv.markers.push(mesh);
  });

  // apply but to the adjacency list NOT IMPLEMENTED
  // this.decomp.applyAJ( ... ); Blame Jamie and Jose - baby steps buddy...

};

/**
 *
 * Change the visible coordinates
 *
 * @param {newDims} an Array of integers in which each integer is the index
 * to the principal coordinate to show
 *
**/
DecompositionView.prototype.changeVisibleDimensions = function(newDims){
  if(newDims.length !== 3){
    throw new Error("Only three dimensions can be shown at the same time");
  }

  this.visibleDimensions = newDims;

  var x = newDims[0], y = newDims[1], z = newDims[2], dv = this;
  this.decomp.apply(function(plottable){
    mesh = dv.markers[plottable.idx];
    mesh.position.set(plottable.coordinates[x],
                      plottable.coordinates[y],
                      plottable.coordinates[z]);
    mesh.updateMatrix();
  });
};

/**
 * Change the plottables attributes based on the metadata category using the
 * provided setPlottableAttributes function
 *
 * @param {attributes} key:value pairs of elements and values to change in
 * plottables
 * @param {setPlottableAttributes} helper function to change the values of
 * plottables, in general this should be implemented in the controller but it
 * can be nullable if not needed. setPlottableAttributes should receive:
 * the scope where the plottables exist, the value to be applied to the
 * plottables and the plotables to change. For more info see:
 * see ColorViewController.setPlottableAttribute
 * @param {category} the category/column in the mapping file
 * @return {dataView} Array of objects to be consumed by Slick grid.
**/
DecompositionView.prototype.setCategory = function(attributes,
                                                   setPlottableAttributes,
                                                   category){
  var scope = this, dataView = [], plottables;

  _.each(attributes, function(value, key) {
    /*
     *
     * WARNING: This is mixing attributes of the view with the model ...
     * it's a bit of a gray area though.
     *
     **/
    plottables = scope.decomp.getPlottablesByMetadataCategoryValue(category, key);
    if (setPlottableAttributes !== null){
      setPlottableAttributes(scope, value, plottables);
    }

    dataView.push({category: key, value: value, plottables: plottables});
  });

  return dataView;
};

/* Change the color for a set of plottables - group: list of plottables */
DecompositionView.prototype.setGroupColor = function(color, group){
  var idx;
  var scope = this;

  _.each(group, function(element) {
    idx = element.idx;
    scope.markers[idx].material.color = new THREE.Color(color);
  });
};

  return DecompositionView;
});
