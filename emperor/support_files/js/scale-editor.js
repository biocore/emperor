define([
    'jquery',
    'underscore',
    'view',
    'viewcontroller',
],
function($, _, DecompositionView, ViewControllers) {

  /**
   *
   * @name Scale
   *
   * @class This class represents a dropdown editor defined by the SlickGrid
   * project.
   *
   * @property {$input} object containing the dropdown
   * @property {defaultValue} initial value of the cell being edited.
   *
   * Note, this object is heavily based on classes in slick.editors.js and in
   * the documentation that can be found here:
   *    https://github.com/mleibman/SlickGrid/wiki/Writing-custom-cell-editors
   *
   * Also see ScaleFormatter, a function in charge of formatting a dropdown for
   * the SlickGrid object.
   *
   */
  function ScaleEditor(args) {
    var $input;
    var defaultValue;
    var scope = this;

    this.init = function() {
      $input = $('<input type="range" value="1" min="0.1" max="5" step="0.1">');
      console.log("THIS " + $input);
      $input.appendTo(args.container);
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
      return $input.val();
    };

    this.loadValue = function(item) {
      defaultValue = item[args.column.field];
      $input.val(defaultValue);
      $input[0].defaultValue = defaultValue;
      $input.select();
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
