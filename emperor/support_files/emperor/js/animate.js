/**
 *
 * @author Yoshiki Vazquez Baeza
 * @copyright Copyright 2013, Emperor
 * @credits Yoshiki Vazquez Baeza
 * @license BSD
 * @version 0.9.2-dev
 * @maintainer Yoshiki Vazquez Baeza
 * @email yoshiki89@gmail.com
 * @status Development
 *
 */


/**
 *
 *
 */
function AnimationDirector(mappingFileHeaders, mappingFileData, coordinatesData, gradientCategory, trajectoryCategory, frames){

	if (mappingFileHeaders === undefined || mappingFileData === undefined ||
		coordinatesData === undefined || gradientCategory === undefined ||
		trajectoryCategory === undefined || frames === undefined) {
		throw new Error("All arguments are required");
	}

	var index;

	index = mappingFileHeaders.indexOf(gradientCategory);
	if (index == -1) {
		throw new Error("Could not find the gradient category in the mapping file");
	}
	index = mappingFileHeaders.indexOf(trajectoryCategory);
	if (index == -1) {
		throw new Error("Could not find the trajectory category in the mapping file");
	}

	this.mappingFileHeaders = mappingFileHeaders;
	this.mappingFileData = mappingFileData;
	this.coordinatesData = coordinatesData;
	this.gradientCategory = gradientCategory;
	this.trajectoryCategory = trajectoryCategory;
	this.frames = frames;

	this.minimumDelta = null;

	this.trajectories = new Array();

	this.initializeTrajectories();

	return this;
}

/**
 *
 *
 */
AnimationDirector.prototype.initializeTrajectories = function(){

	var chewedData = null, trajectoryBuffer = null, minimumDelta;
	var sampleNamesBuffer, gradientPointsBuffer, coordinatesBuffer;

	// console.log(this.mappingFileHeaders);

	// function getSampleNamesAndDataForSortedTrajectories(mappingFileHeaders, mappingFileData, coordinatesData, trajectoryCategory, gradientCategory){
	chewedData = getSampleNamesAndDataForSortedTrajectories(this.mappingFileHeaders,
		this.mappingFileData, this.coordinatesData, this.trajectoryCategory,
		this.gradientCategory);

	if (chewedData == null){
		throw new Error("Error initializing the trajectories");
	}

	// function getMinimumDelta(sampleData){
	this.minimumDelta = getMinimumDelta(chewedData);
	console.log('The minimum delta is '+this.minimumDelta);

	for (var key in chewedData){
		sampleNamesBuffer = new Array();
		gradientPointsBuffer = new Array();
		coordinatesBuffer = new Array();

		for (var index = 0; index < chewedData[key].length; index++){
			sampleNamesBuffer.push(chewedData[key][index]['name']);

			gradientPointsBuffer.push(chewedData[key][index]['value']);

			coordinatesBuffer.push({'x':chewedData[key][index]['x'],
				'y':chewedData[key][index]['y'], 'z':chewedData[key][index]['z']});
		}

		// function TrajectoryOfSamples(sampleNames, gradientPoints, coordinates, minimumDelta, suppliedN){
		trajectoryBuffer = new TrajectoryOfSamples(sampleNamesBuffer,
			gradientPointsBuffer, coordinatesBuffer, this.minimumDelta);

		this.trajectories.push(trajectoryBuffer);

	}
	return;
}

/**
 *
 *
 */
AnimationDirector.prototype.computeN = function (){
	return 60;
}

/**
 *
 *
 */
AnimationDirector.prototype.getInflectionPoints = function (){
	return null;
}

/**
 *
 *
 */
AnimationDirector.prototype.getVectorPoints = function (){
	return null;
}

/**
 *
 *
 */
AnimationDirector.prototype.getGroup = function (){
	return null;
}

/**
 *
 *
 */
AnimationDirector.prototype.updateFrame = function (){
	return null;
}
