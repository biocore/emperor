/*
 * __author__ = "Meg Pirrung"
 * __copyright__ = "Copyright 2013, Emperor"
 * __credits__ = ["Meg Pirrung","Antonio Gonzalez Pena","Yoshiki Vazquez Baeza"]
 * __license__ = "GPL"
 * __version__ = "0.0.0-dev"
 * __maintainer__ = "Meg Pirrung"
 * __email__ = "meganap@gmail.com"
 * __status__ = "Development"
 */

// spheres and ellipses that are being displayed on screen
var g_plotSpheres = {};
var g_plotEllipses = {};

// sample identifiers of all items that are plotted
var g_plotIds = [];

// line objects used to represent the axes
var g_xAxisLine;
var g_yAxisLine;
var g_zAxisLine;

// scene elements for the webgl plot
var g_mainScene;
var g_sceneCamera;
var g_sceneLight;

// general multipurpose variables
var g_elementsGroup; // group that holds the plotted shapes
var g_categoryIndex = 0; // current coloring category index
var g_genericSphere; // generic sphere used for plots
var g_categoryName = ""; // current coloring category
var g_foundId = ""; // id of currently located point
var g_time;
var g_visiblePoints = 0;
var g_sphereScaler = 1.0;
var g_keyBuilt = false;
var g_useDiscreteColors = false;

// taken from the qiime/colors.py module; a total of 29 colors
k_QIIME_COLORS = [
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

/*This function recenter the camera to the initial position it had*/
function resetCamera() {
	g_sceneCamera.aspect = document.getElementById('main_plot').offsetWidth/document.getElementById('main_plot').offsetHeight;
	g_sceneCamera.position.set( 0, 0, g_maximum*4);
	g_sceneCamera.rotation.set( 0, 0, 0);
	g_sceneCamera.updateProjectionMatrix();
}

/*Removes duplicates from a list of samples*/
function dedupe(list) {
	var set = {};
	for (var i = 0; i < list.length; i++){
		set[list[i]] = true;
	}
	list = [];
	for (var obj in set){
		list.push(obj);
	}
	return list;
}

/*Toggle between the scaled and unscaled version of the plot

  This function will change multiple elements in the plot, as described by the
  percentage explained in each of the PC axes.

  Note that this function will also change the position of the camera, light and
  adds a scaling value to the sphere size slider to make the size consistent
  between scaled and unscaled versions of the plot.
*/
function toggleScaleCoordinates(element){

	var axesLen;
	var operation;

	// modifying the properties basically requires to create the elemnts
	// again from scratch, so just remove them from scene and re-build them
	// the lines are all global variables hence just a call to remove them
	g_mainScene.remove(g_xAxisLine);
	g_mainScene.remove(g_yAxisLine);
	g_mainScene.remove(g_zAxisLine);

	// XOR operation for the checkbox widget, this will select an operation
	// to perform over various properties, either a multiplication or a division
	if(element.checked == true){
		operation = function(a, b){return a*b};
		g_sphereScaler = g_fractionExplained[0];
	}
	else{
		operation = function(a, b){return a/b};
		g_sphereScaler = 1;
	}

	// force an update of the size of the spheres
	$("#sradiusslider").slider("value",$("#sradiusslider").slider("value"));

	// scale other properties
	g_xMaximumValue = operation(g_xMaximumValue,g_fractionExplained[0]);
	g_yMaximumValue = operation(g_yMaximumValue,g_fractionExplained[1]);
	g_zMaximumValue = operation(g_zMaximumValue,g_fractionExplained[2]);
	g_xMinimumValue = operation(g_xMinimumValue,g_fractionExplained[0]);
	g_yMinimumValue = operation(g_yMinimumValue,g_fractionExplained[1]);
	g_zMinimumValue = operation(g_zMinimumValue,g_fractionExplained[2]);
	g_maximum = operation(g_maximum, g_fractionExplained[0])

	// scale the position of the camera according to pc1
	g_sceneCamera.position.set(
		operation(g_sceneCamera.position.x, g_fractionExplained[0]),
		operation(g_sceneCamera.position.y, g_fractionExplained[0]),
		operation(g_sceneCamera.position.z, g_fractionExplained[0]))

	// scale the position of the light
	g_sceneLight.position.set(
		operation(g_sceneLight.position.x, g_fractionExplained[0]),
		operation(g_sceneLight.position.y, g_fractionExplained[0]),
		operation(g_sceneLight.position.z, g_fractionExplained[0]));

	// scale the axis lines
	axesLen = Math.max(g_xMaximumValue+Math.abs(g_xMinimumValue),g_yMaximumValue+Math.abs(g_yMinimumValue),
		g_zMaximumValue+Math.abs(g_zMinimumValue));
	drawAxisLines(axesLen, g_xMinimumValue, g_yMinimumValue, g_zMinimumValue);

	// set the new position of each of the sphere objects
	for (sample_id in g_plotSpheres){
		// scale the position of the spheres
		g_plotSpheres[sample_id].position.set(
			operation(g_plotSpheres[sample_id].position.x,g_fractionExplained[0]),
			operation(g_plotSpheres[sample_id].position.y,g_fractionExplained[1]),
			operation(g_plotSpheres[sample_id].position.z,g_fractionExplained[2]));
	}

	// ellipses won't always be available hence the two separate loops
	for (sample_id in g_plotEllipses){
		// scale the dimensions of the positions of each ellipse
		g_plotEllipses[sample_id].position.set(
			operation(g_plotEllipses[sample_id].position.x, g_fractionExplained[0]),
			operation(g_plotEllipses[sample_id].position.y, g_fractionExplained[1]),
			operation(g_plotEllipses[sample_id].position.z, g_fractionExplained[2]));

		// scale the dimensions of the ellipse
		g_plotEllipses[sample_id].scale.set(
			operation(g_plotEllipses[sample_id].scale.x, g_fractionExplained[0]),
			operation(g_plotEllipses[sample_id].scale.y, g_fractionExplained[1]),
			operation(g_plotEllipses[sample_id].scale.z, g_fractionExplained[2]));
	}

}

/* Toggle between discrete and continuous coloring for samples and labels */
function toggleContinuousAndDiscreteColors(element){
	g_useDiscreteColors = element.checked;

	// re-coloring the samples and labels now will use the appropriate coloring
	colorByMenuChanged();
	labelMenuChanged();
}

/*Generate a list of colors that corresponds to all the samples in the plot

  This function will generate a list of coloring values depending on the
  coloring scheme that the system is currently using (discrete or continuous).
*/
function getColorList(vals) {
	var colors = [];

	// cases with one or two categories are basically the same no matter if the
	// coloring scheme is continuous or discrete; choose red or red and blue
	if(vals.length == 1){
		colors[0] = new THREE.Color();
		colors[0].setHex("0xff0000");
	}
	else if (vals.length == 2) {
		colors[0] = new THREE.Color();
		colors[0].setHex("0xff0000");
		colors[1] = new THREE.Color();
		colors[1].setHex("0x0000ff");
	}
	else {
		for(var index in vals){
			colors[index] = new THREE.Color();
			if(g_useDiscreteColors){
				// get the next available color
				colors[index].setHex(getDiscreteColor(index)*1);
			}
			else{
				// multiplying the value by 0.66 makes the colormap go R->G->B
				colors[index].setHSV(index*.66/vals.length,1,1);
			}
		}
	}
	return colors;
}

/* Retrieve one of the discrete colors from the list

  This function will return the color at the requested index, if this value
  value is greater than the number of colors available, the function will just
  rollover and retrieve the next available color.
*/
function getDiscreteColor(index){
	var size = k_QIIME_COLORS.length;
	if(index >= size){
		index = index - (Math.floor(index/size)*size)
	}

	return k_QIIME_COLORS[index]
}

/*Start timer (for debugging)*/
function startTimer() {
	var d=new Date()
	g_time = d.getTime();
}

/*End timer (for debugging)*/
function stopTimer(info) {
	var d=new Date()
	g_time = d.getTime() - g_time;
	console.log("time to " +info +":"+g_time+"ms")
}

/*This function is called when a new value is selected in the colorBy menu */
function colorByMenuChanged() {
	// set the new current category and index
	g_categoryName = document.getElementById('colorbycombo')[document.getElementById('colorbycombo').selectedIndex].value;
	g_categoryIndex = g_mappingFileHeaders.indexOf(g_categoryName);

	// get all values of this category from the mapping
	var vals = [];
	for(var i in g_plotIds){
		vals.push(g_mappingFileData[g_plotIds[i]][g_categoryIndex]);
	}

	vals = dedupe(vals).sort();
	colors = getColorList(vals);

	// build the colorby table in HTML
	var lines = "<table>";
	for(var i in vals){
		// html classes have a special meaning for '.' and spaces, must remove them
		// as well as special chars
		var validVal = vals[i].replace(/[\. :!@#$%^&*()]/g,'');
		// set the div id so that we can reference this div later
		lines += "<tr><td><div id=\""+validVal+"\"class=\"colorbox\" name=\""+vals[i]+"\"></div></td><td title=\""+vals[i]+"\">";

		if(vals[i].length > 25){
			lines+= vals[i].substring(0,25) + "..."
		}
		else{
			lines += vals[i];
		}

		lines+= "</td></tr>";
	}
	lines += "</table>";
	document.getElementById("colorbylist").innerHTML = lines;

	for(var i in vals){
		var validVal = vals[i].replace(/[\. :!@#$%^&*()]/g,'');
		// get the div built earlier and turn it into a color picker
		$('#'+validVal).css('backgroundColor',"#"+colors[i].getHex());
		$("#"+validVal).spectrum({
			localStorageKey: 'key',
			color: colors[i].getHex(),
			showInitial: true,
			showInput: true,
			change:
				function(color) {
					$(this).css('backgroundColor', color.toHexString());
					var c = color.toHexString();
					if(c.length == 4){
						c = "#"+c.charAt(1)+c.charAt(1)+c.charAt(2)+c.charAt(2)+c.charAt(3)+c.charAt(3);
					}
					colorChanged($(this).attr('name'), c);
				}
		});
	}

	setKey(vals, colors);
}

/*This function is called when a new value is selected in the showBy menu*/
function showByMenuChanged() {
	g_categoryName = document.getElementById('showbycombo')[document.getElementById('showbycombo').selectedIndex].value;
	var index = g_mappingFileHeaders.indexOf(g_categoryName);
	var vals = [];

	for(var i in g_plotIds){
		var sid = g_plotIds[i];
		var divid = sid.replace(/\./g,'');
		// get all of the values for the selected category
		vals.push(g_mappingFileData[sid][index]);
		// set everything to visible
		try {
			g_elementsGroup.add(g_plotEllipses[sid])
		}
		catch(TypeError){}
		try {
			g_elementsGroup.add(g_plotSpheres[sid])
		}
		catch(TypeError){}
		$('#'+divid+"_label").css('display','block');
	}

	g_visiblePoints = g_plotIds.length
	changePointCount()

	vals = dedupe(vals).sort();

	// build the showby checkbox table in HTML
	var lines = "<form name=\"showbyform\"><table>"
	for(var i in vals){
		lines += "<tr><td>";
		lines +="<input name=\""+vals[i]+"_show\" value=\""+vals[i]+"\" type=\"checkbox\" checked=\"yes\" onClick=\"toggleVisible(\'"+vals[i]+"\')\">";
		lines +="</input></td><td title=\""+vals[i]+"\">";
		if(vals[i].length > 25){
			lines+= vals[i].substring(0,25) + "..."
		}
		else{
			lines += vals[i];
		}
		lines +="</td></tr>";
	}
	lines += "</table></form>";
	document.getElementById("showbylist").innerHTML = lines;
}

/*Toggle plot items by category selected in showby menu*/
function toggleVisible(value) {

	var hidden = !document.showbyform.elements[value+'_show'].checked;
	g_categoryName = document.getElementById('showbycombo')[document.getElementById('showbycombo').selectedIndex].value;

	//change visibility of points depending on metadata category
	for(var i in g_plotIds){
	var sid = g_plotIds[i];
	var divid = sid.replace(/\./g,'');
	var mappingVal = g_mappingFileData[sid][g_mappingFileHeaders.indexOf(g_categoryName)]
		if(mappingVal == value && hidden){
			try{
				g_elementsGroup.remove(g_plotEllipses[sid])
			}
			catch(TypeError){}
			try{
				g_elementsGroup.remove(g_plotSpheres[sid])
				g_visiblePoints--
			}
			catch(TypeError){}
			$('#'+divid+"_label").css('display','none');
		}
		else if(mappingVal == value && !hidden)
		{
			try {
				g_elementsGroup.add(g_plotEllipses[sid])
			}
			catch(TypeError){}
			try {
				g_elementsGroup.add(g_plotSpheres[sid])
				g_visiblePoints++
			}
			catch(TypeError){}
			$('#'+divid+"_label").css('display','block');
		}
	}
	changePointCount()

}

/*Build the plot legend in HTML*/
function setKey(values, colors) {
	if(g_keyBuilt){
		for(var i = 0; i < values.length; i++){
			colorChanged(values[i], '#'+colors[i].getHex());
		}
	}
	else {
		var keyHTML = "<table class=\"key\">";
		for(var i in g_plotIds){
			var sid = g_plotIds[i];
			var divid = sid.replace(/\./g,'')+"_key";
			var catValue = g_mappingFileData[sid][g_categoryIndex];
			var catColor = colors[values.indexOf(catValue)];
			keyHTML += "<tr id=\""+divid+"row\"><td><div id=\""+divid+"\" name=\""+sid+"\" class=\"colorbox\" style=\"background-color:#";
			keyHTML += catColor.getHex();
			keyHTML += ";\"></div>";
			keyHTML +="</td><td>";
			keyHTML += sid;
			keyHTML += "</td></tr>";

			try {
				g_plotEllipses[g_plotIds[i]].material.color.setHex("0x"+catColor.getHex());
			}
			catch(TypeError){}
			try {
				g_plotSpheres[g_plotIds[i]].material.color.setHex("0x"+catColor.getHex());
			}
			catch(TypeError){}
		}
		keyHTML += "</table>";
		document.getElementById("key").innerHTML = keyHTML;

		for(var i in g_plotIds){
			var sid = g_plotIds[i];
			var divid = sid.replace(/\./g,'')+"_key";
			$('#'+divid).attr('name',sid);
			$('#'+divid).dblclick(function () {
			toggleFinder($(this), $(this).attr('name'));
			});
		}
		g_keyBuilt = true;
	}
}

/*Toggle an arrow to locate a sample by double clicking the box @ the key menu*/
function toggleFinder(div, divName) {
	if(g_foundId != divName) {
		$('.colorbox').css('border','1px solid black');
		div.css('border','1px solid white');
		$('#finder').css('opacity',1);
		var coords = toScreenXY(g_plotSpheres[divName].position, g_sceneCamera, $('#main_plot'));
		$('#finder').css('left',coords['x']-15);
		$('#finder').css('top',coords['y']-5);
		g_foundId = divName;
	}
	else {
		if($('#finder').css('opacity') == 1) {
			$('#finder').css('opacity',0);
			div.css('border','1px solid black');
			g_foundId = null
		}
		else {
			$('#finder').css('opacity',1);
			div.css('border','1px solid white');
		}
	}
}

/*Callback for the colorChanged event as triggered by the color picker*/
function colorChanged(catValue,color) {
	for(var i in g_plotIds)
	{
		var sid = g_plotIds[i]
		if(g_mappingFileData[g_plotIds[i]][g_categoryIndex] == catValue)
		{
			// get the valid divId for the key and set its color
			$("#"+sid.replace(/\./g,'')+"_key").css('backgroundColor',color);
			// set the color of the corresponding sphere and ellipse 
			try {
				g_plotEllipses[sid].material.color.setHex(color.replace('#','0x'));
			}
			catch(TypeError){}
			try {
				g_plotSpheres[sid].material.color.setHex(color.replace('#','0x'));
			}
			catch(TypeError){}
		}
	}
}

/*This function is called when a new value is selected in the label menu*/
function labelMenuChanged() {
	if(document.getElementById('labelcombo').selectedIndex == 0){
		document.getElementById("labellist").innerHTML = "";
		return;
	}

	// set the new current category and index
	var labelCategory = document.getElementById('labelcombo')[document.getElementById('labelcombo').selectedIndex].value;
	var labelCatIndex = g_mappingFileHeaders.indexOf(labelCategory);

	// get all values of this category from the mapping
	var vals = [];
	for(var i in g_plotIds){
		vals.push(g_mappingFileData[g_plotIds[i]][labelCatIndex]);
	}

	vals = dedupe(vals).sort();
	colors = getColorList(vals);

	// build the label table in HTML
	var lines = "<form name=\"labels\" id=\"labelForm\"><table>";
	for(var i in vals){
		// html classes have a special meaning for '.' and spaces, must remove them
		// as well as special chars
		var validVal = vals[i].replace(/[\. :!@#$%^&*()]/g,'');

		// set the div id, checkbox name so that we can reference this later
		lines += "<tr><td><input name=\""+vals[i]+"\" type=\"checkbox\" checked=\"true\" onClick=\"toggleLabels()\" ></input></td><td><div id=\""+validVal+"Label\" class=\"colorbox\" name=\""+vals[i]+"\"></div></td><td title=\""+vals[i]+"\">";

		if(vals[i].length > 25){
			lines+= vals[i].substring(0,25) + "..."
		}
		else{
			lines += vals[i];
		}

		lines+= "</td></tr>";
	}

	lines += "</table></form>";
	document.getElementById("labellist").innerHTML = lines;

	for(var i in vals){
		var validVal = vals[i].replace(/[\. :!@#$%^&*()]/g,'');
		// get the div built earlier and turn it into a color picker
		$('#'+validVal+'Label').css('backgroundColor',"#"+colors[i].getHex());
		labelColorChanged(vals[i], "#"+colors[i].getHex());

		$("#"+validVal+'Label').spectrum({
			color: colors[i].getHex(),
			showInitial: true,
			showPalette: true,
			palette: [['red', 'green', 'blue']],
			change:
				function(color) {
					$(this).css('backgroundColor', color.toHexString());
					labelColorChanged($(this).attr('name'), color.toHexString());
				}
		});
	}
}

/*This function is called when a label color is changed*/
function labelColorChanged(value, color) {
	g_categoryName = document.getElementById('labelcombo')[document.getElementById('labelcombo').selectedIndex].value;
	value = value.replace('_','');

	for(var i in g_plotIds){
		var sid = g_plotIds[i];
		var divid = sid.replace(/\./g,'');
		if(g_mappingFileData[sid][g_mappingFileHeaders.indexOf(g_categoryName)] == value){
			$('#'+divid+"_label").css('color', color);
		}
	}
}

/*This function turns the labels on and off*/
function toggleLabels() {
	if(document.plotoptions.elements[0].checked){
		$('#labelForm').css('display','block');
		$('#labels').css('display','block');
		$('#labels').css('display','block');
		$("#lopacityslider").slider('enable');
		$("#labelColor").spectrum('enable');
		document.getElementById('labelcombo').disabled = false;

		if(document.labels == null){
			return;
		}

		g_categoryName = document.getElementById('labelcombo')[document.getElementById('labelcombo').selectedIndex].value;
		for(var i = 0; i < document.labels.elements.length; i++){
			var hidden = !document.labels.elements[i].checked;
			var value = document.labels.elements[i].name;

			for(var j in g_plotIds){
				var sid = g_plotIds[j];
				var divid = sid.replace(/\./g,'');

				if(g_mappingFileData[sid][g_mappingFileHeaders.indexOf(g_categoryName)] == value && hidden){
					$('#'+divid+"_label").css('display', 'none');
				}
				else if(g_mappingFileData[sid][g_mappingFileHeaders.indexOf(g_categoryName)] == value && !hidden){
					$('#'+divid+"_label").css('display', 'block');
				}
			}
		}
	}
	else{
		$('#labels').css('display','none');
	}
}

/*This function finds the screen coordinates of any position in the current plot.

  The main purpose of this function is to be used for calculating the placement
  of the labels.
*/
function toScreenXY( position, camera, jqdiv ) {

	var pos = position.clone();
	projScreenMat = new THREE.Matrix4();
	projScreenMat.multiply( camera.projectionMatrix, camera.matrixWorldInverse );
	projScreenMat.multiplyVector3( pos );

	return { x: ( pos.x + 1 ) * jqdiv.width() / 2 + jqdiv.offset().left,
		y: ( - pos.y + 1 ) * jqdiv.height() / 2 + jqdiv.offset().top };
}

/*This function is used to filter the key to a user's provided search string*/
function filterKey() {
	var searchVal = document.keyFilter.filterBox.value.toLowerCase();

	for(var i in g_plotIds){
		var sid = g_plotIds[i];
		var divid = sid.replace(/\./g,'')+"_keyrow";

		if(sid.toLowerCase().indexOf(searchVal) != -1){
			$('#'+divid).css('display','block');
		}
		else{
			$('#'+divid).css('display','none');
		}
	}
}

/*This function handles events from the ellipse opacity slider*/
function ellipseOpacityChange(ui) {
	document.getElementById('ellipseopacity').innerHTML = ui.value + "%";
	ellipseOpacity = ui.value/100;

	for(var sid in g_plotEllipses){
		g_plotEllipses[sid].material.opacity = ellipseOpacity;
	}
}

/*This function handles events from the sphere opacity slider*/
function sphereOpacityChange(ui) {
	document.getElementById('sphereopacity').innerHTML = ui.value + "%";
	sphereOpacity = ui.value/100;

	for(var sid in g_plotSpheres){
		g_plotSpheres[sid].material.opacity = sphereOpacity;
	}
}

/*This function handles events from the label opacity slider*/
function labelOpacityChange(ui) {
	document.getElementById('labelopacity').innerHTML = ui.value + "%";
	labelOpacity = ui.value/100;

	$('#labels').css('opacity', labelOpacity);
}

/*This function handles events from the sphere radius slider

  Note that this function will get a scaling value added depending on whether or
  not the plot being displayed is scaled by the percent explained in each axis.
*/
function sphereRadiusChange(ui) {
	document.getElementById('sphereradius').innerHTML = ui.value/5;
	var scale = (ui.value/5.0)*g_sphereScaler;

	// set the value to all the spheres
	for(var sample_id in g_plotSpheres){
		g_plotSpheres[sample_id].scale.set(scale, scale, scale);
	}
}

/*Setup the interface elements required for the sidebar of the main interface*/
function setJqueryUi() {
	$("#menutabs").tabs();
	$("#labelColor").css('backgroundColor', '#fff');

	$("#labelColor").spectrum({
		color: '#fff',
		showInitial: true,
		showPalette: true,
		palette: [['black', 'red', 'green', 'blue']],
		change:
			function(color) {
				$(this).css('backgroundColor', color.toHexString());
				$('#labels').css('color', color.toHexString());
				for(var i in g_plotIds){
					var sid = g_plotIds[i];
					var divid = sid.replace(/\./g,'');
					$('#'+divid+"_label").css('color', color.toHexString());
				}
				document.getElementById('labelcombo').selectedIndex = 0;
				labelMenuChanged();
			}
	});

	$("#eopacityslider").slider({
		range: "max",
		min: 0,
		max: 100,
		value: 20,
		slide: function( event, ui ) {
			ellipseOpacityChange(ui);
		},
		change: function( event, ui ) {
			ellipseOpacityChange(ui);
		}
	});
	document.getElementById('ellipseopacity').innerHTML = $( "#eopacityslider" ).slider( "value")+"%";

	$("#sopacityslider").slider({
		range: "max",
		min: 0,
		max: 100,
		value: 100,
		slide: function( event, ui ) {
			sphereOpacityChange(ui);
		},
		change: function( event, ui ) {
			sphereOpacityChange(ui);
		}
	});
	document.getElementById('sphereopacity').innerHTML = $( "#sopacityslider" ).slider( "value")+"%";

	$("#sradiusslider" ).slider({
		range: "max",
		min: 1,
		max: 20,
		value: 5,
		slide: function( event, ui ) {
			sphereRadiusChange(ui);
		},
		change: function( event, ui ) {
			sphereRadiusChange(ui);
		}
	});
	document.getElementById('sphereradius').innerHTML = $( "#sradiusslider" ).slider( "value")/5;

	$("#lopacityslider").slider({
		range: "max",
		min: 0,
		max: 100,
		value: 100,
		slide: function( event, ui ) {
			labelOpacityChange(ui);
		},
		change: function( event, ui ) {
			labelOpacityChange(ui);
		}
	});
	document.getElementById('labelopacity').innerHTML = $( "#lopacityslider" ).slider( "value")+"%"
}

/*Draw the ellipses in the plot as described by the g_ellipsesDimensions array

  Note that this is a function that won't always get executed since this should
  only happen when plotting a jaccknifed principal coordinates analysis
*/
function drawEllipses() {
	for(var sid in g_ellipsesDimensions) {
		//draw ellipsoid
		var emesh = new THREE.Mesh( g_genericSphere,new THREE.MeshLambertMaterial() );
		emesh.scale.x = g_ellipsesDimensions[sid]['width']/g_radius;
		emesh.scale.y = g_ellipsesDimensions[sid]['height']/g_radius;
		emesh.scale.z = g_ellipsesDimensions[sid]['length']/g_radius;
		emesh.position.set(g_ellipsesDimensions[sid]['x'],g_ellipsesDimensions[sid]['y'] ,g_ellipsesDimensions[sid]['z'] );
		emesh.material.color = new THREE.Color()
		emesh.material.transparent = true;
		emesh.material.opacity = 0.2;
		emesh.updateMatrix();
		emesh.matrixAutoUpdate = true;
		if(g_mappingFileData[sid] != undefined){
			g_elementsGroup.add( emesh );
			g_plotEllipses[sid] = emesh;
		}
	}
}

/*Draw the spheres in the plot as described by the g_spherePositions array*/
function drawSpheres() {
	for(var sid in g_spherePositions){
		//draw ball
		var mesh = new THREE.Mesh( g_genericSphere, new THREE.MeshLambertMaterial() );
		mesh.material.color = new THREE.Color()
		mesh.material.transparent = false;
		mesh.material.opacity = 1;
		mesh.position.set(g_spherePositions[sid]['x'], g_spherePositions[sid]['y'], g_spherePositions[sid]['z']);
		mesh.updateMatrix();
		mesh.matrixAutoUpdate = true;
		if(g_mappingFileData[sid] != undefined){
			g_elementsGroup.add( mesh );
			g_plotSpheres[sid] = mesh;
			g_plotIds.push(sid);
		}
	}
}

function saveSVG(){
	open("data:image/svg+xml," + encodeURIComponent(document.getElementById('main_plot').innerHTML));
}
function SVGSaved(response){
	var fileName = eval('('+response+')')
	var dlwin = open('','Download SVG', 'width=400,height=50')

	dlwin.document.open();
	dlwin.document.write('<HTML><HEAD><meta name="content-disposition" content="inline; filename=\''+fileName+'\'">');
	dlwin.document.write('</HEAD><BODY>');
	dlwin.document.write('<a href=\''+fileName+'\'>'+fileName+'</a>')
	dlwin.document.write('</BODY></HTML>');
	dlwin.document.close();
	console.log(fileName)
}

/*Draw each of the lines that represent the X, Y and Z axes in the plot

  The length of each of these axes depend on the ranges that the data being
  displayed uses.
*/
var drawAxisLines = function(axisLength, xstart, ystart, zstart){
	//Shorten the vertex function
	function v(x,y,z){
			return new THREE.Vertex(new THREE.Vector3(x,y,z));
	}

	//Create axis (point1, point2, colour)
	function createAxis(p1, p2, color){
			var line, lineGeometry = new THREE.Geometry(),
			lineMat = new THREE.LineBasicMaterial({color: color, lineWidth: 1});
			lineMat.matrixAutoUpdate = true;
			lineGeometry.vertices.push(p1, p2);
			line = new THREE.Line(lineGeometry, lineMat);
			g_mainScene.add(line);

			return line;
	}

	g_xAxisLine = createAxis(v(xstart, ystart, zstart), v(axisLength, ystart, zstart), 0xFF0000);
	g_yAxisLine = createAxis(v(xstart, ystart, zstart), v(xstart, axisLength, zstart), 0x00FF00);
	g_zAxisLine = createAxis(v(xstart, ystart, zstart), v(xstart, ystart, axisLength), 0x0000FF);
};

/* update point count label */
function changePointCount() {
	document.getElementById('pointCount').innerHTML = g_visiblePoints+'/'+g_plotIds.length+' points'
}

/*Setup and initialization function for the whole system

  This function will set all of the WebGL elements that are required to exist
  for the plot to work properly. This in turn will draw the ellipses, spheres
  and all the other elements that could be part of a plot.
*/
$(document).ready(function() {
	setJqueryUi()

	// Detecting that webgl is activated
	if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

	var main_plot = $('#main_plot');
	var renderer, particles, geometry, parameters, i, h, color;
	var mouseX = 0, mouseY = 0;

	var winWidth = Math.min(document.getElementById('main_plot').offsetWidth,document.getElementById('main_plot').offsetHeight), view_angle = 35, view_near = 0.1, view_far = 10000;
	var winAspect = document.getElementById('main_plot').offsetWidth/document.getElementById('main_plot').offsetHeight;

	$(window).resize(function() {
		winWidth = Math.min(document.getElementById('main_plot').offsetWidth,document.getElementById('main_plot').offsetHeight);
		winAspect = document.getElementById('main_plot').offsetWidth/document.getElementById('main_plot').offsetHeight;
		g_sceneCamera.aspect = winAspect;
		g_sceneCamera.updateProjectionMatrix();
	});

	init();
	animate();

	function init() {
		g_sceneCamera = new THREE.PerspectiveCamera(view_angle, winAspect, view_near, view_far);

		$('#main_plot canvas').attr('width',document.getElementById('main_plot').offsetWidth);
		$('#main_plot canvas').attr('height',document.getElementById('main_plot').offsetHeight);

		g_mainScene = new THREE.Scene();
		g_mainScene.fog = new THREE.FogExp2( 0x000000, 0.0009);

		g_genericSphere = new THREE.SphereGeometry(g_radius, g_segments, g_rings);

		g_sceneCamera.position.x = g_sceneCamera.position.y = 0;
		g_sceneCamera.position.z = g_maximum * 4;
		g_mainScene.add(g_sceneCamera);


		g_elementsGroup = new THREE.Object3D();
		g_mainScene.add(g_elementsGroup);
		drawEllipses()
		drawSpheres()

		// set some of the scene properties
		g_plotIds = g_plotIds.sort();
		g_visiblePoints = g_plotIds.length;
		changePointCount(g_visiblePoints)

		// build the colorby and showby menus
		var line = "";
		$("#labelcombo").append("<option>Select A Category...</option>");

		for(var i in g_mappingFileHeaders){
			var temp = [];
			for(var j in g_plotIds) {
				if(g_mappingFileData[g_plotIds[j]] == undefined){
					console.log(g_plotIds[j] +" not in mapping")
					continue
				}
				temp.push(g_mappingFileData[g_plotIds[j]][i])
			}
			temp = dedupe(temp);

			line = "<option value=\""+g_mappingFileHeaders[i]+"\">"+g_mappingFileHeaders[i]+"</option>"
			$("#colorbycombo").append(line);
			$("#showbycombo").append(line);
			$("#labelcombo").append(line);
		}

		var rv = colorByMenuChanged();
		showByMenuChanged();

		var axesLen = Math.max(g_xMaximumValue+Math.abs(g_xMinimumValue),g_yMaximumValue+Math.abs(g_yMinimumValue),g_zMaximumValue+Math.abs(g_zMinimumValue));
		drawAxisLines(axesLen, g_xMinimumValue, g_yMinimumValue, g_zMinimumValue);
		buildAxisLabels()

		// the light is attached to the camera to provide a 3d perspective
		g_sceneLight = new THREE.DirectionalLight(0x999999, 2);
		g_sceneLight.position.set(1,1,1).normalize();
		g_sceneCamera.add(g_sceneLight);

		// Adding camera
		controls = new THREE.TrackballControls(g_sceneCamera, document.getElementById('main_plot'));
		controls.rotateSpeed = 1.0;
		controls.zoomSpeed = 1.2;
		controls.panSpeed = 0.8;
		controls.noZoom = false;
		controls.noPan = false;
		controls.staticMoving = true;
		controls.dynamicDampingFactor = 0.3;
		controls.keys = [ 65, 83, 68 ];

		// renderer
		renderer = new THREE.WebGLRenderer({ antialias: true });
		renderer.setClearColorHex( 0x333333, 1 );
		renderer.setSize( document.getElementById('main_plot').offsetWidth, document.getElementById('main_plot').offsetHeight );
		renderer.sortObjects = false;
		main_plot.append( renderer.domElement );

		// build divs to hold point labels and position them
		var labelshtml = "";
		for(var i in g_plotIds) {
			var sid = g_plotIds[i];
			var divid = sid.replace(/\./g,'');
			mesh = g_plotSpheres[sid];
			var coords = toScreenXY(mesh.position,g_sceneCamera,$('#main_plot'));
			labelshtml += "<label id=\""+divid+"_label\" class=\"unselectable labels\" style=\"position:absolute; left:"+parseInt(coords['x'])+"px; top:"+parseInt(coords['y'])+"px;\">";
			labelshtml += sid;
			labelshtml += "</label>";
		}
		document.getElementById("labels").innerHTML = labelshtml;
	}

	function buildAxisLabels() {
		//build axis labels
		var axesLen = Math.max(g_xMaximumValue+Math.abs(g_xMinimumValue),g_yMaximumValue+Math.abs(g_yMinimumValue),g_zMaximumValue+Math.abs(g_zMinimumValue));
		var axislabelhtml = "";

		var xcoords = toScreenXY(new THREE.Vector3(axesLen, g_yMinimumValue, g_zMinimumValue),g_sceneCamera,$('#main_plot'));
		axislabelhtml += "<label id=\"pc1_label\" class=\"unselectable labels\" style=\"position:absolute; left:"+parseInt(xcoords['x'])+"px; top:"+parseInt(xcoords['y'])+"px;\">";
		axislabelhtml += g_pc1Label;
		axislabelhtml += "</label>";
		var ycoords = toScreenXY(new THREE.Vector3(g_xMinimumValue, axesLen, g_zMinimumValue),g_sceneCamera,$('#main_plot'));
		axislabelhtml += "<label id=\"pc2_label\" class=\"unselectable labels\" style=\"position:absolute; left:"+parseInt(ycoords['x'])+"px; top:"+parseInt(ycoords['y'])+"px;\">";
		axislabelhtml += g_pc2Label;
		axislabelhtml += "</label>";
		var zcoords = toScreenXY(new THREE.Vector3(g_xMinimumValue, g_yMinimumValue, axesLen),g_sceneCamera,$('#main_plot'));
		axislabelhtml += "<label id=\"pc3_label\" class=\"unselectable labels\" style=\"position:absolute; left:"+parseInt(zcoords['x'])+"px; top:"+parseInt(zcoords['y'])+"px;\">";
		axislabelhtml += g_pc3Label;
		axislabelhtml += "</label>";
		document.getElementById("axislabels").innerHTML = axislabelhtml;
	}

	function animate() {
		requestAnimationFrame( animate );

		render();
		buildAxisLabels();
		// move labels when the plot is moved
		if(document.plotoptions.elements[0].checked){
			for(var i in g_plotIds) {
				var sid = g_plotIds[i];
				mesh = g_plotSpheres[sid];
				var coords = toScreenXY(mesh.position, g_sceneCamera, $('#main_plot'));
				var divid = sid.replace(/\./g,'');
				$('#'+divid+"_label").css('left',coords['x']);
				$('#'+divid+"_label").css('top',coords['y']);
			}
		}
		if(g_foundId) {
			var coords = toScreenXY(g_plotSpheres[g_foundId].position, g_sceneCamera, $('#main_plot'));
			$('#finder').css('left',coords['x']-15);
			$('#finder').css('top',coords['y']-5);
		}
	}
   
	function render() {
		controls.update();
		renderer.setSize( document.getElementById('main_plot').offsetWidth, document.getElementById('main_plot').offsetHeight );
		renderer.render( g_mainScene, g_sceneCamera);
	}
});