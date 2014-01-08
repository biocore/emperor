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
	this.maximumTrajectoryLength = null;
	this.currentFrame = -1;
	this.trajectories = new Array();

	this.initializeTrajectories();
	this.getMaximumTrajectoryLength();

	return this;
}

/**
 *
 *
 */
AnimationDirector.prototype.initializeTrajectories = function(){

	var chewedData = null, trajectoryBuffer = null, minimumDelta;
	var sampleNamesBuffer = new Array(), gradientPointsBuffer = new Array();
	var coordinatesBuffer = new Array();

	// compute a dictionary from where we will extract the germane data
	chewedData = getSampleNamesAndDataForSortedTrajectories(this.mappingFileHeaders,
		this.mappingFileData, this.coordinatesData, this.trajectoryCategory,
		this.gradientCategory);

	if (chewedData === null){
		throw new Error("Error initializing the trajectories, could not compute the data");
	}

	// calculate the minimum delta per step
	this.minimumDelta = getMinimumDelta(chewedData);

	for (var key in chewedData){
		sampleNamesBuffer.length = 0;
		gradientPointsBuffer.length = 0;
		coordinatesBuffer.length = 0;

		// each of the keys is a trajectory name i. e. CONTROL, TREATMENT, etc
		// we are going to generate buffers so we can initialize the trajectory
		for (var index = 0; index < chewedData[key].length; index++){
			// list of sample identifiers
			sampleNamesBuffer.push(chewedData[key][index]['name']);

			// list of the value each sample has in the gradient
			gradientPointsBuffer.push(chewedData[key][index]['value']);

			// x, y and z values for the coordinates data
			coordinatesBuffer.push({'x':chewedData[key][index]['x'],
				'y':chewedData[key][index]['y'], 'z':chewedData[key][index]['z']});
		}

		// create the trajectory object
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
AnimationDirector.prototype.getMaximumTrajectoryLength = function (){
	if(this.maximumTrajectoryLength === null){
		this._computeN();
	}

	return this.maximumTrajectoryLength;
}

AnimationDirector.prototype._computeN = function (){
	var arrayOfLengths = new Array();

	// retrieve the length of all the trajectories
	for (var index = 0; index < this.trajectories.length; index++){
		arrayOfLengths.push(this.trajectories[index].interpolatedCoordinates.length);
	}

	// assign the value of the maximum value for these lengths
	this.maximumTrajectoryLength = _.max(arrayOfLengths);
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
	this.currentFrame = this.currentFrame + 1;
}

AnimationDirector.prototype.animationCycleFinished = function (){
	return this.currentFrame > this.getMaximumTrajectoryLength();
}
