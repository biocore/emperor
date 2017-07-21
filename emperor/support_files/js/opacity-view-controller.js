define([
    'jquery',
    'underscore',
    'util',
    'viewcontroller',
    'scale-editor'
], function($, _, util, ViewControllers, ScaleEditor) {

  // we only use the base attribute class, no need to get the base class
  var EmperorAttributeABC = ViewControllers.EmperorAttributeABC;

  /**
   * @class OpacityViewController
   *
   * Alters the scale of points displayed on the screen.
   *
   * @param {Node} container Container node to create the controller in.
   * @param {Object} decompViewDict This object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   *
   * @return {OpacityViewController}
   * @constructs OpacityViewController
   * @extends EmperorAttributeABC
   *
   **/
  function OpacityViewController(container, decompViewDict) {
    var helpmenu = 'Change the opacity of the attributes on the plot';
    var title = 'Opacity';
    // Create checkbox for scaling by values
    /**
     * jQuery node for checkbox controlling whether to scale by values or not
     * @type {Node}
     */
    this.$scaledCheckbox = $('<input type="checkbox">');
    /**
     * jQuery node for label of $scaledCheckboxs
     * @type {Node}
     */
    this.$scaledLabel = $('<label>Opacity by values</label>');

    // Constant for width in slick-grid
    var SLICK_WIDTH = 50, scope = this;

    // Build the options dictionary
    var options = {
      'valueUpdatedCallback': function(e, args) {
        var scale = +args.item.value;
        var group = args.item.plottables;
        var element = scope.getView();
        scope.setPlottableAttributes(element, scale, group);
      },
      'categorySelectionCallback': function(evt, params) {
        var category = scope.$select.val(), attributes;

        var decompViewDict = scope.getView();

        // getting all unique values per categories
        var uniqueVals = decompViewDict.decomp.getUniqueValuesByCategory(
          category);
        // getting scale value for each point
        var scaled = scope.$scaledCheckbox.is(':checked');
        try {
          attributes = scope.getScale(uniqueVals, scaled);
        } catch (err) {
          // Do not fire off action
          scope.$scaledCheckbox.prop('checked', false);
          return;
        }
        scope.resize();

        // fetch the slickgrid-formatted data
        var data = decompViewDict.setCategory(attributes,
                                              scope.setPlottableAttributes,
                                              category);

        scope.setSlickGridDataset(data);
      },
      'slickGridColumn': {id: 'title', name: title, field: 'value',
        sortable: false, maxWidth: SLICK_WIDTH,
        minWidth: SLICK_WIDTH,
        autoEdit: true,
        editor: ScaleEditor.ScaleEditor
      },
      'editorOptions': {'min': 0, 'max': 1, 'step': 0.05}
    };

    EmperorAttributeABC.call(this, container, title, helpmenu,
        decompViewDict, options);
    this.$header.append(this.$scaledCheckbox);
    this.$header.append(this.$scaledLabel);

    scope.$scaledCheckbox.on('change', options.categorySelectionCallback);

    return this;
  }
  OpacityViewController.prototype = Object.create(EmperorAttributeABC.prototype);
  OpacityViewController.prototype.constructor = EmperorAttributeABC;

  /**
   *
   * Private method to reset the scale of all the objects to one.
   *
   * @extends EmperorAttributeABC
   * @private
   *
   */
  OpacityViewController.prototype._resetAttribute = function() {
    EmperorAttributeABC.prototype._resetAttribute.call(this);
    var scope = this;

    _.each(this.decompViewDict, function(view) {
      scope.setPlottableAttributes(view, 1, view.decomp.plottable);
      view.needsUpdate = true;
    });
    this.$scaledCheckbox.prop('checked', false);
  };

  /**
   * Converts the current instance into a JSON string.
   *
   * @return {Object} JSON ready representation of self.
   */
  OpacityViewController.prototype.toJSON = function() {
    var json = EmperorAttributeABC.prototype.toJSON.call(this);
    json.scaleVal = this.$scaledCheckbox.is(':checked');
    return json;
  };

  /**
   * Decodes JSON string and modifies its own instance variables accordingly.
   *
   * @param {Object} Parsed JSON string representation of self.
   */
  OpacityViewController.prototype.fromJSON = function(json) {
    // Can't call super because select needs to be set first
    // Order here is important. We want to set all the extra controller
    // settings before we load from json, as they can override the JSON when set

    this.setMetadataField(json.category);

    // if the category is null, then there's nothing to set about the state
    // of the controller
    if (json.category === null) {
      return;
    }

    this.$select.val(json.category);
    this.$select.trigger('chosen:updated');
    this.$scaledCheckbox.prop('checked', json.scaleVal);
    this.$scaledCheckbox.trigger('change');

    // fetch and set the SlickGrid-formatted data
    var data = this.getView().setCategory(
      json.data, this.setPlottableAttributes, json.category);
    this.setSlickGridDataset(data);
    // set all to needsUpdate
    this.getView().needsUpdate = true;
  };

  /**
   * Resizes the container and the individual elements.
   *
   * Note, the consumer of this class, likely the main controller should call
   * the resize function any time a resizing event happens.
   *
   * @param {float} width the container width.
   * @param {float} height the container height.
   */
  OpacityViewController.prototype.resize = function(width, height) {
    this.$body.height(this.$canvas.height() - this.$header.height());
    this.$body.width(this.$canvas.width());

    //scale gridDiv based on whether global scaling available or not
    if (this.$scaledCheckbox.is(':checked')) {
      this.$gridDiv.css('height', '100%');
    }
    else {
      this.$gridDiv.css('height', this.$body.height() - 10);
    }

    // call super, most of the header and body resizing logic is done there
    EmperorAttributeABC.prototype.resize.call(this, width, height);
  };

  /**
   * Sets whether or not elements in the tab can be modified.
   *
   * @param {Boolean} trulse option to enable elements.
   */
  OpacityViewController.prototype.setEnabled = function(trulse) {
    EmperorAttributeABC.prototype.setEnabled.call(this, trulse);

    this.$scaledCheckbox.prop('disabled', !trulse);
  };

  /**
   * Helper function to set the opacity of plottable
   *
   * @param {Object} scope The scope where the plottables exist
   * @param {Boolean} opacity New scaling factor of the plottables
   * (1.0 being standard opacity)
   * @param {Object[]} group list of mesh objects that should be changed
   * in scope
   *
   */
  OpacityViewController.prototype.setPlottableAttributes = function(
      scope, opacity, group) {
    var transparent = opacity !== 1;

    // webgl acts up with transparent objects, so we only set them to be
    // explicitly transparent if the opacity is not at full
    _.each(group, function(element) {
      scope.markers[element.idx].material.transparent = transparent;
      scope.markers[element.idx].material.opacity = opacity;
    });
    scope.needsUpdate = true;
  };

  /**
   * Helper function to get the scale for each metadata value
   *
   * @param {String[]} values The values to get scale for
   * @param {Boolean} scaled Whether or not to scale by values or just reset to
   * standard scale (1.0)
   *
   * @throws {Error} No or one numeric value in category and trying to scale by
   * value
   */
  OpacityViewController.prototype.getScale = function(values, scaled) {
    var scale = {}, numbers, val;
    if (!scaled) {
      _.each(values, function(element) {
        scale[element] = 1.0;
      });
    } else {
      //See if we have numeric values, fail if no
      var split = util.splitNumericValues(values);
      if (split.numeric.length < 2) {
        alert('Not enough numeric values in category, can not scale by value!');
        throw new Error('no numeric values');
      }

      // Alert if we have non-numerics and scale them to 0
      if (split.nonNumeric.length > 0) {
        _.each(split.nonNumeric, function(element) {
          scale[element] = 0.0;
        });
        alert('Non-numeric values detected. These will be hidden!');
      }

      // convert objects to numbers so we can map them to a color, we keep a
      // copy of the untransformed object so we can search the metadata
      numbers = _.map(split.numeric, parseFloat);

      //scale remaining values between 1 and 5 scale
      var min = _.min(numbers);
      var max = _.max(numbers);
      var range = max - min;

      _.each(split.numeric, function(element) {
        // note these elements are not numbers
        val = parseFloat(element);

        // Scale the values, then round to 4 decimal places.
        scale[element] = Math.round(((val - min) / range) * 10000) / 10000;
        });
    }
    return scale;
  };

  return OpacityViewController;
});
