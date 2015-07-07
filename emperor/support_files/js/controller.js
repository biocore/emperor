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

EmperorController = function(dm, divId){
  this.$divId = $('#' + divId);
  this.width = this.$divId.width();
  this.height = this.$divId.height();

  this.dm = dm;
  this.sceneViews = [];

  // main divs where the content of the plots will be located
  this.$plotSpaceId = $("<div id='emperor-plot-wrapper'></div>");
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

EmperorController.prototype.resize = function(width, height){
  // update the available space we have
  this.width = width;
  this.height = height;

  // the area we have to present the plot is smaller than the total
  var plotWidth = this.$plotSpaceId.width();

  if (this.sceneViews.length === 1) {
    this.sceneViews[0].resize(0, 0, plotWidth, this.height);
  }
  else if (this.sceneViews.length === 2) {
    this.sceneViews[0].resize(0, 0, 0.5 * plotWidth, this.height);
    this.sceneViews[1].resize(0.5 * plotWidth, 0, 0.5 * plotWidth, this.height);
  }
  else if (this.sceneViews.length === 3) {
    this.sceneViews[0].resize(0, 0, 0.5 * plotWidth, 0.5 * this.height);
    this.sceneViews[1].resize(0.5 * plotWidth, 0, 0.5 * plotWidth, 0.5 * this.height);
    this.sceneViews[2].resize(0, 0.5 * this.height, plotWidth, 0.5 * this.height);
  }
  else if (this.sceneViews.length === 4) {
    this.sceneViews[0].resize(0, 0, 0.5 * plotWidth, 0.5 * this.height);
    this.sceneViews[1].resize(0.5 * plotWidth, 0, 0.5 * plotWidth, 0.5 * this.height);
    this.sceneViews[2].resize(0, 0.5 * this.height, 0.5 * plotWidth, 0.5 * this.height);
    this.sceneViews[3].resize(0.5 * plotWidth, 0.5 * this.height, 0.5 * plotWidth, 0.5 * this.height);
  }
  else {
    throw Error('More than four views are currently not supported');
  }

  this.renderer.setSize(plotWidth, this.height);

  // resize the grid according to the size of the container, since we are
  // inside the tabs we have to account for that lost space, hence the 0.9
  var gridWidth = this.$plotMenu.width() * 0.9,
      gridHeight = this.$plotMenu.height() * 0.9;
  $('#myGrid').width(gridWidth);
  $('#myGrid').height(gridHeight);
};

EmperorController.prototype.render = function() {
  this.renderer.setViewport(0, 0, this.width, this.height);
  this.renderer.clear();
  for (var i = 0; i < this.sceneViews.length; i++) {
    this.sceneViews[i].render();
  }
};

EmperorController.prototype.buildUI = function() {

  this.$plotMenu.append("<div id='emperor-menu-tabs'></div>");
  $('#emperor-menu-tabs').append("<ul><li><a href='#keys'>Key</a></li></ul>");
  $('#emperor-menu-tabs').append("<div id='keys' class='emperor-tab-div'></div>");
  $('#emperor-menu-tabs').tabs({heightStyle: 'fill'});

  var gridWidth = this.$plotMenu.width() * 0.9,
      gridHeight = this.$plotMenu.height() * 0.9;

  // http://stackoverflow.com/a/6602002
  var $select = $("<select class='emperor-tab-drop-down'>");
  _.each(this.dm.md_headers, function(header) {
    $select.append($('<option>').attr('value', header).text(header));
  });

  $('#keys').append($select);
  $('#keys').append("<div id='myGrid'></div>");
  $('#myGrid').width(gridWidth);
  $('#myGrid').height(gridHeight);

  var grid;
  var columns = [
    {id: 'title', name: '', field: 'color', sortable: false,
     maxWidth: 25, minWidth: 25, editor: ColorEditor,
     formatter: ColorFormatter},
    {id: 'field1', name: 'Category Name', field: 'category'}
  ];

  var options = {
    editable: true,
    enableAddRow: false,
    enableCellNavigation: true,
    forceFitColumns: true
  };

  $(function(ec) {
    grid = new Slick.Grid('#myGrid', [], columns, options);

    // subscribe to events when a cell is changed
    grid.onCellChange.subscribe(function(e, args) {
      var val = args.item.category, color = args.item.color, group = [];

      group = args.item.plottables;
      ec.sceneViews[0].decViews[0].setGroupColor(color, group);
    });

    function categorySelectorChanged(evt, params) {
      var newCategory = params.selected;

      data = ec.sceneViews[0].decViews[0].setCategoryColors(null, newCategory);
      grid.setData(data);
      grid.invalidate();
      grid.render();
    }
    // fire a callback to initialize the data grid
    categorySelectorChanged(null, {selected: $select.val()});

    // setup chosen
    $select.chosen({width: "100%", search_contains: true});
    $select.chosen().change(categorySelectorChanged);

    // make the columns fit the available spce whenever the window resizes
    // http://stackoverflow.com/a/29835739
    $(window).resize(function() {
      grid.setColumns(grid.getColumns());
    });
  }(this));
};
