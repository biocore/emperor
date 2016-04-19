define(['jquery'], function($) {

  var shapes = {
    'sphere': new THREE.SphereGeometry(0.1, 8, 8),
    'cube': new THREE.CubeGeometry(0.2, 0.2, 0.2, 8, 8, 8),
    'cone': new THREE.CylinderGeometry(0.1, 0, 0.1, 10),
    'icosahedron': new THREE.IcosahedronGeometry(0.1, 0),
    'cylinder': new THREE.CylinderGeometry(0.05, 0.05, 0.2, 10)
  };

  var $shapesDropdown = $('<select>');
  for (shape in shapes) {
    $shapesDropdown.append(new Option(shape, shape));
  }

  return {shapes: shapes, $shapesDropdown: $shapesDropdown};
});
