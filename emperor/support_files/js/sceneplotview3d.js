define([
    'three',
    'orbitcontrols',
    'draw'
], function(THREE, OrbitControls, draw) {
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
   * @param {THREE.renderer} renderer THREE renderer object.
   * @param {Object} decViews dictionary of DecompositionViews shown in this
   * scene
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
   function ScenePlotView3D(renderer, decViews, container, xView, yView,
                            width, height) {
    var scope = this;

    // convert to jquery object for consistency with the rest of the objects
    var $container = $(container);
    this.decViews = decViews;
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
     * @type {integer}
     * @default 0xFFFFFF (white)
     */
    this.axesColor = 0xFFFFFF;
    /**
     * Background color.
     * @type {integer}
     * @default 0x000000 (black)
     */
    this.backgroundColor = 0x000000;

    // used to name the axis lines/labels in the scene
    this._axisPrefix = 'emperor-axis-line-';
    this._axisLabelPrefix = 'emperor-axis-label-';

    // Set up the camera
    var max = _.max(decViews.scatter.decomp.dimensionRanges.max);
    var frontFrust = _.min([max * 0.001, 1]);
    var backFrust = _.max([max * 100, 100]);
    /**
     * Camera used to display the scene.
     * @type {THREE.PerspectiveCamera}
     */
    this.camera = new THREE.PerspectiveCamera(35, width / height,
                                              frontFrust, backFrust);
    this.camera.position.set(0, 0, max * 5);

    //need to initialize the scene
    this.scene = new THREE.Scene();
    this.scene.add(this.camera);
    /**
     * Object used to light the scene, by default is set to a light and
     * transparent color (0x99999999).
     * @type {THREE.DirectionalLight}
     */
    this.light = new THREE.DirectionalLight(0x999999, 2);
    this.light.position.set(1, 1, 1).normalize();
    this.camera.add(this.light);

    // Add all the meshes to the scene, iterate through all keys in
    // decomposition view dictionary
    for (var decViewName in this.decViews) {
      for (var j = 0; j < this.decViews[decViewName].markers.length; j++) {
        this.scene.add(this.decViews[decViewName].markers[j]);
      }
    }

    // use get(0) to retrieve the native DOM object
    /**
     * Object used to interact with the scene. By default it uses the mouse.
     * @type {THREE.OrbitControls}
     */
    this.control = new THREE.OrbitControls(this.camera,
                                           $container.get(0));
    this.control.enableKeys = false;
    this.control.rotateSpeed = 1.0;
    this.control.zoomSpeed = 1.2;
    this.control.panSpeed = 0.8;
    this.control.enableZoom = true;
    this.control.enablePan = true;
    this.control.enableDamping = true;
    this.control.dampingFactor = 0.3;
    this.control.addEventListener('change', function() {
      scope.needsUpdate = true;
    });
    this.control.update();
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
    this.visibleDimensions = [0, 1, 2];
    /**
     * Object with "min" and "max" attributes each of which is an array with
     * the ranges that covers all of the decomposition views.
     * @type {Object}
     */
    this.dimensionRanges = {'max': [], 'min': []};
    this.drawAxesWithColor(0xFFFFFF);
    this.drawAxesLabelsWithColor(0xFFFFFF);

    this._raycaster = new THREE.Raycaster();
    this._mouse = new THREE.Vector2();

    // initialize subscribers for event callbacks
    /**
     * Events allowed for callbacks. DO NOT EDIT.
     * @type {String[]}
     */
    this.EVENTS = ['click', 'dblclick'];
    /** @private */
    this._subscribers = {};

    for (var i = 0; i < this.EVENTS.length; i++) {
      this._subscribers[this.EVENTS[i]] = [];
    }

    // Add callback call when sample is clicked
    // Double and single click together from: http://stackoverflow.com/a/7845282
    var DELAY = 200, clicks = 0, timer = null;
    $container.on('click', function(event) {
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

    //Add info div as bottom of canvas
    this.$info = $('<div>');
    this.$info.css('position', 'absolute')
      .css('bottom', 0)
      .css('height', 16)
      .css('width', '50%')
      .css('padding-left', 10)
      .css('padding-right', 10)
      .css('font-size', 12)
      .css('z-index', 10000)
      .css('background-color', 'rgb(238, 238, 238)')
      .css('border', '1px solid black')
      .css('font-family', 'Verdana,Arial,sans-serif')
      .hide();
    $(this.renderer.domElement).parent().append(this.$info);

    // register callback for populating info with clicked sample name
    // set the timeout for fading out the info div
    var infoDuration = 2500;
    var infoTimeout = setTimeout(function() {
        scope.$info.fadeOut();
      }, infoDuration);

    this.on('click', function(n, i) {
      clearTimeout(infoTimeout);
      scope.$info.text(n);
      scope.$info.show();

      // reset the timeout for fading out the info div
      infoTimeout = setTimeout(function() {
        scope.$info.fadeOut();
        scope.$info.text('');
      }, infoDuration);
    });
  };

  /**
   *
   * Utility method to find the union of the ranges in the decomposition views
   * this method will populate the dimensionRanges attributes.
   * @private
   *
   */
  ScenePlotView3D.prototype._unionRanges = function() {
    var scope = this;

    // means we already have the data, so let's say goodbye
    if (this.dimensionRanges.max.length !== 0) {
      return;
    }

    _.each(this.decViews, function(decView, name) {
      // get each decomposition object
      var decomp = decView.decomp;

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
    this._unionRanges();

    // shortcut to the index of the visible dimension and the range object
    var x = this.visibleDimensions[0], y = this.visibleDimensions[1],
        z = this.visibleDimensions[2], range = this.dimensionRanges;

    // this is the "origin" of our ordination
    var start = [range.min[x], range.min[y], range.min[z]];

    var ends = [
      [range.max[x], range.min[y], range.min[z]],
      [range.min[x], range.max[y], range.min[z]],
      [range.min[x], range.min[y], range.max[z]]
    ];

    action(start, ends[0], x);
    action(start, ends[1], y);
    action(start, ends[2], z);
  };

  /**
   *
   * Draw the axes lines in the plot
   *
   * @param {Integer} color An integer in hexadecimal that specifies the color
   * of each of the axes lines, the length of these lines is determined by the
   * dimensionRanges property.
   *
   */
  ScenePlotView3D.prototype.drawAxesWithColor = function(color) {
    var scope = this, axisLine;

    this.removeAxes();

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
   * @param {Integer} color An integer in hexadecimal that specifies the color
   * of the labels, these labels will be positioned at the end of the axes line.
   *
   */
  ScenePlotView3D.prototype.drawAxesLabelsWithColor = function(color) {
    var scope = this, axisLabel, decomp, firstKey, text, factor;

    factor = (this.dimensionRanges.max[0] - this.dimensionRanges.min[0]) * 0.9;

    this.removeAxesLabels();

    // get the first decomposition object, it doesn't really mater which one
    // we look at though, as all of them should have the same percentage
    // explained on each axis
    firstKey = _.keys(this.decViews)[0];
    decomp = this.decViews[firstKey].decomp;

    this._dimensionsIterator(function(start, end, index) {

      // construct a label of the format: AbbNam (xx.xx %)
      if (decomp.abbreviatedName !== '') {
        text = decomp.abbreviatedName;
      }
      else {
        // when the labels get too long, it's a bit hard to look at
        if (decomp.axesNames[index].length > 25) {
          text = decomp.axesNames[index].slice(0, 20) + '...';
        }
        else {
          text = decomp.axesNames[index];
        }
      }
      text += ' (' + decomp.percExpl[index].toPrecision(4) + ' %)';

      axisLabel = makeLabel(end, text, color, factor);
      axisLabel.name = scope._axisLabelPrefix + index;

      scope.scene.add(axisLabel);
    });
  };

  /**
   *
   * Helper method to remove objects that match a prefix from the view's scene
   * this method is used by removeAxes and removeAxesLabels. This function
   * iterates "num" times, and for each iteration it finds and removes objects
   * with the name of the form "prefix" + "iteration".
   *
   * @param {String} prefix The label that will prepended to the iterating
   * index.
   *
   */
  ScenePlotView3D.prototype._removeObjectsWithPrefix = function(prefix) {
    var scope = this;
    _.each(this.visibleDimensions, function(i) {
      var axisLine = scope.scene.getObjectByName(prefix + i);
      scope.scene.remove(axisLine);
    });
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
   * Sets the aspect ratio of the camera according to the current size of the
   * scene.
   *
   * @param {Float} winAspect ratio of width to height of the scene.
   *
   */
  ScenePlotView3D.prototype.setCameraAspectRatio = function(winAspect) {
    this.camera.aspect = winAspect;
    this.camera.updateProjectionMatrix();
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
    this.setCameraAspectRatio(width / height);
    this.needsUpdate = true;
  };

  /**
   *
   * Convenience method to check if this or any of the decViews under this need
   * rendering
   *
   */
   ScenePlotView3D.prototype.checkUpdate = function() {
    var updateDimensions = false, updateColors = false,
        currentDimensions, backgroundColor, axesColor;

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

    // check if the visible dimensions have changed
    if (!_.isEqual(currentDimensions, this.visibleDimensions)) {
      // remove the current axes
      this.removeAxes();
      this.removeAxesLabels();

      // get the new dimensions and re-display the data
      this.visibleDimensions = _.clone(currentDimensions);
      this.drawAxesWithColor(this.axesColor);
      this.drawAxesLabelsWithColor(this.axesColor);

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
      this.renderer.setClearColor(new THREE.Color(backgroundColor));
      this.backgroundColor = _.clone(backgroundColor);

      updateColors = true;
    }

    // if anything has changed, then trigger an update
    return this.needsUpdate || updateData || updateDimensions || updateColors;
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
    //point all samples towards the camera
    _.each(this.decViews.scatter.markers, function(element) {
      element.quaternion.copy(camera.quaternion);
    });
    this.needsUpdate = false;
    $.each(this.decViews, function(key, val) {
      val.needsUpdate = false;
    });
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

    var element = this.renderer.domElement;
    var offset = $(element).offset();
    this._mouse.x = ((event.clientX - offset.left) / element.width) * 2 - 1;
    this._mouse.y = -((event.clientY - offset.top) / element.height) * 2 + 1;

    this._raycaster.setFromCamera(this._mouse, this.camera);

    var intersects = this._raycaster.intersectObjects(
      this.decViews.scatter.markers);

    // Get first intersected item and call callback with it.
    if (intersects.length > 0) {
      var intersect = intersects[0].object;

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

  return ScenePlotView3D;
});
