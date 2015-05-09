/**
 *
 * @author Jamie Morton, Jose Navas Molina, Andrew Hodges & Yoshiki
 *         Vazquez-Baeza
 * @copyright Copyright 2013--, The Emperor Project
 * @credits Jamie Morton, Jose Navas Molina, Andrew Hodges & Yoshiki
 *          Vazquez-Baeza
 * @license BSD
 * @version 0.9.51-dev
 * @maintainer Yoshiki Vazquez Baeza
 * @email yoshiki89@gmail.com
 * @status Development
 *
 */


/**
 *
 * @name ScenePlotView3D
 *
 * @class Represents a sample and the associated metadata in the ordination
 * space.
 *
 */


/**
 *
 * @name ScenePlotView3D
 *
 * @class Represents a sample and the associated metadata in the ordination
 * space.
 *
 * @param {width} a float with the width of the renderer
 * @param {height} a float with the height of the renderer
 * @param {decViews} an Array of DecompositionViews shown in this scene
 *
 **/
ScenePlotView3D = function(width, height, decViews){
  this.decViews = decViews;
  // Set up the renderer
  this.rendererBackgroundColor = new THREE.Color();
  this.rendererBackgroundColor.setHex("0x000000");

  this.renderer = new THREE.WebGLRenderer( {antialias: true, preserveDrawingBuffer: true});
  this.renderer.setClearColor(this.rendererBackgroundColor);
  this.renderer.setSize(width, height);
  this.renderer.sortObjects = true;

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
  // Add all the meshes to the scene
  for (var i = 0; i < this.decViews.length; i++) {
    for (var j = 0; j < this.decViews[i].markers.length; j++) {
      this.scene.add(this.decViews[i].markers[j]);
    };
  };
};

ScenePlotView3D.prototype.setCameraAspectRatio = function(winAspect){
  this.camera.aspect = winAspect;
  this.camera.updateProjectionMatrix();
};

ScenePlotView3D.prototype.resize = function(width, height){
  this.renderer.setSize(width, height);
  this.setCameraAspectRatio(width / height);
};

ScenePlotView3D.prototype.render = function(){
  this.renderer.render(this.scene, this.camera)
};