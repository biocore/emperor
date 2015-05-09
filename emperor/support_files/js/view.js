/* Models axes */
function Axes(params){
  this.labels = []; // list, len == num of axes
  this.lines = []; // List Three.lines
};

/* The ScenePlotViews map to Viewports on WebGL */

/* This represents a camera */
function ScenePlotView3D(params){
  this.ndim = 3; // Number of dimensions shown
  this.visibleDimensions = []; // List of indices to the PCoA
  this.axes = new Axes(); // the axes of the plot
  this.decompositionViews = []; // all the decomposition view in the scene

  /* Setter to change the dimensions */
  this.changeVisibleDimensions = function(dimensions){};
};

/* This represents a camera */
function ScenePlotView2D(params){
  this.ndim = 2; // Number of dimensions shown
  this.visibleDimensions = []; // List of indices to the PCoA
  this.axes = new Axes(); // the axes of the plot
  this.decompositionViews = []; // all the decomposition view in the scene

  /* Setter to change the dimensions */
  this.changeVisibleDimensions = function(dimensions){};
};

/**
 *
 * @name DecompositionView
 *
 * @class Contains all the information on how the model is being presented to
 *        the user.
 *
 * @param {decomp} a DecompositionModel object that will be represented on
 *                 screen.
 *
 **/
function DecompositionView(decomp){
  /* The length of this list attributes is len(DecompositionModel.ids) */

  this.decomp = decomp; // The decomposition model seen by the view

  this.count = decomp.length;
  this.visibleCount = this.count;
  this.visibleDimensions = [0, 1, 2]; // really? :O

  this.tubes = []; // Three.meshes
  this.labels = []; // Three.text

  this.markers = []; // Three.meshes
  this.lines = []; // Three.lines

  // setup this.markers and this.lines
  this._initBaseScene();
  // this.elementOrdering = []; // list of ints - Not sure if needed

  // these sizes should likely be changed but, they should be modified here
  this._genericSphere = new THREE.SphereGeometry(1, 8, 8);
};

/*
 *
 * Helper method to initialize the base THREE.js objects.
 *
 **/
DecompositionView.prototype._initBaseScene = function(){
  var mesh, x = this.visibleDimensions[0], y = this.visibleDimensions[1],
      z = this.visibleDimensions[2];

  this.decomp.apply(function(plottable){
    mesh = new THREE.Mesh(this._genericSphere, new THREE.MeshPhongMaterial());

    mesh.material.color = new THREE.Color()
    mesh.material.transparent = true;
    mesh.material.depthWrite = true;
    mesh.material.opacity = 1;
    mesh.matrixAutoUpdate = true;

    mesh.position.set(plottable.coordinates[x], plottable.coordinates[y],
                      plottable.coordinates[z]);

    mesh.updateMatrix();

    this.markers.push(mesh);
  });

  // apply but to the adjacency list NOT IMPLEMENTED
  // this.decomp.applyAJ( ... ); Blame Jamie and Jose

};

/* Change the color for a set of plottables - group: list of plottables */
DecompositionView.prototype.setGroupColor = function(color, group){
  this.setGroupAttribute(color, group, "color")
};

/* Change the opacity for a set of plottables - group: list of plottables */
DecompositionView.prototype.setGroupOpacity = function(opacity, group){
  this.setGroupAttribute(opacity, group, "opacity")
};

/* Change the shape for a set of plottables - group: list of plottables */
DecompositionView.prototype.setGroupShape = function(shape, group){
  this.setGroupAttribute(shape, group, "shape")
};

/* Change the scale for a set of plottables - group: list of plottables */
DecompositionView.prototype.setGroupScale = function(scale, group){
  this.setGroupAttribute(scale, group, "scale")
};

DecompositionView.prototype.setGroupAttribue = function(value, group, attr){

};

/* Change the color for a set of plottables */
DecompositionView.prototype.setCategoryColors = function(colorFunc, category){
  this.setCategoryAttribute(colorFunc, category, "color")
};

/* Change the opacity for all plottables */
DecompositionView.prototype.setCategoryOpacity = function(opacityFunc, category){
  this.setCategoryAttribute(opacity, group, "opacity")
};

/* Change the shape for all plottables */
DecompositionView.prototype.setCategoryShape = function(shape, category){
  this.setCategoryAttribute(shape, group, "shape")
};

/* Change the scale for all plottables */
DecompositionView.prototype.setCategoryScale = function(scale, category){
  this.setCategoryAttribute(scale, group, "scale")
};

DecompositionView.prototype.setCategoryAttribue = function(value, category, attr){

};
