/*
 * __author__ = "Yoshiki Vazquez Baeza"
 * __copyright__ = "Copyright 2013, Emperor"
 * __credits__ = ["Yoshiki Vazquez Baeza"]
 * __license__ = "BSD"
 * __version__ = "0.9.2-dev"
 * __maintainer__ = "Yoshiki Vazquez Baeza"
 * __email__ = "yoshiki89@gmail.com"
 * __status__ = "Development"
 */

function TrajectoryOfSamples(sampleNames, dataPoints, minimumDelta, suppliedN){
	this.sampleNames = sampleNames;
	this.dataPoints = dataPoints;
	this.minimumDelta = minimumDelta;

	// the default supplied N will last "ideally" a couple seconds
	this.suppliedN = suppliedN !== undefined ? suppliedN : 60;

	// initialize as an empty array but fill it up upon request
	this.interpolatedDataPoints = null;
}

TrajectoryOfSamples.prototype._generateInterpolatedDataPoints = function(){
	var pointsPerStep = 0;

	for (var index = 0; index < this.dataPoints.length-1; index++){
		
	}
}
