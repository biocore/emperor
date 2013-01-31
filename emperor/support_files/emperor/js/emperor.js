/*
 * __author__ = "Meg Pirrung"
 * __copyright__ = "Copyright 2012, E-vident"
 * __credits__ = ["Meg Pirrung, Antonio Gonzalez Pena"]
 * __license__ = "GPL"
 * __version__ = "0.01-dev"
 * __maintainer__ = "Meg Pirrung"
 * __email__ = "meganap@gmail.com"
 * __status__ = "Development"
 */

var headers = [];		//headers of the mapping file
var mapping = {};		//mapping dictionary
var plotIds = [];		//IDs of all items that are plotted
var plotSpheres = {};	//all spheres that are plotted
var ellipses;
var plotEllipses = {};	//all ellipses that are plotted
var pc1; //label for pc1
var pc2; //label for pc2
var pc3; //label for pc3
var ellipseOpacity = .2;
var sphereOpacity = 1.0;
var sphereScale;
var sphere;         //generic sphere used for plots
var particle;       //generic particle use for plots
var scene;          //scene that holds the plot
var group;          //group that holds the plotted shapes
var camera;			//plot camera
var max; 			//maximum value of a plot, used for camera placement
var category = "";	//current coloring category
var catIndex = 0;	//current coloring category index
var foundId = "";   //id of currently located point
var keyBuilt = false;
var animationSpeed = 60;
var time;
var visiblePoints = 0;


/* This function recenters the camera, needs to be fixed so that it
actually resets to the original position */
function resetCamera() {
	 camera.aspect = document.getElementById('main_plot').offsetWidth/document.getElementById('main_plot').offsetHeight;
     camera.position.set( 0, 0, max*4); 
	 camera.rotation.set( 0, 0, 0 );
	camera.updateProjectionMatrix();
}

/* Removes duplicates from a list */
function dedupe(list) {
   var set = {};
   for (var i = 0; i < list.length; i++)
	  set[list[i]] = true;
   list = [];
   for (var obj in set)
	  list.push(obj);
   return list;
}

/* generates a list of colors that corresponds to a list of values
if the values are continuous the colors correspond to their numeric
value, if values are discreet it is just a gradient with an even
step size in between each value */
function getColorList(vals) {
    var colorVals = [];
	var isNumeric = true;
	
	//figure out if the values are continuous or not
	for(var i = 0; i < vals.length; i++)
	{
		if(isNaN(parseFloat(vals[i])))
			isNumeric = false;
		else
			colorVals[i] = parseFloat(vals[i]);
	}
	
	// figure out start and max values, list is sorted
	var start = colorVals[0];
	var max = colorVals[colorVals.length-1]-colorVals[0];

	var colors = [];
	
	// set the colors for each category value
	if(vals.length == 1)
	{
		colors[0] = new THREE.Color();
		colors[0].setHex("0xff0000");
	}
	else if (vals.length == 2) {
		colors[0] = new THREE.Color();
		colors[0].setHex("0xff0000");
		colors[1] = new THREE.Color();
		colors[1].setHex("0x0000ff");
	}
	else if (vals.length == 3 && !isNumeric) {
		for(var i in vals)
		{
			colors[i] = new THREE.Color();
			colors[i].setHSV(i/vals.length,1,1);
		}
	}
	else {
		if(isNumeric) {
			for(var i in vals)
			{
				colors[i] = new THREE.Color();
				// i*.66 makes it so the gradient goes red->green->blue instead of
				// back around to red
				colors[i].setHSV((colorVals[i]-start)*.66/max,1,1);
			}
		}else {
			for(var i in vals)
			{
				colors[i] = new THREE.Color();
				// i*.66 makes it so the gradient goes red->green->blue instead of
				// back around to red
				colors[i].setHSV(i*.66/vals.length,1,1);
			}
		}
		
	}
	return colors;
}

/* timers for debugging */
function startTimer() {
    var d=new Date()
    time = d.getTime();
}

/* timers for debugging */
function stopTimer(info) {
    var d=new Date()
    time = d.getTime() - time;
    console.log("time to " +info +":"+time+"ms")
}

/* This function is called when a new value is selected in the colorBy menu */
function colorByMenuChanged() {
	// set the new current category and index
	category = document.getElementById('colorbycombo')[document.getElementById('colorbycombo').selectedIndex].value;
	catIndex = headers.indexOf(category);
	
	// get all values of this category from the mapping
	var vals = [];
	for(var i in plotIds){
		vals.push(mapping[plotIds[i]][catIndex]);
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
		
		if(vals[i].length > 25)
			lines+= vals[i].substring(0,25) + "..."
		else
			lines += vals[i];
			
		lines+= "</td></tr>";
	}
	lines += "</table>";
	document.getElementById("colorbylist").innerHTML = lines;

    // startTimer()
	for(var i in vals){
		var validVal = vals[i].replace(/[\. :!@#$%^&*()]/g,'');
		// get the div built earlier and turn it into a color picker
		$('#'+validVal).css('backgroundColor',"#"+colors[i].getHex());
        $("#"+validVal).spectrum({
                                   localStorageKey: 'key',
                                   color: colors[i].getHex(),
                                   showInitial: true,
                                   showInput: true,
                                   change: function(color) {
                                    $(this).css('backgroundColor', color.toHexString());
                                   var c = color.toHexString();
                                   if(c.length == 4)
                                       c = "#"+c.charAt(1)+c.charAt(1)+c.charAt(2)+c.charAt(2)+c.charAt(3)+c.charAt(3);
                                    // startTimer()
                                    colorChanged($(this).attr('name'), c);
                                    // stopTimer('colorChanged')
                                   }
                               });
	}
    // stopTimer('set color box')
    setKey(vals, colors);
}

/* This function is called when a new value is selected in the showBy menu */
function showByMenuChanged() {
	var category = document.getElementById('showbycombo')[document.getElementById('showbycombo').selectedIndex].value;
	var index = headers.indexOf(category);
	var vals = [];
	
	for(var i in plotIds)
	{
	    var sid = plotIds[i];
	    var divid = sid.replace(/\./g,'');
	    // get all of the values for the selected category
	    vals.push(mapping[sid][index]);
	    // set everything to visible
	    try {
		    group.add(plotEllipses[sid])
		    }catch(TypeError){}
		    try {
		    group.add(plotSpheres[sid])
		    }catch(TypeError){}
		$('#'+divid+"_label").css('display','block');
	}
	
	visiblePoints = plotIds.length
	changePointCount()
	
	vals = dedupe(vals).sort();
	
	// build the showby checkbox table in HTML
	var lines = "<form name=\"showbyform\"><table>"
	for(var i in vals){
		lines += "<tr><td>";
		lines +="<input name=\""+vals[i]+"_show\" value=\""+vals[i]+"\" type=\"checkbox\" checked=\"yes\" onClick=\"toggleVisible(\'"+vals[i]+"\')\">";
		
		lines +="</input></td><td title=\""+vals[i]+"\">";
		if(vals[i].length > 25)
			lines+= vals[i].substring(0,25) + "..."
		else
			lines += vals[i];
		
		lines +="</td></tr>";
		}
	lines += "</table></form>";
	document.getElementById("showbylist").innerHTML = lines;
}

/* Toggle plot items by category selected in showby menu */
function toggleVisible(value) {
    // startTimer()
	var hidden = !document.showbyform.elements[value+'_show'].checked;
	
	var category = document.getElementById('showbycombo')[document.getElementById('showbycombo').selectedIndex].value;
    // value = value.replace('_','');
    // console.log(value)
    //change visibility of points depending on metadata category
	for(var i in plotIds)
	{
	var sid = plotIds[i];
	var divid = sid.replace(/\./g,'');
    var mappingVal = mapping[sid][headers.indexOf(category)]
		if(mappingVal == value && hidden)
		{
		    try{
		    group.remove(plotEllipses[sid])
		    }catch(TypeError){}
		    try{
		    group.remove(plotSpheres[sid])
		    visiblePoints--
		    }catch(TypeError){}
			$('#'+divid+"_label").css('display','none');
		}
		else if(mappingVal == value && !hidden)
		{
		    try {
		    group.add(plotEllipses[sid])
		    }catch(TypeError){}
		    try {
		    group.add(plotSpheres[sid])
		    visiblePoints++
		    }catch(TypeError){}
			$('#'+divid+"_label").css('display','block');
		}
	}
	changePointCount()
    // stopTimer('toggleVisibiity')
}

/* build the plot legend in HTML*/
function setKey(values, colors) {
	if(keyBuilt){
		for(var i = 0; i < values.length; i++)
			colorChanged(values[i], '#'+colors[i].getHex());
	} else {
		var keyHTML = "<table class=\"key\">";
		for(var i in plotIds)
		{
			var sid = plotIds[i];
			var divid = sid.replace(/\./g,'')+"_key";
			var catValue = mapping[sid][catIndex];
			var catColor = colors[values.indexOf(catValue)];
			keyHTML += "<tr id=\""+divid+"row\"><td><div id=\""+divid+"\" name=\""+sid+"\" class=\"colorbox\" style=\"background-color:#";
			keyHTML += catColor.getHex();
			keyHTML += ";\"></div>";
			keyHTML +="</td><td>";
			keyHTML += sid;
			keyHTML += "</td></tr>";
		
		    try {
			plotEllipses[plotIds[i]].material.color.setHex("0x"+catColor.getHex());
		    }catch(TypeError){}
		    try {
			plotSpheres[plotIds[i]].material.color.setHex("0x"+catColor.getHex());
			}catch(TypeError){}
		}
		keyHTML += "</table>";
        document.getElementById("key").innerHTML = keyHTML;
	
		for(var i in plotIds)
		{
			var sid = plotIds[i];
			var divid = sid.replace(/\./g,'')+"_key";
			$('#'+divid).attr('name',sid);
			$('#'+divid).dblclick(function () {
			toggleFinder($(this), $(this).attr('name'));
			});
		}
		keyBuilt = true;
	}	
}

/*toggles the little arrow used to locate a point by double clicking
its colorbox in the key */
function toggleFinder(div, divName) {
	if(foundId != divName) {
			$('.colorbox').css('border','1px solid black');
			div.css('border','1px solid white');
			$('#finder').css('opacity',1);
			var coords = toScreenXY(plotSpheres[divName].position, camera, $('#main_plot'));
			$('#finder').css('left',coords['x']-15);
			$('#finder').css('top',coords['y']-5);
			foundId = divName;
		}
		else {
		    if($('#finder').css('opacity') == 1) {
    			$('#finder').css('opacity',0);
    			div.css('border','1px solid black');
    			foundId = null
    		}
    		else {
    			$('#finder').css('opacity',1);
    			div.css('border','1px solid white');
    		}
		}
}

/* colorChanged event called by the colorpicker */
function colorChanged(catValue,color) {
	for(var i in plotIds)
	{
	    var sid = plotIds[i]
		if(mapping[plotIds[i]][catIndex] == catValue)
		{
			// get the valid divId for the key and set its color
			$("#"+sid.replace(/\./g,'')+"_key").css('backgroundColor',color);
			// set the color of the corresponding sphere and ellipse 
			try {
			plotEllipses[sid].material.color.setHex(color.replace('#','0x'));
		    }catch(TypeError){}
		    try {
			plotSpheres[sid].material.color.setHex(color.replace('#','0x'));
			}catch(TypeError){}
		}
	}
}

/* This function is called when a new value is selected in the label menu */
function labelMenuChanged() {
	if(document.getElementById('labelcombo').selectedIndex == 0)
	{
		document.getElementById("labellist").innerHTML = "";
		return;
	}

	// set the new current category and index
	var labelCategory = document.getElementById('labelcombo')[document.getElementById('labelcombo').selectedIndex].value;
	var labelCatIndex = headers.indexOf(labelCategory);
	
	// get all values of this category from the mapping
	var vals = [];
	for(var i in plotIds){
		vals.push(mapping[plotIds[i]][labelCatIndex]);
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
		
		if(vals[i].length > 25)
			lines+= vals[i].substring(0,25) + "..."
		else
			lines += vals[i];
			
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
                   palette: [
                       ['red', 'green', 'blue']
                   ],
                   change: function(color) {               
                    $(this).css('backgroundColor', color.toHexString());
                    labelColorChanged($(this).attr('name'), color.toHexString());
                   }
               });
	}
}

/* function called when a label color is changed */
function labelColorChanged(value, color) {
	var category = document.getElementById('labelcombo')[document.getElementById('labelcombo').selectedIndex].value;

	value = value.replace('_','');
	
	for(var i in plotIds)
	{
	var sid = plotIds[i];
	var divid = sid.replace(/\./g,'');
	if(mapping[sid][headers.indexOf(category)] == value)
		$('#'+divid+"_label").css('color', color);
	}
}

/* This function turns the labels on and off */
function toggleLabels() {	
	if(document.plotoptions.elements[0].checked)
	{
		$('#labelForm').css('display','block');
		$('#labels').css('display','block');
		$('#labels').css('display','block');
		$("#lopacityslider").slider('enable');
		$("#labelColor").spectrum('enable');
		document.getElementById('labelcombo').disabled = false;
		
		if(document.labels == null)
			return;
			
		var category = document.getElementById('labelcombo')[document.getElementById('labelcombo').selectedIndex].value;
		for(var i = 0; i < document.labels.elements.length; i++)
		{
			var hidden = !document.labels.elements[i].checked;
			var value = document.labels.elements[i].name;
			for(var j in plotIds)
			{
				var sid = plotIds[j];
				var divid = sid.replace(/\./g,'');
				
				if(mapping[sid][headers.indexOf(category)] == value && hidden)
					$('#'+divid+"_label").css('display', 'none');
				else if(mapping[sid][headers.indexOf(category)] == value && !hidden)
					$('#'+divid+"_label").css('display', 'block');	
			}
		}
	}
	else
	{
        // $('#labelForm').css('display','none');
        $('#labels').css('display','none');
        // $("#lopacityslider").slider('disable');
        // document.getElementById('labelcombo').disabled = true;
	}
}

/* This function finds the screen coordinates of any
 position in the current plot.
Used for calculating label placement */
function toScreenXY( position, camera, jqdiv ) {

    var pos = position.clone();
    projScreenMat = new THREE.Matrix4();
    projScreenMat.multiply( camera.projectionMatrix, camera.matrixWorldInverse );
    projScreenMat.multiplyVector3( pos );

		return { x: ( pos.x + 1 ) * jqdiv.width() / 2 + jqdiv.offset().left,
         y: ( - pos.y + 1 ) * jqdiv.height() / 2 + jqdiv.offset().top };
}

/* used to filter the key to a user's provided search string */
function filterKey() {
	var searchVal = document.keyFilter.filterBox.value.toLowerCase();
	for(var i in plotIds)
	{
		var sid = plotIds[i];
		var divid = sid.replace(/\./g,'')+"_keyrow";
		if(sid.toLowerCase().indexOf(searchVal) != -1)
			$('#'+divid).css('display','block');
		else
			$('#'+divid).css('display','none');
	}
}

/* handle events from the ellipse opacity slider */
function eopacitychange(ui) {
	document.getElementById('ellipseopacity').innerHTML = ui.value + "%";
	ellipseOpacity = ui.value/100;
	
	for(var sid in plotEllipses)
		plotEllipses[sid].material.opacity = ellipseOpacity;
}

/* handle events from the sphere opacity slider */
function sopacitychange(ui) {
	document.getElementById('sphereopacity').innerHTML = ui.value + "%";
	sphereOpacity = ui.value/100;
	
	for(var sid in plotSpheres)
		plotSpheres[sid].material.opacity = sphereOpacity;
}

/* handle events from the label opacity slider */
function lopacitychange(ui) {
	document.getElementById('labelopacity').innerHTML = ui.value + "%";
	labelOpacity = ui.value/100;
	
	$('#labels').css('opacity', labelOpacity);
}

/* handle events from the sphere radius slider */
function sradiuschange(ui) {
	document.getElementById('sphereradius').innerHTML = ui.value/5;
	var scale = ui.value/5.0;
	sphereScale = new THREE.Vector3(scale,scale,scale)
	
	for(var sid in plotSpheres)
		plotSpheres[sid].scale = sphereScale;
	
	for(var sid in plotEllipses)
	{
		plotEllipses[sid].scale.x = scale*ellipses[sid]['width']/radius;
	    plotEllipses[sid].scale.y = scale*ellipses[sid]['height']/radius;
	    plotEllipses[sid].scale.z = scale*ellipses[sid]['length']/radius;
	}
}

// function animSpeedChange(ui) {
//     document.getElementById('animationspeed').innerHTML = ui.value + "fps";
//     animationSpeed = ui.value
//     console.log('Animation speed: '+animationSpeed)
// }

// function animationMenuChanged() {
//     // console.log('animationMenuChanged')
//     var animationCategory = document.getElementById('animationcombo')[document.getElementById('animationcombo').selectedIndex].value;
//  var index = headers.indexOf(animationCategory);
//  var vals = [];
//  
//  // get all of the values for the selected category
//  for(var i in plotIds){
//      vals.push(mapping[plotIds[i]][index]);
//  }
//  
//  vals = dedupe(vals).sort();
//  
//  // build the showby checkbox table in HTML
//  var lines = "<form name=\"animationform\"><table>"
//  for(var i in vals){
//      lines += "<tr><td>";
//      lines +="<input name=\""+vals[i]+"_\" value=\""+vals[i]+"\" type=\"checkbox\" checked=\"yes\">";
//      
//      lines +="</input></td><td title=\""+vals[i]+"\">";
//      if(vals[i].length > 25)
//          lines+= vals[i].substring(0,25) + "..."
//      else
//          lines += vals[i];
//      
//      lines +="</td></tr>";
//      }
//  lines += "</table></form>";
//  document.getElementById("animationlist").innerHTML = lines;
// }
// 
// function animationOverMenuChanged() {
//     var animateOverCategory = document.getElementById('animationovercombo')[document.getElementById('animationovercombo').selectedIndex].value;
//     console.log('animationOverMenuChanged:'+animateOverCategory)
// }

// function resetAnimation() {
//     console.log('resetAnimation')
// }
// 
// function playAnimation() {
//     console.log('playAnimation')
// }
// 
// function pauseAnimation() {
//     console.log('pauseAnimation')
// }

function setJqueryUi() {
    $("#menutabs").tabs();
	
	$("#labelColor").css('backgroundColor', '#fff');
	
	$("#labelColor").spectrum({
			color: '#fff',
			showInitial: true,
			showPalette: true,
			palette: [
				['black', 'red', 'green', 'blue']
			],
			change: function(color) {
		   	 $(this).css('backgroundColor', color.toHexString());
			 $('#labels').css('color', color.toHexString());
			for(var i in plotIds)
			{
				var sid = plotIds[i];
				var divid = sid.replace(/\./g,'');
				$('#'+divid+"_label").css('color', color.toHexString());
			}
			document.getElementById('labelcombo').selectedIndex = 0;
			labelMenuChanged();
			}
		});
	
	$( "#eopacityslider" ).slider({
		range: "max",
		min: 0,
		max: 100,
		value: 20,
		slide: function( event, ui ) {
		    eopacitychange(ui);
		},
		change: function( event, ui ) {
		    eopacitychange(ui);
		}
	});
	document.getElementById('ellipseopacity').innerHTML = $( "#eopacityslider" ).slider( "value")+"%";
	
	$( "#sopacityslider" ).slider({
		range: "max",
		min: 0,
		max: 100,
		value: 100,
		slide: function( event, ui ) {
		    sopacitychange(ui);
		},
		change: function( event, ui ) {
		    sopacitychange(ui);
		}
	});
	document.getElementById('sphereopacity').innerHTML = $( "#sopacityslider" ).slider( "value")+"%";
	
	$( "#sradiusslider" ).slider({
		range: "max",
		min: 1,
		max: 20,
		value: 5,
		slide: function( event, ui ) {
		    sradiuschange(ui);
		},
		change: function( event, ui ) {
		    sradiuschange(ui);
		}
	});
	document.getElementById('sphereradius').innerHTML = $( "#sradiusslider" ).slider( "value")/5;
	
	$( "#lopacityslider" ).slider({
		range: "max",
		min: 0,
		max: 100,
		value: 100,
		slide: function( event, ui ) {
		    lopacitychange(ui);
		},
		change: function( event, ui ) {
		    lopacitychange(ui);
		}
	});
	document.getElementById('labelopacity').innerHTML = $( "#lopacityslider" ).slider( "value")+"%"
	
    // $( "#animspeedslider" ).slider({
    //  range: "max",
    //  min: 1,
    //  max: 100,
    //  value: 100,
    //  slide: function( event, ui ) {
    //      animSpeedChange(ui)
    //  },
    //  change: function( event, ui ) {
    //      animSpeedChange(ui)
    //  }
    // });
    // document.getElementById('animationspeed').innerHTML = $( "#animspeedslider" ).slider("value")+"fps"
}

function setEllipses() {
    for(var sid in ellipses) {
		 //draw ellipsoid
         // var emesh = new THREE.Particle( new THREE.ParticleCanvasMaterial());
         var emesh = new THREE.Mesh( sphere,new THREE.MeshLambertMaterial() );
         emesh.scale.x = ellipses[sid]['width']/radius;
	     emesh.scale.y = ellipses[sid]['height']/radius;
	     emesh.scale.z = ellipses[sid]['length']/radius;
		 emesh.position.set(ellipses[sid]['x'],ellipses[sid]['y'] ,ellipses[sid]['z'] );
		 emesh.material.color = new THREE.Color()
	     emesh.material.transparent = true;
	     emesh.material.opacity = 0.2;
	     emesh.updateMatrix();
         emesh.matrixAutoUpdate = true;
	     if(mapping[sid] != undefined)
	     {
    	     group.add( emesh );
    		 plotEllipses[sid] = emesh;
    	 }
	}
}

function setPoints() {
    for(var sid in points)
	{
		 //draw ball
         // var mesh = new THREE.Particle( new THREE.ParticleCanvasMaterial({color: new THREE.Color()}));
         var mesh = new THREE.Mesh( sphere, new THREE.MeshLambertMaterial() );
		 mesh.material.color = new THREE.Color()
		 mesh.material.transparent = false;
		 mesh.material.opacity = 1;
         mesh.position.set(points[sid]['x'], points[sid]['y'], points[sid]['z']);
         mesh.updateMatrix();
         mesh.matrixAutoUpdate = true;
         if(mapping[sid] != undefined)
	     {
             // scene.add( mesh );
             group.add( mesh );
             plotSpheres[sid] = mesh;
             plotIds.push(sid);
	     }
    }
	sphereScale = new THREE.Vector3(1,1,1);
}

function saveSVG(){
    open("data:image/svg+xml," + encodeURIComponent(document.getElementById('main_plot').innerHTML));
    // $.ajax({ url: 'lib.psp',
                // data: {fn:'saveSVG', SVGdata: document.getElementById('main_plot').innerHTML},
                // success: SVGSaved});
}

function SVGSaved(response){
    var fileName = eval('('+response+')')
    
    // document.execCommand('SaveAs',true,fileName);
    
    var dlwin = open('','Download SVG', 'width=400,height=50')
    dlwin.document.open();
    dlwin.document.write('<HTML><HEAD><meta name="content-disposition" content="inline; filename=\''+fileName+'\'">');
    dlwin.document.write('</HEAD><BODY>');
    dlwin.document.write('<a href=\''+fileName+'\'>'+fileName+'</a>')
    dlwin.document.write('</BODY></HTML>');
    dlwin.document.close();
    console.log(fileName)
}

/* update point count label */
function changePointCount() {
    document.getElementById('pointCount').innerHTML = visiblePoints+'/'+plotIds.length+' points'
}

$(document).ready(function() {
    setJqueryUi()
	
   // Detecting that webgl is activated
   if ( ! Detector.webgl ) Detector.addGetWebGLMessage();
   
   var main_plot = $('#main_plot');
   var renderer, particles, geometry, parameters, i, h, color;
   var mouseX = 0, mouseY = 0;
   
   var winWidth = Math.min(document.getElementById('main_plot').offsetWidth,document.getElementById('main_plot').offsetHeight), view_angle = 35, view_near = 1, view_far = 10000;
   var winAspect = document.getElementById('main_plot').offsetWidth/document.getElementById('main_plot').offsetHeight;
   
   $(window).resize(function() {
	  winWidth	= Math.min(document.getElementById('main_plot').offsetWidth,document.getElementById('main_plot').offsetHeight);
	  winAspect = document.getElementById('main_plot').offsetWidth/document.getElementById('main_plot').offsetHeight;
	  camera.aspect = winAspect;
	  camera.updateProjectionMatrix();
   });
   
   init();
   animate();
   
   function init() {
	  camera = new THREE.PerspectiveCamera(view_angle, winAspect, view_near, view_far);
	
	  
	  $('#main_plot canvas').attr('width',document.getElementById('main_plot').offsetWidth);
	  $('#main_plot canvas').attr('height',document.getElementById('main_plot').offsetHeight);
	  
	  scene = new THREE.Scene();
	  scene.fog = new THREE.FogExp2( 0x000000, 0.0009 );
	  
      sphere = new THREE.SphereGeometry(radius, segments, rings);
	
	 camera.position.x = camera.position.y = 0;
     camera.position.z = max * 4;
      //var len=ellipses.length;
     scene.add( camera );
     
     
    group = new THREE.Object3D();
	scene.add( group );
    // startTimer()
    setEllipses()
    // stopTimer('set ellipses')
	len = points.length;
    // startTimer()
	setPoints()
    // stopTimer('set points')
	plotIds = plotIds.sort();
    visiblePoints = plotIds.length;
    changePointCount(visiblePoints)

	// build the colorby and showby menus
	var line = "";
           $("#labelcombo").append("<option>Select A Category...</option>");
           // $("#animationovercombo").append("<option>Select A Category...</option>");
           // $("#animationcombo").append("<option>Select A Category...</option>");
	       
	       for(var i in headers){
	           //console.log(headers[i]);
	           var temp = [];
	           for(var j in plotIds) 
	           {
	               if(mapping[plotIds[j]] == undefined)
	               {
	                   console.log(plotIds[j] +" not in mapping")
	                   continue
	               }
	               temp.push(mapping[plotIds[j]][i])
	           }
	           
	           temp = dedupe(temp);
	           
	           // get rid of categories that have only one value
	           if(temp.length == 1)
	               continue;
	           
	           line = "<option value=\""+headers[i]+"\">"+headers[i]+"</option>"
               $("#colorbycombo").append(line);
               $("#showbycombo").append(line);
               $("#labelcombo").append(line);
               // $("#animationovercombo").append(line);
               // $("#animationcombo").append(line);
	       }
	       
           var rv = colorByMenuChanged();
           showByMenuChanged();

	var debugaxis = function(axisLength, xstart, ystart, zstart){
	    //Shorten the vertex function
	    function v(x,y,z){ 
	            return new THREE.Vertex(new THREE.Vector3(x,y,z)); 
	    }
    
	    //Create axis (point1, point2, colour)
	    function createAxis(p1, p2, color){
	            var line, lineGeometry = new THREE.Geometry(),
	            lineMat = new THREE.LineBasicMaterial({color: color, lineWidth: 1});
	            lineGeometry.vertices.push(p1, p2);
	            line = new THREE.Line(lineGeometry, lineMat);
	            scene.add(line);
	    }
    
	    createAxis(v(xstart, ystart, zstart), v(axisLength, ystart, zstart), 0xFF0000);
	    createAxis(v(xstart, ystart, zstart), v(xstart, axisLength, zstart), 0x00FF00);
	    createAxis(v(xstart, ystart, zstart), v(xstart, ystart, axisLength), 0x0000FF);
	    
	};
		
	  var axesLen = Math.max(max_x+Math.abs(min_x),max_y+Math.abs(min_y),max_z+Math.abs(min_z));	  
	  debugaxis(axesLen, min_x, min_y, min_z);
	  //debugaxis(axesLen, 0, 0, 0);
	  buildAxisLabels()
      // lights
      var light = new THREE.DirectionalLight( 0xffffff, 2 );
	  light.position.set( 1, 1, 1 ).normalize();
	  scene.add( light );
      
	  var light = new THREE.DirectionalLight( 0xffffff );
	  light.position.set( -1, -1, -1 ).normalize();
	  scene.add( light );
				
      // light1 = new THREE.DirectionalLight( 0xffffff );
      // light1.position.set( max, 0, 0 );
      // scene.add( light1 );
      // light2 = new THREE.DirectionalLight( 0xffffff );
      // light2.position.set( -max, 0, 0 );
      // scene.add( light2 );
      // 
      // light3 = new THREE.DirectionalLight( 0xffffff );
      // light3.position.set( 0, max, 0 );
      // scene.add( light3 );
      // light4 = new THREE.DirectionalLight( 0xffffff );
      // light4.position.set( 0, -max, 0 );
      // scene.add( light4 );
      // 
      // light5 = new THREE.DirectionalLight( 0xffffff );
      // light5.position.set( 0, 0, max );
      // scene.add( light5 );
      // light6 = new THREE.DirectionalLight( 0xffffff );
      // light6.position.set( 0, 0, -max );
      // scene.add( light6 );
      
      // Adding camera
	  
	  
      light = new THREE.DirectionalLight( 0xffffff );
	  controls = new THREE.TrackballControls(camera, document.getElementById('main_plot'));
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
      // renderer = new THREE.SVGRenderer();
      renderer.setClearColorHex( 0x333333, 1 );
      renderer.setSize( document.getElementById('main_plot').offsetWidth, document.getElementById('main_plot').offsetHeight );
      renderer.sortObjects = false;
      main_plot.append( renderer.domElement );
	
	// build divs to hold point labels and position them
	var labelshtml = "";
	       for(var i in plotIds) {
	           var sid = plotIds[i];
	           var divid = sid.replace(/\./g,'');
	           mesh = plotSpheres[sid];
	           var coords = toScreenXY(mesh.position,camera,$('#main_plot'));
	           labelshtml += "<label id=\""+divid+"_label\" class=\"unselectable labels\" style=\"position:absolute; left:"+parseInt(coords['x'])+"px; top:"+parseInt(coords['y'])+"px;\">";
	           labelshtml += sid;
	           labelshtml += "</label>";
	       }
	       document.getElementById("labels").innerHTML = labelshtml;
   }

   function buildAxisLabels() {
      //build axis labels
      var axesLen = Math.max(max_x+Math.abs(min_x),max_y+Math.abs(min_y),max_z+Math.abs(min_z));
      var axislabelhtml = "";
      // var xcoords = toScreenXY(new THREE.Vector3(0, 0, 0),camera,$('#main_plot'));
      var xcoords = toScreenXY(new THREE.Vector3(axesLen, min_y, min_z),camera,$('#main_plot'));
      axislabelhtml += "<label id=\"pc1_label\" class=\"unselectable labels\" style=\"position:absolute; left:"+parseInt(xcoords['x'])+"px; top:"+parseInt(xcoords['y'])+"px;\">";
      axislabelhtml += pc1+"%";
      axislabelhtml += "</label>";
	  var ycoords = toScreenXY(new THREE.Vector3(min_x, axesLen, min_z),camera,$('#main_plot'));
      axislabelhtml += "<label id=\"pc2_label\" class=\"unselectable labels\" style=\"position:absolute; left:"+parseInt(ycoords['x'])+"px; top:"+parseInt(ycoords['y'])+"px;\">";
      axislabelhtml += pc2+"%";
      axislabelhtml += "</label>";
	  var zcoords = toScreenXY(new THREE.Vector3(min_x, min_y, axesLen),camera,$('#main_plot'));
      axislabelhtml += "<label id=\"pc3_label\" class=\"unselectable labels\" style=\"position:absolute; left:"+parseInt(zcoords['x'])+"px; top:"+parseInt(zcoords['y'])+"px;\">";
      axislabelhtml += pc3+"%";
      axislabelhtml += "</label>";
      document.getElementById("axislabels").innerHTML = axislabelhtml;
   }

   function animate() {
    // setTimeout( function() {

        requestAnimationFrame( animate );

    // }, 1000 / 30 );
    render();
    buildAxisLabels();
	// move labels when the plot is moved
	if(document.plotoptions.elements[0].checked)
	{
	    for(var i in plotIds) {
    	           var sid = plotIds[i];
    	           mesh = plotSpheres[sid];
    	           var coords = toScreenXY(mesh.position, camera, $('#main_plot'));
    	           var divid = sid.replace(/\./g,'');
    	           $('#'+divid+"_label").css('left',coords['x']);
    	           $('#'+divid+"_label").css('top',coords['y']);
    	       }
    }
    if(foundId) {
       var coords = toScreenXY(plotSpheres[foundId].position, camera, $('#main_plot'));
       $('#finder').css('left',coords['x']-15);
       $('#finder').css('top',coords['y']-5);
       }
   }
   
   function render() {
      controls.update();
      renderer.setSize( document.getElementById('main_plot').offsetWidth, document.getElementById('main_plot').offsetHeight );
      renderer.render( scene, camera );
   }
});