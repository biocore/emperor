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
      scope.$play.button({icons: {primary: "ui-icon-play"}});
      scope.$pause.button({icons: {primary: "ui-icon-pause"}});
    });

    return this;
  }
  AnimationsController.prototype = Object.create(EmperorViewController.prototype);
  AnimationsController.prototype.constructor = EmperorViewController;

  AnimationsController.prototype._sliderChanged = function(evt, ui) {

  }

  AnimationsController.prototype._gradientChanged = function(evt, params) {

  }

  AnimationsController.prototype._trajectoryChanged = function(evt, params) {

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
