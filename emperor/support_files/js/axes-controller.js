define([
    "jquery",
    "underscore",
    "view",
    "viewcontroller"
], function ($, _, DecompositionView, ViewControllers) {

  // we only use the base attribute class, no need to get the base class
  var EmperorViewControllerABC = ViewControllers.EmperorViewControllerABC;

  /**
   * @name AxesController
   *
   *  I know nothing about this ... yet :D
   *
   **/

  /*
   * @name AxesController
   *
   * I kinda know something about this, but not really
   *
   **/
  function AxesController(container, decompViewDict){
    var helpmenu = 'Change the visible dimensions of the data';
    var title = 'Axes';
    var scope = this;

    if (decompViewDict === undefined){
      throw Error('The decomposition view dictionary cannot be undefined');
    }
    for(var dv in decompViewDict){
      if(!dv instanceof DecompositionView){
        throw Error('The decomposition view dictionary ' +
            'can only have decomposition views');
      }
    }
    if (_.size(decompViewDict) <= 0){
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
  AxesController.prototype = Object.create(EmperorViewControllerABC.prototype);
  AxesController.prototype.constructor = EmperorViewControllerABC;

  return AxesController;
});
