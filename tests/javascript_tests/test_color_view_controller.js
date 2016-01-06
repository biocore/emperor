$(document).ready(function() {

  module("ColorViewController", {
    setup: function(){
      sharedDecompositionViewDict = {}
      var $slickid = $('<div id="fooligans"></div>');
      $slickid.appendTo(document.body);

      // setup function
      name = "pcoa";
      ids = ['PC.636', 'PC.635'];
      coords = [
        [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
         -0.229889, -0.046599],
        [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
         -0.112864, 0.064794]];
      pct_var = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
                 10.024774995, 8.22835130237, 7.55971173665, 6.24945796136];
      md_headers = ['SampleID', 'LinkerPrimerSequence', 'Treatment', 'DOB'];
      metadata = [['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
                  ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112']];
      decomp = new DecompositionModel(name, ids, coords, pct_var, md_headers,
                                      metadata);
      var dv = new DecompositionView(decomp);
      sharedDecompositionViewDict['pcoa'] = dv;

      name = "biplot";
      ids = ['tax_1', 'tax_2'];
      coords = [
        [-1, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
         -0.229889, -0.046599],
        [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
         -0.112864, 0.064794]];
      pct_var = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
                 10.024774995, 8.22835130237, 7.55971173665, 6.24945796136];
      md_headers = ['SampleID', 'Gram'];
      metadata = [['tax_1', '1'],
                  ['tax_2', '0']];
      decomp = new DecompositionModel(name, ids, coords, pct_var, md_headers,
                                      metadata);
      dv = new DecompositionView(decomp);
      sharedDecompositionViewDict['biplot'] = dv;

      // Slickgrid
      var columns = [
        {id: "pc1", name: "pc1", field: "pc1"},
        {id: "pc2", name: "pc2", field: "pc2"},
        {id: "pc3", name: "pc3", field: "pc3"},
      ];

      var options = {
        enableCellNavigation: true,
        enableColumnReorder: false
      };
      var data = [];
      data.push({'pc1':1, 'pc2':1, 'pc3':1});
      data.push({'pc1':1, 'pc2':1, 'pc3':2});

      grid = new Slick.Grid("#fooligans", data, columns, options);
    },
    teardown: function(){
      sharedDecompositionViewDict = undefined;
      $("#fooligans").remove();
      decomp = undefined;
    }
  });

  test("Constructor tests", function(assert) {
    var container = $('<div id="does-not-exist" style="height:11px; width:12px"></div>');

    assert.ok(ColorViewController.prototype instanceof EmperorAttributeABC);

    var controller = new ColorViewController(container, sharedDecompositionViewDict);
    equal(controller.title, 'Color');

    var testColumn = controller.bodyGrid.getColumns()[0];
    equal(testColumn.field, 'value');

    // verify the color value is set properly
    equal(controller.$colormapSelect.val(), 'discrete-coloring-qiime');
    equal(controller.$select.val(), 'SampleID');
  });

  test("Test discrete colors are retrieved correctly", function(){
    equal(ColorViewController.getDiscreteColor(0), "#8dd3c7", "Test color is indeed red");
    equal(ColorViewController.getDiscreteColor(1), "#ffffb3", "Test color is indeed blue");
    equal(ColorViewController.getDiscreteColor(2), "#bebada", "Test color is indeed orange");
  });

  test("Test discrete colors are retrieved on roll-over", function(){
    equal(ColorViewController.getDiscreteColor(24), "#8dd3c7", "Test color is indeed red even in"+
          " the event of a roll-over");
    equal(ColorViewController.getDiscreteColor(25), "#ffffb3", "Test color is indeed red even in"+
          " the event of a roll-over");
    equal(ColorViewController.getDiscreteColor(26), "#bebada", "Test color is indeed red even in"+
          " the event of a roll-over");
  });

  test("Test discrete colors with other maps", function(){
    equal(ColorViewController.getDiscreteColor(0, 'discrete-coloring'), "#8dd3c7",
          "Test color is indeed red");
    equal(ColorViewController.getDiscreteColor(1, 'discrete-coloring-qiime'), "#0000ff",
          "Test color is indeed blue");
  });

  test("Test discrete colors with other maps (rollover)", function(){
    equal(ColorViewController.getDiscreteColor(24, "discrete-coloring"), "#8dd3c7",
          "Test color is indeed red even in the event of a roll-over");
    equal(ColorViewController.getDiscreteColor(25, "discrete-coloring-qiime"), "#0000ff",
          "Test color is indeed red even in the event of a roll-over");
    equal(ColorViewController.getDiscreteColor(26, "discrete-coloring-qiime"), "#f27304",
          "Test color is indeed red even in the event of a roll-over");
  });


  test("Test ColorViewController.getColorList exceptions", function(){
    var five;
    five = [0, 1, 2, 3, 4];

    throws(
      function (){
        var color = ColorViewController.getDiscreteColor(0, 'discrete-coloring-non-existant');
      },
      Error,
      'An error is raised if the colormap does not exist'
    );
  });

  test("Test ColorViewController.getColorList works", function(){
    var five, ten, twenty;

    five = [0, 1, 2, 3, 4];
    ten = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    twenty = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
              19]


    deepEqual(ColorViewController.getColorList(five, 'discrete-coloring'), { "0": "#8dd3c7", "1":
        "#ffffb3", "2": "#bebada", "3": "#fb8072", "4": "#80b1d3" });

    deepEqual(ColorViewController.getColorList(five, 'OrRd'), { "0": "#fff7ec", "1":
        "#ffbf92", "2": "#fc8d59", "3": "#d6593a", "4": "#7f0000" });
    deepEqual(ColorViewController.getColorList([0], 'OrRd'), {"0": "#fff7ec"});

    deepEqual(ColorViewController.getColorList(ten, 'Blues'), { "0": "#f7fbff", "1":
        "#d2e6f3", "2": "#b1d3e8", "3": "#93c3df", "4": "#78b4d9", "5":
        "#63a7d1", "6": "#5092c3", "7": "#3c77ac", "8": "#26568f", "9":
        "#08306b" });
    deepEqual(ColorViewController.getColorList([0], 'Blues'), {"0": "#f7fbff"});

    deepEqual(ColorViewController.getColorList(twenty, 'BrBG'), { "0": "#543005", "1":
        "#6f4b1d", "10": "#f6e9c8", "11": "#f2e9cf", "12": "#eae7d3", "13":
        "#dee3d3", "14": "#cedcd0", "15": "#bad3c9", "16": "#a2c7bf", "17":
        "#85bab2", "18": "#63a9a2", "19": "#35978f", "2": "#886533", "3":
        "#9f7d49", "4": "#b4945e", "5": "#c6a973", "6": "#d5bb87", "7":
        "#e2cb99", "8": "#ecd9ab", "9": "#f3e4bb" });
    deepEqual(ColorViewController.getColorList([0], 'OrRd'), {"0": "#fff7ec"});

  });

  test("Test ColorViewController.getColorList exceptions", function(){
    var five;
    five = [0, 1, 2, 3, 4];

    throws(
        function (){
          var colors = ColorViewController.getColorList(five, false, 'Non-existant');
        },
      Error,
      'An error is raised if the colormap does not exist'
    );

  });



});
