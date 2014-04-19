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
 */
function buildColorSelectorTable(headers, data, category, discrete, id){
  var categoryIndex, table, values = [], row, cell, div;

  categoryIndex = headers.indexOf(category);
  
  if (categoryIndex === -1){
    throw new Error('The category to build the table does not exist');
  }

  discrete = (discrete === undefined) ? false : discrete;
  id = (id === undefined) ? '' : id+'-';

	// get all values of this category from the mapping file
  values = _.map(data, function(sample){ return sample[categoryIndex] });
  values = _.uniq(values);

  table = document.createElement('table');

  // see emperor.css
  table.className = 'emperor-tab-table';

  for (var i=0; i < values.length; i++){
    row = table.insertRow();

    // add the name of the category to the right of the color box
    cell = row.insertCell();
    cell.title = values[i];
    cell.appendChild(document.createTextNode(values[i]));

    // create the div with the color selector
    cell = row.insertCell();
    div = document.createElement('div');
    div.id = id+'row-'+i+'-column-'+categoryIndex;
    div.className = 'colorbox';
    div.setAttribute('name', values[i]);
    cell.appendChild(div);

  }
  
  return table;
}
