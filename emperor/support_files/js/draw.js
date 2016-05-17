define(['underscore', 'three'], function(_, THREE) {
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
      function(points) {
        this.points = (points == undefined) ? [] : points;
      },

      function(t ) {
        var points = this.points;
        var index = (points.length - 1) * t;
        var floorIndex = Math.floor(index);

        if (floorIndex == points.length - 1) {
          return points[floorIndex];
        }

        var floorPoint = points[floorIndex];
        var ceilPoint = points[floorIndex + 1];

        return floorPoint.clone().lerp(ceilPoint, index - floorIndex);
      }
      );

  THREE.EmperorTrajectory.prototype.getUtoTmapping = function(u) {
    return u;
  };


  /**
   *
   * Create a generic THREE.Line object
   *
   * @param {start} Array with the x, y and z coordinates of one of the ends
   * of the line.
   * @param {end} Array with the x, y and z coordinates of one of the ends
   * of the line.
   * @param {color} Integer in hexadecimal base that specifies the color of the
   * line.
   * @param {width} Float with the width of the line being drawn.
   * @param {transparent} Bool , whether the line will be transparent or not.
   *
   * @return THREE.Line object.
   *
   **/
  function makeLine(start, end, color, width, transparent) {
    // based on the example described in:
    // https://github.com/mrdoob/three.js/wiki/Drawing-lines
    var material, geometry, line;

    // make the material transparent and with full opacity
    material = new THREE.LineBasicMaterial({color: color, linewidth: width});
    material.matrixAutoUpdate = true;
    material.transparent = transparent;
    material.opacity = 1.0;

    // add the two vertices to the geometry
    geometry = new THREE.Geometry();
    geometry.vertices.push(new THREE.Vector3(start[0], start[1], start[2]));
    geometry.vertices.push(new THREE.Vector3(end[0], end[1], end[2]));

    // the line will contain the two vertices and the described material
    line = new THREE.Line(geometry, material);

    return line;
  }

  /**
   *
   * Create a THREE object that displays 2D text, this implementation is based
   * on the answer found here: http://stackoverflow.com/a/14106703/379593
   *
   * @param {position} Array representing the location of the label.
   * @param {text} String with the text to be shown on screen.
   * @param {color} Integer in hexadecimal base that represents the color of
   * the text.
   *
   * @return THREE.Sprite object with the text displaying in it.
   *
   **/
  function makeLabel(position, text, color) {
    var canvas = document.createElement('canvas');
    var size = 512;
    canvas.width = size;
    canvas.height = size;
    var context = canvas.getContext('2d');
    context.fillStyle = '#ffffff';
    context.textAlign = 'center';
    context.font = '30px Arial';
    context.fillText(text, size / 2, size / 2);

    var amap = new THREE.Texture(canvas);
    amap.needsUpdate = true;

    var mat = new THREE.SpriteMaterial({
        map: amap,
        transparent: true,
        color: color
    });

    var sp = new THREE.Sprite(mat);
    sp.position.set(position[0], position[1], position[2]);

    return sp;
  }

  /**
   *
   * Format an SVG string with labels and colors.
   *
   * @param {labels} Array object with the name of the labels.
   * @param {colors} Array object with the colors for each label.
   *
   * @return Returns an SVG string with the labels and colors values formated as
   * a legend.
   *
   */
  function formatSVGLegend(labels, colors) {
    var labels_svg = '', pos_y = 1, increment = 40, max_len = 0, rect_width,
    font_size = 12;

    for (var i = 0; i < labels.length; i++) {
      // add the rectangle with the corresponding color
      labels_svg += '<rect height="27" width="27" y="' + pos_y +
        '" x="5" style="stroke-width:1;stroke:rgb(0,0,0)" fill="' +
        colors[i] + '"/>';

      // add the name of the category
      labels_svg += '<text xml:space="preserve" y="' + (pos_y + 20) + '" x="40" ' +
        'font-size="' + font_size + '" stroke-width="0" stroke="#000000" ' +
        'fill="#000000">' + labels[i] + '</text>';

      pos_y += increment;
    }

    // get the name with the maximum number of characters and get the length
    max_len = _.max(labels, function(a) {return a.length}).length;

      // duplicate the size of the rectangle to make sure it fits the labels
      rect_width = font_size * max_len * 2;

    labels_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' +
      rect_width + '" height="' + (pos_y - 10) + '"><g>' + labels_svg + '</g></svg>';

    return labels_svg;
  }

  return {'formatSVGLegend': formatSVGLegend, 'makeLine': makeLine,
          'makeLabel': makeLabel};
});
