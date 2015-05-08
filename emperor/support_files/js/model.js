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
 * @name Plottable
 *
 * @class Represents a sample and the associated metadata in the ordination
 * space.
 *
 */

/* Represents an object that can be drawn (i.e. a sample or taxa)
*/


/**
 *
 * @name Plottable
 *
 * @class Represents a sample and the associated metadata in the ordination
 * space.
 *
 * @param {name} a string indicating the name of the sample.
 * @param {idx} the index where the object is located in a decomposition model.
 * @param {metadata} an Array of strings with the metadata values.
 * @param {coordinates} an Array of floats indicating the position in space
 *                      where this sample is located.
 *
 * @param {idx} an *optional* integer representing the index where the object
 *              is located in a DecompositionModel.
 * @param {ci} an *optional* Array of floats indicating the confidence
 *             intervals in each dimension.
 *
 **/
function Plottable(name, metadata, coordinates, idx, ci) {
  this.name = name;
  this.metadata = metadata;
  this.coordinates = coordinates;

  this.idx = idx === undefined ? -1 : idx;
  this.ci = ci === undefined ? [] : ci;

  if (this.ci.length !== 0){
    if (this.ci.length !== this.coordinates.length){
      throw new Error("The number of confidence intervals doesn't match with"+
                      " the number of dimensions in the coordinates "+
                      "attribute. coords: " + this.coordinates.length +
                      " ci: " + this.ci.length);
    }
  }
}

/**
 *
 * Helper method to convert a Plottable into a string.
 *
 * @return a string describing the Plottable object.
 *
 */
Plottable.prototype.toString = function(){
  var ret = 'Sample: ' + this.name + ' located at: (' +
            this.coordinates.join(', ') + ') metadata: ' +
            this.metadata.join(', ');

  if (this.idx === -1){
    ret = ret + ' without index';
  }
  else{
    ret = ret + ' at index: ' + this.idx;
  }

  if (this.ci.length === 0){
    ret = ret + ' and without confidence intervals.';
  }
  else{
    ret = ret + ' and with confidence intervals at (' + this.ci.join(', ') +
      ').';
  }

  return ret;
}

/* Models all the data loaded to be drawn (i.e. all samples, taxa, vectors...)
  Params: representation of the PC and the MetadataMap
*/
function DecompositionModel(params){
  this.abbreviatedName = "pcoa";
  this.percExpl = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
                   10.024774995, 8.22835130237, 7.55971173665, 6.24945796136,
                   1.17437418531e-14];
  this.serialComparison = false;
  this.headers = ["BarcodeSequence", "LinkerPrimerSequence", "Treatment",
                  "DOB", "Description"];
  this.ids = ["PC.354", "PC.355", "PC.356", "PC.481", "PC.593", "PC.607",
              "PC.634", "PC.635", "PC.636"];
  this.plottable = [new Plottable(), new Plottable(), new Plottable(),
                    new Plottable(), new Plottable(), new Plottable(),
                    new Plottable(), new Plottable(), new Plottable()];
  this.plottableGroup = [];
  this.plotEdge = false;

  /* Get's a string with the plottable id and returns the plottable */
  this.getPlottableByID = function(id){
    return this.getPlottableByIDs([id])[0];
  };

  /* Get's a metadata category and a value and returns a list of 
  plottable objects that match that search
  */
  this.getPlottablesByMetadataCategoryValue = function(category, value){
    return [this.plottable[0], this.plottable[1]];
  };

  /* Get's a metadata category and returns the unique values on that category
  */
  this.getUniqueValuesByCategory = function(category){
    return ["Control", "Fast"];
  };

  /* Get's a list of strings with the plottable ids and returns a list of
  plottable */
  this.getPlottableByIDs = function(idArray){
    return [this.plottable[0], this.plottable[1]];
  };
}
