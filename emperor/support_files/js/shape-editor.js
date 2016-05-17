define([
    'jquery',
    'underscore',
    'view',
    'viewcontroller',
    'shapes'
],
function($, _, DecompositionView, ViewControllers, shapes) {

  /**
   *
   * @name Shape
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
   * Also see ShapeFormatter, a function in charge of formatting a dropdown for
   * the SlickGrid object.
   *
   */
  function ShapeEditor(args) {
    var $input;
    var defaultValue;
    var scope = this;

    this.init = function() {
      $input = shapes.$shapesDropdown;
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


  /**
   *
   * Function to format shape dropdown for the SlickGrid object.
   *
   * @param row SlickGrid row.
   * @param cell SlickGrid cell.
   * @param value the value in the row.
   * @param columnDef SlickGrid column definition.
   * @param dataContext data model of the SlickGrid object
   *
   * @return string with a div
   *
   * This formatter is heavily based in the examples found in
   * slick.formattters.js.
   *
   */
  function ShapeFormatter(row, cell, value, columnDef, dataContext) {
    return '<div>' + value + '</div>';
  }

  return {'ShapeEditor': ShapeEditor, 'ShapeFormatter': ShapeFormatter};
});
