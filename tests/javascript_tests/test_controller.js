define([
    "jquery",
    "underscore",
    "contextmenu",
    "three",
    "view",
    "scene3d",
    "colorviewcontroller",
    "visibilitycontroller",
    "shapecontroller",
    "filesaver"
], function ($, _, contextMenu, THREE, DecompositionView, ScenePlotView3D,
             ColorViewController, VisibilityController, ShapeController,
             FileSaver) {
  $(document).ready(function() {
    var Plottable = model.Plottable;

    module("Controller", {

      setup: function() {
      },

      teardown: function() {
      }
    });

    /**
     *
     * Test that the Plottable object is initialized correctly, without optional
     * arguments.
     *
     */
    test("Test saveConfig", function() {

    }
});