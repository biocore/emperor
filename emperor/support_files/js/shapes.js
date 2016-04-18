define(['jquery'], function($) {

  var shapes = ['sphere', 'cube', 'cone', 'icosahedron', 'cylinder'];

  var $shapesDropdown = $('<select>');
  for (var i = 0; i < shapes.length; i++) {
    $shapesDropdown.append(new Option(shapes[i], shapes[i]));
  }

  function getGeometry(shape) {
    var geometry;
    switch (shape) {
      case 'sphere':
        geometry = new THREE.SphereGeometry(0.1, 8, 8);
        break;
      case 'cube':
        geometry = new THREE.CubeGeometry(0.2, 0.2, 0.2, 8, 8, 8);
        break;
      case 'cone':
        geometry = new THREE.CylinderGeometry(0.1, 0, 0.1, 10);
        break;
      case 'icosahedron':
        geometry = new THREE.IcosahedronGeometry(0.1, 0);
        break;
      case 'cylinder':
        geometry = new THREE.CylinderGeometry(0.05, 0.05, 0.2, 10);
        break;
      default:
        throw new Error('Unknown shape ' + shape);
      }
      return geometry;
  }

  return {shapes: shapes, $shapesDropdown: $shapesDropdown, getGeometry: getGeometry};
});
