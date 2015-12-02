$(document).ready(function() {

  module("EmperorViewControllerABC", {

    setup: function(){
    },
    teardown: function(){
    }

  });

  /**
   *
   * Test that the constructor for EmperorViewControllerABC.
   *
   */
  test("Constructor tests", function(assert) {

    var container = $('<div id="does-not-exist"></div>');
    var controller = new EmperorViewControllerABC(container, 'foo', 'bar');

    equal(controller.title, 'foo', 'Check the title is correctly set');
    equal(controller.description, 'bar', 'Check the description is correctly'+
                                        ' set');
    equal(controller.$container.id, container.id, 'Check the id of the '+
                                                  'parent is correct');
    equal(controller.active, false, 'Check the active property');
    equal(controller.identifier.slice(0, 7), 'EMPtab-', 'Check the identifier'+
                                                        ' property');
    parseFloat(controller.identifier.slice(7));
    equal(controller.enabled, true, 'Check the enabled property');

    // check all the elements were successfully created
    assert.ok(controller.$canvas.length);
    assert.ok(controller.$header.length);
    assert.ok(controller.$body.length);

    assert.ok($.contains(controller.$canvas, controller.$header));
    assert.ok($.contains(controller.$canvas, controller.$body));
  });

  /**
   *
   * Test the enabled method
   *
   */
  test('Test the enabled method works', function(){

    var container = $('<div id="does-not-exist"></div>');
    var controller = new EmperorViewControllerABC(container, 'foo', 'bar');

    equal(controller.enabled, true);
    controller.setEnabled(false);
    equal(controller.enabled, false);

    throws(function(){
      controller.setEnabled('shenanigans');
    }, Error, 'setEnabled can only take a boolean');
  });

  /**
   *
   * Test the enabled method
   *
   */
  test('Test the setActive method works', function(){

    var container = $('<div id="does-not-exist"></div>');
    var controller = new EmperorViewControllerABC(container, 'foo', 'bar');

    equal(controller.active, false);
    controller.setActive(true);
    equal(controller.active, true);

    throws(function(){
      controller.setActive('shenanigans');
    }, Error, 'setActive can only take a boolean');
  });

  /**
   *
   * Test the resize, toJSON and fromJSON methods raise the appropriate errors.
   *
   */
  test('Test resize, toJSON and fromJSON methods', function(){

    var container = $('<div id="does-not-exist"></div>');
    var controller = EmperorViewControllerABC(container, 'foo', 'bar');
    throws(function(){
      controller.resize(10, 10);
    }, Error, 'Cannot call this abstract method');

    throws(function(){
      controller.fromJSON('{foo:11}');
    }, Error, 'Cannot call this abstract method');

    throws(function(){
      controller.toJSON();
    }, Error, 'Cannot call this abstract method');
  });



  module("EmperorAttributeABC", {

    setup: function(){
      sharedDecompositionViewDict = {}
      var decomp;

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
    },
    teardown: function(){
      sharedDecompositionViewDict = undefined;
    }
  });

  /**
   *
   * Test that the constructor for EmperorViewControllerABC.
   *
   */
  test("Constructor tests", function(assert) {

    var container = $('<div id="does-not-exist"></div>');
    var controller = new EmperorAttributeABC(container, 'foo', 'bar',
                                             sharedDecompositionViewDict);

    // verify the subclassing was set properly
    assert.ok(EmperorAttributeABC.prototype instanceof
              EmperorViewControllerABC);

    deepEqual(controller.

  });

  /**
   *
   * Test the enabled method
   *
   */
  test('Test the enabled method works', function(){

    var container = $('<div id="does-not-exist"></div>');
    var controller = new EmperorViewControllerABC(container, 'foo', 'bar');

    equal(controller.enabled, true);
    controller.setEnabled(false);
    equal(controller.enabled, false);

    throws(function(){
      controller.setEnabled('shenanigans');
    }, Error, 'setEnabled can only take a boolean');
  });

  /**
   *
   * Test the enabled method
   *
   */
  test('Test the setActive method works', function(){

    var container = $('<div id="does-not-exist"></div>');
    var controller = new EmperorViewControllerABC(container, 'foo', 'bar');

    equal(controller.active, false);
    controller.setActive(true);
    equal(controller.active, true);

    throws(function(){
      controller.setActive('shenanigans');
    }, Error, 'setActive can only take a boolean');
  });

  /**
   *
   * Test the resize, toJSON and fromJSON methods raise the appropriate errors.
   *
   */
  test('Test resize, toJSON and fromJSON methods', function(){

    var container = $('<div id="does-not-exist"></div>');
    var controller = EmperorViewControllerABC(container, 'foo', 'bar');
    throws(function(){
      controller.resize(10, 10);
    }, Error, 'Cannot call this abstract method');

    throws(function(){
      controller.fromJSON('{foo:11}');
    }, Error, 'Cannot call this abstract method');

    throws(function(){
      controller.toJSON();
    }, Error, 'Cannot call this abstract method');
  });


});
