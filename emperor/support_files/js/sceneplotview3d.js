define([
    "three",
    "orbitcontrols",
    "draw"
], function (THREE, OrbitControls, draw) {
  var makeLine = draw.makeLine;
  var makeLabel = draw.makeLabel;
  /**
   *
   * @name ScenePlotView3D
   *
   * @class Represents a three dimensional scene in THREE.js, this is a helper
   * class that wraps around the functionality provided to display objects on
   * screen.
   *
   * @property {Float} [xView] horizontal position of the scene.
   * @property {Float} [yView] vertical position of the scene.
   * @property {Float} [width] width of the scene.
   * @property {Float} [height] height of the scene.
   * @property {Array} [visibleDimensions] array of integers indicating the index
   * of the visible dimension at each axis ([x, y, z]).
   * @property {Object} [dimensionRanges] object with a "min" and "max"
   * attributes each of which is an array with the ranges that covers all of
   * the decomposition views.
   *
   * @property {THREE.PerspectiveCamera} [camera] camera used to display the
   * scene.
   * @property {THREE.DirectionalLight} [light] object used to light the scene,
   * by default is set to a light and transparent color (0x99999999).
   * @property {THREE.OrbitControls} [control] object used to interact with the
   * scene. By default it uses the mouse.
   *
   */

  /**
   *
   * @name ScenePlotView3D
   *
   * @class Represents a three dimensional scene in THREE.js.
   *
   * @param {renderer} THREE renderer object.
   * @param {decViews} dictionary of DecompositionViews shown in this scene
   * @param {container} Node where the scene will be rendered.
   * @param {xView} Horizontal position of the rendered scene in the container
   * element.
   * @param {yView} Vertical position of the rendered sciene in the container
   * element.
   * @param {width} a float with the width of the renderer
   * @param {height} a float with the height of the renderer
   * @param {EVENTS} array of events allowed for on addition. DO NOT EDIT.
   *
   **/
  ScenePlotView3D = function(renderer, decViews, container, xView, yView,
                             width, height){
    var scope = this;

    // convert to jquery object for consistency with the rest of the objects
    var $container = $(container);
    this.decViews = decViews;
    this.renderer = renderer;
    this.xView = xView;
    this.yView = yView;
    this.width = width;
    this.height = height;

    // used to name the axis lines/labels in the scene
    this._axisPrefix = 'emperor-axis-line-';
    this._axisLabelPrefix = 'emperor-axis-label-';

    // Set up the camera
    // Note: if we change the near parameter to something smaller than this
    // the raytracing will not work as expected.
    this.camera = new THREE.PerspectiveCamera(35, width/height,
                                              0.0001, 10000);
    this.camera.position.set(0, 0, 6);

    //need to initialize the scene
    this.scene = new THREE.Scene();
    this.scene.add(this.camera);
    this.light = new THREE.DirectionalLight(0x999999, 2);
    this.light.position.set(1,1,1).normalize();
    this.camera.add(this.light);

    // Add all the meshes to the scene, iterate through all keys in
    // decomposition view dictionary
    for(var decViewName in this.decViews){
      for (var j = 0; j < this.decViews[decViewName].markers.length; j++) {
        this.scene.add(this.decViews[decViewName].markers[j]);
      }
    }

    // use get(0) to retrieve the native DOM object
    this.control = new THREE.OrbitControls(this.camera,
                                           $container.get(0));
    this.control.addEventListener('change', function() {
      scope.needsUpdate = true;
    });
    this.control.rotateSpeed = 1.0;
    this.control.zoomSpeed = 1.2;
    this.control.panSpeed = 0.8;
    this.control.enableZoom = true;
    this.control.enablePan = true;
    this.control.enableDamping = true;
    this.control.dampingFactor = 0.3;
    this.needsUpdate = true;

    this.visibleDimensions = [0, 1, 2];
    this.dimensionRanges = {'max': [], 'min': []};
    this.drawAxesWithColor(0xFFFFFF);
    this.drawAxesLabelsWithColor(0xFFFFFF);

    this._raycaster = new THREE.Raycaster();
    this._mouse = new THREE.Vector2();

    // initialize subscribers for event callbacks
    this.EVENTS = ['click', 'dblclick'];
    this._subscribers = {};

    for (var i = 0; i < this.EVENTS.length; i++) {
      this._subscribers[this.EVENTS[i]] = [];
    }

    // Add callback call when sample is clicked double and single click
    // together from: http://stackoverflow.com/a/7845282
    var DELAY = 200, clicks = 0, timer = null;
    $container.on("click", function(event) {
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
    .on("dblclick", function(event) {
        event.preventDefault();  //cancel system double-click event
    });

  };

  /**
   *
   * Utility method to find the union of the ranges in the decomposition views
   * this method will populate the dimensionRanges attributes.
   *
   **/
  ScenePlotView3D.prototype._unionRanges = function(){
    var scope = this;

    // means we already have the data, so let's say goodbye
    if (this.dimensionRanges.max.length !== 0){
      return;
    }

    _.each(this.decViews, function(decView, name){
      // get each decomposition object
      var decomp = decView.decomp;

      if ( scope.dimensionRanges.max.length === 0 ){
        scope.dimensionRanges.max = decomp.dimensionRanges.max.slice();
        scope.dimensionRanges.min = decomp.dimensionRanges.min.slice();
      }
      else {
        // when we have more than one decomposition view we need to figure out
        // the absolute largest range that views span over
        _.each(decomp.dimensionRanges.max, function(value, index){
          var vMax = decomp.dimensionRanges.max[index],
              vMin = decomp.dimensionRanges.min[index];

          if (vMax > scope.dimensionRanges.max[index]){
            scope.dimensionRanges.max[index] = vMax;
          }
          if (vMin < scope.dimensionRanges.min[index]){
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
   * @param {action} a function that can take up to three arguments "start",
   * "end" and "index".  And for each visible dimension the function will get
   * the "start" and "end" of the range, and the current "index" of the visible
   * dimension.
   *
   **/
  ScenePlotView3D.prototype._dimensionsIterator = function(action){
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

    action(start, ends[0], 0);
    action(start, ends[1], 1);
    action(start, ends[2], 2);
  };

  /**
   *
   * Draw the axes lines in the plot
   *
   * @parameter {color} an integer in hexadecimal that specifies the color of
   * each of the axes lines, the length of these lines is determined by the
   * dimensionRanges property.
   *
   **/
  ScenePlotView3D.prototype.drawAxesWithColor = function(color){
    var scope = this, axisLine;

    this.removeAxes();

    this._dimensionsIterator(function(start, end, index){
      axisLine = makeLine(start, end, color, 3, false);
      axisLine.name = scope._axisPrefix + index;

      scope.scene.add(axisLine);
    });
  };

  /**
   *
   * Draw the axes labels for each visible dimension.
   *
   * @parameter {color} an integer in hexadecimal that specifies the color of
   * the labels, these labels will be positioned at the end of the axes line.
   * The text in the labels is determined using the percentage explained by
   * each dimension and the abbreviated name of a single decomposition object.
   * Note that we arbitrarily use the first one, as all decomposition objects
   * presented in the same scene should have the same percentages explained by
   * each axis.
   *
   **/
  ScenePlotView3D.prototype.drawAxesLabelsWithColor = function(color){
    var scope = this, axisLabel, decomp, firstKey, text;

    this.removeAxesLabels();

    // get the first decomposition object, it doesn't really mater which one
    // we look at though, as all of them should have the same percentage
    // explained on each axis
    firstKey = _.keys(this.decViews)[0];
    decomp = this.decViews[firstKey].decomp;

    this._dimensionsIterator(function(start, end, index){

      // construct a label of the format: AbbNam (xx.xx %)
      text = decomp.abbreviatedName + ' (' +
             decomp.percExpl[index].toPrecision(4) + ' %)';

      axisLabel = makeLabel(end, text, color);
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
   * @param {prefix} a string indicating the label that will prepended to the
   * iterating index.
   * @param {num} an integer specifying the number of iterations to perform.
   *
   **/
  ScenePlotView3D.prototype._removeObjectsWithPrefix = function(prefix, num){
    for (var i = 0; i < num; i++){
      var axisLine = this.scene.getObjectByName(prefix + i);
      this.scene.remove(axisLine);
    }
  };

  /**
   *
   * Remove the axis lines from the scene
   *
   **/
  ScenePlotView3D.prototype.removeAxes = function(){
    this._removeObjectsWithPrefix(this._axisPrefix, 3);
  };

  /**
   *
   * Remove the axis labels from the scene
   *
   **/
  ScenePlotView3D.prototype.removeAxesLabels = function(){
    this._removeObjectsWithPrefix(this._axisLabelPrefix, 3);
  };

  /**
   *
   * Sets the aspect ratio of the camera according to the current size of the
   * scene.
   *
   * @param {winAspect} ratio of width to height of the scene.
   *
   **/
  ScenePlotView3D.prototype.setCameraAspectRatio = function(winAspect){
    this.camera.aspect = winAspect;
    this.camera.updateProjectionMatrix();
  };

  /**
   *
   * Resizes and relocates the scene.
   *
   * @param {xView} New horizontal location.
   * @param {yView} New vertical location.
   * @param {width} New scene width.
   * @param {height} New scene height.
   *
   **/
  ScenePlotView3D.prototype.resize = function(xView, yView, width, height){
    this.xView = xView;
    this.yView = yView;
    this.width = width;
    this.height = height;
    this.setCameraAspectRatio(width/height);
  };

  /**
   *
   * Convenience method to re-render the contents of the scene.
   *
   **/
  ScenePlotView3D.prototype.render = function(){
    console.log('SPV3D');
    this.renderer.setViewport(this.xView, this.yView, this.width, this.height);
    this.renderer.render(this.scene, this.camera);
    var camera = this.camera;
    //point all samples towards the camera
    _.each(this.decViews.scatter.markers, function(element) {
      element.quaternion.copy(camera.quaternion);
    });
  };

  /**
   *
   * Helper method thats subscribed to the container's callbacks, see init.
   *
   **/
  ScenePlotView3D.prototype._eventCallback = function(eventType, event) {
    event.preventDefault();

    // don't do anything if no subscribers
    if (this._subscribers[eventType].length === 0) {
      return;
    }

    var element = this.renderer.domElement;
    this._mouse.x = ((event.clientX - element.offsetLeft) / element.width) * 2 - 1;
    this._mouse.y = -((event.clientY - element.offsetTop) / element.height) * 2 + 1;

    this._raycaster.setFromCamera(this._mouse, this.camera);

    var intersects = this._raycaster.intersectObjects(this.decViews.scatter.markers);

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
      }
    }
  };

  /*
   *
   * Interface to subscribe to event types in the canvas, see the EVENTS
   * property.
   *
   * @param {eventType} String indicating the type of event to subscribe to.
   * @param {handler} Function to call when `eventType` is triggered, receives
   * two parameters, a string with the name of the object, and the object
   * itself i.e. f(objectName, object).
   *
   * If the event is unknown an Error will be thrown.
   *
   **/
  ScenePlotView3D.prototype.on = function(eventType, handler) {
    if (this.EVENTS.indexOf(eventType) === -1) {
      throw new Error('Unknown event ' + eventType + '. Known events are: ' +
                      this.EVENTS.join(', '));
    }

    this._subscribers[eventType].push(handler);
  };

  /*
   *
   * Interface to unsubscribe a function from an event type, see the EVENTS
   * property.
   *
   * @param {eventType} String with the type of event to unsubscribe from.
   * @param {handler} Function to remove from the subscribers list.
   *
   * If the event is unknown an Error will be thrown.
   *
   **/
  ScenePlotView3D.prototype.off = function(eventType, handler) {
    if (this.EVENTS.indexOf(eventType) === -1) {
      throw new Error('Unknown event ' + eventType + '. Known events are ' +
                      this.EVENTS.join(', '));
    }

    var pos = this._subscribers[eventType].find(handler);
    if (pos !== -1) {
      this._subscribers[eventType].splice(pos, 1);
    }
  };

  return ScenePlotView3D;
});
