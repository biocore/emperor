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
 * @param {name} a string indicating the name of the scene plot view.
 * @param {start} 
 * @param {width} width of the window object container
 * @param {height} height of the window object container
 * @param {idy} an *optional* integer representing the index where the object
 * @param {countt} an *optional* Array of floats indicating the confidence
 *             intervals in each dimension.
 *
 **/
ScenePlotView3D = function( start, width, height, idy, countt ){

//need to initialize the scene
 this.scene = new THREE.Scene();
 
  this.start = start === undefined ? 75 : start;
  this.width = width === undefined ? 0 : width;
  this.height = height === undefined ? 1 : height;
  this.idy = idy === undefined ? 0.1 : idy;
  this.countt = countt === undefined ? 1000 : countt;
  
  /*
  if (this.ci.length !== 0){
    if (this.ci.length !== this.coordinates.length){
      throw new Error("The number of confidence intervals doesn't match with"+
                      " the number of dimensions in the coordinates "+
                      "attribute. coords: " + this.coordinates.length +
                      " ci: " + this.ci.length);
    }
  }*/
 
  this.camera = new THREE.PerspectiveCamera( start, width / height, idy, countt );
  this.renderer = new THREE.WebGLRenderer();
  this.renderer.setSize( window.innerWidth, window.innerHeight );
  //document.body.appendChild( renderer.domElement );
  
  //camera, scene, ortho or perspective camera

};

ScenePlotView3D.prototype.setCamera = function( ){

}
