define([
    "jquery",
    "underscore",
    "view",
    "viewcontroller",
    "color-editor",
    "chroma"
], function ($, _, DecompositionView, ViewControllers, Color, chroma) {

  // we only use the base attribute class, no need to get the base class
  var EmperorAttributeABC = ViewControllers.EmperorAttributeABC;
  var ColorEditor = Color.ColorEditor, ColorFormatter = Color.ColorFormatter;
  /**
   * @name ColorViewController
   *
   * @class Manipulates and displays the coloring of objects on screen.
   * @property {String} [title=""] Title of the controller.
   * @property {Node} [header=div node] jQuery element for the header
   * which contains the uppermost elements displayed in a tab.
   * @property {Node} [body=div node] jQuery element for the body,
   * which contains the lowermost elements displayed in tab.
   * This goes below the header.
   * @property {Node} [canvas=div node] jQuery element for the canvas,
   * which contains the header and the body.
   * @property {Node} [container=div node] jQuery element for the parent
   * container.
   * This only contains the canvas.
   * @property {Boolean} [active=false] Indicates whether the tab is front most
   * @property {String} [identifier="EMPtab-xxxxxxx"] Unique hash identifier
   * for the tab instance.
   * @property {Boolean} [enabled=true] Indicates if tab can be accessed.
   * @property {String} [description=""] Human-readable description of the tab.
   * @property {Node} [$select=chosen node] Drop-down menu to select the
   * metadata category to color by.
   * @property {Node} [$colormapSelect=chosen node] Drop-down menu to select
   * the colormap.
   * @property {Node} [$scaleDiv=div] jQuery element for the div containing the
   * SVG scale data
   * @property {SVG} [$colorScale] The SVG colorbar scale for the data
   * @property {Node} [$scaled=checkbox node] jQuery element for the checkbox
   * for toggling scaled coloring
   * @property {Node} [$scaledLabel=label node] jQuery element for the label for
   * the $scaled checkbox
   **/

  /*
   * @name ColorViewController
   *
   * @param {Node} container, Container node to create the controller in.
   * @params {Object} [decompViewDict] This is object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   *
   **/
  function ColorViewController(container, decompViewDict){
    var helpmenu = 'Change the colors of the attributes on the plot, such as ' +
      'spheres, vectors and ellipsoids.';
    var title = 'Color';

    // Constant for width in slick-grid
    var SLICK_WIDTH = 25, scope = this;
    var name, value, colorItem;

    // Create scale div and checkbox for whether using scalar data or not
    this.$colorScale = $("<svg width='90%' height='80%' style='display:block;margin:auto;'></svg>");
    this.$scaled = $("<input type='checkbox'>");
    this.$scaledLabel = $("<label for='scaled'>Continuous values</label>");

    // this class uses a colormap selector, so populate it before calling super
    // because otherwise the categorySelectionCallback will be called before the
    // data is populated
    this.$colormapSelect = $("<select class='emperor-tab-drop-down'>");
    var currType = ColorViewController.Colormaps[0].type;
    var selectOpts = $('<optgroup>').attr('label', currType);

    for (var i = 0; i < ColorViewController.Colormaps.length; i++) {
      var colormap = ColorViewController.Colormaps[i];
      // Check if we are in a new optgroup
      if (colormap.type !== currType) {
        currType = colormap.type;
        scope.$colormapSelect.append(selectOpts);
        selectOpts = $('<optgroup>').attr('label', currType);
      }
      var colorItem = $('<option>')
        .attr('value', colormap.id)
        .attr('data-type', currType)
        .text(colormap.name);
      selectOpts.append(colorItem);
    }
    scope.$colormapSelect.append(selectOpts);

    // Build the options dictionary
    var options = {
      'valueUpdatedCallback':
        function(e, args) {
          var val = args.item.category, color = args.item.value;
          var group = args.item.plottables;
          var element = scope.decompViewDict[scope.getActiveDecompViewKey()];
          scope.setPlottableAttributes(element, color, group);
        },
      'categorySelectionCallback':
        function(evt, params) {
          // we re-use this same callback regardless of whether the
          // color or the metadata category changed, maybe we can do
          // something better about this
          var category = scope.$select.val();
          var discrete = $('option:selected', scope.$colormapSelect)
                           .attr('data-type') == DISCRETE;
          var colorScheme = scope.$colormapSelect.val();

          var k = scope.getActiveDecompViewKey();
          var decompViewDict = scope.decompViewDict[k];

          if (discrete) {
            scope.$scaled.prop('checked', false);
            scope.$scaled.prop('hidden', true);
            scope.$scaledLabel.prop('hidden', true);
          } else {
            scope.$scaled.prop('hidden', false);
            scope.$scaledLabel.prop('hidden', false);
          }
          var scaled = scope.$scaled.is(':checked');
          // getting all unique values per categories
          var uniqueVals = decompViewDict.decomp.getUniqueValuesByCategory(category);
          // getting color for each uniqueVals
          var colorInfo = ColorViewController.getColorList(uniqueVals, colorScheme, discrete, scaled);
          var attributes = colorInfo[0];
          // fetch the slickgrid-formatted data
          var data = decompViewDict.setCategory(attributes, scope.setPlottableAttributes, category);

          if (scaled) {
            plottables = ColorViewController._nonNumericPlottables(uniqueVals, data);
            // Set SlickGrid for color of non-numeric values and show color bar for rest
            // if there are non numeric categories
            if (plottables.length > 0) {
              scope.setSlickGridDataset([{category: 'Non-numeric values', value: '#64655d', plottables: plottables}]);
            }
            else {
              scope.setSlickGridDataset([]);
            }
            scope.$colorScale.show();
            scope.$colorScale.html(colorInfo[1]);
          }
          else {
            scope.setSlickGridDataset(data);
            scope.$colorScale.hide();
          }
          // Call resize to update all methods for new shows/hides/resizes
          scope.resize()
        },
      'slickGridColumn': {
        id: 'title', name: '', field: 'value',
        sortable: false, maxWidth: SLICK_WIDTH,
        minWidth: SLICK_WIDTH,
        autoEdit: true,
        editor: ColorEditor,
        formatter: ColorFormatter
      }
    };

    EmperorAttributeABC.call(this, container, title, helpmenu,
                             decompViewDict, options);
    this.$header.append(this.$colormapSelect);
    this.$header.append(this.$scaled);
    this.$header.append(this.$scaledLabel);
    this.$body.prepend(this.$colorScale);

    // the chosen select can only be set when the document is ready
    $(function() {
      scope.$colormapSelect.chosen({width: "100%", search_contains: true});
      scope.$colormapSelect.chosen().change(options.categorySelectionCallback);
      scope.$scaled.on('change', options.categorySelectionCallback);
    });

    return this;
  }
  ColorViewController.prototype = Object.create(EmperorAttributeABC.prototype);
  ColorViewController.prototype.constructor = EmperorAttributeABC;


  /*
   * Helper for building the plottables for non-numeric data
   *
   * @param {uniqueVals} Array of unique values for the category
   * @param {data} SlickGrid formatted data from setCategory function
   *
   * @return {plottables} Array of plottables for all non-numeric values
   *
   */
   ColorViewController._nonNumericPlottables = function(uniqueVals, data) {
     // Filter down to only non-numeric data
     var nonNumeric = uniqueVals.filter(isNaN);
     var plotList = data.filter(function(x) {
       return $.inArray(x.category, nonNumeric) !== -1;
     });
     // Build list of plottables and return
     var plottables = [];
     for (var i = 0; i < plotList.length; i++) {
       plottables = plottables.concat(plotList[i].plottables);
     }
     return plottables;
   }


  /**
   *
   * Wrapper for generating a list of colors that corresponds to all samples
   * in the plot by coloring type requested
   *
   * @param {values} list of objects to generate a color for, usually a
   * category in a given metadata column.
   * @param {map} name of the color map to use, see
   * ColorViewController.Colormaps
   * @param {discrete} Whether to treat colormap requested as a discrete set
   * of colors or use interpolation to create gradient of colors
   * @param {scaled} Whether to use a scaled colormap or equidistant colors for
   * each value. Default is false.
   *
   * @return {colors} The object containing the hex colors keyed to each sample
   * @return {gradientSVG} The SVG string for the scaled data or null
   *
   */
  ColorViewController.getColorList = function(values, map, discrete, scaled) {
    var colors = {}, gradientSVG;
    scaled = scaled || false;

    if (_.findWhere(ColorViewController.Colormaps, {id: map}) === undefined){
      throw new Error("Could not find " + map + " as a colormap.");
    }

    // 1 color and continuous coloring should return the first element in map
    if (values.length == 1 && discrete === false) {
      colors[values[0]] = chroma.brewer[map][0];
      return [colors, gradientSVG];
    }

    //Call helper function to create the required colormap type
    if (discrete) {
      colors = ColorViewController.getDiscreteColors(values, map);
    }
    else if (scaled) {
      try {
        var info = ColorViewController.getScaledColors(values, map);
      } catch (e) {
        alert('less than 2 numeric values found, can not create scale for category!');
        throw new Error('non-numeric category');
      }
      colors = info[0];
      gradientSVG = info[1];
    }
    else {
      colors = ColorViewController.getInterpolatedColors(values, map);
    }
    return [colors, gradientSVG];
  };

  /**
   *
   * Retrieve a discrete color.
   *
   * @param {values} list of objects to generate a color for, usually a
   * category in a given metadata column.
   * @param {map} string, name of the discrete color map to use.
   *
   * @return {colors} The object containing the hex colors keyed to each sample
   *
   * Defaults to use qiime discrete colors if there's no map passed in.
   *
   */
  ColorViewController.getDiscreteColors = function(values, map) {
    map = map || 'discrete-coloring-qiime';

    if (map == 'discrete-coloring-qiime') {
      map = ColorViewController._qiimeDiscrete;
    } else {
      map = chroma.brewer[map];
    }
    var size = map.length;
    var colors = {};
    for (var i = 0; i < values.length; i++) {
        mapIndex = i - (Math.floor(i / size) * size);
        colors[values[i]] = map[mapIndex];
    }
    return colors;
  };

  /**
   *
   * Retrieve a scaled color set with scale bar.
   *
   * @param {values} list of objects to generate a color for, usually a
   * category in a given metadata column.
   * @param {map} string, name of the discrete color map to use.
   *
   * @return {colors} The object containing the hex colors keyed to each sample
   * @return {gradientSVG} The SVG string for the scaled data or null
   *
   * Defaults to use viridis colormap if there's no map passed in.
   *
   */
  ColorViewController.getScaledColors = function(values, map, nanColor) {
    map = map || 'viridis';
    nanColor = nanColor || '#64655d';
    map = chroma.brewer[map];

    // Get list of only numeric values, error if none
    numericValues = [];
    for(var i = 0; i < values.length; i++) {
      if (!isNaN(values[i])) {
        numericValues.push(Number(values[i]));
      }
    }
    if (numericValues.length < 2) {
      throw new Error('non-numeric category');
    }
    min = _.min(numericValues);
    max = _.max(numericValues);
    interpolator = chroma.scale(map).domain([min, max]);
    var colors = {};
    for (var i = 0; i < values.length; i++) {
      var val = Number(values[i]);
      if (!isNaN(val)) {
        colors[values[i]] = interpolator(val).hex();
      } else {
        //Gray out non-numeric values
        colors[values[i]] = nanColor;
      }
    }
    //build the SVG showing the gradient of colors for values
    var mid = (min + max) / 2;
    var step = (max - min) / 100;
    var stopColors = [];
    for (var s = min; s <= max; s += step) {
      stopColors.push(interpolator(s).hex());
    }
    var gradientSVG = '<defs><linearGradient id="Gradient" x1="0" x2="0" y1="0" y2="1">';
    for (var pos = 0; pos < stopColors.length; pos++) {
      gradientSVG += '<stop offset="' + pos + '%" stop-color="' + stopColors[pos] + '"/>';
    }
    gradientSVG += '</defs><rect id="gradientRect" width="20" height="100%" fill="url(#Gradient)"/>';
    // Note the plus sign before min, midm and max drops any extra zeroes at the end.
    gradientSVG += '<text x="25" y="12px" font-family="sans-serif" font-size="12px" text-anchor="start">' + min + '</text>';
    gradientSVG += '<text x="25" y="50%" font-family="sans-serif" font-size="12px" text-anchor="start">' + mid + '</text>';
    gradientSVG += '<text x="25" y="100%" font-family="sans-serif" font-size="12px" text-anchor="start">' + max + '</text>';
    return [colors, gradientSVG];
  };

  /**
   *
   * Retrieve an interpolatd color set.
   *
   * @param {values} list of objects to generate a color for, usually a
   * category in a given metadata column.
   * @param {map} string, name of the discrete color map to use.
   *
   * @return {colors} The object containing the hex colors keyed to each sample
   *
   * Defaults to use viridis colormap if there's no map passed in.
   *
   */
  ColorViewController.getInterpolatedColors = function(values, map) {
    map = map || 'viridis';
    map = chroma.brewer[map];

    var total = values.length;
    interpolator = chroma.bezier([map[0], map[3], map[4], map[5], map[8]]);
    var colors = {};
    for(var i = 0; i < values.length; i++) {
      colors[values[i]] = interpolator(i / total).hex();
    }
    return colors;
  }

  /**
   * Converts the current instance into a JSON string.
   *
   * @return {Object} JSON ready representation of self.
   */
  ColorViewController.prototype.toJSON = function() {
    var json = EmperorAttributeABC.prototype.toJSON.call(this);
    json.colormap = this.$colormapSelect.val();
    json.continuous = this.$scaled.is(':checked');
    return json;
  }

  /**
   * Decodes JSON string and modifies its own instance variables accordingly.
   *
   * @param {Object} Parsed JSON string representation of self.
   */
  ColorViewController.prototype.fromJSON = function(json) {
    // Order here is important. We want to set all the extra controller
    // settings before we load from json, as they can override the JSON when set
    this.$colormapSelect.val(json.colormap);
    this.$colormapSelect.trigger('chosen:updated');
    this.$scaled.prop('checked', json.continuous);
    this.$scaled.trigger('change');
    EmperorAttributeABC.prototype.fromJSON.call(this, json);
  }

  /**
   * Helper function to set the color of plottable
   *
   * @param {scope} object, the scope where the plottables exist
   * @param {color} string, hexadecimal representation of a color, which will
   * be applied to the plottables
   * @param {group} array of objects, list of object that should be changed in
   * scope
   */
  ColorViewController.prototype.setPlottableAttributes = function(scope, color, group){
    var idx;

    _.each(group, function(element) {
      idx = element.idx;
      scope.markers[idx].material.color = new THREE.Color(color);
    });
  };

  var DISCRETE = 'Discrete';
  var SEQUENTIAL = 'Sequential';
  var DIVERGING = 'Diverging';
  ColorViewController.Colormaps = [
    {id: 'discrete-coloring-qiime', name: 'Classic QIIME Colors', type: DISCRETE},
    {id: 'Paired', name: 'Paired', type: DISCRETE},
    {id: 'Accent', name: 'Accent', type: DISCRETE},
    {id: 'Dark2', name: 'Dark', type: DISCRETE},
    {id: 'Set1', name: 'Set1', type: DISCRETE},
    {id: 'Set2', name: 'Set2', type: DISCRETE},
    {id: 'Set3', name: 'Set3', type: DISCRETE},
    {id: 'Pastel1', name: 'Pastel1', type: DISCRETE},
    {id: 'Pastel2', name: 'Pastel2', type: DISCRETE},

    {id: 'Viridis', name: 'Viridis', type: SEQUENTIAL},
    {id: 'Reds', name: 'Reds', type: SEQUENTIAL},
    {id: 'RdPu', name: 'Red-Purple', type: SEQUENTIAL},
    {id: 'Oranges', name: 'Oranges', type: SEQUENTIAL},
    {id: 'OrRd', name: 'Orange-Red', type: SEQUENTIAL},
    {id: 'YlOrBr', name: 'Yellow-Orange-Brown', type: SEQUENTIAL},
    {id: 'YlOrRd', name: 'Yellow-Orange-Red', type: SEQUENTIAL},
    {id: 'YlGn', name: 'Yellow-Green', type: SEQUENTIAL},
    {id: 'YlGnBu', name: 'Yellow-Green-Blue', type: SEQUENTIAL},
    {id: 'Greens', name: 'Greens', type: SEQUENTIAL},
    {id: 'GnBu', name: 'Green-Blue', type: SEQUENTIAL},
    {id: 'Blues', name: 'Blues', type: SEQUENTIAL},
    {id: 'BuGn', name: 'Blue-Green', type: SEQUENTIAL},
    {id: 'BuPu', name: 'Blue-Purple', type: SEQUENTIAL},
    {id: 'Purples', name: 'Purples', type: SEQUENTIAL},
    {id: 'PuRd', name: 'Purple-Red', type: SEQUENTIAL},
    {id: 'PuBuGn', name: 'Purple-Blue-Green', type: SEQUENTIAL},
    {id: 'Greys', name: 'Greys', type: SEQUENTIAL},

    {id: 'Spectral', name: 'Spectral', type: DIVERGING},
    {id: 'RdBu', name: 'Red-Blue', type: DIVERGING},
    {id: 'RdYlGn', name: 'Red-Yellow-Green', type: DIVERGING},
    {id: 'RdYlB', name: 'Red-Yellow-Blue', type: DIVERGING},
    {id: 'RdGy', name: 'Red-Grey', type: DIVERGING},
    {id: 'PiYG', name: 'Pink-Yellow-Green', type: DIVERGING},
    {id: 'BrBG', name: 'Brown-Blue-Green', type: DIVERGING},
    {id: 'PuOr', name: 'Purple-Orange', type: DIVERGING},
    {id: 'PRGn', name: 'Purple-Green', type: DIVERGING}
  ];


  // taken from the qiime/colors.py module; a total of 24 colors
  ColorViewController._qiimeDiscrete = ["#ff0000", "#0000ff", "#f27304",
  "#008000", "#91278d", "#ffff00", "#7cecf4", "#f49ac2", "#5da09e", "#6b440b",
  "#808080", "#f79679", "#7da9d8", "#fcc688", "#80c99b", "#a287bf", "#fff899",
  "#c49c6b", "#c0c0c0", "#ed008a", "#00b6ff", "#a54700", "#808000", "#008080"];

  return ColorViewController;
});
