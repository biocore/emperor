define([
    'jquery',
    'underscore',
    'view',
    'viewcontroller',
],
function($, _, DecompositionView, ViewControllers) {

  /**
   *
   * @class Scale
   *
   * This class represents a range editor defined by the SlickGrid
   * project.
   * Note, this object is heavily based on classes in slick.editors.js and in
   * the documentation that can be found [here]{@link
   * https://github.com/mleibman/SlickGrid/wiki/Writing-custom-cell-editors}.
   *
   */
  function ScaleEditor(args) {
    /**
     * Node containing the jQuery slider
     * @type {Node}
     */
    var $input;
    /**
     * Node containing the textbox for showing the slider value
     * @type {Node}
     */
    var $viewval;
    /**
     * Initial value of the cell being edited.
     * @type {Float}
     */
    var defaultValue;
    var scope = this;

    /* @constructor */
    this.init = function() {
      $viewval = $('<input type="text" value="1.0" readonly ' +
                   'style="border:0;width:25px;">');
      var $sliderDiv = $('<div style="width:115px;display:inline-block;' +
                         'background-color:rgb(238, 238, 238)">');
      $input = $sliderDiv.slider({
        range: 'max',
        min: 0.1,
        max: 5.0,
        value: 1.0,
        step: 0.1,
        slide: function(event, ui) {
          $viewval.val(ui.value);
        }
      });
      $sliderDiv.appendTo(args.container);
      $viewval.appendTo(args.container);
    };

    this.destroy = function() {
      $input.remove();
    };

    this.focus = function() {
      $input.focus();
    };

    this.focusout = function() {
      $input.focusout();
    };

    this.isValueChanged = function() {
      return $input.val() !== defaultValue;
    };

    this.serializeValue = function() {
      return $viewval.val();
    };

    this.loadValue = function(item) {
      defaultValue = item[args.column.field];
      $input.val(defaultValue);
    };

    this.applyValue = function(item, state) {
      item[args.column.field] = state;
    };

    this.validate = function() {
      return {valid: true, msg: null};
    };

    this.init();
  }

  return {'ScaleEditor': ScaleEditor};
});
