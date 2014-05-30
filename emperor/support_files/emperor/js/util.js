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


// taken from the qiime/colors.py module; a total of 24 colors
var k_QIIME_COLORS = [
"0xFF0000", // red1
"0x0000FF", // blue1
"0xF27304", // orange1
"0x008000", // green
"0x91278D", // purple1
"0xFFFF00", // yellow1
"0x7CECF4", // cyan1
"0xF49AC2", // pink1
"0x5DA09E", // teal1
"0x6B440B", // brown1
"0x808080", // gray1
"0xF79679", // red2
"0x7DA9D8", // blue2
"0xFCC688", // orange2
"0x80C99B", // green2
"0xA287BF", // purple2
"0xFFF899", // yellow2
"0xC49C6B", // brown2
"0xC0C0C0", // gray2
"0xED008A", // red3
"0x00B6FF", // blue3
"0xA54700", // orange3
"0x808000", // green3
"0x008080"] // teal3

/**
 *
 * Sorting function that deals with alpha and numeric elements
 * 
 * This function takes a list of strings, divides it into two new lists, one
 * that's alpha-only and one that's numeric only.
 *
 * @param {list} an Array of strings.
 *
 * @return a sorted Array where all alpha elements at the beginning & all
 * numeric elements at the end.
 *
 */
function naturalSort(list){
  var numericPart = [], alphaPart = [], result = [];

  // separate the numeric and the alpha elements of the array
  for(var index = 0; index < list.length; index++){
    if(isNaN(parseFloat(list[index]))){
      alphaPart.push(list[index])
    }
    else{
      numericPart.push(list[index])
    }
  }

  // ignore casing of the strings, taken from:
  // http://stackoverflow.com/a/9645447/379593
  alphaPart.sort(function (a, b) {
    return a.toLowerCase().localeCompare(b.toLowerCase());
  });

  // sort in ascending order
  numericPart.sort(function(a,b){return parseFloat(a)-parseFloat(b)})

  return result.concat(alphaPart, numericPart);
}

/**
 *
 * Utility function to convert an XML DOM documents to a string useful for unit
 * testing
 *
 * @param {node} XML DOM object, usually as created by the document object.
 *
 * @return string representation of the node object.
 *
 * This code is based on this answer http://stackoverflow.com/a/1750890
 *
 */
function convertXMLToString(node) {
  if (typeof(XMLSerializer) !== 'undefined') {
    var serializer = new XMLSerializer();
    return serializer.serializeToString(node);
  }
  else if (node.xml) {
    return node.xml;
  }
}

/**
 *
 * Retrieve a discrete color from the list of QIIME colors
 *
 * @param {index} int, the index of the color to retrieve.
 *
 * @return string representation of the hexadecimal value for a color in the
 * list of k_QIIME_COLORS. If this value value is greater than the number of
 * colors available, the function will just rollover and retrieve the next
 * available color.
 *
 * See k_QIIME_COLORS at the top level of this module.
 *
 */
function getDiscreteColor(index){
	var size = k_QIIME_COLORS.length;
	if(index >= size){
		index = index - (Math.floor(index/size)*size)
	}

	return k_QIIME_COLORS[index]
}

