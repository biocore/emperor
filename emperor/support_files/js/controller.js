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
 * @name EmperorViewControllerABC
 *
 * @class The main controller class used in Emperor.
 * @property {String} [title=""] Title of the color view controller.
 * @property {String} [title=""] Title of the opacity view controller.
 * @property {String} [title=""] Title of the size view controller.
 **/

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
  var scope = this;

  // Constants
  this.GRID_SCALE = 0.9;         // Scaling constant for grid dimensions
  this.SCENE_VIEW_SCALE = 0.5;   // Scaling constant for scene plot view dimensions
  this.SLICK_WIDTH = 25;         // Constant for width in slick-grid

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

  // FIXME: This is a hack to go around the fact that the constructor takes
  // a single decomposition model instead of a dictionary
  this.decViews = {'scatter': new DecompositionView(this.dm)};

  // default decomposition view uses the full window
  this.addView();

  this.$plotMenu.append("<div id='emperor-menu-tabs'></div>");
  $('#emperor-menu-tabs').append("<ul id='emperor-controller-list'></ul>");

  $(function() {
    scope.buildUI();
  });

};

/**
 * Helper method to add additional ScenePlotViews (i.e. another plot)
 *
 **/
EmperorController.prototype.addView = function() {
  if (this.sceneViews.length > 4) {
    throw Error('Cannot add another scene plot view');
  }

  var spv = new ScenePlotView3D(this.renderer, this.decViews,
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
    this.sceneViews[0].resize(0, 0, this.SCENE_VIEW_SCALE * plotWidth,
                              this.height);
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

  if (this.colorController !== undefined){
    // resize the grid according to the size of the container, since we are
    // inside the tabs we have to account for that lost space, hence the
    // this.GRID_SCALE=0.9
    var tabWidth = this.$plotMenu.width() * this.GRID_SCALE,
        tabHeight = this.$plotMenu.height() * this.GRID_SCALE;

    this.colorController.resize(tabWidth, tabHeight);
  }
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
  //FIXME: This only works for 1 scene plot view
  this.colorController = this.addTab(this.sceneViews[0].decViews,
                                     ColorViewController);

  // We are tabifying this div, I don't know man.
  $('#emperor-menu-tabs').tabs({heightStyle: 'fill'});
};

/**
 * Helper method to resize the plots.
 *
 * @param {Array} [dvdict] Dictionary of DecompositionViews.
 * @param {function} [viewConstructor] Constructor of the view controller.
 **/
EmperorController.prototype.addTab = function(dvdict, viewConstructor){
  // nothing but a temporary id
  var id = "" + Math.round(1000000 * Math.random());

  $('#emperor-menu-tabs').append("<div id='" + id +
                                 "' class='emperor-tab-div' ></div>");
  $('#' + id).height(this.$plotMenu.height());

  // dynamically instantiate the controller, see:
  // http://stackoverflow.com/a/8843181
  var obj = new (Function.prototype.bind.apply(viewConstructor,
                                               [null, '#' + id, dvdict]));

  // set the identifier of the div to the one defined by the object
  $('#' + id).attr('id', obj.identifier);

  // now add the list element linking to the container div with the proper
  // title
  $('#emperor-controller-list').append("<li><a  href='#" + obj.identifier +
                                       "-tab'>" + obj.title + "</a></li>");

  return obj;
};
