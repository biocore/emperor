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

  module("General utilities", {

    setup: function(){
    },

    teardown: function(){
    }

  });

  /**
   *
   * Test that elements in the list are sorted correctly when only words are
   * contained.
   *
   */
  test("Test naturalSort with words only", function() {
    var res, elements;

    elements = ['foo', 'Bar', 'BAZ', 'duck', 'duck', 'go'];
    res = naturalSort(elements);
    deepEqual(res, ['Bar', 'BAZ', 'duck', 'duck', 'foo', 'go'], 'Arrays is '+
              'sorted correctly');

    elements = ['foo', 'foo', 'FOO', 'FoO', 'FOOOO', 'fOO']
    res = naturalSort(elements);
    deepEqual(res, ["foo","foo","FOO","FoO","fOO", "FOOOO"], 'Arrays is '+
              'sorted correctly');

    elements = ['a', 'c', 'X', 'Y', 'Z', 'y']
    res = naturalSort(elements);
    deepEqual(res, ['a', 'c', 'X', 'Y', 'y', 'Z'], 'Arrays is sorted '+
              'correctly');

  });

  /**
   *
   * Test that elements in the list are sorted correctly when only numbers are
   * contained.
   *
   */
  test("Test naturalSort with numbers only", function() {
    var res, elements;

    elements = ['8', '7', '3', '2', '1', '0'];
    res = naturalSort(elements);
    deepEqual(res, ['0', '1', '2', '3', '7', '8'], 'Arrays is '+
              'sorted correctly');

    elements = ['1', '2', '3', '4', '5', '0']
    res = naturalSort(elements);
    deepEqual(res, ['0', '1', '2', '3', '4', '5'], 'Arrays is '+
              'sorted correctly');

    elements = ['-100', '0', '-0', '-200', '100', '100.001']
    res = naturalSort(elements);
    deepEqual(res, ['-200', '-100', '0', '-0', '100', '100.001'], 'Arrays is '+
              'sorted correctly');

  });

  test('Test Taxonomy Truncation', function() {
     lineage = 'k__qwerf;p__asdfjkj;c__'

     //Test if default string works
     res = truncateLevel(lineage, 0);
     equal(res,lineage);

     //Test if first taxonomy works
     res = truncateLevel(lineage, 1);
     equal(res,"k__qwerf");

     //Test if second taxonomy works
     res = truncateLevel(lineage, 2);
     equal(res,"p__asdfjkj");

     //Make sure that last known taxonomy is displayed
     res = truncateLevel(lineage, 3);
     equal(res,"p__asdfjkj;c__");

     //Make sure that second taxonomy doesn't change
     res = truncateLevel(lineage, 4);
     equal(res,"p__asdfjkj;c__");

  });

  /**
   *
   * Test that elements in the list are sorted correctly when there's a mixture
   * of numbers and words.
   *
   */
  test("Test naturalSort with numbers only", function() {
    var res, elements;

    elements = ['foo', '7', 'bar', '2', 'baz', '0'];
    res = naturalSort(elements);
    deepEqual(res, ['bar', 'baz', 'foo', '0', '2', '7'],'Arrays is sorted '+
              'correctly');

    elements = ['Foo', 'floo', 'BAAARR', '-1', '2', '0']
    res = naturalSort(elements);
    deepEqual(res, ['BAAARR', 'floo', 'Foo', '-1', '0', '2'], 'Arrays is '+
              'sorted correctly');

    elements = ['lorem', 'ipsum', 'boom.mooo', '-2.345563353', '-2.4']
    res = naturalSort(elements);
    deepEqual(res, ['boom.mooo', 'ipsum', 'lorem', '-2.4', '-2.345563353'],
              'Arrays is sorted correctly');

  });

  test("Test convertXMLToString", function(){
    var el;

    el = document.createElement("p");
    el.appendChild(document.createTextNode("Test"));
    equal(cleanHTML(convertXMLToString(el)),
          cleanHTML('<p xmlns="http://www.w3.org/1999/xhtml">Test</p>'),
          'Test a parragraph tag is converted correctly');

    el = document.createElement("div");
    el.appendChild(document.createTextNode("Test"));
    el.className="test-div-class"
    equal(cleanHTML(convertXMLToString(el)),
          cleanHTML('<div xmlns="http://www.w3.org/1999/xhtml" class="test-di'+
          'v-class">Test</div>'),
          'Test a div tag is converted correctly');
  });

  test("Test discrete colors are retrieved correctly", function(){
    equal(getDiscreteColor(0), "#8dd3c7", "Test color is indeed red");
    equal(getDiscreteColor(1), "#ffffb3", "Test color is indeed blue");
    equal(getDiscreteColor(2), "#bebada", "Test color is indeed orange");
  });

  test("Test discrete colors are retrieved on roll-over", function(){
    equal(getDiscreteColor(24), "#8dd3c7", "Test color is indeed red even in"+
          " the event of a roll-over");
    equal(getDiscreteColor(25), "#ffffb3", "Test color is indeed red even in"+
          " the event of a roll-over");
    equal(getDiscreteColor(26), "#bebada", "Test color is indeed red even in"+
          " the event of a roll-over");
  });

  test("Test discrete colors with other maps", function(){
    equal(getDiscreteColor(0, 'discrete-coloring'), "#8dd3c7",
          "Test color is indeed red");
    equal(getDiscreteColor(1, 'discrete-coloring-qiime'), "#0000ff",
          "Test color is indeed blue");
  });

  test("Test discrete colors with other maps (rollover)", function(){
    equal(getDiscreteColor(24, "discrete-coloring"), "#8dd3c7",
          "Test color is indeed red even in the event of a roll-over");
    equal(getDiscreteColor(25, "discrete-coloring-qiime"), "#0000ff",
          "Test color is indeed red even in the event of a roll-over");
    equal(getDiscreteColor(26, "discrete-coloring-qiime"), "#f27304",
          "Test color is indeed red even in the event of a roll-over");
  });

  test("Test getColorList exceptions", function(){
    var five;
    five = [0, 1, 2, 3, 4];

    throws(
      function (){
        var color = getDiscreteColor(0, 'discrete-coloring-non-existant');
      },
      Error,
      'An error is raised if the colormap does not exist'
    );
  });

  test("Test getColorList works", function(){
    var five, ten, twenty;

    five = [0, 1, 2, 3, 4];
    ten = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    twenty = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
              19]


    deepEqual(getColorList(five, 'discrete-coloring'), { "0": "#8dd3c7", "1":
        "#ffffb3", "2": "#bebada", "3": "#fb8072", "4": "#80b1d3" });

    deepEqual(getColorList(five, 'OrRd'), { "0": "#fff7ec", "1":
        "#ffbf92", "2": "#fc8d59", "3": "#d6593a", "4": "#7f0000" });
    deepEqual(getColorList([0], 'OrRd'), {"0": "#fff7ec"});

    deepEqual(getColorList(ten, 'Blues'), { "0": "#f7fbff", "1":
        "#d2e6f3", "2": "#b1d3e8", "3": "#93c3df", "4": "#78b4d9", "5":
        "#63a7d1", "6": "#5092c3", "7": "#3c77ac", "8": "#26568f", "9":
        "#08306b" });
    deepEqual(getColorList([0], 'Blues'), {"0": "#f7fbff"});

    deepEqual(getColorList(twenty, 'BrBG'), { "0": "#543005", "1":
        "#6f4b1d", "10": "#f6e9c8", "11": "#f2e9cf", "12": "#eae7d3", "13":
        "#dee3d3", "14": "#cedcd0", "15": "#bad3c9", "16": "#a2c7bf", "17":
        "#85bab2", "18": "#63a9a2", "19": "#35978f", "2": "#886533", "3":
        "#9f7d49", "4": "#b4945e", "5": "#c6a973", "6": "#d5bb87", "7":
        "#e2cb99", "8": "#ecd9ab", "9": "#f3e4bb" });
    deepEqual(getColorList([0], 'OrRd'), {"0": "#fff7ec"});

  });

  test("Test getColorList exceptions", function(){
    var five;
    five = [0, 1, 2, 3, 4];

    throws(
        function (){
          var colors = getColorList(five, false, 'Non-existant');
        },
      Error,
      'An error is raised if the colormap does not exist'
    );

  });

  test("Test regular expressions are escaped correctly", function(){
    equal(escapeRegularExpression('some.sample.id'), 'some\\.sample\\.id');
    equal(escapeRegularExpression('some-sample.id'), 'some\\-sample\\.id');
    equal(escapeRegularExpression('s/.*?ome.sample.id'), 's/\\.\\*\\?ome\\.sample\\.id');
  });

});
