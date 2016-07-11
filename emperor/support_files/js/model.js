define([
    'jquery',
    'underscore'
],
function($, _) {
  /**
   *
   * @class Plottable
   *
   * Represents a sample and the associated metadata in the ordination space.
   *
   * @param {string} name A string indicating the name of the sample.
   * @param {string[]} metadata An Array of strings with the metadata values.
   * @param {float[]} coordinates An Array of floats indicating the position in
   * space where this sample is located.
   * @param {integer} [idx = -1] An integer representing the index where the
   * object is located in a DecompositionModel.
   * @param {float[]} [ci = []] An array of floats indicating the confidence
   * intervals in each dimension.
   *
   * @return {Plottable}
   * @constructs Plottable
   *
   **/
  function Plottable(name, metadata, coordinates, idx, ci) {
    /**
     * Sample name.
     * @type {string}
     */
    this.name = name;
    /**
     * Metadata values for the sample.
     * @type {string[]}
     */
    this.metadata = metadata;
    /**
     * Position of the sample in the N-dimensional space.
     * @type {float[]}
     */
    this.coordinates = coordinates;

    /**
     * The index of the sample in the array of meshes.
     * @type {integer}
     */
    this.idx = idx === undefined ? -1 : idx;
    /**
     * Confidence intervals.
     * @type {float[]}
     */
    this.ci = ci === undefined ? [] : ci;

    if (this.ci.length !== 0) {
      if (this.ci.length !== this.coordinates.length) {
        throw new Error("The number of confidence intervals doesn't match " +
                        'with the number of dimensions in the coordinates ' +
                        'attribute. coords: ' + this.coordinates.length +
                        ' ci: ' + this.ci.length);
      }
    }
  };

  /**
   *
   * Helper method to convert a Plottable into a string.
   *
   * @return {string} A string describing the Plottable object.
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
   * @class DecompositionModel
   *
   * Models all the ordination data to be plotted.
   *
   * @param {string} name A string containing the abbreviated name of the
   * ordination method.
   * @param {string[]} ids An array of strings where each string is a sample
   * identifier
   * @param {float[]} coords A 2D Array of floats where each row contains the
   * coordinates of a sample. The rows are in ids order.
   * @param {float[]} pct_var An Array of floats where each position contains
   * the percentage explained by that axis
   * @param {float[]} md_headers An Array of string where each string is a
   * metadata column header
   * @param {string[]} metadata A 2D Array of strings where each row contains
   * the metadata values for a given sample. The rows are in ids order. The
   * columns are in `md_headers` order.
   *
   * @throws {Error} In any of the following cases:
   * - The number of coordinates does not match the number of samples.
   * - If there's a coordinate in `coords` that doesn't have the same length as
   *   the rest.
   * - The number of samples is different than the rows provided as metadata.
   * - Not all metadata rows have the same number of fields.
   *
   * @return {DecompositionModel}
   * @constructs DecompositionModel
   *
   */
  function DecompositionModel(name, ids, coords, pct_var, md_headers,
                              metadata, axesNames) {
    var num_coords;
    /**
     * Abbreviated name of the ordination method used to create the data.
     * @type {string}
     */
    this.abbreviatedName = name;
    /**
     * List of sample name identifiers.
     * @type {string[]}
     */
    this.ids = ids;
    /**
     * Percentage explained by each of the axes in the ordination.
     * @type {float[]}
     */
    this.percExpl = pct_var;
    /**
     * Column names for the metadata in the samples.
     * @type {string[]}
     */
    this.md_headers = md_headers;
    /**
     * Names of the axes in the ordination
     * @type {string[]}
     */
    this.axesNames = axesNames === undefined ? [] : axesNames;

    /*
      Check that the number of coordinates set provided are the same as the
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

    // use slice to make a copy of the array so we can modify it
    /**
     * Minimum and maximum values for each axis in the ordination. More
     * concretely this object has a `min` and a `max` attributes, each with a
     * list of floating point arrays that describe the minimum and maximum for
     * each axis.
     * @type {Object}
     */
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
   * Retrieve the plottable object with the given id.
   *
   * @param {string} id A string with the plottable.
   *
   * @return {Plottable} The plottable object for the given id.
   *
   */
  DecompositionModel.prototype.getPlottableByID = function(id) {
    idx = this.ids.indexOf(id);
    if (idx === -1) {
      throw new Error(id + ' is not found in the Decomposition Model ids');
    }
    return this.plottable[idx];
  };

  /**
   *
   * Retrieve all the plottable objects with the given ids.
   *
   * @param {integer[]} idArray an Array of strings where each string is a
   * plottable id.
   *
   * @return {Plottable[]} An Array of plottable objects for the given ids.
   *
   */
  DecompositionModel.prototype.getPlottableByIDs = function(idArray) {
    dm = this;
    return _.map(idArray, function(id) {return dm.getPlottableByID(id);});
  };

  /**
   *
   * Helper function that returns the index of a given metadata category.
   *
   * @param {string} category A string with the metadata header.
   *
   * @return {integer} An integer representing the index of the metadata
   * category in the `md_headers` array.
   *
   */
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
   * Retrieve all the plottable objects under the metadata header value.
   *
   * @param {string} category A string with the metadata header.
   * @param {string} value A string with the value under the metadata category.
   *
   * @return {Plottable[]} An Array of plottable objects for the given category
   * value pair.
   *
   */
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
   * @param {string} category A string with the metadata header.
   *
   * @return {string[]} An array of the available values for the given metadata
   * header.
   *
   */
  DecompositionModel.prototype.getUniqueValuesByCategory = function(category) {
    var md_idx = this._getMetadataIndex(category);
    return _.uniq(
      _.map(this.plottable, function(pl) {return pl.metadata[md_idx];}));
  };

  /**
   *
   * Executes the provided `func` passing all the plottables as parameters.
   *
   * @param {function} func The function to call for each plottable. It should
   * accept a single parameter which will be the plottable.
   *
   * @return {Object[]} An array with the results of executing func over all
   * plottables.
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
   * @param {Object} accumulator An object with a "min" and "max" arrays that
   * store the minimum and maximum values over all the plottables.
   * @param {Plottable} plottable A plottable object to compare with.
   *
   * @return {Object} An updated version of accumulator, integrating the ranges
   * of the newly seen plottable object.
   * @private
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
   * @return {string} String representation describing the Decomposition
   * object.
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
