/**
 *
 * @author Yoshiki Vazquez Baeza
 * @copyright Copyright 2013, The Emperor Project
 * @credits Yoshiki Vazquez Baeza
 * @license BSD
 * @version 0.9.3-dev
 * @maintainer Yoshiki Vazquez Baeza
 * @email yoshiki89@gmail.com
 * @status Development
 *
 */

/**
 *
 * @name THREE.EmperorTrajectory
 *
 * @class This class represents the internal logic for a linearly interpolated
 * tube/trajectory in THREE.js the object itself is a subclass of the
 * THREE.Curve.
 *
 * @credits: This answer in StackOverflow helped a lot:
 * http://stackoverflow.com/a/18580832/379593
 *
 */
THREE.EmperorTrajectory = THREE.Curve.create(
  function ( points) {
    this.points = (points == undefined) ? [] : points;
  },

  function ( t ) {    
    var points = this.points;
    var index = ( points.length - 1 ) * t;
    var floorIndex = Math.floor(index);

    if(floorIndex == points.length-1){
      return points[floorIndex];
    }

    var floorPoint = points[floorIndex];
    var ceilPoint = points[floorIndex+1];

    return floorPoint.clone().lerp(ceilPoint, index - floorIndex);
  }
);

THREE.EmperorTrajectory.prototype.getUtoTmapping = function(u) {
    return u;
};

