define([
    'jquery',
    'underscore',
],
function($, _) {
  /**
   *
   * @name Plottable
   *
   * @class Represents a sample and the associated metadata in the ordination
   * space.
   *
   */


  /**
   *
   * @name Plottable
   *
   * @class Represents a sample and the associated metadata in the ordination
   * space.
   *
   * @param {name} a string indicating the name of the sample.
   * @param {metadata} an Array of strings with the metadata values.
   * @param {coordinates} an Array of floats indicating the position in space
   * where this sample is located.
   * @param {idx} an *optional* integer representing the index where the object
   * is located in a DecompositionModel.
   * @param {ci} an *optional* Array of floats indicating the confidence
   * intervals in each dimension.
   *
   **/
  function Plottable(name, metadata, coordinates, idx, ci) {
    this.name = name;
    this.metadata = metadata;
    this.coordinates = coordinates;

    this.idx = idx === undefined ? -1 : idx;
    this.ci = ci === undefined ? [] : ci;

    if (this.ci.length !== 0) {
      if (this.ci.length !== this.coordinates.length) {
        throw new Error("The number of confidence intervals doesn't match with" +
                        ' the number of dimensions in the coordinates '+
                        'attribute. coords: ' + this.coordinates.length +
                        ' ci: ' + this.ci.length);
      }
    }
  };

  /**
   *
   * Helper method to convert a Plottable into a string.
   *
   * @return a string describing the Plottable object.
   *
   */
  Plottable.prototype.toString = function() {
    var ret = 'Sample: ' + this.name + ' located at: (' +
              this.coordinates.join(', ') + ') metadata: [' +
              this.metadata.join(', ') + ']';

    if (this.idx === -1) {
      ret = ret + ' without index';
    }
    else {
      ret = ret + ' at index: ' + this.idx;
    }

    if (this.ci.length === 0) {
      ret = ret + ' and without confidence intervals.';
    }
    else {
      ret = ret + ' and with confidence intervals at (' + this.ci.join(', ') +
        ').';
    }

    return ret;
  };

  /**
   *
   * @name DecompositionModel
   *
   * @class Represents all the information that need to be plotted
   *
   * @property {String} [abbreviatedName] abbreviated name of the decomposition
   * object being visualized.
   * @property {Array} [ids] array of strings with the sample identifiers.
   * @property {Array} [percExpl] array of floats with the percent explained by
   * each axes.
   * @property {Array} [md_headers] array of strings with the names of the
   * available metadta.
   * @property {Array} [plottable] array of plottable objects.
   * @property {Object} [dimensionRanges] object with two properties "min" and
   * "max", these determine the ranges over which all the samples span.
   *
   */

  /**
   * @name DecompositionModel
   *
   * @class Models all the ordination method data to be plotted
   *
   * @param {name} a string containing the abbreviated name of the ordination
   * method
   * @param {ids} an Array of strings where each string is a sample identifier
   * @param {coords} a 2D Array of floats where each row contains the
   * coordinates of a sample. The rows are in ids order.
   * @param {pct_var} an Array of floats where each position contains the
   * percentage explained by that axis
   * @param {md_headers} an Array of string where each string is a metadata
   * column header
   * @param {metadata} a 2D Array of strings where each row contains the
   * metadata values for a given sample. The rows are in ids order. The columns
   * are in md_headers order.
   *
  **/
  function DecompositionModel(name, ids, coords, pct_var, md_headers, metadata) {
    var num_coords;
    this.abbreviatedName = name;
    this.ids = ids;
    this.percExpl = pct_var;
    this.md_headers = md_headers;

    /*
      Check that the number of coordnates set provided are the same as the
      number of samples
    */
    if (this.ids.length !== coords.length) {
      throw new Error('The number of coordinates differs from the number of ' +
                      'samples. Coords: ' + coords.length + ' samples: ' +
                      this.ids.length);
    }

    /*
      Check that all the coords set have the same number of coordinates
    */
    num_coords = coords[0].length;
    var res = _.find(coords, function(c) {return c.length !== num_coords;});
    if (res !== undefined) {
      throw new Error('Not all samples have the same number of coordinates');
    }

    /*
      Check that we have the percentage explained values for all coordinates
    */
    if (pct_var.length !== num_coords) {
      throw new Error('The number of percentage explained values does not ' +
                      'match the number of coordinates. Perc expl: ' +
                      pct_var.length + ' Num coord: ' + num_coords);
    }

    /*
      Check that we have the metadata for all samples
    */
    if (this.ids.length !== metadata.length) {
      throw new Error('The number of metadata rows and the the number of ' +
                      'samples do not match. Samples: ' + this.ids.length +
                      ' Metadata rows: ' + metadata.length);
    }

    /*
      Check that we have all the metadata categories in all rows
    */
    res = _.find(metadata, function(m) {
                  return m.length !== md_headers.length;
    });
    if (res !== undefined) {
      throw new Error('Not all metadata rows have the same number of values');
    }

    this.plottable = new Array(ids.length);
    for (var i = 0; i < ids.length; i++) {
      this.plottable[i] = new Plottable(ids[i], metadata[i], coords[i], i);
    }

    // use slice to make a copy of the array so we can modfiy it
    this.dimensionRanges = {'min': coords[0].slice(),
                            'max': coords[0].slice()};
    this.dimensionRanges = _.reduce(this.plottable,
                                    DecompositionModel._minMaxReduce,
                                    this.dimensionRanges);

    this.length = this.plottable.length;
    // TODO:
    // this.edges = [];
    // this.plotEdge = false;
    // this.serialComparison = false;
  }

  /**
   *
   * Retrieve the plottable object with the given id
   *
   * @param {id} a string with the plottable
   *
   * @return the plottable object for the given id
   *
  **/
  DecompositionModel.prototype.getPlottableByID = function(id) {
    idx = this.ids.indexOf(id);
    if (idx === -1) {
      throw new Error(id + ' is not found in the Decomposition Model ids');
    }
    return this.plottable[idx];
  };

  /**
   *
   * Retrieve all the plottable objects with the given ids
   *
   * @param {idArray} an Array of strings where each string is a plottable id
   *
   * @return an Array of plottable objects for the given ids
   *
  **/
  DecompositionModel.prototype.getPlottableByIDs = function(idArray) {
    dm = this;
    return _.map(idArray, function(id) {return dm.getPlottableByID(id);});
  };

  /**
   *
   * Helper function that return the index of a given metadata category
   *
   * @ param {category} a string with the metadata header
   *
   * @ return an integer representing the index of the metadata category in
   * the md_headers array
   *
  **/
  DecompositionModel.prototype._getMetadataIndex = function(category) {
    var md_idx = this.md_headers.indexOf(category);
    if (md_idx === -1) {
      throw new Error('The header ' + category +
                      ' is not found in the metadata categories');
    }
    return md_idx;
  };

  /**
   *
   * Retrieve all the plottable objects under the metadata header value
   *
   * @param {category} a string with the metadata header
   * @param {value} a string with the value under the metadata category
   *
   * @return an Array of plottable object for the given category value pair
   *
  **/
  DecompositionModel.prototype.getPlottablesByMetadataCategoryValue = function(
      category, value) {

    var md_idx = this._getMetadataIndex(category);
    var res = _.filter(this.plottable, function(pl) {
      return pl.metadata[md_idx] === value; });

    if (res.length === 0) {
      throw new Error('The value ' + value +
                      ' is not found in the metadata category ' + category);
    }
    return res;
  };

  /**
   *
   * Retrieve the available values for a given metadata category
   *
   * @param {category} a string with the metadata header
   *
   * @return an Array of the available values for the given metadata header
   *
  **/
  DecompositionModel.prototype.getUniqueValuesByCategory = function(category) {
    var md_idx = this._getMetadataIndex(category);
    return _.uniq(
      _.map(this.plottable, function(pl) {return pl.metadata[md_idx];}));
  };

  /**
   *
   * Executes the provided func passing all the plottables as parameters
   *
   * @param {func} the function to call for each plottable. It should accept
   * a single parameter which will be the plottable
   *
   * @return An array with the results of executing func over all plottables
   *
   */
  DecompositionModel.prototype.apply = function(func) {
    return _.map(this.plottable, func);
  };

  /**
   *
   * Helper function used to find the minimum and maximum values every
   * dimension in the plottable objects. This function is used with
   * underscore.js' reduce function (_.reduce).
   *
   * @param {accumulator} Object with a "min" and "max" arrays that store the
   * minimum and maximum values over all the plottables.
   * @param {plottable} Plottable object to compare with.
   *
   * @return Updated version of accumulator, integrating the ranges of the
   * newly seen plottable object.
   *
   **/
  DecompositionModel._minMaxReduce = function(accumulator, plottable) {

    // iterate over every dimension
    _.each(plottable.coordinates, function(value, index) {
      if (value > accumulator.max[index]) {
        accumulator.max[index] = value;
      }
      else if (value < accumulator.min[index]) {
        accumulator.min[index] = value;
      }
    });

    return accumulator;
  };

  /**
   *
   * Helper method to convert a DecompositionModel into a string.
   *
   * @return a string describing the Decomposition object.
   *
   */
  DecompositionModel.prototype.toString = function() {
    return 'name: ' + this.abbreviatedName + '\n' +
      'Metadata headers: [' + this.md_headers.join(', ') + ']\n' +
      'Plottables:\n' + _.map(this.plottable, function(plt) {
        return plt.toString();
      }).join('\n');
  };

  return { 'DecompositionModel': DecompositionModel,
           'Plottable': Plottable};
});
