define([
    "three",
    "orbitcontrols"
], function (THREE, OrbitControls) {
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
   * @param {div_id} Unique identifier for an element in the DOM.
   * @param {xView} Horizontal position of the rendered scene in the div_id
   * container.
   * @param {yView} Vertical position of the rendered sciene in the div_id
   * container.
   * @param {width} a float with the width of the renderer
   * @param {height} a float with the height of the renderer
   *
   **/
  ScenePlotView3D = function(renderer, decViews, div_id, xView, yView, width,
      height){

    this.decViews = decViews;
    this.renderer = renderer;
    this.xView = xView;
    this.yView = yView;
    this.width = width;
    this.height = height;

    // Set up the camera
    this.camera = new THREE.PerspectiveCamera(35, width/height,
        0.0000001, 10000);
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

    this.control = new THREE.OrbitControls(this.camera,
        document.getElementById(div_id));
    this.control.rotateSpeed = 1.0;
    this.control.zoomSpeed = 1.2;
    this.control.panSpeed = 0.8;
    this.control.enableZoom = true;
    this.control.enablePan = true;
    this.control.enableDamping = true;
    this.control.dampingFactor = 0.3;
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
    this.renderer.setViewport(this.xView, this.yView, this.width, this.height);
    this.renderer.render(this.scene, this.camera);
  };

  return ScenePlotView3D;
});
