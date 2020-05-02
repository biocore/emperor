define(['three'], function(THREE) {
  /**
   *
   * @class UIState
   *
   * An object that shares UI level state information across all entities under
   * a single emperor instance and exposes events when this information changes.
   * Do not access properties directly, go through the register event handlers
   * and use the getters/setters
   *
   */
  function UIState() {
    this.events = new THREE.EventDispatcher();

    //PROPERTY INITIALIZATION - (serialization and deserialization go here.)
    //Properties must be flattened into UIState until we determine how to handle
    //tiered events.
    this['view.usesPointCloud'] = false;
    this['view.viewType'] = 'scatter';
  }

  /**
   * Retrieve a keyed property
   */
  UIState.prototype.getProperty = function(key) {
    return this[key];
  };

  /**
   * Register for changes to a non collection backed keyed property.
   * The newly registered function is immediately called with the property's
   * current value.
   */
  UIState.prototype.registerProperty = function(key, onChange) {
    this.events.addEventListener(key, onChange);
    propertyValue = this.getProperty(key);
    onChange({type: key, newVal: propertyValue});
  };

  /**
   * Register for changes to a list backed keyed property.
   * onInit will be called whenever the list object is replaced
   * onAdd will be called whenever a new element is added to the list
   * onRemove will be called whenever an element is removed from the list
   * onUpdate will be called whenever an element at a given position is
   * replaced.
   *
   * onInit will be immediately called with the property's current value.
   */
  UIState.prototype.registerListProperty = function(key,
                                                    onInit,
                                                    onAdd,
                                                    onRemove,
                                                    onUpdate) {
    this.events.addEventListener(key + '/ADD', onAdd);
    this.events.addEventListener(key + '/REMOVE', onRemove);
    this.events.addEventListener(key + '/UPDATE', onUpdate);
    this.registerProperty(key, onInit);
  };

  /**
   * Register for changes to a dictionary backed keyed property.
   * onInit will be called whenever the dictionary object is replaced
   * onPut will be called whenever a new key value pair is put into the dict
   * onRemove will be called when a key is deleted from the dictionary
   *
   * onInit will be immediately called with the property's current value.
   */
  UIState.prototype.registerDictProperty = function(key,
                                                    onInit,
                                                    onPut,
                                                    onRemove) {
    this.events.addEventListener(key + '/PUT', onPut);
    this.events.addEventListener(key + '/REMOVE', onRemove);
    this.registerProperty(key, onInit);
  };

  /**
   * Set a keyed property and fire off its corresponding event
   */
  UIState.prototype.setProperty = function(key, value) {
    var oldValue = this.getProperty(key);
    this[key] = value;
    if (oldValue !== value) {
      this.events.dispatchEvent(
        {type: key, oldVal: oldValue, newVal: value}
      );
    }
  };

  /**
   * Set a series of keyed properties.
   * If a bulk event is set, this will be dispatched rather than individual
   * events for each property
   *
   * Bulk events must be objects of the form { type: xxx, ... } to pass
   * through the event dispatcher
   *
   * TODO: We could allow list and dictionary mutations to be part of
   * bulk events, is that a use case we think is realistic?
   */
  UIState.prototype.setProperties = function(keyValueDict, bulkEvent) {

    if (bulkEvent === undefined) {
      bulkEvent = null;
    }

    var oldValueDict = {};
    for (var key in keyValueDict) {
      oldValueDict[key] = this.getProperty(key);
    }
    for (key in keyValueDict) {
      this[key] = value;
    }

    if (bulkEvent === null) {
      for (key in keyValueDict) {
        if (oldValueDict[key] !== keyValueDict[key]) {
          this.events.dispatchEvent(
            {type: key, oldVal: oldValueDict[key], newVal: keyValueDict[key]}
          );
        }
      }
    }
    else {
      this.events.dispatchEvent(bulkEvent);
    }
  };

  //Observable List Functionality
  UIState.prototype.listPropertyAdd = function(propertyKey, index, value) {
    var list = this.getProperty(propertyKey);
    list.splice(index, 0, value);
    this.events.dispatchEvent(
      {type: propertyKey + '/ADD', index: index, val: value}
    );
  };

  UIState.prototype.listPropertyRemove = function(propertyKey, valueToRemove) {
    var index = this.getProperty(propertyKey).indexOf(valueToRemove);
    if (index != -1)
      this.listPropertyRemoveAt(propertyKey, index);
  };

  UIState.prototype.listPropertyRemoveAt = function(propertyKey, index) {
    var list = this.getProperty(propertyKey);
    var oldVal = list[index];
    list.splice(index, 1);
    this.events.dispatchEvent(
      {type: propertyKey + '/REMOVE', index: index, oldVal: oldVal}
    );
  };

  UIState.prototype.listPropertyUpdate = function(propertyKey,
                                                  index,
                                                  newValue) {
    var list = this.getProperty(propertyKey);
    var oldVal = list[index];
    list[index] = newValue;
    this.events.dispatchEvent(
      {type: propertyKey + '/UPDATE',
        index: index,
        oldVal: oldVal,
        newVal: newVal}
    );
  };

  //Observable Dictionary Functionality
  UIState.prototype.dictPropertyPut = function(propertyKey, dictKey, value) {
    var dict = this.getProperty(propertyKey);
    var oldVal = dict[dictKey];
    dict[dictKey] = value;
    this.events.dispatchEvent(
      {type: propertyKey + '/PUT',
        key: dictKey,
        oldVal: oldVal,
        newVal: value
      }
    );
  };

  UIState.prototype.dictPropertyRemove = function(propertyKey, dictKey) {
    var dict = this.getProperty(propertyKey);
    var oldVal = dict[dictKey];
    delete dict[dictKey];
    this.events.dispatchEvent(
      {type: propertyKey + '/REMOVE',
      key: dictKey,
      oldVal: oldVal
      });
  };

  //TODO FIXME HACK:  When we worry about removing linked event handlers
  //(because an object that is listening to UIState needs to go out of scope)
  //We must ensure that we are properly handling delinking of methods,
  //especially when developers linking in their handler functions will often
  //be careless about using function.bind vs wrapper functions vs anonymous
  //functions unless we throw exceptions in their faces.

  return UIState;
});
