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
   * @class ScaleViewController
   *
   * Alters the scale of points displayed on the screen.
   *
   * @param {Node} container Container node to create the controller in.
   * @param {Object} decompViewDict This object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   *
   * @return {ScaleViewController}
   * @constructs ScaleViewController
   * @extends EmperorAttributeABC
   *
   **/
  function ScaleViewController(container, decompViewDict) {
    var helpmenu = 'Change the scale of the attributes on the plot, allowing ' +
                   'highlighting of points using size.';
    var title = 'Scale';
    // Create checkbox for scaling by values
    /**
     * jQuery node for checkbox controlling whether to scale by values or not
     * @type {Node}
     */
    this.$scaledValue = $('<input type="checkbox">');
    /**
     * jQuery node for label of $scaledValues
     * @type {Node}
     */
    this.$scaledLabel = $('<label>Scale by values</label>');

    //Create global scale bar
    /**
     * jQuery node for global scale bar container div
     * @type {Node}
     */
    this.$globalDiv = $('<div style="width:100%;padding:5px;">');
    this.$globalDiv.html('<p>Global Scaling</p>');
    var $sliderDiv = $('<div style="width:80%;display:inline-block;">');
    var $viewval = $('<input type="text" value="1.0" readonly ' +
                     'style="border:0;width:25px;' +
                     'background-color:rgb(238, 238, 238)">');
    /**
     * jQuery node for global scale bar
     * @type {Node}
     */
    this.$sliderGlobal = $sliderDiv.slider({
        range: 'max',
        min: 0.1,
        max: 5.0,
        value: 1.0,
        step: 0.1,
        slide: function(event, ui) {
          $viewval.val(ui.value);
        },
        stop: function(event, ui) {
          // Update the slickgrid values with the new scale
          var data = scope.getSlickGridDataset();
          _.each(data, function(element) {
            element.value = ui.value;
          });
          scope.setSlickGridDataset(data);

          //Update the scales for all meshes
          var dv = scope.decompViewDict[scope.getActiveDecompViewKey()];
          _.each(dv.markers, function(element) {
            element.scale.set(ui.value, ui.value, ui.value);
          });
          dv.needsUpdate = true;
        }
      });
    this.$globalDiv.append($viewval);
    this.$globalDiv.append($sliderDiv);

    // Constant for width in slick-grid
    var SLICK_WIDTH = 50, scope = this;

    // Build the options dictionary
    var options = {'valueUpdatedCallback': function(e, args) {
      var scale = +args.item.value;
      var group = args.item.plottables;
      var element = scope.decompViewDict[scope.getActiveDecompViewKey()];
      scope.setPlottableAttributes(element, scale, group);
    },
      'categorySelectionCallback': function(evt, params) {
        var category = scope.$select.val();

        var k = scope.getActiveDecompViewKey();
        var decompViewDict = scope.decompViewDict[k];

        // getting all unique values per categories
        var uniqueVals = decompViewDict.decomp.getUniqueValuesByCategory(
          category);
        // getting scale value for each point
        var scaled = scope.$scaledValue.is(':checked');
        try {
          var attributes = scope.getScale(uniqueVals, scaled);
        } catch (err) {
          // Do not fire off action, instead just reshow globalDiv so we don't
          // lose the current scaling values.
          scope.$scaledValue.prop('checked', false);
          return;
        }
        if (scaled) {
          scope.$globalDiv.hide();
        }
        else {
          scope.$globalDiv.show();
        }
        scope.resize();

        // fetch the slickgrid-formatted data
        var data = decompViewDict.setCategory(
          attributes, scope.setPlottableAttributes, category);

        scope.setSlickGridDataset(data);
      },
      'slickGridColumn': {id: 'title', name: '', field: 'value',
        sortable: false, maxWidth: SLICK_WIDTH,
        minWidth: SLICK_WIDTH,
        autoEdit: true,
        editor: ScaleEditor.ScaleEditor}};

    EmperorAttributeABC.call(this, container, title, helpmenu,
        decompViewDict, options);
    this.$header.append(this.$scaledValue);
    this.$header.append(this.$scaledLabel);
    this.$body.prepend(this.$globalDiv);

    scope.$scaledValue.on('change', options.categorySelectionCallback);

    return this;
  }
  ScaleViewController.prototype = Object.create(EmperorAttributeABC.prototype);
  ScaleViewController.prototype.constructor = EmperorAttributeABC;

  /**
   * Converts the current instance into a JSON string.
   *
   * @return {Object} JSON ready representation of self.
   */
  ScaleViewController.prototype.toJSON = function() {
    var json = EmperorAttributeABC.prototype.toJSON.call(this);
    json.globalScale = this.$globalDiv.children('input').val();
    json.scaleVal = this.$scaledValue.is(':checked');
    return json;
  };

  /**
   * Decodes JSON string and modifies its own instance variables accordingly.
   *
   * @param {Object} Parsed JSON string representation of self.
   */
  ScaleViewController.prototype.fromJSON = function(json) {
    // Can't call super because select needs to be set first
    // Order here is important. We want to set all the extra controller
    // settings before we load from json, as they can override the JSON when set
    this.$select.val(json.category);
    this.$select.trigger('chosen:updated');
    this.$sliderGlobal.slider('value', json.globalScale);
    this.$scaledValue.prop('checked', json.scaleVal);
    this.$scaledValue.trigger('change');

    // fetch and set the SlickGrid-formatted data
    var k = this.getActiveDecompViewKey();
    var data = this.decompViewDict[k].setCategory(
      json.data, this.setPlottableAttributes, json.category);
    this.setSlickGridDataset(data);
    // set all to needsUpdate
    this.decompViewDict[k].needsUpdate = true;
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
  ScaleViewController.prototype.resize = function(width, height) {
    this.$body.height(this.$canvas.height() - this.$header.height());
    this.$body.width(this.$canvas.width());

    //scale gridDiv based on whether global scaling available or not
    if (this.$scaledValue.is(':checked')) {
      this.$gridDiv.css('height', '100%');
    }
    else {
      this.$gridDiv.css(
        'height', this.$body.height() - this.$globalDiv.height() - 10);
    }

    // call super, most of the header and body resizing logic is done there
    EmperorAttributeABC.prototype.resize.call(this, width, height);
  };

  /**
   * Helper function to set the scale of plottable
   *
   * @param {Object} scope The scope where the plottables exist
   * @param {Boolean} scale New scaling factor of the plottables
   * (1.0 being standard scale)
   * @param {Object[]} group list of mesh objects that should be changed
   * in scope
   *
   */
  ScaleViewController.prototype.setPlottableAttributes = function(
      scope, scale, group) {
    var idx;

    _.each(group, function(element) {
      idx = element.idx;
      scope.markers[idx].scale.set(scale, scale, scale);
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
  ScaleViewController.prototype.getScale = function(values, scaled) {
    var scale = {};
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

      //scale remaining values between 1 and 5 scale
      var min = _.min(split.numeric);
      var max = _.max(split.numeric);
      var range = max - min;
      _.each(split.numeric, function(element) {
          // Scale the values, then round to 4 decimaal places.
          scale[element] = Math.round(
            (1 + (element - min) * 4 / range) * 10000) / 10000;
        });
    }
    return scale;
  };

  return ScaleViewController;
});
