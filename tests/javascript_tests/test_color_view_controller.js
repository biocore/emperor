requirejs([
    'jquery',
    'underscore',
    'model',
    'view',
    'viewcontroller',
    'slickgrid',
    'colorviewcontroller'
], function($, _, model, DecompositionView, viewcontroller, SlickGrid,
            ColorViewController) {
  $(document).ready(function() {
    var EmperorAttributeABC = viewcontroller.EmperorAttributeABC;
    var DecompositionModel = model.DecompositionModel;
    var Plottable = model.Plottable;

    module('ColorViewController', {
      setup: function() {
        this.sharedDecompositionViewDict = {};
        var $slickid = $('<div id="fooligans"></div>');
        $slickid.appendTo(document.body);

        // setup function
        name = 'pcoa';
        ids = ['PC.636', 'PC.635', 'PC.634'];
        coords = [
          [-0.276542, -0.144964, 0.066647, -0.067711, 0.176070, 0.072969,
          -0.229889, -0.046599],
          [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
          -0.112864, 0.064794],
          [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
          -0.112864, 0.064794]];
        pct_var = [26.6887048633, 16.2563704022, 13.7754129161, 11.217215823,
        10.024774995, 8.22835130237, 7.55971173665, 6.24945796136];
        md_headers = ['SampleID', 'Mixed', 'Treatment', 'DOB'];
        metadata = [['PC.636', '14.2', 'Control', '20070314'],
        ['PC.635', 'StringValue', 'Fast', '20071112'],
        ['PC.634', '14.7', 'Fast', '20071112']];
        decomp = new DecompositionModel(name, ids, coords, pct_var, md_headers,
            metadata);
        var dv = new DecompositionView(decomp);
        this.sharedDecompositionViewDict.scatter = dv;

        name = 'biplot';
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
        this.decomp = new DecompositionModel(name, ids, coords, pct_var,
                                             md_headers, metadata);
        this.dv = new DecompositionView(this.decomp);
        this.sharedDecompositionViewDict.biplot = dv;

        // Slickgrid
        var columns = [
        {id: 'pc1', name: 'pc1', field: 'pc1'},
        {id: 'pc2', name: 'pc2', field: 'pc2'},
        {id: 'pc3', name: 'pc3', field: 'pc3'}
        ];

        var options = {
          enableCellNavigation: true,
          enableColumnReorder: false
        };
        var data = [];
        data.push({'pc1': 1, 'pc2': 1, 'pc3': 1});
        data.push({'pc1': 1, 'pc2': 1, 'pc3': 2});
        data.push({'pc1': 2, 'pc2': 1, 'pc3': 2});

        grid = new Slick.Grid('#fooligans', data, columns, options);
      },
      teardown: function() {
        this.sharedDecompositionViewDict = undefined;
        $('#fooligans').remove();
        this.decomp = undefined;
      }
    });

    test('Constructor tests', function(assert) {
      var container = $('<div id="no-exist" style="height:11px; ' +
                        'width:12px"></div>');

      assert.ok(ColorViewController.prototype instanceof EmperorAttributeABC);

      var controller = new ColorViewController(
        container, this.sharedDecompositionViewDict);
      equal(controller.title, 'Color');

      var testColumn = controller.bodyGrid.getColumns()[0];
      equal(testColumn.field, 'value');

      // verify the color value is set properly
      equal(controller.$colormapSelect.val(), 'discrete-coloring-qiime');
      equal(controller.$select.val(), 'SampleID');
    });

    test('Test _nonNumericPlottables', function() {
      var container = $('<div id="no-exist" style="height:11px; ' +
                        'width:12px"></div>');
      var controller = new ColorViewController(
        container, this.sharedDecompositionViewDict);
      var k = controller.getActiveDecompViewKey();
      var decompViewDict = controller.decompViewDict[k];

      var colors = {'14.7': '#f7fbff',
                    '14.2': '#f3f8fd',
                    'StringValue': '#e8f2fd'};
      var data = decompViewDict.setCategory(
        colors, ColorViewController.prototype.setPlottableAttributes, 'Mixed');
      var uniqueVars = ['14.7', '14.2', 'StringValue'];

      // Test all are string
      ColorViewController._nonNumericPlottables(uniqueVars, data);
      var plottables = ColorViewController._nonNumericPlottables(uniqueVars,
                                                                 data);
      var exp = [
        new Plottable(
            'PC.635',
            ['PC.635', 'StringValue', 'Fast', '20071112'],
            [-0.237661, 0.046053, -0.138136, 0.159061, -0.247485, -0.115211,
            -0.112864, 0.064794],
            1)
        ];
      deepEqual(plottables, exp);

      // Test all are numeric
      var colors = {'20070314': '#f7fbff', '20071112': '#f3f8fd'};
      var data = decompViewDict.setCategory(
        colors, ColorViewController.prototype.setPlottableAttributes, 'DOB');
      var uniqueVars = ['20070314', '20071112'];
      var plottables = ColorViewController._nonNumericPlottables(uniqueVars,
                                                                 data);
      deepEqual(plottables, []);
    });

    test('Test discrete colors are retrieved correctly', function() {
      deepEqual(ColorViewController.getDiscreteColors([0, 1, 2]),
                {0: '#ff0000', 1: '#0000ff', 2: '#f27304'});
    });

    test('Test discrete colors are retrieved on roll-over', function() {
      var fifteen = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
      var obs = ColorViewController.getDiscreteColors(fifteen, 'Pastel1');
      var exp = {'0': '#fbb4ae', '1': '#b3cde3', '2': '#ccebc5',
                 '3': '#decbe4', '4': '#fed9a6', '5': '#ffffcc',
                 '6': '#e5d8bd', '7': '#fddaec', '8': '#f2f2f2',
                 '9': '#fbb4ae', '10': '#b3cde3', '11': '#ccebc5',
                 '12': '#decbe4', '13': '#fed9a6', '14': '#ffffcc'};
      deepEqual(obs, exp);
    });

    test('Test discrete colors with other maps', function() {
      deepEqual(ColorViewController.getDiscreteColors([0], 'Set1'),
                {0: '#e41a1c'});
    });


    test('Test getScaledColors', function() {
      var five = ['0', '1', '2', '3', '4'];
      var color = ColorViewController.getScaledColors(five, 'Viridis');
      deepEqual(color, [{0: '#440154', 1: '#3f4a8a', 2: '#26838f',
                         3: '#6cce5a', 4: '#fee825'},
        '<defs><linearGradient id="Gradient" x1="0" x2="0" y1="1" y2="0">' +
        '<stop offset="0%" stop-color="#440154"/>' +
        '<stop offset="1%" stop-color="#440456"/>' +
        '<stop offset="2%" stop-color="#440759"/>' +
        '<stop offset="3%" stop-color="#440a5c"/>' +
        '<stop offset="4%" stop-color="#450d5f"/>' +
        '<stop offset="5%" stop-color="#451062"/>' +
        '<stop offset="6%" stop-color="#451364"/>' +
        '<stop offset="7%" stop-color="#461667"/>' +
        '<stop offset="8%" stop-color="#46196a"/>' +
        '<stop offset="9%" stop-color="#461c6d"/>' +
        '<stop offset="10%" stop-color="#471f70"/>' +
        '<stop offset="11%" stop-color="#472272"/>' +
        '<stop offset="12%" stop-color="#472575"/>' +
        '<stop offset="13%" stop-color="#472877"/>' +
        '<stop offset="14%" stop-color="#462b79"/>' +
        '<stop offset="15%" stop-color="#462e7a"/>' +
        '<stop offset="16%" stop-color="#45307c"/>' +
        '<stop offset="17%" stop-color="#44337d"/>' +
        '<stop offset="18%" stop-color="#44367f"/>' +
        '<stop offset="19%" stop-color="#433980"/>' +
        '<stop offset="20%" stop-color="#423c82"/>' +
        '<stop offset="21%" stop-color="#413e83"/>' +
        '<stop offset="22%" stop-color="#414185"/>' +
        '<stop offset="23%" stop-color="#404486"/>' +
        '<stop offset="24%" stop-color="#3f4788"/>' +
        '<stop offset="25%" stop-color="#3f4a8a"/>' +
        '<stop offset="26%" stop-color="#3d4c8a"/>' +
        '<stop offset="27%" stop-color="#3c4e8a"/>' +
        '<stop offset="28%" stop-color="#3b508a"/>' +
        '<stop offset="29%" stop-color="#3a538b"/>' +
        '<stop offset="30%" stop-color="#39558b"/>' +
        '<stop offset="31%" stop-color="#38578b"/>' +
        '<stop offset="32%" stop-color="#375a8c"/>' +
        '<stop offset="33%" stop-color="#365c8c"/>' +
        '<stop offset="34%" stop-color="#345e8c"/>' +
        '<stop offset="35%" stop-color="#33618d"/>' +
        '<stop offset="36%" stop-color="#32638d"/>' +
        '<stop offset="37%" stop-color="#31658d"/>' +
        '<stop offset="38%" stop-color="#30688e"/>' +
        '<stop offset="39%" stop-color="#2f6a8e"/>' +
        '<stop offset="40%" stop-color="#2e6c8e"/>' +
        '<stop offset="41%" stop-color="#2d6e8e"/>' +
        '<stop offset="42%" stop-color="#2d718e"/>' +
        '<stop offset="43%" stop-color="#2c738e"/>' +
        '<stop offset="44%" stop-color="#2b758e"/>' +
        '<stop offset="45%" stop-color="#2a778e"/>' +
        '<stop offset="46%" stop-color="#297a8e"/>' +
        '<stop offset="47%" stop-color="#287c8e"/>' +
        '<stop offset="48%" stop-color="#277e8e"/>' +
        '<stop offset="49%" stop-color="#26808e"/>' +
        '<stop offset="50%" stop-color="#26838f"/>' +
        '<stop offset="51%" stop-color="#25858e"/>' +
        '<stop offset="52%" stop-color="#24878e"/>' +
        '<stop offset="53%" stop-color="#24898d"/>' +
        '<stop offset="54%" stop-color="#238b8d"/>' +
        '<stop offset="55%" stop-color="#238d8d"/>' +
        '<stop offset="56%" stop-color="#228f8c"/>' +
        '<stop offset="57%" stop-color="#22918c"/>' +
        '<stop offset="58%" stop-color="#21938b"/>' +
        '<stop offset="59%" stop-color="#20958b"/>' +
        '<stop offset="60%" stop-color="#20978b"/>' +
        '<stop offset="61%" stop-color="#1f998a"/>' +
        '<stop offset="62%" stop-color="#1f9b8a"/>' +
        '<stop offset="63%" stop-color="#229e88"/>' +
        '<stop offset="64%" stop-color="#28a284"/>' +
        '<stop offset="65%" stop-color="#2ea680"/>' +
        '<stop offset="66%" stop-color="#34aa7c"/>' +
        '<stop offset="67%" stop-color="#3aae78"/>' +
        '<stop offset="68%" stop-color="#40b274"/>' +
        '<stop offset="69%" stop-color="#47b671"/>' +
        '<stop offset="70%" stop-color="#4dba6d"/>' +
        '<stop offset="71%" stop-color="#53be69"/>' +
        '<stop offset="72%" stop-color="#59c265"/>' +
        '<stop offset="73%" stop-color="#5fc661"/>' +
        '<stop offset="74%" stop-color="#65ca5d"/>' +
        '<stop offset="75%" stop-color="#6cce5a"/>' +
        '<stop offset="76%" stop-color="#71cf56"/>' +
        '<stop offset="77%" stop-color="#77d052"/>' +
        '<stop offset="78%" stop-color="#7dd14e"/>' +
        '<stop offset="79%" stop-color="#83d34a"/>' +
        '<stop offset="80%" stop-color="#89d447"/>' +
        '<stop offset="81%" stop-color="#8fd543"/>' +
        '<stop offset="82%" stop-color="#95d63f"/>' +
        '<stop offset="83%" stop-color="#9bd83b"/>' +
        '<stop offset="84%" stop-color="#a1d938"/>' +
        '<stop offset="85%" stop-color="#a7da34"/>' +
        '<stop offset="86%" stop-color="#addc30"/>' +
        '<stop offset="87%" stop-color="#b3dd2c"/>' +
        '<stop offset="88%" stop-color="#b8de2a"/>' +
        '<stop offset="89%" stop-color="#bedf2a"/>' +
        '<stop offset="90%" stop-color="#c4e029"/>' +
        '<stop offset="91%" stop-color="#cae029"/>' +
        '<stop offset="92%" stop-color="#cfe128"/>' +
        '<stop offset="93%" stop-color="#d5e228"/>' +
        '<stop offset="94%" stop-color="#dbe327"/>' +
        '<stop offset="95%" stop-color="#e1e427"/>' +
        '<stop offset="96%" stop-color="#e6e426"/>' +
        '<stop offset="97%" stop-color="#ece526"/>' +
        '<stop offset="98%" stop-color="#f2e625"/>' +
        '<stop offset="99%" stop-color="#f8e725"/></linearGradient></defs>' +
        '<rect id="gradientRect" width="20" height="95%" ' +
        'fill="url(#Gradient)"/><text x="25" y="12px" ' +
        'font-family="sans-serif" font-size="12px" text-anchor="start">4' +
        '</text><text x="25" y="50%" font-family="sans-serif" ' +
        'font-size="12px" text-anchor="start">2</text><text x="25" y="95%" ' +
        'font-family="sans-serif" font-size="12px" text-anchor="start">0</text>'
      ]);
    });

    test('Test getInterpolatedColors', function() {
      var five = ['0', '1', '2', '3', '4'];
      var color = ColorViewController.getInterpolatedColors(five, 'Viridis');
      deepEqual(color, { '0': '#440154', '1':
        '#424c79', '2': '#30758c', '3': '#398f8b', '4': '#8cb373' });
    });

    test('Test ColorViewController.getScaledColors exceptions', function() {
      var five = ['0', 'string1', 'string2', 'string3', 'string4'];

      throws(
          function() {
            var color = ColorViewController.getScaledColors(five, 'Viridis');
          },
          Error,
          'An error is raised if there are not 2+ numeric values'
          );
    });

    test('Test ColorViewController.getColorList works', function() {
      var one, five, ten, twenty, scaled, colors;

      one = [0];
      five = [0, 1, 2, 3, 4];
      ten = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
      twenty = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                18, 19];
      scaled = [0, 1, 2, 3, 7, 20, 50];

      colors = ColorViewController.getColorList(scaled, 'Blues', false, true);
      deepEqual(colors[0], {'0': '#f7fbff', '1': '#f3f8fd', '2': '#eff5fc',
                            '20': '#93c4de', '3': '#ebf3fb', '50': '#08306b',
                            '7': '#dbe9f6'});
      equal(colors[1], '<defs><linearGradient id=\"Gradient\" ' +
        'x1=\"0\" x2=\"0\" y1=\"1\" y2=\"0\">' +
        '<stop offset=\"0%\" stop-color=\"#f7fbff\"/>' +
        '<stop offset=\"1%\" stop-color=\"#f5f9fe\"/>' +
        '<stop offset=\"2%\" stop-color=\"#f3f8fd\"/>' +
        '<stop offset=\"3%\" stop-color=\"#f1f7fd\"/>' +
        '<stop offset=\"4%\" stop-color=\"#eff5fc\"/>' +
        '<stop offset=\"5%\" stop-color=\"#edf4fb\"/>' +
        '<stop offset=\"6%\" stop-color=\"#ebf3fb\"/>' +
        '<stop offset=\"7%\" stop-color=\"#e9f2fa\"/>' +
        '<stop offset=\"8%\" stop-color=\"#e7f0f9\"/>' +
        '<stop offset=\"9%\" stop-color=\"#e5eff9\"/>' +
        '<stop offset=\"10%\" stop-color=\"#e3eef8\"/>' +
        '<stop offset=\"11%\" stop-color=\"#e1ecf7\"/>' +
        '<stop offset=\"12%\" stop-color=\"#dfebf7\"/>' +
        '<stop offset=\"13%\" stop-color=\"#ddeaf6\"/>' +
        '<stop offset=\"14%\" stop-color=\"#dbe9f6\"/>' +
        '<stop offset=\"15%\" stop-color=\"#d9e7f5\"/>' +
        '<stop offset=\"16%\" stop-color=\"#d7e6f4\"/>' +
        '<stop offset=\"17%\" stop-color=\"#d5e5f4\"/>' +
        '<stop offset=\"18%\" stop-color=\"#d3e3f3\"/>' +
        '<stop offset=\"19%\" stop-color=\"#d1e2f2\"/>' +
        '<stop offset=\"20%\" stop-color=\"#cfe1f2\"/>' +
        '<stop offset=\"21%\" stop-color=\"#cde0f1\"/>' +
        '<stop offset=\"22%\" stop-color=\"#cbdef0\"/>' +
        '<stop offset=\"23%\" stop-color=\"#c9ddf0\"/>' +
        '<stop offset=\"24%\" stop-color=\"#c7dcef\"/>' +
        '<stop offset=\"25%\" stop-color=\"#c6dbef\"/>' +
        '<stop offset=\"26%\" stop-color=\"#c2d9ed\"/>' +
        '<stop offset=\"27%\" stop-color=\"#bfd8ec\"/>' +
        '<stop offset=\"28%\" stop-color=\"#bcd6eb\"/>' +
        '<stop offset=\"29%\" stop-color=\"#b9d5ea\"/>' +
        '<stop offset=\"30%\" stop-color=\"#b6d4e9\"/>' +
        '<stop offset=\"31%\" stop-color=\"#b2d2e8\"/>' +
        '<stop offset=\"32%\" stop-color=\"#afd1e7\"/>' +
        '<stop offset=\"33%\" stop-color=\"#acd0e6\"/>' +
        '<stop offset=\"34%\" stop-color=\"#a9cee4\"/>' +
        '<stop offset=\"35%\" stop-color=\"#a6cde3\"/>' +
        '<stop offset=\"36%\" stop-color=\"#a2cce2\"/>' +
        '<stop offset=\"37%\" stop-color=\"#9fcae1\"/>' +
        '<stop offset=\"38%\" stop-color=\"#9bc8e0\"/>' +
        '<stop offset=\"39%\" stop-color=\"#97c6df\"/>' +
        '<stop offset=\"40%\" stop-color=\"#93c4de\"/>' +
        '<stop offset=\"41%\" stop-color=\"#8fc2dd\"/>' +
        '<stop offset=\"42%\" stop-color=\"#8bbfdd\"/>' +
        '<stop offset=\"43%\" stop-color=\"#87bddc\"/>' +
        '<stop offset=\"44%\" stop-color=\"#83bbdb\"/>' +
        '<stop offset=\"45%\" stop-color=\"#7fb9da\"/>' +
        '<stop offset=\"46%\" stop-color=\"#7bb6d9\"/>' +
        '<stop offset=\"47%\" stop-color=\"#77b4d8\"/>' +
        '<stop offset=\"48%\" stop-color=\"#73b2d7\"/>' +
        '<stop offset=\"49%\" stop-color=\"#6fb0d6\"/>' +
        '<stop offset=\"50%\" stop-color=\"#6baed6\"/>' +
        '<stop offset=\"51%\" stop-color=\"#67abd4\"/>' +
        '<stop offset=\"52%\" stop-color=\"#64a9d3\"/>' +
        '<stop offset=\"53%\" stop-color=\"#61a7d2\"/>' +
        '<stop offset=\"54%\" stop-color=\"#5da5d0\"/>' +
        '<stop offset=\"55%\" stop-color=\"#5aa2cf\"/>' +
        '<stop offset=\"56%\" stop-color=\"#57a0ce\"/>' +
        '<stop offset=\"57%\" stop-color=\"#549ecd\"/>' +
        '<stop offset=\"58%\" stop-color=\"#509ccb\"/>' +
        '<stop offset=\"59%\" stop-color=\"#4d99ca\"/>' +
        '<stop offset=\"60%\" stop-color=\"#4a97c9\"/>' +
        '<stop offset=\"61%\" stop-color=\"#4695c7\"/>' +
        '<stop offset=\"62%\" stop-color=\"#4393c6\"/>' +
        '<stop offset=\"63%\" stop-color=\"#4090c5\"/>' +
        '<stop offset=\"64%\" stop-color=\"#3e8ec3\"/>' +
        '<stop offset=\"65%\" stop-color=\"#3b8bc2\"/>' +
        '<stop offset=\"66%\" stop-color=\"#3888c1\"/>' +
        '<stop offset=\"67%\" stop-color=\"#3686bf\"/>' +
        '<stop offset=\"68%\" stop-color=\"#3383be\"/>' +
        '<stop offset=\"69%\" stop-color=\"#3080bd\"/>' +
        '<stop offset=\"70%\" stop-color=\"#2e7ebb\"/>' +
        '<stop offset=\"71%\" stop-color=\"#2b7bba\"/>' +
        '<stop offset=\"72%\" stop-color=\"#2878b9\"/>' +
        '<stop offset=\"73%\" stop-color=\"#2676b7\"/>' +
        '<stop offset=\"74%\" stop-color=\"#2373b6\"/>' +
        '<stop offset=\"75%\" stop-color=\"#2171b5\"/>' +
        '<stop offset=\"76%\" stop-color=\"#1f6eb3\"/>' +
        '<stop offset=\"77%\" stop-color=\"#1c6bb1\"/>' +
        '<stop offset=\"78%\" stop-color=\"#1a69af\"/>' +
        '<stop offset=\"79%\" stop-color=\"#1866ad\"/>' +
        '<stop offset=\"80%\" stop-color=\"#1664ab\"/>' +
        '<stop offset=\"81%\" stop-color=\"#1461a9\"/>' +
        '<stop offset=\"82%\" stop-color=\"#135fa7\"/>' +
        '<stop offset=\"83%\" stop-color=\"#115ca5\"/>' +
        '<stop offset=\"84%\" stop-color=\"#0f59a3\"/>' +
        '<stop offset=\"85%\" stop-color=\"#0d57a1\"/>' +
        '<stop offset=\"86%\" stop-color=\"#0b549f\"/>' +
        '<stop offset=\"87%\" stop-color=\"#09529d\"/>' +
        '<stop offset=\"88%\" stop-color=\"#084f9a\"/>' +
        '<stop offset=\"89%\" stop-color=\"#084d96\"/>' +
        '<stop offset=\"90%\" stop-color=\"#084a92\"/>' +
        '<stop offset=\"91%\" stop-color=\"#08478e\"/>' +
        '<stop offset=\"92%\" stop-color=\"#08458a\"/>' +
        '<stop offset=\"93%\" stop-color=\"#084286\"/>' +
        '<stop offset=\"94%\" stop-color=\"#083f82\"/>' +
        '<stop offset=\"95%\" stop-color=\"#083d7e\"/>' +
        '<stop offset=\"96%\" stop-color=\"#083a7a\"/>' +
        '<stop offset=\"97%\" stop-color=\"#083776\"/>' +
        '<stop offset=\"98%\" stop-color=\"#083572\"/>' +
        '<stop offset=\"99%\" stop-color=\"#08326e\"/>' +
        '<stop offset=\"100%\" stop-color=\"#08306b\"/>' +
        '</linearGradient></defs><rect id=\"gradientRect\" width=\"20\" ' +
        'height=\"95%\" fill=\"url(#Gradient)\"/><text x=\"25\" y=\"12px\" ' +
        'font-family=\"sans-serif\" font-size=\"12px\" text-anchor=\"start\">' +
        '50</text><text x=\"25\" y=\"50%\" font-family=\"sans-serif\" ' +
        'font-size=\"12px\" text-anchor=\"start\">25</text><text x=\"25\" ' +
        'y=\"95%\" font-family=\"sans-serif\" font-size=\"12px\" ' +
        'text-anchor=\"start\">0</text>');

      deepEqual(ColorViewController.getColorList(five, 'Set1', true),
                [{'0': '#e41a1c', '1': '#377eb8', '2': '#4daf4a',
                  '3': '#984ea3', '4': '#ff7f00'}, undefined]);

      deepEqual(ColorViewController.getColorList(twenty, 'BrBG', false),
                [{'0': '#543005', '1': '#6e4a1c', '2': '#866231',
                  '3': '#9c7a46', '4': '#b0905a', '5': '#c1a46e',
                  '6': '#d1b681', '7': '#dec693', '8': '#e9d4a4',
                  '9': '#f1dfb4', '10': '#f6e8c3', '11': '#f4e9cb',
                  '12': '#efe9d1', '13': '#e6e6d3', '14': '#dae1d2',
                  '15': '#c9dace', '16': '#b6d1c7', '17': '#9ec6bd',
                  '18': '#82b8b1', '19': '#61a9a1'}, undefined]);

      deepEqual(ColorViewController.getColorList(one, 'OrRd', false),
                [{'0': '#fff7ec'}, undefined]);
      deepEqual(ColorViewController.getColorList(one, 'RdGy', true),
                [{'0': '#67001f'}, undefined]);

    });

    test('Test ColorViewController.getColorList exceptions', function() {
      var five;
      five = [0, 1, 2, 3, 4];
      throws(
          function() {
            ColorViewController.getColorList(five, false, 'Non-existant');
          },
          Error,
          'An error is raised if the colormap does not exist'
          );

      five = [0, 'string1', 'string2', 'string3', 'string4'];
      throws(
          function() {
            ColorViewController.getColorList(five, 'Blues', false, true);
          },
          Error,
          'Error is raised if there are less than 2 numeric values when scaled'
          );
    });

    test('Testing setPlottableAttributes helper function', function(assert) {
      // testing with one plottable
      var idx = 0;
      plottables = [{idx: idx}];
      equal(this.dv.markers[idx].material.color.getHexString(), 'ff0000');
      equal(this.dv.markers[idx + 1].material.color.getHexString(), 'ff0000');
      ColorViewController.prototype.setPlottableAttributes(this.dv, '#00ff00',
                                                           plottables);
      equal(this.dv.markers[idx].material.color.getHexString(), '00ff00');
      equal(this.dv.markers[idx + 1].material.color.getHexString(), 'ff0000');
      equal(this.dv.needsUpdate, true);

      // testing with multiple plottable
      plottables = [{idx: idx}, {idx: idx + 1}];
      ColorViewController.prototype.setPlottableAttributes(this.dv, '#000000',
                                                           plottables);
      equal(this.dv.markers[idx].material.color.getHexString(), '000000');
      equal(this.dv.markers[idx + 1].material.color.getHexString(), '000000');
      equal(this.dv.needsUpdate, true);
    });

    test('Testing toJSON', function() {
      var container = $('<div style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(
        container, this.sharedDecompositionViewDict);
      // Change color on one point
      var idx = 0;
      plottables = [{idx: idx}];
      ColorViewController.prototype.setPlottableAttributes(this.dv, '#00ff00',
                                                           plottables);

      var obs = controller.toJSON();
      var exp = {category: 'SampleID',
                 colormap: 'discrete-coloring-qiime',
                 continuous: false,
                 data: {'PC.636': '#ff0000', 'PC.635': '#0000ff',
                        'PC.634': '#f27304'}};
      deepEqual(obs, exp);
    });

    test('Testing fromJSON', function() {
      var json = {category: 'DOB',
                  colormap: 'discrete-coloring-qiime',
                  continuous: false,
                  data: {20070314: '#ff0000', 20071112: '#0000ff'}};

      var container = $('<div style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(
        container, this.sharedDecompositionViewDict);

      controller.fromJSON(json);
      var idx = 0;
      var markers = controller.decompViewDict.scatter.markers;
      equal(markers[idx].material.color.getHexString(), 'ff0000');
      equal(markers[idx + 1].material.color.getHexString(), '0000ff');
      equal(markers[idx + 2].material.color.getHexString(), '0000ff');
      equal(controller.$select.val(), 'DOB');
      equal(controller.$colormapSelect.val(), 'discrete-coloring-qiime');
      equal(controller.$scaled.is(':checked'), false);
    });

    test('Testing fromJSON scaled', function() {
      var json = {category: 'Mixed', colormap: 'Viridis',
                  continuous: true, data: {'Non-numeric values': '#ae1221'}};

      var container = $('<div style="height:11px; width:12px"></div>');
      var controller = new ColorViewController(
        container, this.sharedDecompositionViewDict);

      controller.fromJSON(json);
      var idx = 0;
      var markers = controller.decompViewDict.scatter.markers;
      equal(markers[idx].material.color.getHexString(), '440154');
      equal(markers[idx + 1].material.color.getHexString(), 'ae1221');
      equal(markers[idx + 2].material.color.getHexString(), 'fee825');
      equal(controller.$select.val(), 'Mixed');
      equal(controller.$colormapSelect.val(), 'Viridis');
      equal(controller.$scaled.is(':checked'), true);
    });
  });
});
