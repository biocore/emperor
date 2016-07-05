define([
    "jquery",
    "underscore",
    "view",
    "viewcontroller",
    "d3"
], function ($, _, DecompositionView, ViewControllers, d3) {

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

    /*
     *
     * All bow to the power of the scree plot.
     *
     **/
    this.$_screePlotContainer = $('<div name="scree-plot">');
    this.$body.append(this.$_screePlotContainer);

    // initialize interface elements here
    $(this).ready(function() {
      scope._buildScreePlot();
    });

    return this;
  }
  AxesController.prototype = Object.create(EmperorViewControllerABC.prototype);
  AxesController.prototype.constructor = EmperorViewControllerABC;

  /*
   *
   *
   **/
  AxesController.prototype._buildScreePlot = function (){
    var percents = this.decompViewDict[this.activeViewKey].decomp.percExpl;
    percents = _.map(percents, function(val, index){
      // +1 to account for zero-indexing
      return {'axis': 'PC ' + (index + 1), 'percent': val};
    });

    // everything here is based on https://bl.ocks.org/mbostock/3885304
    var margin = {top: 10, right: 10, bottom: 30, left: 40},
        width = this.$body.width() - margin.left - margin.right,
        height = (this.$body.height() * 0.40) - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], 0.1);

    var y = d3.scale.linear()
      .range([height, 0]);

    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

    var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(4);

    var svg = d3.select(this.$_screePlotContainer.get(0)).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // creation of the chart itself
    x.domain(percents.map(function(d) { return d.axis; }));
    y.domain([0, d3.max(percents, function(d) { return d.percent; })]);

    svg.append("g")
      .attr("font", "10px sans-serif")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
      .attr("font", "10px sans-serif")
      .call(yAxis)
      .append("text")
      .attr('transform', 'translate(' + -30 + "," + height/2 + ") rotate(-90)")
      .style("text-anchor", "middle")
      .text("Variation Explained");

    svg.selectAll(".bar")
      .data(percents)
      .enter().append("rect")
      .attr("fill", "steelblue")
      .attr("x", function(d) { return x(d.axis); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.percent); })
      .attr("height", function(d) { return height - y(d.percent); });

    // set the axes style
    svg.selectAll('axis,path,line')
      .style('fill', 'none')
      .style('stroke', 'black')
      .style('shape-rendering', 'crispEdges');

    this.screePlot = svg;
  }

  return AxesController;
});
