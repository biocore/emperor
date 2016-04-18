var shapes = ['sphere', 'cube', 'cone', 'icosahedron', 'cylinder'];

var $shapesDropdown = $('<select>');
for (var i = 0; i < shapes.length; i++) {
  $shapesDropdown.append(new Option(shapes[i], shapes[i]));
}

function getGeometry(shape) {
  switch (shape) {
    case 'sphere':
      return new THREE.SphereGeometry(0.1, 8, 8);
      break;
    case 'cube':
      return new THREE.CubeGeometry(0.2, 0.2, 0.2, 8, 8, 8);
      break;
    case 'cone':
      return new THREE.CylinderGeometry(0.1, 0, 0.1, 10);
      break;
    case 'icosahedron':
      return new THREE.IcosahedronGeometry(0.1, 0);
      break;
    case 'cylinder':
      return new THREE.CylinderGeometry(0.1, 0.1, 0.1, 10);
      break;
    default:
      new Error('Unknown shape ' + shape);
    }
}