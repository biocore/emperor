/**
 *
 * @author Yoshiki Vazquez Baeza
 * @copyright Copyright 2013, The Emperor Project
 * @credits Yoshiki Vazquez Baeza
 * @license BSD
 * @version 0.9.4
 * @maintainer Yoshiki Vazquez Baeza
 * @email yoshiki89@gmail.com
 * @status Release
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
    equal(getDiscreteColor(0), "0xFF0000", "Test color is indeed red");
    equal(getDiscreteColor(1), "0x0000FF", "Test color is indeed blue");
    equal(getDiscreteColor(2), "0xF27304", "Test color is indeed orange");
  });

  test("Test discrete colors are retrieved on roll-over", function(){
    equal(getDiscreteColor(24), "0xFF0000", "Test color is indeed red even in"+
          " the event of a roll-over");
    equal(getDiscreteColor(25), "0x0000FF", "Test color is indeed red even in"+
          " the event of a roll-over");
    equal(getDiscreteColor(26), "0xF27304", "Test color is indeed red even in"+
          " the event of a roll-over");

  });

  test("Test regular expressions are escaped correctly", function(){
    equal(escapeRegularExpression('some.sample.id'), 'some\\.sample\\.id');
    equal(escapeRegularExpression('some-sample.id'), 'some\\-sample\\.id');
    equal(escapeRegularExpression('s/.*?ome.sample.id'), 's/\\.\\*\\?ome\\.sample\\.id');
  });

});
