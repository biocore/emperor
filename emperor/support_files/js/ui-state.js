define(['three', 'underscore'], function(THREE, _) {
  
  /**
   *
   * @class UIState
   *
   * A singleton that shares UI level state information globally and exposes
   * events when this information changes.  Do not access properties directly,
   * go through the register event handlers and use the getters/setters
   *
   */
  function UIState(){
    var stateScope = this;
    this.events = new THREE.EventDispatcher();
    
    console.log("Initializing UI State");
    //PROPERTY INITIALIZATION -
    //Properties must be flattened into UIState until we determine how to handle
    //tiered events.
    this["view.viewType"] = 'scatter';
    this["rules.color"] = null;
    this["rules.shape"] = null;
    this["favorite.numbers"] = [7, 13, 29, 42];
    
    /**
     * Retrieve a keyed property
     */
    function getProperty(key){
      return stateScope[key];
    }
    
    /**
     * Register for changes to a non collection backed keyed property.
     * The newly registered function is immediately called with the property's
     * current value.
     */
    function registerProperty(key, onChange){
      stateScope.events.addEventListener(key, onChange);
      propertyValue = getProperty(key);
      onChange({type: key, oldVal: propertyValue, newVal: propertyValue});
    }
    
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
    function registerListProperty(key, onInit, onAdd, onRemove, onUpdate){
      stateScope.events.addEventListener(key + "/ADD", onAdd);
      stateScope.events.addEventListener(key + "/REMOVE", onRemove);
      stateScope.events.addEventListener(key + "/UPDATE", onUpdate);
      registerProperty(key, onInit);
    }
    
    /**
     * Register for changes to a dictionary backed keyed property.
     * onInit will be called whenever the dictionary object is replaced
     * onPut will be called whenever a new key value pair is put into the dict
     * onRemove will be called when a key is deleted from the dictionary
     *
     * onInit will be immediately called with the property's current value.
     */
    function registerDictProperty(key, onInit, onPut, onRemove){
      stateScope.events.addEventListener(key + "/PUT", onPut);
      stateScope.events.addEventListener(key + "/REMOVE", onRemove);
      registerProperty(key, onInit);
    }
    
    /**
     * Set a keyed property and fire off its corresponding event
     */
    function setProperty(key, value){
      var oldValue = getProperty(key);
      stateScope[key] = value;
      stateScope.events.dispatchEvent(
        {type: key, oldVal: oldValue, newVal: value});
    }
    
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
    function setProperties(keyValueDict, bulkEvent = null){
      var oldValueDict = {};
      for (var key in keyValueDict){
        oldValueDict[key] = getProperty(key);
      }
      for (var key in keyValueDict){
        stateScope[key] = value;
      }
      
      if (bulkEvent == null) {
        for (var key in keyValueDict){
          stateScope.events.dispatchEvent(
            {type:key, oldVal: oldValueDict[key], newVal: keyValueDict[key]}
          );
        }
      }
      else {
        stateScope.events.dispatchEvent(bulkEvent);
      }
    }
  
    //Observable List Functionality
    function listPropertyAdd(propertyKey, index, value){
      var list = getProperty(propertyKey);
      list.splice(index, 0, value);
      stateScope.events.dispatchEvent(
        {type:propertyKey + "/ADD", index:index, val:value}
      );
    }
  
    function listPropertyRemove(propertyKey, index){
      var list = getProperty(propertyKey);
      var oldVal = list[index];
      list.splice(index, 1);
      stateScope.events.dispatchEvent(
        {type:propertyKey + "/REMOVE", index:index, oldVal:oldVal}
      );
    }
  
    function listPropertyUpdate(propertyKey, index, newValue){
      var list = getProperty(propertyKey);
      var oldVal = list[index];
      list[index] = newValue;
      stateScope.events.dispatchEvent(
        {type:propertyKey + "/UPDATE",
         index:index,
         oldVal:oldVal,
         newVal:newVal}
      );
    }
  
    //Observable Dictionary Functionality
    function dictPropertyPut(propertyKey, dictKey, value){
      var dict = getProperty(propertyKey);
      var oldVal = dict[dictKey];
      dict[dictKey] = value;
      stateScope.events.dispatchEvent(
        {type:propertyKey + "/PUT",
         key:dictKey,
         oldVal:oldVal,
         newVal:value
        }
      );
    }
  
    function dictPropertyRemove(propertyKey, dictKey){
      var dict = getProperty(propertyKey);
      var oldVal = dict[dictKey];
      delete dict[dictKey];
      stateScope.events.dispatchEvent(
        {type:propertyKey + "/REMOVE",
        key:dictKey,
        oldVal:oldVal
        });
    }
  }
  
  //Note, as as singleton, we could have just defined it anonymously in this
  //function.  However, should we choose to support multiple state objects
  //with different responsibilities (perhaps saved to different files?)
  //it might make sense to refactor this class out of this file.
  return new UIState();
});
