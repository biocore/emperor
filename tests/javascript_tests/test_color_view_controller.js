requirejs([
    "jquery",
    "underscore",
    "model",
    "view",
    "viewcontroller",
    "slickgrid",
    "colorviewcontroller"
], function ($, _, model, DecompositionView, viewcontroller, SlickGrid, ColorViewController) {
  $(document).ready(function() {
    var EmperorAttributeABC = viewcontroller.EmperorAttributeABC;
    var DecompositionModel = model.DecompositionModel;

    module("ColorViewController", {
      setup: function(){
        this.sharedDecompositionViewDict = {};
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
        this.sharedDecompositionViewDict.scatter = dv;

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
        this.decomp = new DecompositionModel(name, ids, coords, pct_var, md_headers,
            metadata);
        this.dv = new DecompositionView(this.decomp);
        this.sharedDecompositionViewDict.biplot = dv;

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
        this.sharedDecompositionViewDict = undefined;
        $("#fooligans").remove();
        this.decomp = undefined;
      }
    });

    test("Constructor tests", function(assert) {
      var container = $('<div id="does-not-exist" style="height:11px; width:12px"></div>');

      assert.ok(ColorViewController.prototype instanceof EmperorAttributeABC);

      var controller = new ColorViewController(container, this.sharedDecompositionViewDict);
      equal(controller.title, 'Color');

      var testColumn = controller.bodyGrid.getColumns()[0];
      equal(testColumn.field, 'value');

      // verify the color value is set properly
      equal(controller.$colormapSelect.val(), 'discrete-coloring-qiime');
      equal(controller.$select.val(), 'SampleID');
    });

    test("Test discrete colors are retrieved correctly", function(){
      equal(ColorViewController.getDiscreteColor(0), "#ff0000", "Test color is indeed red");
      equal(ColorViewController.getDiscreteColor(1), "#0000ff", "Test color is indeed blue");
      equal(ColorViewController.getDiscreteColor(2), "#f27304", "Test color is indeed orange");
    });

    test("Test discrete colors are retrieved on roll-over", function(){
      equal(ColorViewController.getDiscreteColor(24), "#ff0000", "Test color is indeed red even in"+
          " the event of a roll-over");
      equal(ColorViewController.getDiscreteColor(25), "#0000ff", "Test color is indeed red even in"+
          " the event of a roll-over");
      equal(ColorViewController.getDiscreteColor(26), "#f27304", "Test color is indeed red even in"+
          " the event of a roll-over");
    });

    test("Test discrete colors with other maps", function(){
      equal(ColorViewController.getDiscreteColor(0, 'Set1'), "#e41a1c",
          "Test color is indeed red");
      equal(ColorViewController.getDiscreteColor(1, 'Pastel1'), "#b3cde3",
          "Test color is indeed blue");
    });

    test("Test discrete colors with other maps (rollover)", function(){
      equal(ColorViewController.getDiscreteColor(24, "Set1"), "#a65628",
          "Test color is indeed red even in the event of a roll-over");
      equal(ColorViewController.getDiscreteColor(25, "Pastel1"), "#fddaec",
          "Test color is indeed red even in the event of a roll-over");
      equal(ColorViewController.getDiscreteColor(26, "Dark2"), "#7570b3",
          "Test color is indeed red even in the event of a roll-over");
    });


    test("Test ColorViewController.getColorList exceptions", function(){
      var five;
      five = ['0', 'string1', 'string2', 'string3', 'string4'];

      throws(
          function (){
            var color = ColorViewController.getDiscreteColor(0, 'discrete-coloring-non-existant');
          },
          Error,
          'An error is raised if the colormap does not exist'
          );

      throws(
          function (){
            var color = ColorViewController.getColorList(five, 'Blues', false, true);
          },
          Error,
          'An error is raised if there are less than 2 numeric values when scaled'
          );
    });

    test("Test ColorViewController.getColorList works", function(){
      var five, ten, twenty, scaled, colors;

      five = [0, 1, 2, 3, 4];
      ten = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
      twenty = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
      19];
      scaled = [0, 1, 2, 3, 7, 20, 50];

      colors = ColorViewController.getColorList(scaled, 'Blues', false, true);
      deepEqual(colors[0], {"0": "#f7fbff","1": "#f3f8fd","2": "#eff5fc",
                "20": "#93c4de","3": "#ebf3fb","50": "#08306b","7": "#dbe9f6"});
      deepEqual(colors[1], "<defs><linearGradient id=\"Gradient\" x1=\"0\" x2=\"1\" y1=\"1\" y2=\"1\"><stop offset=\"0%\" stop-color=\"#f7fbff\"/><stop offset=\"1%\" stop-color=\"#f5f9fe\"/><stop offset=\"2%\" stop-color=\"#f3f8fd\"/><stop offset=\"3%\" stop-color=\"#f1f7fd\"/><stop offset=\"4%\" stop-color=\"#eff5fc\"/><stop offset=\"5%\" stop-color=\"#edf4fb\"/><stop offset=\"6%\" stop-color=\"#ebf3fb\"/><stop offset=\"7%\" stop-color=\"#e9f2fa\"/><stop offset=\"8%\" stop-color=\"#e7f0f9\"/><stop offset=\"9%\" stop-color=\"#e5eff9\"/><stop offset=\"10%\" stop-color=\"#e3eef8\"/><stop offset=\"11%\" stop-color=\"#e1ecf7\"/><stop offset=\"12%\" stop-color=\"#dfebf7\"/><stop offset=\"13%\" stop-color=\"#ddeaf6\"/><stop offset=\"14%\" stop-color=\"#dbe9f6\"/><stop offset=\"15%\" stop-color=\"#d9e7f5\"/><stop offset=\"16%\" stop-color=\"#d7e6f4\"/><stop offset=\"17%\" stop-color=\"#d5e5f4\"/><stop offset=\"18%\" stop-color=\"#d3e3f3\"/><stop offset=\"19%\" stop-color=\"#d1e2f2\"/><stop offset=\"20%\" stop-color=\"#cfe1f2\"/><stop offset=\"21%\" stop-color=\"#cde0f1\"/><stop offset=\"22%\" stop-color=\"#cbdef0\"/><stop offset=\"23%\" stop-color=\"#c9ddf0\"/><stop offset=\"24%\" stop-color=\"#c7dcef\"/><stop offset=\"25%\" stop-color=\"#c6dbef\"/><stop offset=\"26%\" stop-color=\"#c2d9ed\"/><stop offset=\"27%\" stop-color=\"#bfd8ec\"/><stop offset=\"28%\" stop-color=\"#bcd6eb\"/><stop offset=\"29%\" stop-color=\"#b9d5ea\"/><stop offset=\"30%\" stop-color=\"#b6d4e9\"/><stop offset=\"31%\" stop-color=\"#b2d2e8\"/><stop offset=\"32%\" stop-color=\"#afd1e7\"/><stop offset=\"33%\" stop-color=\"#acd0e6\"/><stop offset=\"34%\" stop-color=\"#a9cee4\"/><stop offset=\"35%\" stop-color=\"#a6cde3\"/><stop offset=\"36%\" stop-color=\"#a2cce2\"/><stop offset=\"37%\" stop-color=\"#9fcae1\"/><stop offset=\"38%\" stop-color=\"#9bc8e0\"/><stop offset=\"39%\" stop-color=\"#97c6df\"/><stop offset=\"40%\" stop-color=\"#93c4de\"/><stop offset=\"41%\" stop-color=\"#8fc2dd\"/><stop offset=\"42%\" stop-color=\"#8bbfdd\"/><stop offset=\"43%\" stop-color=\"#87bddc\"/><stop offset=\"44%\" stop-color=\"#83bbdb\"/><stop offset=\"45%\" stop-color=\"#7fb9da\"/><stop offset=\"46%\" stop-color=\"#7bb6d9\"/><stop offset=\"47%\" stop-color=\"#77b4d8\"/><stop offset=\"48%\" stop-color=\"#73b2d7\"/><stop offset=\"49%\" stop-color=\"#6fb0d6\"/><stop offset=\"50%\" stop-color=\"#6baed6\"/><stop offset=\"51%\" stop-color=\"#67abd4\"/><stop offset=\"52%\" stop-color=\"#64a9d3\"/><stop offset=\"53%\" stop-color=\"#61a7d2\"/><stop offset=\"54%\" stop-color=\"#5da5d0\"/><stop offset=\"55%\" stop-color=\"#5aa2cf\"/><stop offset=\"56%\" stop-color=\"#57a0ce\"/><stop offset=\"57%\" stop-color=\"#549ecd\"/><stop offset=\"58%\" stop-color=\"#509ccb\"/><stop offset=\"59%\" stop-color=\"#4d99ca\"/><stop offset=\"60%\" stop-color=\"#4a97c9\"/><stop offset=\"61%\" stop-color=\"#4695c7\"/><stop offset=\"62%\" stop-color=\"#4393c6\"/><stop offset=\"63%\" stop-color=\"#4090c5\"/><stop offset=\"64%\" stop-color=\"#3e8ec3\"/><stop offset=\"65%\" stop-color=\"#3b8bc2\"/><stop offset=\"66%\" stop-color=\"#3888c1\"/><stop offset=\"67%\" stop-color=\"#3686bf\"/><stop offset=\"68%\" stop-color=\"#3383be\"/><stop offset=\"69%\" stop-color=\"#3080bd\"/><stop offset=\"70%\" stop-color=\"#2e7ebb\"/><stop offset=\"71%\" stop-color=\"#2b7bba\"/><stop offset=\"72%\" stop-color=\"#2878b9\"/><stop offset=\"73%\" stop-color=\"#2676b7\"/><stop offset=\"74%\" stop-color=\"#2373b6\"/><stop offset=\"75%\" stop-color=\"#2171b5\"/><stop offset=\"76%\" stop-color=\"#1f6eb3\"/><stop offset=\"77%\" stop-color=\"#1c6bb1\"/><stop offset=\"78%\" stop-color=\"#1a69af\"/><stop offset=\"79%\" stop-color=\"#1866ad\"/><stop offset=\"80%\" stop-color=\"#1664ab\"/><stop offset=\"81%\" stop-color=\"#1461a9\"/><stop offset=\"82%\" stop-color=\"#135fa7\"/><stop offset=\"83%\" stop-color=\"#115ca5\"/><stop offset=\"84%\" stop-color=\"#0f59a3\"/><stop offset=\"85%\" stop-color=\"#0d57a1\"/><stop offset=\"86%\" stop-color=\"#0b549f\"/><stop offset=\"87%\" stop-color=\"#09529d\"/><stop offset=\"88%\" stop-color=\"#084f9a\"/><stop offset=\"89%\" stop-color=\"#084d96\"/><stop offset=\"90%\" stop-color=\"#084a92\"/><stop offset=\"91%\" stop-color=\"#08478e\"/><stop offset=\"92%\" stop-color=\"#08458a\"/><stop offset=\"93%\" stop-color=\"#084286\"/><stop offset=\"94%\" stop-color=\"#083f82\"/><stop offset=\"95%\" stop-color=\"#083d7e\"/><stop offset=\"96%\" stop-color=\"#083a7a\"/><stop offset=\"97%\" stop-color=\"#083776\"/><stop offset=\"98%\" stop-color=\"#083572\"/><stop offset=\"99%\" stop-color=\"#08326e\"/><stop offset=\"100%\" stop-color=\"#08306b\"/></defs><rect id=\"gradientRect\" width=\"100%\" height=\"20\" fill=\"url(#Gradient)\"/><text x=\"0%\" y=\"38\" font-family=\"sans-serif\" font-size=\"12px\">0</text><text x=\"50%\" y=\"38\" font-family=\"sans-serif\" font-size=\"12px\" text-anchor=\"middle\">25</text><text x=\"100%\" y=\"38\" font-family=\"sans-serif\" font-size=\"12px\" text-anchor=\"end\">50</text>")

      deepEqual(ColorViewController.getColorList(five, 'Set1', true), [{
        "0": "#e41a1c","1": "#377eb8","2": "#4daf4a","3": "#984ea3","4": "#ff7f00"}, undefined]);

      deepEqual(ColorViewController.getColorList(five, 'OrRd', false), [{ "0": "#fff7ec", "1":
        "#ffbf92", "2": "#fc8d59", "3": "#d6593a", "4": "#7f0000" }, undefined]);
      deepEqual(ColorViewController.getColorList([0], 'OrRd', false), [{"0": "#fff7ec"}, undefined]);

      deepEqual(ColorViewController.getColorList(ten, 'Blues', false), [{ "0": "#f7fbff", "1":
        "#d2e6f3", "2": "#b1d3e8", "3": "#93c3df", "4": "#78b4d9", "5":
          "#63a7d1", "6": "#5092c3", "7": "#3c77ac", "8": "#26568f", "9":
          "#08306b" }, undefined]);
      deepEqual(ColorViewController.getColorList([0], 'Blues', false), [{"0": "#f7fbff"}, undefined]);

      deepEqual(ColorViewController.getColorList(twenty, 'BrBG', false), [{ "0": "#543005", "1":
        "#6f4b1d", "10": "#f6e9c8", "11": "#f2e9cf", "12": "#eae7d3", "13":
          "#dee3d3", "14": "#cedcd0", "15": "#bad3c9", "16": "#a2c7bf", "17":
          "#85bab2", "18": "#63a9a2", "19": "#35978f", "2": "#886533", "3":
          "#9f7d49", "4": "#b4945e", "5": "#c6a973", "6": "#d5bb87", "7":
          "#e2cb99", "8": "#ecd9ab", "9": "#f3e4bb" }, undefined]);
      deepEqual(ColorViewController.getColorList([0], 'OrRd', false), [{"0": "#fff7ec"}, undefined]);

    });

    test("Test ColorViewController.getColorList exceptions", function(){
      var five;
      five = [0, 1, 2, 3, 4];
      onAlert(
      throws(
          function (){
            var colors = ColorViewController.getColorList(five, false, 'Non-existant');
          },
          Error,
          'An error is raised if the colormap does not exist'
          ));

    });

    test("Testing setPlottableAttributes helper function", function(assert) {
      // testing with one plottable
      var idx = 0;
      plottables = [{idx:idx}];
      equal(this.dv.markers[idx].material.color.getHexString(), 'ff0000');
      equal(this.dv.markers[idx+1].material.color.getHexString(), 'ff0000');
      ColorViewController.prototype.setPlottableAttributes(this.dv, '#00ff00', plottables);
      equal(this.dv.markers[idx].material.color.getHexString(), '00ff00');
      equal(this.dv.markers[idx+1].material.color.getHexString(), 'ff0000');

      // testing with multiple plottable
      plottables = [{idx:idx}, {idx:idx+1}];
      ColorViewController.prototype.setPlottableAttributes(this.dv, '#000000', plottables);
      equal(this.dv.markers[idx].material.color.getHexString(), '000000');
      equal(this.dv.markers[idx+1].material.color.getHexString(), '000000');
    });

    test("Testing toJSON", function() {
      var container = $('<div id="does-not-exist" style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(container, this.sharedDecompositionViewDict);
      // Change color on one point
      var idx = 0;
      plottables = [{idx:idx}];
      ColorViewController.prototype.setPlottableAttributes(this.dv, '#00ff00', plottables);

      var obs = controller.toJSON();
      var exp = {category: 'SampleID', colormap: 'discrete-coloring-qiime',
                 continuous: false, data: {'PC.636': '#ff0000', 'PC.635': '#0000ff'}};
      deepEqual(obs, exp);
    });

    test("Testing fromJSON", function() {
      var json = {category: 'DOB', colormap: 'discrete-coloring-qiime',
                  continuous: false, data: {20070314: '#ff0000', 20071112: '#0000ff'}};

      var container = $('<div id="does-not-exist" style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(container, this.sharedDecompositionViewDict);

      controller.fromJSON(json);
      var idx = 0;
      equal(controller.decompViewDict.scatter.markers[idx].material.color.getHexString(), 'ff0000');
      equal(controller.decompViewDict.scatter.markers[idx+1].material.color.getHexString(), '0000ff');
      equal(controller.$select.val(), 'DOB');
      equal(controller.$colormapSelect.val(), 'discrete-coloring-qiime');
      equal(controller.$scaled.is(':checked'), false);
    });

  });

});
