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
"#8dd3c7", // first list starts here
"#ffffb3",
"#bebada",
"#fb8072",
"#80b1d3",
"#fdb462",
"#b3de69",
"#fccde5",
"#d9d9d9",
"#bc80bd",
"#ccebc5",
"#ffed6f",
"#a6cee3", // second list starts here
"#1f78b4",
"#b2df8a",
"#33a02c",
"#fb9a99",
"#e31a1c",
"#fdbf6f",
"#ff7f00",
"#cab2d6",
"#6a3d9a",
"#ffff99",
"#b15928"]

// these colors are included in chroma and are the only ones we should
// use to interpolate through whe coloring in a continuous mode
var k_CHROMABREWER_MAPS = ['OrRd', 'PuBu', 'BuPu', 'Oranges', 'BuGn', 'YlOrBr',
    'YlGn', 'Reds', 'RdPu', 'Greens', 'YlGnBu', 'Purples', 'GnBu', 'Greys',
    'YlOrRd', 'PuRd', 'Blues', 'PuBuGn', 'Spectral', 'RdYlGn', 'RdBu', 'PiYG',
    'PRGn', 'RdYlBu', 'BrBG', 'RdGy', 'PuOr'];
var k_CHROMABREWER_MAPNAMES = ['Orange-Red', 'Purple-Blue', 'Blue-Purple',
    'Oranges', 'Blue-Green', 'Yellow-Orange-Brown', 'Yellow-Green',
    'Reds', 'Red-Purple', 'Greens', 'Yellow-Green-Blue', 'Purples',
    'Green-Blue', 'Greys', 'Yellow-Orange-Red', 'Purple-Red', 'Blues',
    'Purple-Blue-Green', 'Spectral', 'Red-Yellow-Green', 'Red-Blue',
    'Pink-Yellow-Green', 'Pink-Red-Green', 'Red-Yellow-Blue',
    'Brown-Blue-Green', 'Red-Grey', 'Purple-Orange']

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
 * Generate a list of colors that corresponds to all the samples in the plot
 *
 * @param {values} list of objects to generate a color for, usually a category
 * in a given metadata column.
 * @param {bool} whether or not the coloring scheme is using divergent or
 * continuous colors.
 *
 *
 * This function will generate a list of coloring values depending on the
 * coloring scheme that the system is currently using (discrete or continuous).
*/
function getColorList(values, discrete, map) {
  var colors = {}, numColors = values.length-1, counter=0, interpolator;

  if (discrete === false){
    map = chroma.brewer[map];
    interpolator = chroma.interpolate.bezier([map[0], map[3], map[4], map[5],
                                              map[8]]);
  }

  for(var index in values){
    if(discrete){
      // get the next available color
      colors[values[index]] = getDiscreteColor(index);
    }
    else{
      colors[values[index]] =  interpolator(counter/numColors).hex();
      counter = counter + 1;
    }
  }

  return colors;
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

