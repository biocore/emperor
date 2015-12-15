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

/**
 *
 * @name EmperorController
 *       This is the application controller
 *
 * @class Contains all the information on how the model is being presented to
 *        the user.
 *
 * @param {dm} a DecompositionModel object that will be
 * represented on screen.
 * @param {divid} the jQuery id correponding to the controller
 *
 **/
EmperorController = function(dm, divId){

  // Constants
  this.GRID_SCALE = 0.9;         // Scaling constant for grid dimensions
  this.SCENE_VIEW_SCALE = 0.5;   // Scaling constant for scene plot view dimensions

  this.$divId = $('#' + divId);
  this.width = this.$divId.width();
  this.height = this.$divId.height();

  this.dm = dm;
  this.sceneViews = [];

  // main divs where the content of the plots will be located
  this.$plotSpaceId = $("<div id='main-wrapper' class='emperor-plot-wrapper'></div>");
  this.$plotMenu = $("<div id='emperor-menu'></div>");

  this.$divId.append(this.$plotSpaceId);
  this.$divId.append(this.$plotMenu);

  // set up the renderer
  this.rendererBackgroundColor = new THREE.Color();
  this.rendererBackgroundColor.setHex('0x000000');

  this.renderer = new THREE.WebGLRenderer({antialias: true});
  this.renderer.setSize(this.width, this.height);
  this.renderer.setClearColor(this.rendererBackgroundColor);
  this.renderer.autoClear = false;
  this.renderer.sortObjects = true;
  this.$plotSpaceId.append(this.renderer.domElement);

  // default decomposition view uses the full window
  this.addView();

  this.buildUI();
};

/**
 * Helper method to add additional ScenePlotViews (i.e. another plot)
 *
 **/
EmperorController.prototype.addView = function() {
  if (this.sceneViews.length > 4) {
    throw Error('Cannot add another scene plot view');
  }

  var spv = new ScenePlotView3D(this.renderer, [new DecompositionView(this.dm)],
                                this.$plotSpaceId.attr('id'), 0, 0, 0, 0);
  this.sceneViews.push(spv);

  // this will setup the appropriate sizes and widths
  this.resize(this.width, this.height);
};

/**
 * Helper method to resize the plots
 *
 * @param {width} the width of the entire plotting space
 * @param {height} the height of the entire plotting space
 **/
EmperorController.prototype.resize = function(width, height){
  // update the available space we have
  this.width = width;
  this.height = height;

  // the area we have to present the plot is smaller than the total
  var plotWidth = this.$plotSpaceId.width();

  // TODO: The below will need refactoring
  // This is addressed in issue #405
  if (this.sceneViews.length === 1) {
    this.sceneViews[0].resize(0, 0, plotWidth, this.height);
  }
  else if (this.sceneViews.length === 2) {
    this.sceneViews[0].resize(0, 0, this.SCENE_VIEW_SCALE * plotWidth, this.height);
    this.sceneViews[1].resize(this.SCENE_VIEW_SCALE * plotWidth, 0,
                              this.SCENE_VIEW_SCALE * plotWidth, this.height);
  }
  else if (this.sceneViews.length === 3) {
    this.sceneViews[0].resize(0, 0,
                              this.SCENE_VIEW_SCALE * plotWidth,
                              this.SCENE_VIEW_SCALE * this.height);
    this.sceneViews[1].resize(this.SCENE_VIEW_SCALE * plotWidth, 0,
                              this.SCENE_VIEW_SCALE * plotWidth,
                              this.SCENE_VIEW_SCALE * this.height);
    this.sceneViews[2].resize(0, this.SCENE_VIEW_SCALE * this.height,
                              plotWidth, this.SCENE_VIEW_SCALE * this.height);
  }
  else if (this.sceneViews.length === 4) {
    this.sceneViews[0].resize(0, 0, this.SCENE_VIEW_SCALE * plotWidth,
                              this.SCENE_VIEW_SCALE * this.height);
    this.sceneViews[1].resize(this.SCENE_VIEW_SCALE * plotWidth, 0,
                              this.SCENE_VIEW_SCALE * plotWidth,
                              this.SCENE_VIEW_SCALE * this.height);
    this.sceneViews[2].resize(0, this.SCENE_VIEW_SCALE * this.height,
                              this.SCENE_VIEW_SCALE * plotWidth,
                              this.SCENE_VIEW_SCALE * this.height);
    this.sceneViews[3].resize(this.SCENE_VIEW_SCALE * plotWidth,
                              this.SCENE_VIEW_SCALE * this.height,
                              this.SCENE_VIEW_SCALE * plotWidth,
                              this.SCENE_VIEW_SCALE * this.height);
  }
  else {
    throw Error('More than four views are currently not supported');
  }

  this.renderer.setSize(plotWidth, this.height);

  // resize the grid according to the size of the container, since we are
  // inside the tabs we have to account for that lost space, hence the
  // this.GRID_SCALE=0.9
  var gridWidth = this.$plotMenu.width() * this.GRID_SCALE,
      gridHeight = this.$plotMenu.height() * this.GRID_SCALE;
  $('#myGrid').width(gridWidth);
  $('#myGrid').height(gridHeight);
};

/**
 * Helper method to render sceneViews
 **/
EmperorController.prototype.render = function() {
  this.renderer.setViewport(0, 0, this.width, this.height);
  this.renderer.clear();
  for (var i = 0; i < this.sceneViews.length; i++) {
    this.sceneViews[i].render();
  }
};

/**
 * Helper method to assemble UI, completely independent of HTML template
 **/
EmperorController.prototype.buildUI = function() {

  this.$plotMenu.append("<div id='emperor-menu-tabs'></div>");
  $('#emperor-menu-tabs').append("<ul><li><a href='#color-tab'>Colors</a></li></ul>");
  $('#emperor-menu-tabs').append("<div id='color-tab' class='emperor-tab-div'></div>");
  $('#emperor-menu-tabs').tabs({heightStyle: 'fill'});

  var gridWidth = this.$plotMenu.width() * this.GRID_SCALE,
      gridHeight = this.$plotMenu.height() * this.GRID_SCALE;

  var colorController = new AttributeViewController('#color-tab', 'color',
                                                    gridWidth, gridHeight,
                                                    this.dm, this.sceneViews,
                                                    null);

};


