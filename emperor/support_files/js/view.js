/* Contents all the information on how the Model is seen by the user */
function DecompositionView(params){
	this.points = []; // Three meshes
	this.lines = []; // Three lines
	this.tubes = []; // Three meshes
	this.labels = []; // Three text
	this.elementOrdering = []; // list of ints


	/* Defined in the subclasses */
	this.changeVisibleDimensions = function(){};

	/* Change the color for a set of plottables */
	this.setGroupColor = function(color, group){};

	/* Change the opacity for a set of plottable */
	this.setGroupOpacity = function(opacity, group){};

	/* Change the shape for a set of plottable */
	this.setGroupShape = function(shape, group){};

	/* Change the scale for a set of plottable */
	this.setGroupScale = function(scale, group){};
};