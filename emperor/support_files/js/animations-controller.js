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
    var scope = this, dm, label, gradientTooltip, trajectoryTooltip;
    EmperorViewController.call(this, container, title, helpmenu,
                               decompViewDict);

    trajectoryTooltip = 'Category to group samples';
    gradientTooltip = 'Category to sort samples';

    dm = this.getView().decomp;

    this.$gradientSelect = $("<select class='emperor-tab-drop-down'>");
    this.$trajectorySelect = $("<select class='emperor-tab-drop-down'>");

    // http://stackoverflow.com/a/6602002
    // prepend an empty string so dropdown shows the "tooltip string"
    _.each([''].concat(dm.md_headers), function(header) {
      scope.$gradientSelect.append(
          $('<option>').attr('value', header).text(header));
      scope.$trajectorySelect.append(
          $('<option>').attr('value', header).text(header));
    });

    // add a label to the chosen drop downs
    label = $('<label>').text('Gradient').append(this.$gradientSelect);
    label.attr('title', gradientTooltip);
    this.$header.append(label);

    label = $('<label>').text('Trajectory').append(this.$trajectorySelect);
    label.attr('title', trajectoryTooltip);
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
    this._$speedLabel.attr('title', 'Speed at which the traces animate');
    this._$mediaContainer.append(this._$speedLabel);

    this.$speed = $('<div></div>').css('margin-top', '10px');
    this.$speed.attr('title', 'Speed at which the traces animate');
    this._$mediaContainer.append(this.$speed);

    this.director = null;
    this.playing = false;

    // initialize interface elements here
    $(this).ready(function() {
      scope.$speed.slider({'min': 0.1,
                           'max': 5,
                           'step': 0.1,
                           'value': 1,
                           'range': 'max',
                           'slide': function(event, ui) {
                             scope._$speedLabel.text('Speed (' + ui.value +
                                                     'x)');
                           },
                           'change': function(event, ui) {
                             scope._$speedLabel.text('Speed (' + ui.value +
                                                     'x)');
                           }});
      scope.$speed.css('background', '#70caff');

      // setup chosen
      scope.$gradientSelect.chosen({
        width: '100%',
        search_contains: true,
        placeholder_text_single: gradientTooltip
      });
      scope.$trajectorySelect.chosen({
        width: '100%',
        search_contains: true,
        placeholder_text_single: trajectoryTooltip
      });

      scope.$gradientSelect.chosen().change(function(e, p) {
                                              scope._gradientChanged(e, p);
                                            });
      scope.$trajectorySelect.chosen().change(function(e, p) {
                                                scope._trajectoryChanged(e, p);
                                              });

      scope.$rewind.button({icons: {primary: 'ui-icon-seek-first'}});
      scope.$rewind.attr('title', 'Restart the animation');
      scope.$rewind.on('click', function() {
        scope._rewindButtonClicked();
      });

      scope.$play.button({icons: {primary: 'ui-icon-play'}});
      scope.$play.attr('title', 'Start the animation');
      scope.$play.on('click', function() {
        scope._playButtonClicked();
      });

      scope.$pause.button({icons: {primary: 'ui-icon-pause'}});
      scope.$pause.attr('title', 'Pause the animation');
      scope.$pause.on('click', function() {
        scope._pauseButtonClicked();
      });

      scope.setEnabled(false);
    });

    return this;
  }
  AnimationsController.prototype = Object.create(
    EmperorViewController.prototype);
  AnimationsController.prototype.constructor = EmperorViewController;

  /**
   * Sets whether or not the tab can be modified or accessed.
   *
   * @param {Boolean} trulse option to enable tab.
   */
  AnimationsController.prototype.setEnabled = function(trulse) {
    EmperorViewController.prototype.setEnabled.call(this, trulse);
    this._updateButtons();
  };

  /**
   *
   * Helper method to update what media buttons should be enabled
   *
   * @private
   */
  AnimationsController.prototype._updateButtons = function() {
    var play, pause, speed, rewind;

    /*
     *
     * The behavior of the media buttons is a bit complicated. It is explained
     * by the following truth table where the variables are "director",
     * "playing" and "enabled". Each output's value determines if the button
     * should be enabled. Note that we negate the values when we make the
     * assignment because jQuery only has a "disabled" method.
     *
     * ||----------|---------|---------||-------|-------|-------|--------|
     * || director | playing | enabled || Play  | Speed | Pause | Rewind |
     * ||----------|---------|---------||-------|-------|-------|--------|
     * || FALSE    | FALSE   | FALSE   || FALSE | FALSE | FALSE | FALSE  |
     * || FALSE    | FALSE   | TRUE    || TRUE  | TRUE  | FALSE | FALSE  |
     * || FALSE    | TRUE    | FALSE   || FALSE | FALSE | FALSE | FALSE  |
     * || FALSE    | TRUE    | TRUE    || FALSE | FALSE | FALSE | FALSE  |
     * || TRUE     | FALSE   | FALSE   || FALSE | FALSE | FALSE | FALSE  |
     * || TRUE     | FALSE   | TRUE    || TRUE  | FALSE | FALSE | TRUE   |
     * || TRUE     | TRUE    | FALSE   || FALSE | FALSE | FALSE | FALSE  |
     * || TRUE     | TRUE    | TRUE    || FALSE | FALSE | TRUE  | TRUE   |
     * ||----------|---------|---------||-------|-------|-------|--------|
     *
     */
    play = ((this.enabled && this.director === null && !this.playing) ||
            (this.enabled && this.director !== null && !this.playing));

    pause = this.director !== null && this.enabled && this.playing;

    speed = this.director === null && !this.playing && this.enabled;

    rewind = this.director !== null && this.enabled;

    this.$speed.slider('option', 'disabled', !speed);
    this.$play.prop('disabled', !play);
    this.$pause.prop('disabled', !pause);
    this.$rewind.prop('disabled', !rewind);
  };

  /**
   *
   * Callback method executed when the Gradient menu changes.
   *
   * @private
   */
  AnimationsController.prototype._gradientChanged = function(evt, params) {
    if (this.getGradientCategory() !== '' && !this.enabled &&
        this.getTrajectoryCategory() !== '') {
      this.setEnabled(true);
    }
    else if (this.getGradientCategory() === '' ||
             this.getTrajectoryCategory() === '') {
      this.setEnabled(false);
    }
  };

  /**
   *
   * Callback method executed when the Trajectory menu changes.
   *
   * @private
   */
  AnimationsController.prototype._trajectoryChanged = function(evt, params) {
    if (this.getGradientCategory() !== '' && !this.enabled &&
        this.getTrajectoryCategory() !== '') {
      this.setEnabled(true);
    }
    else if (this.getGradientCategory() === '' ||
             this.getTrajectoryCategory() === '') {
      this.setEnabled(false);
    }
  };

  /**
   *
   * Callback method executed when the Rewind button is clicked.
   *
   * @private
   */
  AnimationsController.prototype._rewindButtonClicked = function(evt, params) {
    var view = this.getView();

    this.playing = false;
    this.director = null;

    view.tubes.forEach(function(tube) {
      if (tube.parent !== null) {
        tube.parent.remove(tube);
      }
    });

    view.tubes = [];
    view.needsUpdate = true;

    this._updateButtons();
  };

  /**
   *
   * Callback method when the Pause button is clicked.
   *
   * @private
   */
  AnimationsController.prototype._pauseButtonClicked = function(evt, params) {
    if (this.playing) {
      this.playing = false;
    }
    this._updateButtons();
  };

  /**
   *
   * Callback method when the Play button is clicked.
   *
   * @private
   */
  AnimationsController.prototype._playButtonClicked = function(evt, params) {

    if (this.playing === false && this.director !== null) {
      this.playing = true;
      this._updateButtons();
      return;
    }

    var headers, data = {}, positions = {}, gradient, trajectory, decomp, p;
    var view, marker, pos, speed;

    view = this.getView();
    decomp = this.getView().decomp;
    headers = decomp.md_headers;

    gradient = this.$gradientSelect.val();
    trajectory = this.$trajectorySelect.val();

    speed = this.getSpeed();

    for (var i = 0; i < decomp.plottable.length; i++) {
      p = decomp.plottable[i];

      data[p.name] = p.metadata;

      // get the view's position, not the metadata's position
      pos = view.markers[p.idx].position;
      positions[p.name] = {'name': p.name, 'color': 0, 'x': pos.x,
                           'y': pos.y, 'z': pos.z};
    }

    this.director = new AnimationDirector(headers, data, positions, gradient,
                                          trajectory, speed);
    this.director.updateFrame();

    this.playing = true;
    this._updateButtons();
  };

  /**
   *
   * Update the portion of the trajectory that needs to be drawn.
   *
   * If the animation is not playing (because it was paused or it has finished)
   * or a director hasn't been instantiated, no action is taken. Otherwise,
   * trajectories are updated on screen.
   *
   */
  AnimationsController.prototype.drawFrame = function() {
    if (this.director === null || this.director.animationCycleFinished() ||
        !this.playing) {
      return;
    }

    var view = this.getView(), tube, scope = this, color;

    // FIXME: this is a bug when the shapes are not spheres
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
      this.playing = false;

      // When the animation cycle finishes, update the state of the media
      // buttons and re-enable the rewind button so users can clear the
      // screen.
      this._updateButtons();
      this.$rewind.prop('disabled', false);
    }
  };

  /**
   *
   * Setter for the gradient category
   *
   * Represents how samples are ordered in each trajectory.
   *
   * @param {String} category The name of the category to set in the menu.
   */
  AnimationsController.prototype.setGradientCategory = function(category) {
    if (!this.hasMetadataField(category)) {
      category = '';
    }

    this.$gradientSelect.val(category);
    this.$gradientSelect.trigger('chosen:updated');
    this.$gradientSelect.change();
  };

  /**
   *
   * Getter for the gradient category
   *
   * Represents how samples are ordered in each trajectory.
   *
   * @return {String} The name of the gradient category in the menu.
   */
  AnimationsController.prototype.getGradientCategory = function() {
    return this.$gradientSelect.val();
  };

  /**
   *
   * Setter for the trajectory category
   *
   * Represents how samples are grouped together.
   *
   * @param {String} category The name of the category to set in the menu.
   */
  AnimationsController.prototype.setTrajectoryCategory = function(category) {
    if (!this.hasMetadataField(category)) {
      category = '';
    }

    this.$trajectorySelect.val(category);
    this.$trajectorySelect.trigger('chosen:updated');
    this.$trajectorySelect.change();
  };

  /**
   *
   * Getter for the trajectory category
   *
   * Represents how samples are grouped together.
   *
   * @return {String} The name of the trajectory category in the menu.
   */
  AnimationsController.prototype.getTrajectoryCategory = function() {
    return this.$trajectorySelect.val();
  };

  /**
   *
   * Setter for the speed of the animation.
   *
   * @param {Float} speed Speed at which the animation is played.
   * @throws {Error} If speed value es below 0.1 or above 5.
   */
  AnimationsController.prototype.setSpeed = function(speed) {
    if (speed < 0.1 || speed > 5) {
      throw new Error('The speed cannot be less than 0.1 or greater than 5');
    }
    this.$speed.slider('option', 'value', speed);
  };

  /**
   *
   * Getter for the speed of the animation.
   *
   * @return {Float} Speed at which the animation is played.
   */
  AnimationsController.prototype.getSpeed = function() {
    return this.$speed.slider('option', 'value');
  };

  AnimationsController.prototype.setColors = function(colors) {
    this._colors = colors;
  };

  /**
   * Converts the current instance into a JSON string.
   *
   * @return {Object} JSON ready representation of self.
   */
  AnimationsController.prototype.toJSON = function() {
    var json = {};

    json.gradientCategory = this.getGradientCategory();
    json.trajectoryCategory = this.getTrajectoryCategory();
    json.speed = this.getSpeed();

    return json;
  };

  /**
   * Decodes JSON string and modifies its own instance variables accordingly.
   *
   * @param {Object} Parsed JSON string representation of self.
   */
  AnimationsController.prototype.fromJSON = function(json) {
    this._rewindButtonClicked();

    this.setGradientCategory(json.gradientCategory);
    this.setTrajectoryCategory(json.trajectoryCategory);

    this.setSpeed(json.speed);
  };

  return AnimationsController;
});
