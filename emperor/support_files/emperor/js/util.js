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

