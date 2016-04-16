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

    // this class uses a colormap selector, so populate it before calling super
    // because otherwise the categorySelectionCallback will be called before the
    // data is populated
    this.$colormapSelect = $("<select class='emperor-tab-drop-down'>");

    for (var i = 0; i < ColorViewController.Colormaps.length; i++){
      // the first array has the values that should be displayed on the UI
      // the second array has the identifiers used to generate the colors
      value = ColorViewController.Colormaps[i];
      name = ColorViewController.ColormapNames[i];
      colorItem = $('<option>').attr('value', value).text(name);

      scope.$colormapSelect.append(colorItem);
    }

    // Build the options dictionary
    var options = {'valueUpdatedCallback':function(e, args) {
      var val = args.item.category, color = args.item.value;
      var group = args.item.plottables;
      var element = scope.decompViewDict[scope.getActiveDecompViewKey()];
      ColorViewController.setPlottableAttributes(element, color, group);
    },
      'categorySelectionCallback':function(evt, params) {
        // we re-use this same callback regardless of whether the
        // color or the metadata category changed, maybe we can do
        // something better about this
        var category = scope.$select.val();
        var colorScheme = scope.$colormapSelect.val();

        var k = scope.getActiveDecompViewKey();
        var decompViewDict = scope.decompViewDict[k];

        // getting all unique values per categories
        var uniqueVals = decompViewDict.decomp.getUniqueValuesByCategory(category);
        // getting color for each uniqueVals
        var attributes = ColorViewController.getColorList(uniqueVals, colorScheme);
        // fetch the slickgrid-formatted data
        var data = decompViewDict.setCategory(attributes, ColorViewController.setPlottableAttributes, category);

        scope.setSlickGridDataset(data);
      },
      'slickGridColumn':{id: 'title', name: '', field: 'value',
        sortable: false, maxWidth: SLICK_WIDTH,
        minWidth: SLICK_WIDTH,
        autoEdit: true,
        editor: ColorEditor,
        formatter: ColorFormatter}};

    EmperorAttributeABC.call(this, container, title, helpmenu,
                             decompViewDict, options);
    this.$header.append(this.$colormapSelect);

    // the chosen select can only be set when the document is ready
    $(function() {
      scope.$colormapSelect.chosen({width: "100%", search_contains: true});
      scope.$colormapSelect.chosen().change(options.categorySelectionCallback);
    });

    return this;
  }
  ColorViewController.prototype = Object.create(EmperorAttributeABC.prototype);
  ColorViewController.prototype.constructor = EmperorAttributeABC;


  /**
   *
   * Generate a list of colors that corresponds to all the samples in the plot
   *
   * @param {values} list of objects to generate a color for, usually a
   * category in a given metadata column.
   * @param {map} name of the color map to use, see
   * ColorViewController.Colormaps
   *
   *
   * This function will generate a list of coloring values depending on the
   * coloring scheme that the system is currently using (discrete or
   * continuous).
   */
  ColorViewController.getColorList = function(values, map) {
    var colors = {}, numColors = values.length-1, counter=0, discrete = false;
    var interpolator;

    if (ColorViewController.Colormaps.indexOf(map) === -1) {
      throw new Error("Could not find "+map+" in the available colormaps");
    }

    if (map === 'discrete-coloring' || map === 'discrete-coloring-qiime'){
      discrete = true;
    }

    // 1 color and continuous coloring should return the first element of the
    // map
    if (numColors === 0 && discrete === false){
      colors[values[0]] = chroma.brewer[map][0];
      return colors;
    }

    if (discrete === false){
      map = chroma.brewer[map];
      interpolator = chroma.bezier([map[0], map[3], map[4], map[5], map[8]]);
    }

    for(var index in values){
      if(discrete){
        // get the next available color
        colors[values[index]] = ColorViewController.getDiscreteColor(index, map);
      }
      else{
        colors[values[index]] =  interpolator(counter/numColors).hex();
        counter = counter + 1;
      }
    }

    return colors;
  };

  /**
   *
   * Retrieve a discrete color.
   *
   * @param {index} int, the index of the color to retrieve.
   * @param {map} string, name of the discrete color map to use.
   *
   * @return string representation of the hexadecimal value for a color in the
   * list the QIIME colors or the ColorBrewer discrete colors. If this value
   * value is greater than the number of colors available, the function will just
   * rollover and retrieve the next available color.
   *
   * Defaults to use ColorBrewer colors if there's no map passed in.
   *
   */
  ColorViewController.getDiscreteColor = function(index, map){
    if (map === undefined){
      map = 'discrete-coloring';
    }
    if (_.has(ColorViewController._discreteColormaps, map) === false){
      throw new Error("Could not find "+map+" as a discrete colormap.");
    }

    var size = ColorViewController._discreteColormaps[map].length;
    if(index >= size){
      index = index - (Math.floor(index/size)*size);
    }

    return ColorViewController._discreteColormaps[map][index];
  };

  /**
   * Helper function to set the color of plottable
   *
   * @param {scope} object, the scope where the plottables exist
   * @param {color} string, hexadecimal representation of a color, which will
   * be applied to the plottables
   * @param {group} array of objects, list of object that should be changed in
   * scope
   */
  ColorViewController.setPlottableAttributes = function(scope, color, group){
    var idx;

    _.each(group, function(element) {
      idx = element.idx;
      scope.markers[idx].material.color = new THREE.Color(color);
    });
  };

  ColorViewController.Colormaps = ['discrete-coloring-qiime',
  'discrete-coloring', 'OrRd', 'PuBu', 'BuPu', 'Oranges', 'BuGn', 'YlOrBr',
  'YlGn', 'Reds', 'RdPu', 'Greens', 'YlGnBu', 'Purples', 'GnBu', 'Greys',
  'YlOrRd', 'PuRd', 'Blues', 'PuBuGn', 'Spectral', 'RdYlGn', 'RdBu', 'PiYG',
  'PRGn', 'RdYlBu', 'BrBG', 'RdGy', 'PuOr', 'Viridis'];
  ColorViewController.ColormapNames = ['Classic QIIME Colors',
  'Discrete Coloring (Colorbrewer)', 'Orange-Red', 'Purple-Blue',
  'Blue-Purple', 'Oranges', 'Blue-Green', 'Yellow-Orange-Brown',
  'Yellow-Green', 'Reds', 'Red-Purple', 'Greens', 'Yellow-Green-Blue',
  'Purples', 'Green-Blue', 'Greys', 'Yellow-Orange-Red', 'Purple-Red', 'Blues',
  'Purple-Blue-Green', 'Spectral', 'Red-Yellow-Green', 'Red-Blue',
  'Pink-Yellow-Green', 'Pink-Red-Green', 'Red-Yellow-Blue', 'Brown-Blue-Green',
  'Red-Grey', 'Purple-Orange', 'Viridis'];
  ColorViewController._colorbrewerDiscrete = ["#8dd3c7", "#ffffb3", "#bebada",
  "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd",
  "#ccebc5", "#ffed6f", /*first list ends here*/ "#a6cee3", "#1f78b4",
  "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6",
  "#6a3d9a", "#ffff99", "#b15928"];

  // taken from the qiime/colors.py module; a total of 24 colors
  ColorViewController._qiimeDiscrete = [ "#ff0000", "#0000ff", "#f27304",
  "#008000", "#91278d", "#ffff00", "#7cecf4", "#f49ac2", "#5da09e", "#6b440b",
  "#808080", "#f79679", "#7da9d8", "#fcc688", "#80c99b", "#a287bf", "#fff899",
  "#c49c6b", "#c0c0c0", "#ed008a", "#00b6ff", "#a54700", "#808000", "#008080"];
  ColorViewController._discreteColormaps = {
    "discrete-coloring":ColorViewController._colorbrewerDiscrete,
    "discrete-coloring-qiime":ColorViewController._qiimeDiscrete
  };

  return ColorViewController;
});
