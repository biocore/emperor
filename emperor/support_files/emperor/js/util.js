/**
 *
 * @author Yoshiki Vazquez Baeza
 * @copyright Copyright 2013, The Emperor Project
 * @credits Yoshiki Vazquez Baeza
 * @license BSD
 * @version 0.9.4-dev
 * @maintainer Yoshiki Vazquez Baeza
 * @email yoshiki89@gmail.com
 * @status Development
 *
 */


// http://colorbrewer2.org > qualitative > Number of Data Classes = 12
// colorbrewer will provide you with two lists of colors, those have been
// added here
var k_COLORBREWER_COLORS = [
"0x8dd3c7", // first list starts here
"0xffffb3",
"0xbebada",
"0xfb8072",
"0x80b1d3",
"0xfdb462",
"0xb3de69",
"0xfccde5",
"0xd9d9d9",
"0xbc80bd",
"0xccebc5",
"0xffed6f",
"0xa6cee3", // second list starts here
"0x1f78b4",
"0xb2df8a",
"0x33a02c",
"0xfb9a99",
"0xe31a1c",
"0xfdbf6f",
"0xff7f00",
"0xcab2d6",
"0x6a3d9a",
"0xffff99",
"0xb15928"]

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
 * list of k_COLORBREWER_COLORS. If this value value is greater than the number
 * of colors available, the function will just rollover and retrieve the next
 * available color.
 *
 * See k_COLORBREWER_COLORS at the top level of this module.
 *
 */
function getDiscreteColor(index){
  var size = k_COLORBREWER_COLORS.length;
  if(index >= size){
    index = index - (Math.floor(index/size)*size)
  }

  return k_COLORBREWER_COLORS[index]
}

/**
 *
 * Escape special characters in a string for use in a regular expression.
 *
 * @param {regex} string to escape for use in a regular expression.
 *
 * @return string with escaped characters for use in a regular expression.
 *
 * Credits go to this SO answer http://stackoverflow.com/a/5306111
 */
function escapeRegularExpression(regex){
    return regex.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
}

/**
 *
 * Clean a string in HTML formatted strings that get created with the namespace
 * tag in some browsers and not in others. Intended to facilitate testing.
 *
 * @param {htmlString} string to remove namespace from.
 *
 * @return string without namespace.
 *
 */
function cleanHTML(htmlString){
    return htmlString.replace(' xmlns="http://www.w3.org/1999/xhtml"', '')
}

