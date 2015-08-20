/**
 *
 * @author Jamie Morton, Jose Navas Molina, Andrew Hodges & Yoshiki
 *         Vazquez-Baeza
 * @copyright Copyright 2013--, The Emperor Project
 * @credits Jamie Morton, Jose Navas Molina, Andrew Hodges & Yoshiki
 *          Vazquez-Baeza
 * @license BSD
 * @version 0.9.51-dev
 * @maintainer Yoshiki Vazquez Baeza
 * @email yoshiki89@gmail.com
 * @status Development
 *
 */

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
 *
 * Change the plottables coloring based on the metadata category using the
 * provided color function
 *
 * @param {colorFunc} a Function that accepts a category value and returns
 * a color
 * @param {category} a string with the metadata header
 *
**/
DecompositionView.prototype.setCategoryColors = function(colorFunc, category){
  var cats = this.decomp.getUniqueValuesByCategory(category), scope = this,
  dataView = [], colors = getColorList(cats, 'discrete-coloring-qiime'),
  plottables;

  _.each(cats, function(value) {
    /*
     *
     * WARNING: This is mixing attributes of the view with the model ...
     * it's a bit of a gray area though.
     *
     **/
    color = colors[value];
    plottables = scope.decomp.getPlottablesByMetadataCategoryValue(category, value);
    scope.setGroupColor(color, plottables);

    dataView.push({category: value, color: color, plottables: plottables});
  });

  return dataView;
};

/**
 *
 * Change the plottables opacity based on the metadata category using the
 * provided opacity function
 *
 * @param {opacityFunc} a Function that accepts a category value and returns
 * an opacity value
 * @param {category} a string with the metadata header
 *
**/
DecompositionView.prototype.setCategoryOpacity = function(opacityFunc,
                                                          category){
  this.setCategoryAttribute(opacityFunc, category, 'opacity');
};

/**
 *
 * Change the plottables scale based on the metadata category using the
 * provided scale function
 *
 * @param {shapeFunc} a Function that accepts a category value and returns
 * a scale value
 * @param {category} a string with the metadata header
 *
**/
DecompositionView.prototype.setCategoryScale = function(scaleFunc, category){
  this.setCategoryAttribute(scaleFunc, group, 'scale');
};

/**
 *
 * Change the plottables opacity based on the metadata category using the
 * provided opacity function
 *
 * @param {shapeFunc} a Function that accepts a category value and returns
 * a THREE.geometry
 * @param {category} a string with the metadata header
 *
**/
DecompositionView.prototype.setCategoryShape = function(shapeFunc, category){
  this.setCategoryAttribute(shapeFunc, category, 'shape');
};


DecompositionView.prototype.setCategoryAttribute = function(value, category, attr){

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

/* Change the opacity for a set of plottables - group: list of plottables */
DecompositionView.prototype.setGroupOpacity = function(opacity, group){
  this.setGroupAttribute(opacity, group, 'opacity');
};

/* Change the shape for a set of plottables - group: list of plottables */
DecompositionView.prototype.setGroupShape = function(shape, group){
  this.setGroupAttribute(shape, group, 'shape');
};

/* Change the scale for a set of plottables - group: list of plottables */
DecompositionView.prototype.setGroupScale = function(scale, group){
  this.setGroupAttribute(scale, group, 'scale');
};

DecompositionView.prototype.setGroupAttribute = function(value, group, attr){

};
