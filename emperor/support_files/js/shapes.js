// Module to avoid duplication of shape sources between controller and
// editor/formatter. This allows one central dict and dropdown of available
// shapes.
define(['jquery', 'three', 'underscore'], function($, THREE, _) {

  var SPHERE = 'Sphere', SQUARE = 'Square', CONE = 'Cone',
      ICOSAHEDRON = 'Icosahedron', CYLINDER = 'Cylinder',
      OCTAHEDRON = 'Diamond', RING = 'Ring', STAR = 'Star';

  var shapes = [SPHERE, OCTAHEDRON, CONE, CYLINDER, RING, SQUARE, ICOSAHEDRON,
                STAR];

  /**
   *
   * Return a correctly sized geometry that matches the plotting space
   *
   * @param {string} shapeName One of 'Sphere', 'Square', 'Cone',
   * 'Icosahedron', 'Cylinder', 'Diamond' and 'Ring'.
   * @param {Float} factor Size for the geometries. Usually as determined by
   * the DecompositionView object.
   *
   * @return {THREE.Geometry} The requested geometry object with a size
   * appropriate for the data presented on screen.
   * @function getGeometry
   */
  function getGeometry(shapeName, factor) {

    /*
     *
     * We arbitrarily rotate "flat-facing" geometries to avoid having the color
     * of the markers being distorted with the scene's light.
     *
     */

    switch (shapeName) {
      case SPHERE:
        return new THREE.SphereGeometry(factor, 8, 8);
      case SQUARE:
        geom = new THREE.PlaneGeometry(factor * 2, factor * 2, 2, 2);
        geom.rotateX(0.3);
        return geom;
      case CONE:
        return new THREE.CylinderGeometry(factor, 0, 2 * factor, 8);
      case ICOSAHEDRON:
        return new THREE.IcosahedronGeometry(factor, 0);
      case OCTAHEDRON:
        return new THREE.OctahedronGeometry(factor, 0);
      case RING:
        // 1.618033 ~= golden ratio
        geom = new THREE.RingGeometry(factor / 1.618033, factor);
        geom.rotateX(0.3);
        return geom;
      case STAR:
        return StarGeometry(factor * 0.5);
      case CYLINDER:
        return new THREE.CylinderGeometry(factor, factor, 2 * factor, 10);
      default:
        throw Error('Unknown geometry requested: ' + shapeName);
    }
  }

  var $shapesDropdown = $('<select>');
  _.each(shapes, function(shape) {
    $shapesDropdown.append(new Option(shape, shape));
  });

  /**
   * Create a star with 6 points.
   *
   * This code was adapted from:
   * https://threejs.org/examples/#webgl_geometry_extrude_shapes
   *
   * @param {Float} scale The scale to apply to the geometry.
   * @return {THREE.ShapeGeometry} The star geometry.
   *
   */
  function StarGeometry(scale) {
    var pts = [], numPts = 6, l, a, shape, geometry;

    for (var i = 0; i < numPts * 2; i++) {
      l = i % 2 == 1 ? 1 : 2;
      a = i / numPts * Math.PI;

      pts.push(new THREE.Vector2(Math.cos(a) * l, Math.sin(a) * l));
    }

    shape = new THREE.Shape(pts);
    geometry = new THREE.ShapeGeometry(shape);

    geometry.scale(scale, scale, scale);
    geometry.rotateX(0.3);
    return geometry;
  }

  return {$shapesDropdown: $shapesDropdown, getGeometry: getGeometry,
          shapes: shapes};
});
