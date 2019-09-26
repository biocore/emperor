define(['underscore'],
function(_) {
  /**
   * @class MultiModel
   *
   * The MultiModel wraps a dictionary of DecompositionModel objects and
   * supplies methods to compute aggregate metrics over all such model objects
   *
   * This is used to provide the 'global' dimension ranges of the scene, rather
   * than the 'local' dimension ranges of any individual scatter or biplot.
   */
  function MultiModel(underlyingModelsDict) {
    this.models = underlyingModelsDict;

    var first = true;
    var firstModel = null;

    for (var key in underlyingModelsDict) {
      if (first) {
        first = false;
        firstModel = underlyingModelsDict[key];
      }
      else {
        if (underlyingModelsDict[key].dimensions != firstModel.dimensions)
          throw 'Underlying models must have same number of dimensions';
      }
    }

    this.dimensionRanges = {'max': [], 'min': []};
    this._unionRanges();
  }

  /**
   *
   * Utility method to find the union of the ranges in the DecompositionModels
   * this method will populate the dimensionRanges attributes.
   * @private
   *
   */
  MultiModel.prototype._unionRanges = function() {
    var scope = this, computeRanges;

    // first check if there's any range data, if there isn't, then we need
    // to compute it by looking at all the decompositions
    computeRanges = scope.dimensionRanges.max.length === 0;

    // if there's range data then check it lies within the global ranges
    if (computeRanges === false) {
      _.each(this.models, function(decomp, unused) {
        for (var i = 0; i < decomp.dimensionRanges.max.length; i++) {
          // global
          var gMax = scope.dimensionRanges.max[i];
          var gMin = scope.dimensionRanges.min[i];

          // local
          var lMax = decomp.dimensionRanges.max[i];
          var lMin = decomp.dimensionRanges.min[i];

          // when we detect a point outside the global ranges we break and
          // recompute them
          if (!(gMin <= lMin && lMin <= gMax) ||
              !(gMin <= lMax && lMax <= gMax)) {
            computeRanges = true;
            break;
          }
        }
      });
    }

    if (computeRanges === false) {
      // If at this point we still don't need to compute the data, it is safe
      // to exit because all data still exists within the expected ranges
      return;
    }
    else {
      // TODO: If this entire function ever becomes a bottleneck we should only
      // update the dimensions that changed.
      // See: https://github.com/biocore/emperor/issues/526

      // if we have to compute the data, clean up the previously known ranges
      this.dimensionRanges.max = [];
      this.dimensionRanges.max.length = 0;
      this.dimensionRanges.min = [];
      this.dimensionRanges.min.length = 0;
    }

    _.each(this.models, function(decomp, unused) {

      if (scope.dimensionRanges.max.length === 0) {
        scope.dimensionRanges.max = decomp.dimensionRanges.max.slice();
        scope.dimensionRanges.min = decomp.dimensionRanges.min.slice();
      }
      else {
        // when we have more than one decomposition view we need to figure out
        // the absolute largest range that views span over
        _.each(decomp.dimensionRanges.max, function(value, index) {
          var vMax = decomp.dimensionRanges.max[index],
              vMin = decomp.dimensionRanges.min[index];

          if (vMax > scope.dimensionRanges.max[index]) {
            scope.dimensionRanges.max[index] = vMax;
          }
          if (vMin < scope.dimensionRanges.min[index]) {
            scope.dimensionRanges.min[index] = vMin;
          }
        });
      }
    });
  };

  return MultiModel;
});
