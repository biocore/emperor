define([
    'jquery',
    'underscore',
    'abcviewcontroller'
], function($, _, abc) {

  var EmperorViewControllerABC = abc.EmperorViewControllerABC;

  function ViewTypeController(container, decompViewDict) {
    var title = "View Type";
    var description = "Change the selected View Type";
    
    EmperorViewControllerABC.call(this, container, title, description);

    this.$gridDiv = $('<div name="emperor-grid-div"></div>')
    this.$gridDiv.css('margin', '0 auto');
    this.$gridDiv.css('width', '100%');
    this.$gridDiv.css('height', '100%');
    this.$gridDiv.attr('title', 'Change the selected View Type');
    this.$body.append(this.$gridDiv);
    
    this.$radioScatter = $('<input type="radio" name="emperor.viewType" value="scatter"> Scatter </input>');
    this.$radioParallelPlot = $('<input type="radio" name="emperor.viewType" value="parallel-plot"> Parallel Plot </input>');
    
    this.$gridDiv.append(this.$radioScatter);
    this.$gridDiv.append(this.$radioParallelPlot);
    
    this.$radioScatter.change(function(){
      decompViewDict['scatter'].setViewType('scatter');
    });
    
    this.$radioParallelPlot.change(function(){
      decompViewDict['scatter'].setViewType('parallel-plot');
    });
    return this;
  }
  
  ViewTypeController.prototype = Object.create(EmperorViewControllerABC.prototype);
  ViewTypeController.prototype.constructor = EmperorViewControllerABC

  return ViewTypeController;
});
