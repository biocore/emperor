/**
 * @name EmperorViewControllerABC
 *
 * @class Abstract base class for view controllers used in Emperor.
 * This includes common functionality shared across all of the tab
 * controllers.
 *
 * @property {String} [title=""] Title of the controller.
 * @property {Node} [header=div node] jQuery element for the header
 * which contains the uppermost elements displayed in a tab.
 * @property {Node} [body=div node] jQuery element for the body,
 * which contains the lowermost elements displayed in tab.
 * This goes below the header.
 * @property {Node} [canvas=div node] jQuery element for the canvas,
 * which contains the header and the body.
 * @property {Node} [container=div node] jQuery element for the parent
 * container.
 * This only contains the canvas.
 * @property {Boolean} [active=false] Indicates whether the tab is front most
 * @property {String} [identifier="EMPtab-xxxxxxx"] Unique hash identifier for
 * the tab instance.
 * @property {Boolean} [enabled=true] Indicates if tab can be accessed.
 * @property {String} [description=""] Human-readable description of the tab.
 *
 */

/**
 *
 * @name EmperorViewControllerABC
 *
 * Initializes an abstract tab. This has to be contained in a DOM object and
 * will use the full size of that container.  The title represents the title
 * of the jQuery tab.  The description will be used as help text to describe
 * the functionality of each subclass tab.
 *
 * @param {Node} [container] Container node to create the controller in.
 * @param {String} [title] title of the tab.
 * @param {String} [description] helper description.
 *
 * @return {EmperorViewControllerABC} Returns an instance of the
 * EmperorViewControllerABC.
 *
 */
function EmperorViewControllerABC(container, title, description){
  this.$container = $(container);
  this.title = title;
  this.description = description;

  this.$canvas = null;
  this.$body = null;
  this.$header = null;
  this.active = false;
  this.identifier = "EMPtab-" + Math.round(1000000 * Math.random());
  this.enabled = true;

  var self = this; // only used within class

  if (this.$container.length < 1) {
    throw new Error("Emperor requires a valid container, " +
                    this.$container + " does not exist in the DOM.");
  }

  // Initializes the canvas and appends the canvas to the container
  // and initializes the header and the body to empty divs.
  this.$canvas = $('<div></div>');
  this.$container.append(this.$canvas);
  this.$canvas.width(this.$container.width());
  this.$canvas.height(this.$container.height());

  this.$header = $('<div></div>');
  this.$body = $('<div></div>');
  this.$canvas.append(this.$header);
  this.$canvas.append(this.$body);

  return this;
}

/**
 * Sets whether or not the tab can be modified or accessed.
 *
 * @param {Boolean} [trulse] option to enable tab.
 */
EmperorViewControllerABC.prototype.setEnabled = function(trulse){
  if(typeof(trulse) === "boolean"){
    this.enabled = trulse;
  }
  else{
    throw new Error("`trulse` can only be of boolean type");
  }
};

/**
 * Sets whether or not the tab is visible.
 *
 * @param {Boolean} [trulse] option to activate tab
 * (i.e. move tab to foreground).
 */
EmperorViewControllerABC.prototype.setActive = function(trulse){
  if(this.enabled === true){
    if(typeof(trulse) === "boolean"){
      this.active = trulse;
    }
    else{
      throw new Error("`trulse` can only be of boolean type");
    }
  }
};

/**
 * Resizes the container.
 *
 * @param {float} width the container width.
 * @param {float} height the container height.
 */
EmperorViewControllerABC.prototype.resize = function(width, height) {
  throw Error('Not implemented');
};

/**
 * Converts the current instance into a JSON string.
 *
 * @return {String} JSON string representation of self.
 */
EmperorViewControllerABC.prototype.toJSON = function(){
  throw Error('Not implemented');
};

/**
 * Decodes JSON string and modifies its own instance variables accordingly.
 *
 * @param {String} JSON string representation of an instance.
 */
EmperorViewControllerABC.prototype.fromJSON = function(jsonString){
  throw Error('Not implemented');
};

/**
 * @name EmperorAttributeABC
 *
 * @class Abstract base class for view controllers that control attributes of
 * the plots. Note, this class inherits from EmperorViewControllerABC.
 *
 * @property {Object} [decompViewDict] This is object is keyed by unique
 * identifiers and the values are DecompositionView objects referring to a set
 * of objects presented on screen. This dictionary will usually be shared by
 * all the tabs in the application. This argument is passed by reference.
 * @property {String} [activeViewKey=undefined] This is the key of the active
 * decomposition view.
 * @property {String} [metadataField] Metadata column name.
 * @property {Slick.Grid} [bodyGrid] Container that lists the metadata
 * categories described unther the `metadataField` column and the attribute
 * that can be modified.
 *
 */

/**
 *
 * @name EmperorViewControllerABC
 *
 * Initializes an abstract tab for attributes i.e. shape, color, size, etc.
 * This has to be contained in a DOM object and will use the full size of that
 * container.
 *
 * @params {Object} [decompViewDict] This is object is keyed by unique
 * identifiers and the values are DecompositionView objects referring to a set
 * of objects presented on screen. This dictionary will usually be shared by
 * all the tabs in the application. This argument is passed by reference.
 * @params {String} [metadataField] Metadata column name.
 * @params {Slick.Grid} [bodyGrid] Container that lists the metadata categories
 * described unther the `metadataField` column and the attribute that can be
 * modified.
 * @return {EmperorAttributeABC} Returns an instance of the EmperorAttributeABC
 * class.
 *
 */
function EmperorAttributeABC(container, title, description, decompViewDict,
                             metadataField, bodyGrid){
  EmperorViewControllerABC.call(this, container, title, description);

  if (decompViewDict === undefined){
    throw Error('The decomposition view dictionary cannot be undefined');
  }
  if (_.size(decompViewDict) <= 0){
    throw Error('The decomposition view dictionary cannot be empty');
  }
  this.decompViewDict = decompViewDict;

  // FIXME: this should be validated against decompViewDict i.e. we should be
  // verifying that the metadata field indeed exists in the decomposition model
  this.metadataField = metadataField;

  this.bodyGrid = bodyGrid;
  // Picks the first key in the dictionary as the active key
  this.activeViewKey = Object.keys(decompViewDict)[0];
  return this;
}
EmperorAttributeABC.prototype = Object.create(EmperorViewControllerABC.prototype);
EmperorAttributeABC.prototype.constructor = EmperorViewControllerABC;

/**
 * Changes the metadata column name to control.
 *
 * @params {String} [m] Metadata column name to control.
 */
EmperorAttributeABC.prototype.setMetadataField = function(m){
  this.metadataField = m;
}

/**
 * Retrieves the metadata field currently being controlled
 *
 * @return {String} Returns a key corresponding to the active
 * decomposition view.
 */
EmperorAttributeABC.prototype.getActiveDecompViewKey = function(){
  return this.activeViewKey;
}

/**
 * Changes the metadata column name to control.
 *
 * @params {String} [k] Key corresponding to active decomposition view.
 */
EmperorAttributeABC.prototype.setActiveDecompViewKey = function(k){
  this.activeViewKey = k;
}

/**
 * Retrieves the underlying data in the slick grid
 * @return {Array} Returns an array of objects
 * displayed by the body grid.
 */
EmperorAttributeABC.prototype.getSlickGridDataset = function(){
  return this.bodyGrid.getData();
}

/**
 * Changes the underlying data in the slick grid
 *
 * @params {Array} [data] data.
 */
EmperorAttributeABC.prototype.setSlickGridDataSet = function(data){
  // Re-render
  this.bodyGrid.setData(data);
  this.bodyGrid.invalidate();
  this.bodyGrid.render();
}
