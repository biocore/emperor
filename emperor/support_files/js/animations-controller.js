define([
    'jquery',
    'underscore',
    'view',
    'viewcontroller',
], function($, _, DecompositionView, ViewControllers) {
  var EmperorViewController = ViewControllers.EmperorViewController;

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

    dm = decompViewDict[this.activeViewKey].decomp;

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

    this.$rewind = $('<button></button>');
    this.$header.append(this.$rewind);

    this.$play = $('<button></button>');
    this.$header.append(this.$play);

    this.$pause = $('<button></button>');
    this.$header.append(this.$pause);

    // initialize interface elements here
    $(this).ready(function() {
      // setup chosen
      scope.$gradientSelect.chosen({width: '100%', search_contains: true});
      scope.$trajectorySelect.chosen({width: '100%', search_contains: true});

      scope.$gradientSelect.chosen().change(scope._gradientChanged);
      scope.$trajectorySelect.chosen().change(scope._trajectoryChanged);

      scope.$rewind.button({icons: { primary: "ui-icon-seek-first"}});
      scope.$play.button({icons: { primary: "ui-icon-play"}});
      scope.$pause.button({icons: { primary: "ui-icon-pause"}});
    });

    return this;
  }
  AnimationsController.prototype = Object.create(EmperorViewController.prototype);
  AnimationsController.prototype.constructor = EmperorViewController;

  AnimationsController.prototype._gradientChanged = function(evt, params) {
    console.log('gradient category changed: ');
    console.log(params);
  }

  AnimationsController.prototype._trajectoryChanged = function(evt, params) {
    console.log('trajectory category changed: ');
    console.log(params);
  }

  /**
   * Converts the current instance into a JSON string.
   *
   * @return {Object} JSON ready representation of self.
   */
  AnimationsController.prototype.toJSON = function() {
    var json = {};

    console.error('Not implemented!');

    return json;
  };

  /**
   * Decodes JSON string and modifies its own instance variables accordingly.
   *
   * @param {Object} Parsed JSON string representation of self.
   */
  AnimationsController.prototype.fromJSON = function(json) {
    var scope = this;

    console.error('Not implemented!');
  };

  return AnimationsController;
});
