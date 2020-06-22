define([
    'three',
    'orbitcontrols',
    'draw',
    'underscore',
    'selectionbox',
    'selectionhelper'
], function(THREE, OrbitControls, draw, _, SelectionBox, SelectionHelper) {
  /** @private */
  var makeLine = draw.makeLine;
  /** @private */
  var makeLabel = draw.makeLabel;

  /**
   *
   * @class ScenePlotView3D
   *
   * Represents a three dimensional scene in THREE.js.
   *
   * @param {UIState} uiState shared UIState state object
   * @param {THREE.renderer} renderer THREE renderer object.
   * @param {Object} decViews dictionary of DecompositionViews shown in this
   * scene
   * @param {MultiModel} decModels MultiModel of DecompositionModels shown in
   * this scene (with extra global data about them)
   * @param {Node} container Div where the scene will be rendered.
   * @param {Float} xView Horizontal position of the rendered scene in the
   * container element.
   * @param {Float} yView Vertical position of the rendered scene in the
   * container element.
   * @param {Float} width The width of the renderer
   * @param {Float} height The height of the renderer
   *
   * @return {ScenePlotView3D} An instance of ScenePlotView3D.
   * @constructs ScenePlotView3D
   */
  function ScenePlotView3D(uiState, renderer, decViews, decModels, container,
                           xView, yView, width, height) {
    var scope = this;

    this.UIState = uiState;

    // convert to jquery object for consistency with the rest of the objects
    var $container = $(container);
    this.decViews = decViews;
    this.decModels = decModels;
    this.renderer = renderer;
    /**
     * Horizontal position of the scene.
     * @type {Float}
     */
    this.xView = xView;
    /**
     * Vertical position of the scene.
     * @type {Float}
     */
    this.yView = yView;
    /**
     * Width of the scene.
     * @type {Float}
     */
    this.width = width;
    /**
     * Height of the scene.
     * @type {Float}
     */
    this.height = height;
    /**
     * Axes color.
     * @type {String}
     * @default '#FFFFFF' (white)
     */
    this.axesColor = '#FFFFFF';
    /**
     * Background color.
     * @type {String}
     * @default '#000000' (black)
     */
    this.backgroundColor = '#000000';
    /**
     * True when changes have occured that require re-rendering of the canvas
     * @type {Boolean}
     */
    this.needsUpdate = true;
    /**
     * Array of integers indicating the index of the visible dimension at each
     * axis ([x, y, z]).
     * @type {Integer[]}
     */
    this.visibleDimensions = _.clone(this.decViews.scatter.visibleDimensions);

    // used to name the axis lines/labels in the scene
    this._axisPrefix = 'emperor-axis-line-';
    this._axisLabelPrefix = 'emperor-axis-label-';

    //need to initialize the scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(this.backgroundColor);

    /**
     * Camera used to display the scatter scene.
     * @type {THREE.OrthographicCamera}
     */
    this.scatterCam = this.buildCamera('scatter');

    /**
     * Object used to light the scene in scatter mode,
     * by default is set to a light and
     * transparent color (0x99999999).
     * @type {THREE.DirectionalLight}
     */
    this.light = new THREE.DirectionalLight(0x999999, 2);
    this.light.position.set(1, 1, 1).normalize();
    this.scatterCam.add(this.light);

    /**
     * Camera used to display the parallel plot scene.
     * @type {THREE.OrthographicCamera}
     */
    this.parallelCam = this.buildCamera('parallel-plot');

    // use $container.get(0) to retrieve the native DOM object
    this.scatterController = this.buildCamController('scatter',
                                                    this.scatterCam,
                                                    $container.get(0));
    this.parallelController = this.buildCamController('parallel-plot',
                                                     this.parallelCam,
                                                     $container.get(0));
    this.control = this.scatterController;

    this.scene.add(this.scatterCam);
    this.scene.add(this.parallelCam);

    this._raycaster = new THREE.Raycaster();
    this._mouse = new THREE.Vector2();

    /**
     * Special purpose group for points that are selectable with the
     * SelectionBox.
     * @type {THREE.Group}
     * @private
     */
    this._selectable = new THREE.Group();
    this.scene.add(this._selectable);

    /**
     * Object to compute bounding boxes from a selection area
     *
     * Selection is only enabled when the user is holding Shift.
     *
     * @type {THREE.SelectionBox}
     * @private
     */
    this._selectionBox = new THREE.SelectionBox(this.camera,
                                                this._selectable);

    /**
     * Helper to view the selection space when the user holds shift
     *
     * This object is disabled by default, and is only renabled when the user
     * holds the shift key.
     * @type {THREE.SelectionHelper}
     * @private
     */
    this._selectionHelper = new THREE.SelectionHelper(this._selectionBox,
                                                     renderer,
                                                     'emperor-selection-area');
    this._selectionHelper.enabled = false;

    //Swap the camera whenever the view type changes
    this.UIState.registerProperty('view.viewType', function(evt) {
      if (evt.newVal === 'parallel-plot') {
        scope.camera = scope.parallelCam;
        scope.control = scope.parallelController;
        //Don't let the controller move around when its not the active camera
        scope.scatterController.enabled = false;
        scope.scatterController.autoRotate = false;
        scope.parallelController.enabled = true;
        scope._selectionBox.camera = scope.camera;
        scope._selectionBox.collection = [];
      } else {
        scope.camera = scope.scatterCam;
        scope.control = scope.scatterController;
        //Don't let the controller move around when its not the active camera
        scope.scatterController.enabled = true;
        scope.parallelController.enabled = false;
        scope._selectionBox.camera = scope.camera;
        scope._selectionBox.collection = [];
      }
    });

    this.addDecompositionsToScene();

    this.updateCameraTarget();
    this.control.update();

    this.scatterController.addEventListener('change', function() {
      scope.needsUpdate = true;
    });
    this.parallelController.addEventListener('change', function() {
      scope.needsUpdate = true;
    });

    /**
     * Object with "min" and "max" attributes each of which is an array with
     * the ranges that covers all of the decomposition views.
     * @type {Object}
     */
    this.drawAxesWithColor('#FFFFFF');
    this.drawAxesLabelsWithColor('#FFFFFF');

    // initialize subscribers for event callbacks
    /**
     * Events allowed for callbacks. DO NOT EDIT.
     * @type {String[]}
     */
    this.EVENTS = ['click', 'dblclick', 'select'];
    /** @private */
    this._subscribers = {};

    for (var i = 0; i < this.EVENTS.length; i++) {
      this._subscribers[this.EVENTS[i]] = [];
    }

    // Add callback call when sample is clicked
    // Double and single click together from: http://stackoverflow.com/a/7845282
    var DELAY = 200, clicks = 0, timer = null;
    $container.on('mousedown', function(event) {
        clicks++;
        if (clicks === 1) {
            timer = setTimeout(function() {
                scope._eventCallback('click', event);
                clicks = 0;
            }, DELAY);
        }
        else {
            clearTimeout(timer);
            scope._eventCallback('dblclick', event);
            clicks = 0;
        }
    })
    .on('dblclick', function(event) {
        event.preventDefault();  //cancel system double-click event
    });

    // setup the selectionBox and selectionHelper objects and callbacks
    this._addSelectionEvents($container);

    this.control.update();

    // register callback for populating info with clicked sample name
    // set the timeout for fading out the info div
    var infoDuration = 4000;
    var infoTimeout = setTimeout(function() {
        scope.$info.fadeOut();
      }, infoDuration);

    /**
     *
     * The functions showText and copyToClipboard are used in the 'click',
     * 'dblclick', and 'select' events.
     *
     * When a sample is clicked we show a legend at the bottom left of the
     * view. If this legend is clicked, we copy the sample name to the
     * clipboard. When a sample is double-clicked we directly copy the sample
     * name to the clipboard and add the legend at the bottom left of the view.
     *
     * When samples are selected we show a message on the bottom left of the
     * view, and copy a comma-separated list of samples to the clipboard.
     *
     */

    function showText(n, i) {
      clearTimeout(infoTimeout);
      scope.$info.text(n);
      scope.$info.show();

      // reset the timeout for fading out the info div
      infoTimeout = setTimeout(function() {
        scope.$info.fadeOut();
        scope.$info.text('');
      }, infoDuration);
    }

    function copyToClipboard(text) {
      var $temp = $('<input>');

      // we need an input element to be able to copy to clipboard, taken from
      // https://codepen.io/shaikmaqsood/pen/XmydxJ/
      $('body').append($temp);
      $temp.val(text).select();
      document.execCommand('copy');
      $temp.remove();
    }

    //Add info div as bottom of canvas
    this.$info = $('<div>').attr('title', 'Click to copy to clipboard');
    this.$info.css({'position': 'absolute',
                    'bottom': 0,
                    'height': 16,
                    'width': '50%',
                    'padding-left': 10,
                    'padding-right': 10,
                    'font-size': 12,
                    'z-index': 10000,
                    'background-color': 'rgb(238, 238, 238)',
                    'border': '1px solid black',
                    'font-family': 'Verdana,Arial,sans-serif'}).hide();
    this.$info.click(function() {
      var text = scope.$info.text();

      // handle the case where multiple clicks are received
      text = text.replace(/\(copied to clipboard\) /g, '');
      copyToClipboard(text);

      scope.$info.effect('highlight', {}, 500);
      scope.$info.text('(copied to clipboard) ' + text);
    });
    $(this.renderer.domElement).parent().append(this.$info);

    // UI callbacks specific to emperor, not to be confused with DOM events
    this.on('click', showText);
    this.on('dblclick', function(n, i) {
      copyToClipboard(n);
      showText('(copied to clipboard) ' + n, i);
    });
    this.on('select', function(names, view) {
      if (names.length) {
        showText(names.length + ' samples copied to your clipboard.');
        copyToClipboard(names.join(','));
      }
    });

    // if a decomposition uses a point cloud, or
    // if a decomposition uses a parallel plot,
    // update the default raycasting tolerance as
    // it is otherwise too large and error-prone
    var updateRaycasterLinePrecision = function(evt) {
      if (scope.UIState.getProperty('view.viewType') === 'parallel-plot')
        scope._raycaster.params.Line.threshold = 0.01;
      else
        scope._raycaster.params.Line.threshold = 1;
    };
    var updateRaycasterPointPrecision = function(evt) {
      if (scope.UIState.getProperty('view.usesPointCloud'))
        scope._raycaster.params.Points.threshold = 0.01;
      else
        scope._raycaster.params.Points.threshold = 1;
    };
    this.UIState.registerProperty('view.usesPointCloud',
                             updateRaycasterPointPrecision);
    this.UIState.registerProperty('view.viewType',
                             updateRaycasterLinePrecision);
  };

  /**
   * Builds a camera (for scatter or parallel plot)
   */
  ScenePlotView3D.prototype.buildCamera = function(viewType) {

    var camera;
    if (viewType === 'scatter')
    {
      // Set up the camera
      var max = _.max(this.decViews.scatter.decomp.dimensionRanges.max);
      var frontFrust = _.min([max * 0.001, 1]);
      var backFrust = _.max([max * 100, 100]);

      // these are placeholders that are
      // later updated in updateCameraAspectRatio
      camera = new THREE.OrthographicCamera(-50, 50, 50, -50);
      camera.position.set(0, 0, max * 5);
      camera.zoom = 0.7;
    }
    else if (viewType === 'parallel-plot')
    {
      var w = this.decModels.dimensionRanges.max.length;

      // Set up the camera
      camera = new THREE.OrthographicCamera(0, w, 1, 0);
      camera.position.set(0, 0, 1); //Must set positive Z because near > 0
      camera.zoom = 0.7;
    }

    return camera;
  };

  /**
   * Builds a camera controller (for scatter or parallel plot)
   */
  ScenePlotView3D.prototype.buildCamController = function(viewType, cam, view) {
    /**
     * Object used to interact with the scene. By default it uses the mouse.
     * @type {THREE.OrbitControls}
     */
    var control = new THREE.OrbitControls(cam, view);
    control.enableKeys = false;
    control.rotateSpeed = 1.0;
    control.zoomSpeed = 1.2;
    control.panSpeed = 0.8;
    control.enableZoom = true;
    control.enablePan = true;

    // don't free panning and rotation for paralle plots
    control.screenSpacePanning = (viewType === 'scatter');
    control.enableRotate = (viewType === 'scatter');

    return control;
  };

  /**
   *
   * Adds all the decomposition views to the current scene.
   *
   */
  ScenePlotView3D.prototype.addDecompositionsToScene = function() {
    var j, marker, scaling = this.getScalingConstant();

    // Note that the internal logic of the THREE.Scene object prevents the
    // objects from being re-added so we can simply iterate over all the
    // decomposition views.

    // Add all the meshes to the scene, iterate through all keys in
    // decomposition view dictionary and put points in a separate group
    for (var decViewName in this.decViews) {
      var isArrowType = this.decViews[decViewName].decomp.isArrowType();

      for (j = 0; j < this.decViews[decViewName].markers.length; j++) {
        marker = this.decViews[decViewName].markers[j];

        // only arrows include text as part of their markers
        // arrows are not selectable
        if (isArrowType) {
          marker.label.scale.set(marker.label.scale.x * scaling,
                                 marker.label.scale.y * scaling, 1);
          this.scene.add(marker);
        }
        else {
          this._selectable.add(marker);
        }
      }
      for (j = 0; j < this.decViews[decViewName].ellipsoids.length; j++) {
        this.scene.add(this.decViews[decViewName].ellipsoids[j]);
      }

      // if the left lines exist so will the right lines
      if (this.decViews[decViewName].lines.left) {
        this.scene.add(this.decViews[decViewName].lines.left);
        this.scene.add(this.decViews[decViewName].lines.right);
      }
    }

    this.needsUpdate = true;
  };

  /**
   * Calculate a scaling constant for the text in the scene.
   *
   * It is important that this factor is calculated based on all the elements
   * in a scene, and that it is the same for all the text elements in the
   * scene. Otherwise, some text will be bigger than other.
   *
   * @return {Number} The scaling factor to use for labels.
   */
  ScenePlotView3D.prototype.getScalingConstant = function() {
    return (this.decModels.dimensionRanges.max[0] -
            this.decModels.dimensionRanges.min[0]) * 0.001;
  };

  /**
   *
   * Helper method used to iterate over the ranges of the visible dimensions.
   *
   * This function that centralizes the pattern followed by drawAxesWithColor
   * and drawAxesLabelsWithColor.
   *
   * @param {Function} action a function that can take up to three arguments
   * "start", "end" and "index".  And for each visible dimension the function
   * will get the "start" and "end" of the range, and the current "index" of the
   * visible dimension.
   * @private
   *
   */
  ScenePlotView3D.prototype._dimensionsIterator = function(action) {

    this.decModels._unionRanges();

    if (this.UIState['view.viewType'] === 'scatter')
    {
      // shortcut to the index of the visible dimension and the range object
      var x = this.visibleDimensions[0], y = this.visibleDimensions[1],
          z = this.visibleDimensions[2], range = this.decModels.dimensionRanges,
          is2D = (z === null || z === undefined);

      // Adds a padding to all dimensions such that samples don't overlap
      // with the axes lines. Determined based on the default sphere radius
      var axesPadding = 1.07;

      /*
       * We special case Z when it is a 2D plot, whenever that's the case we set
       * the range to be zero so no lines are shown on screen.
       */

      // this is the "origin" of our ordination
      var start = [range.min[x] * axesPadding,
                   range.min[y] * axesPadding,
                   is2D ? 0 : range.min[z] * axesPadding];

      var ends = [
        [range.max[x] * axesPadding,
         range.min[y] * axesPadding,
         is2D ? 0 : range.min[z] * axesPadding],
        [range.min[x] * axesPadding,
         range.max[y] * axesPadding,
         is2D ? 0 : range.min[z] * axesPadding],
        [range.min[x] * axesPadding,
         range.min[y] * axesPadding,
         is2D ? 0 : range.max[z] * axesPadding]
      ];

      action(start, ends[0], x);
      action(start, ends[1], y);

      // when transitioning to 2D disable rotation to avoid awkward angles
      if (is2D) {
        this.control.enableRotate = false;
      }
      else {
        action(start, ends[2], z);
        this.control.enableRotate = true;
      }
    }
    else {
      //Parallel Plots show all axes
      for (var i = 0; i < this.decViews['scatter'].decomp.dimensions; i++)
      {
        action([i, 0, 0], [i, 1, 0], i);
      }
    }
  };

  /**
   *
   * Draw the axes lines in the plot
   *
   * @param {String} color A CSS-compatible value that specifies the color
   * of each of the axes lines, the length of these lines is determined by the
   * global dimensionRanges property computed in decModels.
   * If the color value is null the lines will be removed.
   *
   */
  ScenePlotView3D.prototype.drawAxesWithColor = function(color) {
    var scope = this, axisLine;

    // axes lines are removed if the color is null
    this.removeAxes();
    if (color === null) {
      return;
    }

    this._dimensionsIterator(function(start, end, index) {
      axisLine = makeLine(start, end, color, 3, false);
      axisLine.name = scope._axisPrefix + index;

      scope.scene.add(axisLine);
    });
  };

  /**
   *
   * Draw the axes labels for each visible dimension.
   *
   * The text in the labels is determined using the percentage explained by
   * each dimension and the abbreviated name of a single decomposition object.
   * Note that we arbitrarily use the first one, as all decomposition objects
   * presented in the same scene should have the same percentages explained by
   * each axis.
   *
   * @param {String} color A CSS-compatible value that specifies the color
   * of the labels, these labels will be positioned at the end of the axes
   * line. If the color value is null the labels will be removed.
   *
   */
  ScenePlotView3D.prototype.drawAxesLabelsWithColor = function(color) {
    var scope = this, axisLabel, decomp, firstKey, text, scaling;
    scaling = this.getScalingConstant();

    // the labels are only removed if the color is null
    this.removeAxesLabels();
    if (color === null) {
      return;
    }

    // get the first decomposition object, it doesn't really matter which one
    // we look at though, as all of them should have the same percentage
    // explained on each axis
    firstKey = _.keys(this.decViews)[0];
    decomp = this.decViews[firstKey].decomp;

    this._dimensionsIterator(function(start, end, index) {
      text = decomp.axesLabels[index];
      axisLabel = makeLabel(end, text, color);

      if (scope.UIState['view.viewType'] === 'scatter') {
        //Scatter has a 1 to 1 aspect ratio and labels in world size
        axisLabel.scale.set(axisLabel.scale.x * scaling,
                            axisLabel.scale.y * scaling,
                            1);
      }
      else if (scope.UIState['view.viewType'] === 'parallel-plot') {
        //Parallel plot aspect ratio depends on number of dimensions
        //We have to correct label size to account for this.
        //But we also have to fix label width so that it fits between
        //axes, which are exactly 1 apart in world space
        var cam = scope.camera;
        var labelWPix = axisLabel.scale.x;
        var labelHPix = axisLabel.scale.y;
        var viewWPix = scope.width;
        var viewHPix = scope.height;

        //Assuming a camera zoom of 1:
        var viewWUnits = cam.right - cam.left;
        var viewHUnits = cam.top - cam.bottom;

        //These are world sizes of label for a camera zoom of 1
        var labelWUnits = labelWPix * viewWUnits / viewWPix;
        var labelHUnits = labelHPix * viewHUnits / viewHPix;

        //TODO FIXME HACK:  Note that our options here are to scale each
        //label to fit in its area, or to scale all labels by the same amount
        //We choose to scale all labels by the same amount based on an
        //empirical 'nice' label length of ~300
        //We could replace this with a max of all label widths, but must note
        //that label widths are always powers of 2 in the current version

        //Resize to fit labels of width 300 between axes
        var scalingFudge = 0.9 / (300 * viewWUnits / viewWPix);

        axisLabel.scale.set(labelWUnits * scalingFudge,
                            labelHUnits * scalingFudge,
                            1);
      }

      axisLabel.name = scope._axisLabelPrefix + index;
      scope.scene.add(axisLabel);
    });
  };

  /**
   *
   * Helper method to remove objects with some prefix from the view's scene
   *
   * @param {String} prefix The prefix of object names to remove
   *
   */
  ScenePlotView3D.prototype._removeObjectsWithPrefix = function(prefix) {
    var scope = this;
    var recursiveRemove = function(rootObj) {
      if (rootObj.name != null && rootObj.name.startsWith(prefix)) {
        scope.scene.remove(rootObj);
      }
      else {
        // We can't iterate the children array while removing from it,
        // So we make a shallow copy.
        var childCopy = Array.from(rootObj.children);
        for (var child in childCopy) {
          recursiveRemove(childCopy[child]);
        }
      }
    };
    recursiveRemove(this.scene);
  };

  /**
   *
   * Helper method to remove the axis lines from the scene
   *
   */
  ScenePlotView3D.prototype.removeAxes = function() {
    this._removeObjectsWithPrefix(this._axisPrefix);
  };

  /**
   *
   * Helper method to remove the axis labels from the scene
   *
   */
  ScenePlotView3D.prototype.removeAxesLabels = function() {
    this._removeObjectsWithPrefix(this._axisLabelPrefix);
  };

  /**
   *
   * Resizes and relocates the scene.
   *
   * @param {Float} xView New horizontal location.
   * @param {Float} yView New vertical location.
   * @param {Float} width New scene width.
   * @param {Float} height New scene height.
   *
   */
  ScenePlotView3D.prototype.resize = function(xView, yView, width, height) {
    this.xView = xView;
    this.yView = yView;
    this.width = width;
    this.height = height;

    this.updateCameraAspectRatio();
    this.control.update();

    //Since parallel plot labels have to correct for aspect ratio, we need
    //to redraw when width/height of view is modified.
    this.drawAxesLabelsWithColor(this.axesColor);

    this.needsUpdate = true;
  };

  /**
   *
   * Resets the aspect ratio of the camera according to the current size of the
   * plot space.
   *
   */
  ScenePlotView3D.prototype.updateCameraAspectRatio = function() {
    if (this.UIState['view.viewType'] === 'scatter')
    {
      var x = this.visibleDimensions[0], y = this.visibleDimensions[1];

      // orthographic cameras operate in space units not in pixel units i.e.
      // the width and height of the view is based on the objects not the window
      var owidth = this.decModels.dimensionRanges.max[x] -
                      this.decModels.dimensionRanges.min[x];
      var oheight = this.decModels.dimensionRanges.max[y] -
                      this.decModels.dimensionRanges.min[y];

      var aspect = this.width / this.height;

      // ensure that the camera's aspect ratio is equal to the window's
      owidth = oheight * aspect;

      this.camera.left = -owidth / 2;
      this.camera.right = owidth / 2;
      this.camera.top = oheight / 2;
      this.camera.bottom = -oheight / 2;

      this.camera.aspect = aspect;
      this.camera.updateProjectionMatrix();
    }
    else if (this.UIState['view.viewType'] === 'parallel-plot')
    {
      var w = this.decModels.dimensionRanges.max.length;
      this.camera.left = 0;
      this.camera.right = w;
      this.camera.top = 1;
      this.camera.bottom = 0;
      this.camera.updateProjectionMatrix();
    }
  };

  /**
   * Updates the target and dimensions of the camera and control
   *
   * The target of the scene depends on the coordinate space of the data, by
   * default it is set to zero, but we need to make sure that the target is
   * reasonable for the data.
   */
  ScenePlotView3D.prototype.updateCameraTarget = function() {
    if (this.UIState['view.viewType'] === 'scatter')
    {
      var x = this.visibleDimensions[0], y = this.visibleDimensions[1];

      var owidth = this.decModels.dimensionRanges.max[x] -
                      this.decModels.dimensionRanges.min[x];
      var oheight = this.decModels.dimensionRanges.max[y] -
                      this.decModels.dimensionRanges.min[y];
      var xcenter = this.decModels.dimensionRanges.max[x] - (owidth / 2);
      var ycenter = this.decModels.dimensionRanges.max[y] - (oheight / 2);

      var max = _.max(this.decViews.scatter.decomp.dimensionRanges.max);

      this.control.target.set(xcenter, ycenter, 0);
      this.camera.position.set(xcenter, ycenter, max * 5);
      this.camera.updateProjectionMatrix();

      this.light.position.set(xcenter, ycenter, max * 5);

      this.updateCameraAspectRatio();

      this.control.saveState();

      this.needsUpdate = true;
    }
    else if (this.UIState['view.viewType'] === 'parallel-plot') {
      this.control.target.set(0, 0, 1); //Must set positive Z because near > 0
      this.camera.position.set(0, 0, 1); //Must set positive Z because near > 0
      this.camera.updateProjectionMatrix();
      this.updateCameraAspectRatio();
      this.control.saveState();
      this.needsUpdate = true;
    }
  };

  ScenePlotView3D.prototype.NEEDS_RENDER = 1;
  ScenePlotView3D.prototype.NEEDS_CONTROLLER_REFRESH = 2;

  /**
   *
   * Convenience method to check if this or any of the decViews under this need
   * rendering
   *
   */
   ScenePlotView3D.prototype.checkUpdate = function() {
    var updateDimensions = false, updateColors = false,
        currentDimensions, backgroundColor, axesColor, scope = this;

    //Check if the view type changed and swap the markers in/out of the scene
    //tree.
    var anyMarkersSwapped = false, isArrowType;

    _.each(this.decViews, function(view) {
      if (view.needsSwapMarkers) {
        isArrowType = view.decomp.isArrowType();
        anyMarkersSwapped = true;

        // arrows are in the scene whereas points/markers are in a different
        // group used for brush selection
        var group = isArrowType ? scope.scene : scope._selectable;
        var oldMarkers = view.getAndClearOldMarkers(), marker;

        for (var i = 0; i < oldMarkers.length; i++) {
          marker = oldMarkers[i];

          group.remove(marker);

          if (isArrowType) {
            marker.dispose();
          }
          else {
            marker.material.dispose();
            marker.geometry.dispose();
          }
        }

        // do not show arrows in a parallel plot
        var newMarkers = view.markers;
        if (isArrowType && scope.UIState['view.viewType'] === 'scatter' ||
            view.decomp.isScatterType()) {
          var scaling = scope.getScalingConstant();

          for (i = 0; i < newMarkers.length; i++) {
            marker = newMarkers[i];

            // when we re-add arrows we need to re-scale the labels
            if (isArrowType) {
              marker.label.scale.set(marker.label.scale.x * scaling,
                                     marker.label.scale.y * scaling, 1);
            }
            group.add(marker);
          }
        }

        var lines = view.lines;
        var ellipsoids = view.ellipsoids;

        if (scope.UIState['view.viewType'] == 'parallel-plot') {
          for (i = 0; i < lines.length; i++)
            scope.scene.remove(lines[i]);
          for (i = 0; i < ellipsoids.length; i++)
            scope.scene.remove(ellipsoids[i]);
        }
        if (scope.UIState['view.viewType'] == 'scatter') {
          for (i = 0; i < lines.length; i++)
            scope.scene.add(lines[i]);
          for (i = 0; i < ellipsoids.length; i++)
            scope.scene.add(ellipsoids[i]);
        }
    }});

    if (anyMarkersSwapped) {
      this.updateCameraTarget();
      this.control.update();
    }


    // check if any of the decomposition views have changed
    var updateData = _.any(this.decViews, function(dv) {
      // note that we may be overwriting these variables, but we have a
      // guarantee that if one of them changes for one of decomposition views,
      // all of them will have changed, so grabbing one should be sufficient to
      // perform the comparisons below
      currentDimensions = dv.visibleDimensions;
      backgroundColor = dv.backgroundColor;
      axesColor = dv.axesColor;

      return dv.needsUpdate;
    });

    _.each(this.decViews, function(view) {
      view.getTubes().forEach(function(tube) {
        if (tube !== null)
          scope.scene.add(tube);
      });
    });

    // check if the visible dimensions have changed
    if (!_.isEqual(currentDimensions, this.visibleDimensions)) {
      // remove the current axes
      this.removeAxes();
      this.removeAxesLabels();

      // get the new dimensions and re-display the data
      this.visibleDimensions = _.clone(currentDimensions);
      this.drawAxesWithColor(this.axesColor);
      this.drawAxesLabelsWithColor(this.axesColor);

      this.updateCameraTarget();
      this.control.update();

      updateDimensions = true;
    }

    // check if we should change the axes color
    if (axesColor !== this.axesColor) {
      this.drawAxesWithColor(axesColor);
      this.drawAxesLabelsWithColor(axesColor);

      this.axesColor = _.clone(axesColor);

      updateColors = true;
    }

    // check if we should change the background color
    if (backgroundColor !== this.backgroundColor) {
      this.backgroundColor = _.clone(backgroundColor);
      this.scene.background = new THREE.Color(this.backgroundColor);

      updateColors = true;
    }

    if (updateData) {
      this.drawAxesWithColor(this.axesColor);
      this.drawAxesLabelsWithColor(this.axesColor);
    }

    var retVal = 0;
    if (anyMarkersSwapped)
      retVal |= ScenePlotView3D.prototype.NEEDS_CONTROLLER_REFRESH;
    if (anyMarkersSwapped || this.needsUpdate || updateData ||
        updateDimensions || updateColors || this.control.autoRotate)
      retVal |= ScenePlotView3D.prototype.NEEDS_RENDER;

    // if anything has changed, then trigger an update
    return retVal;
   };

  /**
   *
   * Convenience method to re-render the contents of the scene.
   *
   */
  ScenePlotView3D.prototype.render = function() {
    this.renderer.setViewport(this.xView, this.yView, this.width, this.height);
    this.renderer.render(this.scene, this.camera);
    var camera = this.camera;

    // if autorotation is enabled, then update the controls
    if (this.control.autoRotate) {
      this.control.update();
    }

    // Only scatter plots that are not using a point cloud should be pointed
    // towards the camera. For arrow types and point clouds doing this will
    // results in odd visual effects
    if (!this.UIState.getProperty('view.usesPointCloud') &&
        this.decViews.scatter.decomp.isScatterType()) {
      _.each(this.decViews.scatter.markers, function(element) {
        element.quaternion.copy(camera.quaternion);
      });
    }

    this.needsUpdate = false;
    $.each(this.decViews, function(key, val) {
      val.needsUpdate = false;
    });
  };

  /**
   * Helper method to highlight and return selected objects.
   *
   * This is mostly necessary because depending on the rendering type we will
   * have a slightly different way to set and return the highlighting
   * attributes. For large plots we return the points geometry together with
   * a userData.selected attribute with the selected indices.
   *
   * Note that we created a group of selectable objects in the constructor so
   * we don't have to check for geometry types, etc.
   *
   * @param {Array} collection An array of objects to highlight
   * @param {Integer} color A hexadecimal-encoded color. For shaders we only
   * use the first bit to decide if the marker is rendered in white or rendered
   * with the original color.
   *
   * @return {Array} selected objects (after checking for visibility and
   * opacity).
   *
   * @private
   */
  ScenePlotView3D.prototype._highlightSelected = function(collection, color) {
    var i = 0, j = 0, selected = [];

    if (this.UIState.getProperty('view.usesPointCloud') ||
        this.UIState.getProperty('view.viewType') === 'parallel-plot') {
      for (i = 0; i < collection.length; i++) {
        // for shaders the emissive attribute is an int
        var indices, emissiveColor = (color > 0) * 1;

        // if there's no selection then update all the points
        if (collection[i].userData.selected === undefined) {
          indices = _.range(collection[i].geometry.attributes.emissive.count);
        }
        else {
          indices = collection[i].userData.selected;
        }

        for (j = 0; j < indices.length; j++) {
          if (collection[i].geometry.attributes.visible.getX(indices[j]) &&
              collection[i].geometry.attributes.opacity.getX(indices[j])) {
            collection[i].geometry.attributes.emissive.setX(indices[j],
                                                            emissiveColor);
          }
        }

        collection[i].geometry.attributes.emissive.needsUpdate = true;
        selected.push(collection[i]);
      }
    }
    else {
      for (i = 0; i < collection.length; i++) {
        var material = collection[i].material;

        if (material.visible && material.opacity && material.emissive) {
          collection[i].material.emissive.set(color);
          selected.push(collection[i]);
        }
      }
    }

    return selected;
  };

  /**
   *
   * Adds the mouse selection events to the current view
   *
   * @param {node} $container The container to add the events to.
   * @private
   */
  ScenePlotView3D.prototype._addSelectionEvents = function($container) {
    var scope = this;

    // There're three stages to the mouse selection:
    //  mousedown -> mousemove -> mouseup
    //
    // The mousdown event is ignored unless the user is holding Shift. Once
    // selection has started the rotation controls are disabled. The mousemove
    // event continues until the user releases the mouse. Once this happens
    // rotation is re-enabled and the selection box disappears. Selected
    // markers are highlighted by changing the light they emit.
    //
    $container.on('mousedown', function(event) {
      // ignore the selection event if shift is not being held or if parallel
      // plots are being visualized at the moment
      if (!event.shiftKey) {
        return;
      }

      scope.control.enabled = false;
      scope.scatterController.enabled = false;
      scope.parallelController.enabled = false;
      scope._selectionHelper.enabled = true;
      scope._selectionHelper.onSelectStart(event);

      // clear up any color setting
      scope._highlightSelected(scope._selectionBox.collection, 0x000000);

      var element = scope.renderer.domElement;
      var offset = $(element).offset(), i = 0;

      scope._selectionBox.startPoint.set(
        ((event.clientX - offset.left) / element.width) * 2 - 1,
        -((event.clientY - offset.top) / element.height) * 2 + 1,
        0.5);
    })
    .on('mousemove', function(event) {
      // ignore if the user is not holding the shift key or the orbit control
      // is enabled and he selection disabled
      if (!event.shiftKey ||
          (scope.control.enabled && !scope._selectionHelper.enabled)) {
        return;
      }

      var element = scope.renderer.domElement, selected;
      var offset = $(element).offset(), i = 0;

      scope._selectionBox.endPoint.set(
        ((event.clientX - offset.left) / element.width) * 2 - 1,
        - ((event.clientY - offset.top) / element.height) * 2 + 1,
        0.5);

      // reset everything before updating the selected color
      scope._highlightSelected(scope._selectionBox.collection, 0x000000);
      scope._highlightSelected(scope._selectionBox.select(), 0x8c8c8f);

      scope.needsUpdate = true;
    })
    .on('mouseup', function(event) {
      // if the user is not already selecting data then ignore
      if (!scope._selectionHelper.enabled || scope.control.enabled) {
        return;
      }

      // otherwise if shift is being held then keep selecting, otherwise ignore
      if (event.shiftKey) {
        var element = scope.renderer.domElement;
        var offset = $(element).offset(), indices = [], names = [];
        scope._selectionBox.endPoint.set(
          ((event.clientX - offset.left) / element.width) * 2 - 1,
          - ((event.clientY - offset.top) / element.height) * 2 + 1,
          0.5);

        selected = scope._highlightSelected(scope._selectionBox.select(),
                                            0x8c8c8f);

        // get the list of sample names from the views
        for (var i = 0; i < selected.length; i++) {
          if (selected[i].isPoints) {
            // this is a list of indices of the selected samples
            indices = selected[i].userData.selected;

            for (var j = 0; j < indices.length; j++) {
              names.push(scope.decViews.scatter.decomp.ids[indices[j]]);
            }
          }
          else if (selected[i].isLineSegments) {
            var index, viewType, view;

            view = scope.decViews.scatter;
            viewType = scope.UIState['view.viewType'];

            // this is a list of indices of the selected samples
            indices = selected[i].userData.selected;

            for (var k = 0; k < indices.length; k++) {
              index = view.getModelPointIndex(indices[k], viewType);
              names.push(view.decomp.ids[index]);
            }

            // every segment is labeled the same for each sample
            names = _.unique(names);
          }
          else {
            names.push(selected[i].name);
          }
        }

        scope._selectCallback(names, scope.decViews.scatter);
      }

      scope.control.enabled = true;
      scope.scatterController.enabled = true;
      scope.parallelController.enabled = true;
      scope._selectionHelper.enabled = false;
      scope.needsUpdate = true;
    });
  };


  /**
   * Handle selection events.
   * @private
   */
  ScenePlotView3D.prototype._selectCallback = function(names, view) {
    var eventType = 'select';

    for (var i = 0; i < this._subscribers[eventType].length; i++) {
      // keep going if one of the callbacks fails
      try {
        this._subscribers[eventType][i](names, view);
      } catch (e) {
        console.error(e);
      }
      this.needsUpdate = true;
    }
  };

  /**
   *
   * Helper method that runs functions subscribed to the container's callbacks.
   * @param {String} eventType Event type being called
   * @param {event} event The event from jQuery, with x and y click coords
   * @private
   *
   */
  ScenePlotView3D.prototype._eventCallback = function(eventType, event) {
    event.preventDefault();
    // don't do anything if no subscribers
    if (this._subscribers[eventType].length === 0) {
      return;
    }

    var element = this.renderer.domElement, scope = this;
    var offset = $(element).offset();
    this._mouse.x = ((event.clientX - offset.left) / element.width) * 2 - 1;
    this._mouse.y = -((event.clientY - offset.top) / element.height) * 2 + 1;

    this._raycaster.setFromCamera(this._mouse, this.camera);

    // get a flattened array of markers
    var objects = _.map(this.decViews, function(decomp) {
      return decomp.markers;
    });
    objects = _.reduce(objects, function(memo, value) {
      return memo.concat(value);
    }, []);
    var intersects = this._raycaster.intersectObjects(objects);

    // Get first intersected item and call callback with it.
    if (intersects && intersects.length > 0) {
      var firstObj = intersects[0].object, intersect;
      /*
       * When the intersect object is a Points object, the raycasting method
       * won't intersect individual mesh objects. Instead it intersects a point
       * and we get the index of the point. This index can then be used to
       * trace the original Plottable object.
       */
      if (firstObj.isPoints || firstObj.isLineSegments) {
        // don't search over invisible things
        intersects = _.filter(intersects, function(marker) {
           return firstObj.geometry.attributes.visible.getX(marker.index) &&
                  firstObj.geometry.attributes.opacity.getX(marker.index);
        });

        // if there's no hits then finish the execution
        if (intersects.length === 0) {
          return;
        }

        var meshIndex = intersects[0].index;
        var modelIndex = this.decViews.scatter.getModelPointIndex(meshIndex,
                                                this.UIState['view.viewType']);
        intersect = this.decViews.scatter.decomp.plottable[modelIndex];
      }
      else {
        intersects = _.filter(intersects, function(marker) {
          return marker.object.visible && marker.object.material.opacity;
        });

        // if there's no hits then finish the execution
        if (intersects.length === 0) {
          return;
        }

        intersect = intersects[0].object;
      }

      for (var i = 0; i < this._subscribers[eventType].length; i++) {
        // keep going if one of the callbacks fails
        try {
          this._subscribers[eventType][i](intersect.name, intersect);
        } catch (e) {
          console.error(e);
        }
        this.needsUpdate = true;
      }
    }
  };

  /**
   *
   * Interface to subscribe to event types in the canvas, see the EVENTS
   * property.
   *
   * @param {String} eventType The type of event to subscribe to.
   * @param {Function} handler Function to call when `eventType` is triggered,
   * receives two parameters, a string with the name of the object, and the
   * object itself i.e. f(objectName, object).
   *
   * @throws {Error} If the given eventType is unknown.
   *
   */
  ScenePlotView3D.prototype.on = function(eventType, handler) {
    if (this.EVENTS.indexOf(eventType) === -1) {
      throw new Error('Unknown event ' + eventType + '. Known events are: ' +
                      this.EVENTS.join(', '));
    }

    this._subscribers[eventType].push(handler);
  };

  /**
   *
   * Interface to unsubscribe a function from an event type, see the EVENTS
   * property.
   *
   * @param {String} eventType The type of event to unsubscribe from.
   * @param {Function} handler Function to remove from the subscribers list.
   *
   * @throws {Error} If the given eventType is unknown.
   *
   */
  ScenePlotView3D.prototype.off = function(eventType, handler) {
    if (this.EVENTS.indexOf(eventType) === -1) {
      throw new Error('Unknown event ' + eventType + '. Known events are ' +
                      this.EVENTS.join(', '));
    }

    var pos = this._subscribers[eventType].indexOf(handler);
    if (pos !== -1) {
      this._subscribers[eventType].splice(pos, 1);
    }
  };

  /**
   *
   * Recenter the position of the camera to the initial default.
   *
   */
  ScenePlotView3D.prototype.recenterCamera = function() {
    this.control.reset();
    this.control.update();

    this.needsUpdate = true;
  };

  return ScenePlotView3D;
});
