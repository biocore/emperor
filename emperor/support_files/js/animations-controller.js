define([
    'jquery',
    'underscore',
    'view',
    'viewcontroller',
], function($, _, DecompositionView, ViewControllers) {
  var EmperorViewControllerABC = ViewControllers.EmperorViewControllerABC;

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
   * @extends EmperorViewControllerABC
   */
  function AnimationsController(container, decompViewDict) {
    var helpmenu = 'Animate trajectories connecting samples in your data';
    var title = 'Animations';
    var scope = this;

    if (decompViewDict === undefined) {
      console.log('herew we are');
      throw Error('The decomposition view dictionary cannot be undefined');
    }
    for (var dv in decompViewDict) {
      if (!dv instanceof DecompositionView) {
        throw Error('The decomposition view dictionary ' +
            'can only have decomposition views');
      }
    }
    if (_.size(decompViewDict) <= 0) {
      throw Error('The decomposition view dictionary cannot be empty');
    }
    this.decompViewDict = decompViewDict;

    // Picks the first key in the dictionary as the active key
    this.activeViewKey = Object.keys(decompViewDict)[0];

    EmperorViewControllerABC.call(this, container, title, helpmenu);

    // initialize interface elements here
    $(this).ready(function() {
    });

    return this;
  }
  AnimationsController.prototype = Object.create(EmperorViewControllerABC.prototype);
  AnimationsController.prototype.constructor = EmperorViewControllerABC;

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
