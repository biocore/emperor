define([
    'jquery',
    'underscore',
    'view',
    'slickgrid',
    'chosen',
    'abcviewcontroller'
], function($, _, DecompositionView, SlickGrid, Chosen, abc) {
  EmperorViewControllerABC = abc.EmperorViewControllerABC;

  /**
   *
   * @class EmperorViewController
   *
   * Base class for view controllers that use a dictionary of decomposition
   * views, but that are not controlled by a metadata category, for those
   * cases, see `EmperorAttributeABC`.
   *
   * @param {Node} container Container node to create the controller in.
   * @param {String} title title of the tab.
   * @param {String} description helper description.
   * @param {Object} decompViewDict This is object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   *
   * @return {EmperorViewController} Returns an instance of the
   * EmperorViewController class.
   * @constructs EmperorViewController
   * @extends EmperorViewControllerABC
   *
   */
  function EmperorViewController(container, title, description,
                                 decompViewDict) {
    EmperorViewControllerABC.call(this, container, title, description);
    if (decompViewDict === undefined) {
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
    // Picks the first key in the dictionary as the active key
    /**
     * @type {String}
     * This is the key of the active decomposition view.
     */
    this.activeViewKey = Object.keys(decompViewDict)[0];

    /**
     * @type {Object}
     * This is object is keyed by unique identifiers and the values are
     * DecompositionView objects referring to a set of objects presented on
     * screen. This dictionary will usually be shared by all the tabs in the
     * application. This argument is passed by reference.
     */
    this.decompViewDict = decompViewDict;

    return this;
  }
  EmperorViewController.prototype = Object.create(
      EmperorViewControllerABC.prototype);
  EmperorViewController.prototype.constructor = EmperorViewControllerABC;

  /**
   * Retrieves the name of the currently active decomposition view.
   *
   * @return {String} A key corresponding to the active decomposition view.
   */
  EmperorViewController.prototype.getActiveDecompViewKey = function() {
    return this.activeViewKey;
  };

  /**
   * Changes the currently active decomposition view.
   *
   * @param {String} k Key corresponding to active decomposition view.
   * @throws {Error} The key must exist, otherwise an exception will be thrown.
   */
  EmperorViewController.prototype.setActiveDecompViewKey = function(k) {
    if (this.decompViewDict[k] === undefined) {
      throw new Error('This key does not exist, "' + k + '" in the ' +
                      'the decompViewDict.');
    }
    this.activeViewKey = k;
  };

  /**
   * Retrieves the currently active decomposition view.
   *
   * @return {DecompositionView} The currently active decomposition view.
   */
  EmperorViewController.prototype.getActiveView = function() {
    return this.decompViewDict[this.getActiveDecompViewKey()];
  };

  /**
   *
   * @class EmperorAttributeABC
   *
   * Initializes an abstract tab for attributes i.e. shape, color, size, etc.
   * This has to be contained in a DOM object and will use the full size of
   * that container.
   *
   * @param {Node} container Container node to create the controller in.
   * @param {String} title title of the tab.
   * @param {String} description helper description.
   * @param {Object} decompViewDict This is object is keyed by unique
   * identifiers and the values are DecompositionView objects referring to a
   * set of objects presented on screen. This dictionary will usually be shared
   * by all the tabs in the application. This argument is passed by reference.
   * @param {Object} options This is a dictionary of options used to build
   * the view controller. Used to set attributes of the slick grid and the
   * metadata category drop down. At the moment the constructor only expects
   * the following attributes:
   *  - categorySelectionCallback: a function object that's called when a new
   *  metadata category is selected in the dropdown living in the header.
   *  See [change]{@link https://api.jquery.com/change/}.
   *  - valueUpdatedCallback: a function object that's called when a metadata
   *  visualization attribute is modified (i.e. a change of color).
   *  See [onCellChange]{@link
   *  https://github.com/mleibman/SlickGrid/wiki/Grid-Events}.
   *  - slickGridColumn: a dictionary specifying options to be passed into the
   *  slickGrid. For instance, the ColorFormatter and the ColorEditor would be
   *  passed here.  For more information, refer to the Slick Grid
   *  documentation.
   *
   * @return {EmperorAttributeABC} Returns an instance of the
   * EmperorAttributeABC class.
   * @constructs EmperorAttributeABC
   * @extends EmperorViewController
   *
   */
  function EmperorAttributeABC(container, title, description,
      decompViewDict, options) {
    EmperorViewController.call(this, container, title, description,
                               decompViewDict);

    /**
     * @type {Node}
     * jQuery element for the div containing the slickgrid of sample information
     */
    this.$gridDiv = $('<div name="emperor-grid-div"></div>');
    this.$gridDiv.css('margin', '0 auto');
    this.$gridDiv.css('width', '100%');
    this.$gridDiv.css('height', '100%');
    this.$body.append(this.$gridDiv);
    /**
     * @type {String}
     * Metadata column name.
     */
    this.metadataField = null;

    var dm = decompViewDict[this.activeViewKey].decomp;
    var scope = this;

    // http://stackoverflow.com/a/6602002
    this.$select = $('<select>');
    _.each(dm.md_headers, function(header) {
      scope.$select.append($('<option>').attr('value', header).text(header));
    });
    this.$header.append(this.$select);

    // there's a few attributes we can only set on "ready" so list them up here
    $(function() {
      // setup the slick grid
      scope._buildGrid(options);

      // setup chosen
      scope.$select.chosen({width: '100%', search_contains: true});

      // only subclasses will provide this callback
      if (options.categorySelectionCallback !== undefined) {
        scope.$select.chosen().change(options.categorySelectionCallback);

        // now that we have the chosen selector and the table fire a callback
        // to initialize the data grid
        options.categorySelectionCallback(
          null, {selected: scope.$select.val()});
      }

    });

    return this;
  }
  EmperorAttributeABC.prototype = Object.create(
    EmperorViewController.prototype);
  EmperorAttributeABC.prototype.constructor = EmperorViewController;

  /**
   * Changes the metadata column name to control.
   *
   * @param {String} m Metadata column name to control.
   */
  EmperorAttributeABC.prototype.setMetadataField = function(m) {
    // FIXME: this should be validated against decompViewDict i.e. we should be
    // verifying that the metadata field indeed exists in the decomposition
    // model
    this.metadataField = m;
  };

  /**
   * Retrieves the underlying data in the slick grid
   * @return {Array} Returns an array of objects
   * displayed by the body grid.
   */
  EmperorAttributeABC.prototype.getSlickGridDataset = function() {
    return this.bodyGrid.getData();
  };

  /**
   * Changes the underlying data in the slick grid
   *
   * @param {Array} data data.
   */
  EmperorAttributeABC.prototype.setSlickGridDataset = function(data) {
    // Re-render
    this.bodyGrid.setData(data);
    this.bodyGrid.invalidate();
    this.bodyGrid.render();
  };

  /**
   * Method in charge of initializing the SlickGrid object
   *
   * @param {Object} [options] additional options to initialize the slick grid
   * of this object.
   * @private
   *
   */
  EmperorAttributeABC.prototype._buildGrid = function(options) {
    var columns = [{id: 'field1', name: '', field: 'category'}];
    var gridOptions = {editable: true, enableAddRow: false,
      enableCellNavigation: true, forceFitColumns: true,
      enableColumnReorder: false, autoEdit: true};

    // If there's a custom slickgrid column then add it to the object
    if (options.slickGridColumn !== undefined) {
      columns.unshift(options.slickGridColumn);
    }

    /**
     * @type {Slick.Grid}
     * Container that lists the metadata categories described under the
     * `metadataField` column and the attribute that can be modified.
     */
    this.bodyGrid = new Slick.Grid(this.$gridDiv, [], columns, gridOptions);

    // hide the header row of the grid
    // http://stackoverflow.com/a/29827664/379593
    $(this.$body).find('.slick-header').css('display', 'none');

    // subscribe to events when a cell is changed
    this.bodyGrid.onCellChange.subscribe(options.valueUpdatedCallback);
  };

  /**
   * Resizes the container and the individual elements.
   *
   * Note, the consumer of this class, likely the main controller should call
   * the resize function any time a resizing event happens.
   *
   * @param {Float} width the container width.
   * @param {Float} height the container height.
   */
  EmperorAttributeABC.prototype.resize = function(width, height) {
    // call super, most of the header and body resizing logic is done there
    EmperorViewController.prototype.resize.call(this, width, height);

    // the whole code is asynchronous, so there may be situations where
    // bodyGrid doesn't exist yet, so check before trying to modify the object
    if (this.bodyGrid !== undefined) {
      // make the columns fit the available space whenever the window resizes
      // http://stackoverflow.com/a/29835739
      this.bodyGrid.setColumns(this.bodyGrid.getColumns());
      // Resize the slickgrid canvas for the new body size.
      this.bodyGrid.resizeCanvas();
    }
  };

  /**
   * Converts the current instance into a JSON object.
   *
   * @return {Object} base object ready for JSON conversion.
   */
  EmperorAttributeABC.prototype.toJSON = function() {
    var json = {};
    json.category = this.$select.val();

    // Convert SlickGrid list of objects to single object
    var gridData = this.bodyGrid.getData();
    var jsonData = {};
    for (var i = 0; i < gridData.length; i++) {
      jsonData[gridData[i].category] = gridData[i].value;
    }
    json.data = jsonData;
    return json;
  };

  /**
   * Decodes JSON string and modifies its own instance variables accordingly.
   *
   * @param {Object} json Parsed JSON string representation of self.
   *
   */
  EmperorAttributeABC.prototype.fromJSON = function(json) {
    this.$select.val(json.category);
    this.$select.trigger('chosen:updated');

    // fetch and set the SlickGrid-formatted data
    var k = this.getActiveDecompViewKey();
    var data = this.decompViewDict[k].setCategory(
      json.data, this.setPlottableAttributes, json.category);
    this.setSlickGridDataset(data);
    // set all to needsUpdate
    this.decompViewDict[k].needsUpdate = true;
  };

  return {'EmperorViewControllerABC': EmperorViewControllerABC,
          'EmperorViewController': EmperorViewController,
          'EmperorAttributeABC': EmperorAttributeABC};
});
