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

/* Contents all the information on how the Model is seen by the user */
function DecompositionView(params){
  /* The length of this list attributes is len(DecompositionModel.ids) */

  this.decompositionModel = null; // The decomposition model seen by the view
  this.markers = []; // Three.meshes
  this.lines = []; // Three.lines
  this.tubes = []; // Three.meshes
  this.labels = []; // Three.text
  // this.elementOrdering = []; // list of ints - Not sure if needed


  /* Change the color for a set of plottables - group: list of plottables */
  this.setGroupColor = function(color, group){
    this.setGroupAttribute(color, group, "color")
  };

  /* Change the opacity for a set of plottables - group: list of plottables */
  this.setGroupOpacity = function(opacity, group){
    this.setGroupAttribute(opacity, group, "opacity")
  };

  /* Change the shape for a set of plottables - group: list of plottables */
  this.setGroupShape = function(shape, group){
    this.setGroupAttribute(shape, group, "shape")
  };

  /* Change the scale for a set of plottables - group: list of plottables */
  this.setGroupScale = function(scale, group){
    this.setGroupAttribute(scale, group, "scale")
  };

  this.setGroupAttribue = function(value, group, attribute){};
};