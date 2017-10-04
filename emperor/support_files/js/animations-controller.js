define([
    'jquery',
    'underscore',
    'view',
    'viewcontroller',
    'animationdirector',
    'draw'
], function($, _, DecompositionView, ViewControllers, AnimationDirector,
            draw) {
  var EmperorViewController = ViewControllers.EmperorViewController;
  var drawTrajectoryLine = draw.drawTrajectoryLine;

  /**
   * @class AnimationsController
   *
   * Controls the axes that are displayed on screen as well as their
   * orientation.
   *
   * @param {Node} container Container node to create the controller in.
   * @param {Object} decompViewDict This is object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   *
   * @return {AnimationsController}
   * @constructs AnimationsController
   * @extends EmperorViewController
   */
  function AnimationsController(container, decompViewDict) {
    var helpmenu = 'Animate trajectories connecting samples in your data';
    var title = 'Animations';
    var scope = this, dm, label;
    EmperorViewController.call(this, container, title, helpmenu,
                               decompViewDict);

    dm = this.getView().decomp;

    this.$gradientSelect = $("<select class='emperor-tab-drop-down'>");
    this.$trajectorySelect = $("<select class='emperor-tab-drop-down'>");

    // http://stackoverflow.com/a/6602002
    _.each(dm.md_headers, function(header) {
      scope.$gradientSelect.append(
          $('<option>').attr('value', header).text(header));
      scope.$trajectorySelect.append(
          $('<option>').attr('value', header).text(header));
    });

    // add a label to the chosen drop downs
    label = $('<label>').text('Gradient').append(this.$gradientSelect);
    this.$header.append(label);
    label = $('<label>').text('Trajectory').append(this.$trajectorySelect);
    this.$header.append(label);

    // container of the sliders and buttons
    this._$mediaContainer = $('<div name="button-container"></div>');
    this._$mediaContainer.css({'padding-top': '10px',
                               'width': 'inherit',
                               'text-align': 'center'});
    this.$body.append(this._$mediaContainer);

    this.$rewind = $('<button></button>');
    this._$mediaContainer.append(this.$rewind);

    this.$play = $('<button></button>');
    this._$mediaContainer.append(this.$play);

    this.$pause = $('<button></button>');
    this._$mediaContainer.append(this.$pause);

    this._colors = {};

    // make the buttons squared
    this._$mediaContainer.find('button').css({'width': '30px',
                                              'height': '30px',
                                              'margin': '0 auto',
                                              'margin-left': '10px',
                                              'margin-right': '10px'});

    this._$mediaContainer.append($('<hr>'));

    this._$speedLabel = $('<text name="speed">Speed (1x)</text>');
    this._$mediaContainer.append(this._$speedLabel);

    this.$speed = $('<div></div>').css('margin-top', '10px');
    this._$mediaContainer.append(this.$speed);

    this.director = null;
    this._isPlaying = false;

    // initialize interface elements here
    $(this).ready(function() {
      scope.$speed.slider({'min': 0.1,
                           'max': 5,
                           'step': 0.1,
                           slide: function(event, ui) {
                             scope._$speedLabel.text('Speed (' + ui.value +
                                                     'x)');
                           },
                           change: function(event, ui) {
                             scope._$speedLabel.text('Speed (' + ui.value +
                                                     'x)');
                             scope._sliderChanged();
                           }});

      // setup chosen
      scope.$gradientSelect.chosen({width: '100%', search_contains: true});
      scope.$trajectorySelect.chosen({width: '100%', search_contains: true});

      scope.$gradientSelect.chosen().change(function (){
                                              scope._gradientChanged();
                                            });
      scope.$trajectorySelect.chosen().change(function () {
                                                scope._trajectoryChanged();
                                              });

      scope.$rewind.button({icons: {primary: "ui-icon-seek-first"}});
      scope.$rewind.on('click', function() {
        scope._rewindButtonClicked();
      });

      scope.$play.button({icons: {primary: "ui-icon-play"}});
      scope.$play.on('click', function(){
        scope._playButtonClicked();
      });

      scope.$pause.button({icons: {primary: "ui-icon-pause"}});
      scope.$pause.on('click', function() {
        scope._pauseButtonClicked();
      });
    });

    return this;
  }
  AnimationsController.prototype = Object.create(EmperorViewController.prototype);
  AnimationsController.prototype.constructor = EmperorViewController;

  AnimationsController.prototype.isPlaying = function() {
    return this._isPlaying;
  }

  AnimationsController.prototype._sliderChanged = function(evt, ui) {

  }

  AnimationsController.prototype._sliderChanged = function(evt, ui) {

  }

  AnimationsController.prototype._gradientChanged = function(evt, params) {

  }

  AnimationsController.prototype._trajectoryChanged = function(evt, params) {

  }

  AnimationsController.prototype._rewindButtonClicked = function(evt, params) {
  /*
  g_isPlaying = false;
  g_animationDirector = null;
  document.getElementById("play-button").disabled="false";
  $('#animation-speed-slider').slider('option', 'disabled', false);

  for (var index = 0; index < g_animationLines.length; index++){
    g_mainScene.remove(g_animationLines[index]);
    g_elementsGroup.remove(g_animationLines[index]);
  }

  // re-initialize as an empty array
  g_animationLines = [];
  */
    console.log('clicked rewind, isPlaying: ' + this.isPlaying());
    var view = this.getView();

    this._isPlaying = false;
    this.AnimationDirector = null;

    this.$play.prop('disabled', false);
    this.$speed.slider('option', 'disabled', false);

    view.tubes.forEach(function(tube) {
      if (tube.parent !== null) {
        tube.parent.remove(tube);
      }
    });

    view.tubes = [];
    view.needsUpdate = true;
  }

  AnimationsController.prototype._pauseButtonClicked = function(evt, params) {
    /*
     *
        if (g_isPlaying === true){
          g_isPlaying = false;
          document.getElementById("play-button").disabled="false"
        }
     *
     * */
    console.log('clicked pause, isPlaying: ' + this.isPlaying());
    if (this.isPlaying()) {
      this._isPlaying = false;
      this.$play.prop('disabled', true);
    }
  }

  AnimationsController.prototype._playButtonClicked = function(evt, params) {

    var headers, data = {}, positions = {}, gradient, trajectory, decomp, p;
    var view, marker, pos;

    view = this.getView();
    decomp = this.getView().decomp;
    headers = decomp.md_headers;

    gradient = this.$gradientSelect.val();
    trajectory = this.$trajectorySelect.val();

    for (var i = 0; i < decomp.plottable.length; i++) {
      p = decomp.plottable[i];

      data[p.name] = p.metadata;

      // get the view's position, not the metadata's position
      pos = view.markers[p.idx].position;
      positions[p.name] = {'name': p.name, 'color': 0, 'x': pos.x,
                           'y': pos.y, 'z': pos.z};
    }

    this.director = new AnimationDirector(headers, data, positions, gradient,
                                          trajectory);
    this.$speed.slider('option', 'disabled', true);
    this.director.updateFrame();

    this._isPlaying = true;
  }

  AnimationsController.prototype.drawFrame = function() {
    if (this.director === null || this.director.animationCycleFinished() ||
        !this.isPlaying()) {
      return;
    }

    var view = this.getView(), tube, scope = this, color;

    var radius = view.markers[0].geometry.parameters.radius;

    view.tubes.forEach(function(tube) {
      if (tube === undefined) {
        return;
      }
      if (tube.parent !== null) {
        tube.parent.remove(tube);
      }
    });


    view.tubes = this.director.trajectories.map(function(trajectory) {
      color = scope._colors[trajectory.metadataCategoryName] || 'yellow';

      var tube = drawTrajectoryLine(trajectory, scope.director.currentFrame,
                                    color, 0.45 * radius);
      return tube;
    });

    view.needsUpdate = true;

    this.director.updateFrame();

    if (this.director.animationCycleFinished()) {
      this.director = null;
      this._isPlaying = false;
      this.$play.prop('disabled', false);
      this.$speed.slider('option', 'disabled', false);
    }
  };

  AnimationsController.prototype.setGradientCategory = function(category) {
    this.$gradientSelect.val(category);
    this.$gradientSelect.trigger('chosen:updated');
    this.$gradientSelect.change();
  };

  AnimationsController.prototype.getGradientCategory = function() {
    return this.$gradientSelect.val();
  };

  AnimationsController.prototype.setTrajectoryCategory = function(category) {
    this.$trajectorySelect.val(category);
    this.$trajectorySelect.trigger('chosen:updated');
    this.$trajectorySelect.change();
  };

  AnimationsController.prototype.getTrajectoryCategory = function() {
    return this.$trajectorySelect.val();
  };

  AnimationsController.prototype.setColors = function(colors) {
    this._colors = colors;
  }

  AnimationsController.prototype._createDecomposition = function(gradient, trajectory){
  
  }

  /**
   * Converts the current instance into a JSON string.
   *
   * @return {Object} JSON ready representation of self.
   */
  AnimationsController.prototype.toJSON = function() {
    var json = {};

    console.error('AnimationsViewController.toJSON Not implemented!');

    return json;
  };

  /**
   * Decodes JSON string and modifies its own instance variables accordingly.
   *
   * @param {Object} Parsed JSON string representation of self.
   */
  AnimationsController.prototype.fromJSON = function(json) {
    var scope = this;

    console.error('AnimationsViewController.fromJSON Not implemented!');
  };

  return AnimationsController;
});
