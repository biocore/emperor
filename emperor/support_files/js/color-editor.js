define([
    'jquery',
    'underscore',
    'view',
    'viewcontroller',
    'spectrum'
],
function($, _, DecompositionView, ViewControllers, spectrum) {

  /**
   *
   * @name ColorEditor
   *
   * @class This class represents a color editor defined by the SlickGrid
   * project.
   *
   * @property {$input} object where the Spectrum color picker lives.
   * @property {defaultValue} initial value of the cell being edited.
   *
   * Note, this object is heavily based on classes in slick.editors.js and in
   * the documentation that can be found here:
   *    https://github.com/mleibman/SlickGrid/wiki/Writing-custom-cell-editors
   *
   * Also see ColorFormatter, a function in charge of formatting colors for the
   * SlickGrid object.
   *
   */
  function ColorEditor(args) {
    var $input;
    var defaultValue;
    var scope = this;

    this.init = function() {
      // make the background look exactly the same when the color is being
      // edited
      $(args.container).css('background-color', '#eeeeee');

      $input = $("<div class='colorbox'></div>");
      $input.css('background-color', args.item.value);
      $input.appendTo(args.container);
      $input.spectrum({
        color: args.item.color,
        showInput: true,
        allowEmpty: false,
        showPalette: false,
        showInitial: true,
        clickoutFiresChange: true,
        className: 'full-spectrum',
        preferredFormat: 'hex6',

        /* On change callback */
        change: function(color) {
          $input.css('background-color', color.toHexString());

          // commit the changes as soon as a new color is selected
          // http://stackoverflow.com/a/15513516/379593
          Slick.GlobalEditorLock.commitCurrentEdit();
        }
      });
    };

    this.destroy = function() {
      $input.spectrum('hide');
      $input.spectrum('destroy');
      $input.remove();
    };

    this.focus = function() {
      $input.spectrum('show');
    };

    this.isValueChanged = function() {
      return $input.spectrum('get').toHexString() !== defaultValue;
    };

    this.serializeValue = function() {
      return $input.spectrum('get').toHexString();
    };

    this.loadValue = function(item) {
      defaultValue = item[args.column.field];
      $input.spectrum('set', defaultValue);
    };

    this.applyValue = function(item, state) {
      item[args.column.field] = state;
    };

    this.validate = function() {
      return {valid: true, msg: null};
    };

    this.hide = function() {
      $input.spectrum('hide');
    };

    this.show = function() {
      $input.spectrum('show');
    };

    this.position = function(cellBox) {
      $input.spectrum('reflow');
    };

    this.init();
  }


  /**
   *
   * Function to format colors for the SlickGrid object.
   *
   * @param row SlickGrid row.
   * @param cell SlickGrid cell.
   * @param value the value in the row.
   * @param columnDef SlickGrid column definition.
   * @param dataContext data model of the SlickGrid object
   *
   * @return string with a div where the background color is set as the value
   * that's passed in.
   *
   * This formatter is heavily based in the examples found in
   * slick.formattters.js and is only intended to be used with ColorFormatter.
   *
   */
  function ColorFormatter(row, cell, value, columnDef, dataContext) {
    return "<div class='colorbox' style='background-color:" + value + ";'></div>";
  }

  return {'ColorEditor': ColorEditor, 'ColorFormatter': ColorFormatter};
});
