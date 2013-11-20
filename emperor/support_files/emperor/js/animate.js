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

function AnimationDirector(mapping_file, coords, animate_through_category, animate_over_category, frames){
	this.mapping_file = mapping_file;
	this.coors = coords;
	this.animate_through_category = animate_through_category;
	this.animate_over_category = animate_over_category;
	this.frames = frames

	return this;
}

AnimationDirector.prototype.generateData(){
	return null;
}

AnimationDirector.prototype.computeN(){
	return null;
}

AnimationDirector.prototype.getInflectionPoints(){
	return null;
}

AnimationDirector.prototype.getVectorPoints(){
	return null;
}

AnimationDirector.prototype.getGroup(){
	return null;
}

AnimationDirector.prototype.updateFrame(){
	return null;
}
