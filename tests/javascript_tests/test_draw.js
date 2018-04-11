/**
 *
 * @author Yoshiki Vazquez Baeza
 * @copyright Copyright 2013, The Emperor Project
 * @credits Yoshiki Vazquez Baeza
 * @license BSD
 * @version 0.9.61
 * @maintainer Yoshiki Vazquez Baeza
 * @email yoshiki89@gmail.com
 * @status Development
 *
 */

$(document).ready(function() {

  module("Drawing utilities", {

    setup: function(){
    },

    teardown: function(){
    }

  });

  /**
   *
   * Test that the SVG file is generated correctly.
   *
   */
  test("Test formatSVGLegend works correctly", function() {
    var res, names=[], colors=[], exp='';

    exp = '<svg xmlns="http://www.w3.org/2000/svg" width="168" height="191">'+
      '<g><rect height="27" width="27" y="1" x="5" style="stroke-width:1;str'+
      'oke:rgb(0,0,0)" fill="#0000ff"/><text xml:space="preserve" y="21" x="'+
      '40" font-size="12" stroke-width="0" stroke="#000000" fill="#000000">B'+
      'lue</text><rect height="27" width="27" y="41" x="5" style="stroke-wid'+
      'th:1;stroke:rgb(0,0,0)" fill="#ff00ff"/><text xml:space="preserve" y='+
      '"61" x="40" font-size="12" stroke-width="0" stroke="#000000" fill="#0'+
      '00000">Purple</text><rect height="27" width="27" y="81" x="5" style="'+
      'stroke-width:1;stroke:rgb(0,0,0)" fill="#000000"/><text xml:space="pr'+
      'eserve" y="101" x="40" font-size="12" stroke-width="0" stroke="#00000'+
      '0" fill="#000000">Black</text><rect height="27" width="27" y="121" x='+
      '"5" style="stroke-width:1;stroke:rgb(0,0,0)" fill="#00ffff"/><text xm'+
      'l:space="preserve" y="141" x="40" font-size="12" stroke-width="0" str'+
      'oke="#000000" fill="#000000">Yellow</text><rect height="27" width="27'+
      '" y="161" x="5" style="stroke-width:1;stroke:rgb(0,0,0)" fill="#aa00b'+
      'b"/><text xml:space="preserve" y="181" x="40" font-size="12" stroke-w'+
      'idth="0" stroke="#000000" fill="#000000">Magenta</text></g></svg>'

    names = ['Blue', 'Purple', 'Black', 'Yellow', 'Magenta'];
    colors = ['#0000ff', '#ff00ff', '#000000', '#00ffff', '#aa00bb'];

    res = formatSVGLegend(names, colors);
    deepEqual(res, exp, 'SVG file is formatted correcly'); 
  });

  /**
   *
   * Test that the SVG file is generated correctly when there are long labels.
   *
   */
  test("Test formatSVGLegend works correctly with long names", function() {
    var res, names=[], colors=[], exp='';

    exp = '<svg xmlns="http://www.w3.org/2000/svg" width="1056" height="191"'+
      '><g><rect height="27" width="27" y="1" x="5" style="stroke-width:1;st'+
      'roke:rgb(0,0,0)" fill="#0000ff"/><text xml:space="preserve" y="21" x='+
      '"40" font-size="12" stroke-width="0" stroke="#000000" fill="#000000">'+
      'Blue with more words (this is a long string)</text><rect height="27" '+
      'width="27" y="41" x="5" style="stroke-width:1;stroke:rgb(0,0,0)" fill'+
      '="#ff00ff"/><text xml:space="preserve" y="61" x="40" font-size="12" s'+
      'troke-width="0" stroke="#000000" fill="#000000">Purple</text><rect he'+
      'ight="27" width="27" y="81" x="5" style="stroke-width:1;stroke:rgb(0,'+
      '0,0)" fill="#000000"/><text xml:space="preserve" y="101" x="40" font-'+
      'size="12" stroke-width="0" stroke="#000000" fill="#000000">Black but '+
      'not as long as blue</text><rect height="27" width="27" y="121" x="5" '+
      'style="stroke-width:1;stroke:rgb(0,0,0)" fill="#00ffff"/><text xml:sp'+
      'ace="preserve" y="141" x="40" font-size="12" stroke-width="0" stroke='+
      '"#000000" fill="#000000">Yellow</text><rect height="27" width="27" y='+
      '"161" x="5" style="stroke-width:1;stroke:rgb(0,0,0)" fill="#aa00bb"/>'+
      '<text xml:space="preserve" y="181" x="40" font-size="12" stroke-width'+
      '="0" stroke="#000000" fill="#000000">Magenta</text></g></svg>'

    names = ['Blue with more words (this is a long string)', 'Purple',
             'Black but not as long as blue', 'Yellow', 'Magenta'];
    colors = ['#0000ff', '#ff00ff', '#000000', '#00ffff', '#aa00bb'];

    res = formatSVGLegend(names, colors);
    deepEqual(res, exp, 'SVG file is formatted correcly'); 
  });
});
