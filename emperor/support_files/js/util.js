define(['underscore'], function(_) {
  /**
   *
   * Sorting function that deals with alpha and numeric elements
   *
   * This function takes a list of strings, divides it into two new lists, one
   * that's alpha-only and one that's numeric only.
   *
   * @param {string}  string of taxonomies
   *
   * @return a truncated string of taxonomies
   *
   */
  function naturalSort(list) {
    var numericPart = [], alphaPart = [], result = [];

    // separate the numeric and the alpha elements of the array
    for (var index = 0; index < list.length; index++) {
      if (isNaN(parseFloat(list[index]))) {
        alphaPart.push(list[index]);
      }
      else {
        numericPart.push(list[index]);
      }
    }

    // ignore casing of the strings, taken from:
    // http://stackoverflow.com/a/9645447/379593
    alphaPart.sort(function(a, b) {
      return a.toLowerCase().localeCompare(b.toLowerCase());
    });

    // sort in ascending order
    numericPart.sort(function(a, b) {return parseFloat(a) - parseFloat(b)});

      return result.concat(alphaPart, numericPart);
  }


  /**
   *
   * Utility function that splits the lineage into taxonomic levels
   * and returns the taxonomic level specified
   *
   * @param {node} XML DOM object, usually as created by the document object.
   *
   * @return string representation of the node object.
   *
   */
  function truncateLevel(lineage, levelIndex) {
    if (levelIndex === 0) {
      return lineage;
    }
    var levels = lineage.split(';');
    var taxaLabel = '';
    for (var i = 0; (i < levelIndex && i < levels.length); i++) {
      var level = levels[i];
      if (level[level.length - 1] == '_') {
        taxaLabel += ';'+ level;
      }else {
        taxaLabel = level;
      }
    }
    return taxaLabel;
  }

  /**
   *
   * Utility function to convert an XML DOM documents to a string useful for
   * unit testing
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
   * Escape special characters in a string for use in a regular expression.
   *
   * @param {regex} string to escape for use in a regular expression.
   *
   * @return string with escaped characters for use in a regular expression.
   *
   * Credits go to this SO answer http://stackoverflow.com/a/5306111
   */
  function escapeRegularExpression(regex) {
    return regex.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
  }

  /**
   *
   * Clean a string in HTML formatted strings that get created with the
   * namespace tag in some browsers and not in others. Intended to facilitate
   * testing.
   *
   * @param {htmlString} string to remove namespace from.
   *
   * @return string without namespace.
   *
   */
  function cleanHTML(htmlString) {
    return htmlString.replace(' xmlns="http://www.w3.org/1999/xhtml"', '');
  }

  return {'truncateLevel': truncateLevel, 'naturalSort': naturalSort,
          'convertXMLToString': convertXMLToString,
          'escapeRegularExpression': escapeRegularExpression,
          'cleanHTML': cleanHTML};
});
