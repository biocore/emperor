define([
    'jquery',
    'underscore',
    'view',
    'slickgrid',
    'chosen'
], function($, _, DecompositionView, SlickGrid, Chosen) {
  /**
   *
   * @class EmperorViewControllerABC
   *
   * Initializes an abstract tab. This has to be contained in a DOM object and
   * will use the full size of that container.  The title represents the title
   * of the jQuery tab.  The description will be used as help text to describe
   * the functionality of each subclass tab.
   *
   * @param {Node} container Container node to create the controller in.
   * @param {String} title title of the tab.
   * @param {String} description helper description.
   *
   * @return {EmperorViewControllerABC} Returns an instance of the
   * EmperorViewControllerABC.
   * @constructs EmperorViewControllerABC
   *
   */
  function EmperorViewControllerABC(container, title, description) {
    /**
     * @type {Node}
     * jQuery element for the parent container.
     */
    this.$container = $(container);
    /**
     * @type {String}
     * Human-readable title of the tab.
     */
    this.title = title;
    /**
     * @type {String}
     * Human-readable description of the tab.
     */
    this.description = description;

    /**
     * @type {Node}
     * jQuery element for the canvas, which contains the header and the body.
     */
    this.$canvas = null;
    /**
     * @type {Node}
     * jQuery element for the body, which contains the lowermost elements
     * displayed in tab. This goes below the header.
     */
    this.$body = null;
    /**
     * @type {Node}
     * jQuery element for the header which contains the uppermost elements
     * displayed in a tab.
     */
    this.$header = null;
    /**
     * @type {Boolean}
     * Indicates whether the tab is front most
     * @default false
     */
    this.active = false;
    /**
     * @type {String}
     * Unique hash identifier for the tab instance.
     * @default "EMPtab-xxxxxxx"
     */
    this.identifier = 'EMPtab-' + Math.round(1000000 * Math.random());
    /**
     * @type {Boolean}
     * Indicates if tab can be accessed.
     * @default true
     */
    this.enabled = true;

    if (this.$container.length < 1) {
      throw new Error('Emperor requires a valid container, ' +
          this.$container + ' does not exist in the DOM.');
    }

    // the canvas contains both the header and the body, note that for all
    // these divs the width should be 100% (whatever we have available), but
    // the height is much trickier, see the resize method for more information
    this.$canvas = $('<div name="emperor-view-controller-canvas"></div>');
    this.$canvas.width('100%');
    this.$container.append(this.$canvas);

    this.$canvas.width(this.$container.width());
    this.$canvas.height(this.$container.height());

    // the margin and width properties are set this way to center all the
    // contents of the divs themselves, see this SO answer:
    // http://stackoverflow.com/a/114549
    this.$header = $('<div name="emperor-view-controller-header"></div>');
    this.$header.css('margin', '0 auto');
    this.$header.css('width', '100%');

    this.$body = $('<div name="emperor-view-controller-body"></div>');
    this.$body.css('margin', '0 auto');
    this.$body.css('width', '100%');

    // inherit the size of the container minus the space being used for the
    // header
    this.$body.height(this.$canvas.height() - this.$header.height());
    this.$body.width(this.$canvas.width());

    this.$canvas.append(this.$header);
    this.$canvas.append(this.$body);

    return this;
  }

  /**
   * Sets whether or not the tab can be modified or accessed.
   *
   * @param {Boolean} trulse option to enable tab.
   */
  EmperorViewControllerABC.prototype.setEnabled = function(trulse) {
    if (typeof(trulse) === 'boolean') {
      this.enabled = trulse;
    }
    else {
      throw new Error('`trulse` can only be of boolean type');
    }
  };

  /**
   * Sets whether or not the tab is visible.
   *
   * @param {Boolean} trulse option to activate tab
   * (i.e. move tab to foreground).
   */
  EmperorViewControllerABC.prototype.setActive = function(trulse) {
    if (this.enabled === true) {
      if (typeof(trulse) === 'boolean') {
        this.active = trulse;
      }
      else {
        throw new Error('`trulse` can only be of boolean type');
      }
    }
  };

  /**
   * Resizes the container, note that the body will take whatever space is
   * available after considering the size of the header. The header shouldn't
   * have height variable objects, once added their height shouldn't really
   * change.
   *
   * @param {Float} width the container width.
   * @param {Float} height the container height.
   */
  EmperorViewControllerABC.prototype.resize = function(width, height) {
    // This padding is required in order to make space
    // for the horizontal menus
    var padding = 10;
    this.$canvas.height(height);
    this.$canvas.width(width - padding);

    this.$header.width(width - padding);

    // the body has to account for the size used by the header
    this.$body.width(width - padding);
    this.$body.height(height - this.$header.height());
  };

  /**
   *
   * Converts the current instance into a JSON string.
   *
   * @return {Object} ready to serialize representation of self.
   */
  EmperorViewControllerABC.prototype.toJSON = function() {
    throw Error('Not implemented');
  };

  /**
   * Decodes JSON string and modifies its own instance variables accordingly.
   *
   * @param {Object} parsed JSON string representation of an instance.
   */
  EmperorViewControllerABC.prototype.fromJSON = function(jsonString) {
    throw Error('Not implemented');
  };

  /**
   *
   * @class EmperorViewControllerABC
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
   * @extends EmperorViewControllerABC
   *
   */
  function EmperorAttributeABC(container, title, description,
      decompViewDict, options) {
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
    EmperorViewControllerABC.prototype);
  EmperorAttributeABC.prototype.constructor = EmperorViewControllerABC;

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
   * Retrieves the metadata field currently being controlled
   *
   * @return {String} A key corresponding to the active decomposition view.
   */
  EmperorAttributeABC.prototype.getActiveDecompViewKey = function() {
    return this.activeViewKey;
  };

  /**
   * Changes the metadata column name to control.
   *
   * @param {String} k Key corresponding to active decomposition view.
   */
  EmperorAttributeABC.prototype.setActiveDecompViewKey = function(k) {
    // FIXME: this should be validated against decompViewDict i.e. we should be
    // verifying that the key indeed exists
    this.activeViewKey = k;
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
    EmperorViewControllerABC.prototype.resize.call(this, width, height);

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
    'EmperorAttributeABC': EmperorAttributeABC};
});
