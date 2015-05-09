EmperorController = function(width, height, dm, div_id){
  this.width = width;
  this.height = height;

  // set up the renderer
  this.rendererBackgroundColor = new THREE.Color();
  this.rendererBackgroundColor.setHex("0x000000");

  this.renderer = new THREE.WebGLRenderer( {antialias: true});
  this.renderer.setSize(width, height);
  this.renderer.setClearColor(this.rendererBackgroundColor);
  this.renderer.autoClear = false;
  this.renderer.sortObjects = true;

  this.sceneViews = [
    new ScenePlotView3D(this.renderer, [new DecompositionView(dm)], div_id, 0, 0, 0.5 * this.width, 0.5 * this.height),
    new ScenePlotView3D(this.renderer, [new DecompositionView(dm)], div_id, 0.5 * this.width, 0, 0.5 * this.width, 0.5 * this.height),
    new ScenePlotView3D(this.renderer, [new DecompositionView(dm)], div_id, 0, 0.5 * this.height, 0.5 * this.width, 0.5 * this.height),
    new ScenePlotView3D(this.renderer, [new DecompositionView(dm)], div_id, 0.5 * this.width, 0.5 * this.height, 0.5 * this.width, 0.5 * this.height)];
};

EmperorController.prototype.resize = function(width, height){
  this.width = width;
  this.height = height;
  this.sceneViews[0].resize(0, 0, 0.5 * this.width, 0.5 * this.height)
  this.sceneViews[1].resize(0.5 * this.width, 0, 0.5 * this.width, 0.5 * this.height)
  this.sceneViews[2].resize(0, 0.5 * this.height, 0.5 * this.width, 0.5 * this.height)
  this.sceneViews[3].resize(0.5 * this.width, 0.5 * this.height, 0.5 * this.width, 0.5 * this.height)
};

EmperorController.prototype.render = function(){
  this.renderer.setViewport(0, 0, this.width, this.height);
  this.renderer.clear();
  for (var i = 0; i < this.sceneViews.length; i++) {
    this.sceneViews[i].render();
  };
};
