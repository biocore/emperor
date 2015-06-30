/**
 *
 * @author Jamie Morton, Jose Navas Molina, Andrew Hodges & Yoshiki
 *         Vazquez-Baeza
 * @copyright Copyright 2013--, The Emperor Project
 * @credits Jamie Morton, Jose Navas Molina, Andrew Hodges & Yoshiki
 *          Vazquez-Baeza
 * @license BSD
 * @version 0.9.51-dev
 * @maintainer Jose Antonio Navas Molina
 * @email josenavas@gmail.com
 * @status Development
 *
 */

EmperorController = function(width, height, dm, divId){
  this.width = width;
  this.height = height;
  this.dm = dm;
  this.sceneViews = [];
  this.divId = divId;

  // set up the renderer
  this.rendererBackgroundColor = new THREE.Color();
  this.rendererBackgroundColor.setHex("0x000000");

  this.renderer = new THREE.WebGLRenderer( {antialias: true});
  this.renderer.setSize(width, height);
  this.renderer.setClearColor(this.rendererBackgroundColor);
  this.renderer.autoClear = false;
  this.renderer.sortObjects = true;

  // default decomposition view uses the full window
  this.addView();
};

EmperorController.prototype.addView = function(){
  if (this.sceneViews.length > 4){
    throw Error('Cannot add another scene plot view');
  }

  var spv = new ScenePlotView3D(this.renderer, [new DecompositionView(this.dm)],
                                this.divId, 0, 0, 0, 0);
  this.sceneViews.push(spv);

  // this will setup the appropriate sizes and widths
  this.resize(this.width, this.height);
};

EmperorController.prototype.resize = function(width, height){
  this.width = width;
  this.height = height;

  if (this.sceneViews.length === 1){
    this.sceneViews[0].resize(0, 0, this.width, this.height);
  }
  else if(this.sceneViews.length === 2){
    this.sceneViews[0].resize(0, 0, 0.5 * this.width, this.height);
    this.sceneViews[1].resize(0.5 * this.width, 0, 0.5 * this.width, this.height);
  }
  else if(this.sceneViews.length === 3){
    this.sceneViews[0].resize(0, 0, 0.5 * this.width, 0.5 * this.height);
    this.sceneViews[1].resize(0.5 * this.width, 0, 0.5 * this.width, 0.5 * this.height);
    this.sceneViews[2].resize(0, 0.5 * this.height, this.width, 0.5 * this.height);
  }
  else if(this.sceneViews.length === 4){
    this.sceneViews[0].resize(0, 0, 0.5 * this.width, 0.5 * this.height);
    this.sceneViews[1].resize(0.5 * this.width, 0, 0.5 * this.width, 0.5 * this.height);
    this.sceneViews[2].resize(0, 0.5 * this.height, 0.5 * this.width, 0.5 * this.height);
    this.sceneViews[3].resize(0.5 * this.width, 0.5 * this.height, 0.5 * this.width, 0.5 * this.height);
  }
  else{
    throw Error('More than four views are currently not supported');
  }
};

EmperorController.prototype.render = function(){
  this.renderer.setViewport(0, 0, this.width, this.height);
  this.renderer.clear();
  for (var i = 0; i < this.sceneViews.length; i++) {
    this.sceneViews[i].render();
  };
};
