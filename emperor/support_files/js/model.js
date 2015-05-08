/* Represents an object that can be drawn (i.e. a sample or taxa)
*/
function Plottable(params){
  this.metadata = ["AGCACGAGCCTA", "YATGCTGCCTCCCGTAGGAGT", "Control",
                   "20061218", "Control_mouse_I.D._354"];
  this.coordinates = [0.280399117569, -0.0060128286014, 0.0234854344148,
                      -0.0468109474823, -0.146624450094, 0.00566979124596,
                      -0.0354299634191, -0.255785794275, -4.84141986706e-09];
  this.confidenceInterval = [];
}

/* Models all the data loaded to be drawn (i.e. all samples, taxa, vectors...)
*/
function DecompositionModel(params){
  this.abbreviatedName = "pcoa";
  this.percExpl = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
                   10.024774995, 8.22835130237, 7.55971173665, 6.24945796136,
                   1.17437418531e-14];
  this.serialComparison = false;
  this.headers = ["BarcodeSequence", "LinkerPrimerSequence", "Treatment",
                  "DOB", "Description"];
  this.ids = ["PC.354", "PC.355", "PC.356", "PC.481", "PC.593", "PC.607",
              "PC.634", "PC.635", "PC.636"];
  this.plottable = [new Plottable(), new Plottable(), new Plottable(),
                    new Plottable(), new Plottable(), new Plottable(),
                    new Plottable(), new Plottable(), new Plottable()];
  this.plottableGroup = [];
  this.plotEdge = false;

  /* Get's a string with the plottable id and returns the plottable */
  this.getPlottableByID = function(id){
    return this.getPlottableByIDs([id])[0];
  };

  /* Get's a metadata category and a value and returns a list of 
  plottable objects that match that search
  */
  this.getPlottablesByMetadataCategoryValue = function(category, value){
    return [this.plottable[0], this.plottable[1]];
  };

  /* Get's a metadata category and returns the unique values on that category
  */
  this.getUniqueValuesByCategory = function(category){
    return ["Control", "Fast"];
  };

  /* Get's a list of strings with the plottable ids and returns a list of
  plottable */
  this.getPlottableByIDs = function(idArray){
    return [this.plottable[0], this.plottable[1]];
  };

  /**/
  this.applyByMetadataCategoryValue = function(func, category, value){

  };
}