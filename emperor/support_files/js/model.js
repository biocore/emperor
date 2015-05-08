/* Represents an object that can be drawn (i.e. a sample or taxa)
*/
function Plottable(params){
  this.name = "PC.354";
  this.idx = 0;
  this.metadata = ["AGCACGAGCCTA", "YATGCTGCCTCCCGTAGGAGT", "Control",
                   "20061218", "Control_mouse_I.D._354"];
  this.coordinates = [0.280399117569, -0.0060128286014, 0.0234854344148,
                      -0.0468109474823, -0.146624450094, 0.00566979124596,
                      -0.0354299634191, -0.255785794275, -4.84141986706e-09];
  this.confidenceInterval = [];
}

/**
 * @name DecompositionModel
 *
 * @class Models all the ordination method data to be plotted
 *
 * @param {name} a string containing the abbreviated name of the ordination
 * method
 * @param {ids} an Array of strings where each string is a sample identifier
 * @param {coords} a 2D Array of floats where each row contains the coordinates
 * of a sample. The rows are in ids order.
 * @param {pct_var} an Array of floats where each position contains the
 * percentage explained by that axis
 * @param {md_headers} an Array of string where each string is a metadata
 * column header
 * @param {metadata} a 2D Array of strings where each row contains the metadata
 * values for a given sample. The rows are in ids order. The columns are in
 * md_headers order.
 *
**/
function DecompositionModel(name, ids, coords, pct_var, md_headers, metadata){
  this.abbreviatedName = name;
  this.percExpl = pct_var;
  this.md_headers = md_headers;
  this.ids = ids;

  this.plottable = new Array(ids.length)
  for (var i = 0; i < ids.length; i++){
    this.plottable[i] = new Plottable(ids[i], metadata[i], coords[i], i)
  }
  // this.edges = [];
  // this.plotEdge = false;
  // this.serialComparison = false;
};

/**
 * Retrieve the plottable object with the given id
 *
 * @param {id} a string with the plottable
 *
 * @return the plottable object for the given id
 *
**/
DecompositionModel.prototype.getPlottableByID = function(id) {
  idx = this.ids.indexOf(id);
  return this.plottable[idx];
};


/**
 *
 * Retrieve all the plottable object with the given ids
 *
 * @param {idArray} an Array of strings where each string is a plottable id
 *
 * @return an Array of plottable objects for the given ids
 *
**/
DecompositionModel.prototype.getPlottableByIDs = function(idArray){
  return _.map(idArray, this.getPlottableByID);
};

/**
 *
 * Retrieve all the plottable object under the metadata header value
 *
 * @param {category} a string with the metadata header
 * @param {value} a string with the value under the metadata category
 *
 * @return an Array of plottable object for the given category value pair
 *
*/
DecompositionModel.prototype.getPlottablesByMetadataCategoryValue = function(
    category, value){
  md_idx = this.md_headers.indexOf(category);
  return _.find(this.plottable, function(pl){
    return pl.metadata[md_idx] === value; });
};

/**
 * Get's a metadata category and returns the unique values on that category
 * @ param {category} a string with the metadata header
 *
 * @ return an Array of meta values under the metadata header
**/
DecompositionModel.prototype.getUniqueValuesByCategory = function(category){
  md_idx = this.md_headers.indexOf(category);
  return _.uniq(
    _.map(this.plottable, function(pl){return pl.metadata[md_idx];}));
};