define([
    'jquery',
    'underscore',
    'contextmenu',
    'three',
    'view',
    'scene3d',
    'colorviewcontroller',
    'visibilitycontroller',
    'shapecontroller',
    'axescontroller',
    'scaleviewcontroller',
    'filesaver'
], function($, _, contextMenu, THREE, DecompositionView, ScenePlotView3D,
             ColorViewController, VisibilityController, ShapeController,
             AxesController, ScaleViewController, FileSaver) {

  /**
   *
   * @class EmperorController
   *       This is the application controller
   *
   * The application controller, contains all the information on how the model
   * is being presented to the user.
   *
   * @param {DecompositionModel} dm An object that will be represented on
   * screen.
   * @param {string} divId The element id where the controller should
   * instantiate itself.
   * @param {node} [webglcanvas = undefined] the canvas to use to render the
   * information. This parameter is optional, and should rarely be set. But is
   * useful for external applications like SAGE2.
   *
   * @return {EmperorController}
   * @constructs EmperorController
   *
   */
  function EmperorController(dm, divId, webglcanvas) {
    var scope = this;

    /**
     * Scaling constant for grid dimensions (read only).
     * @type {float}
     */
    this.GRID_SCALE = 0.97;

    /**
     * Scaling constant for scene plot view dimensions
     * @type {float}
     */
    this.SCENE_VIEW_SCALE = 0.5;
    /**
     * jQuery object where the object lives in.
     * @type {node}
     */
    this.$divId = $('#' + divId);
    /**
     * Width of the object.
     * @type {float}
     */
    this.width = this.$divId.width();
    /**
     * Height of the object.
     * @type {float}
     */
    this.height = this.$divId.height();

    /**
     * Ordination data being plotted.
     * @type {DecompositionModel}
     */
    this.dm = dm;
    /**
     * List of the scene plots views being rendered.
     * @type {ScenePlotView3D[]}
     */
    this.sceneViews = [];

    /**
     * Internal div where the menus live in (jQuery object).
     * @type {node}
     */
    this.$plotSpace = $("<div class='emperor-plot-wrapper'></div>");
    /**
     * Internal div where the plots live in (jQuery object).
     * @type {node}
     */
    this.$plotMenu = $("<div class='emperor-plot-menu'></div>");

    this.$divId.append(this.$plotSpace);
    this.$divId.append(this.$plotMenu);

    /**
     * Holds a reference to all the tabs (view controllers) in the `$plotMenu`.
     * @type {object}
     */
    this.controllers = {};

    /**
     * Background color of the scene.
     * @type {THREE.Color}
     * @default 0x00000000
     */
    this.rendererBackgroundColor = new THREE.Color();
    this.rendererBackgroundColor.setHex('0x000000');

    /**
     * Object in charge of doing the rendering of the scenes.
     * @type {THREE.Renderer}
     */
    this.renderer = null;
    if (webglcanvas !== undefined) {
        this.renderer = new THREE.WebGLRenderer({canvas: webglcanvas,
                                                 antialias: true});
    }
    else {
        this.renderer = new THREE.WebGLRenderer({antialias: true});
    }

    this.renderer.setSize(this.width, this.height);
    this.renderer.setClearColor(this.rendererBackgroundColor);
    this.renderer.autoClear = false;
    this.renderer.sortObjects = true;
    this.$plotSpace.append(this.renderer.domElement);

    /**
     * Menu tabs containers, note that we need them in this format to have
     * jQuery's UI tabs work properly. All the view controllers will be added
     * to this container, see the addTab method
     * @see EmperorController.addTab
     * @type {node}
     * @private
     */
    this._$tabsContainer = $("<div name='emperor-tabs-container'></div>");
    this._$tabsContainer.css('background-color', '#EEEEEE');
    /**
     * List of available tabs, lives inside `_$tabsContainer`.
     * @type {node}
     * @private
     */
    this._$tabsList = $("<ul name='emperor-tabs-list'></ul>");

    // These will both live in the menu space. As of the writing of this code
    // there's nothing else but tabs on the menu, but this may change in the
    // future, that's why we are creating the extra "tabsContainer" div
    this.$plotMenu.append(this._$tabsContainer);
    this._$tabsContainer.append(this._$tabsList);

    /**
     * Object with all the available decomposition views.
     *
     * FIXME: This is a hack to go around the fact that the constructor takes
     * a single decomposition model instead of a dictionary
     *
     * @type {object}
     */
    this.decViews = {'scatter': new DecompositionView(this.dm)};

    // default decomposition view uses the full window
    this.addView();

    $(function() {
      scope._buildUI();
      // Hide the loading splashscreen
      scope.$divId.find('.loading').hide();
    });

    // once the object finishes loading, resize the contents so everything fits
    // nicely
    $(this).ready(function() {
      scope.resize(scope.$divId.width(), scope.$divId.height());
    });

  };

  /**
   *
   * Helper method to add additional ScenePlotViews (i.e. another plot)
   *
   */
  EmperorController.prototype.addView = function() {
    if (this.sceneViews.length > 4) {
      throw Error('Cannot add another scene plot view');
    }

    var spv = new ScenePlotView3D(this.renderer, this.decViews,
                                  this.$plotSpace, 0, 0, 0, 0);
    this.sceneViews.push(spv);

    // this will setup the appropriate sizes and widths
    this.resize(this.width, this.height);
  };

  /**
   *
   * Helper method to resize the plots
   *
   * @param {width} the width of the entire plotting space
   * @param {height} the height of the entire plotting space
   *
   */
  EmperorController.prototype.resize = function(width, height) {
    // update the available space we have
    this.width = width;
    this.height = height;

    this.$plotSpace.height(height);
    this.$plotMenu.height(height);

    this._$tabsContainer.height(height);

    // the area we have to present the plot is smaller than the total
    var plotWidth = this.$plotSpace.width();

    // TODO: The below will need refactoring
    // This is addressed in issue #405
    if (this.sceneViews.length === 1) {
      this.sceneViews[0].resize(0, 0, plotWidth, this.height);
    }
    else if (this.sceneViews.length === 2) {
      this.sceneViews[0].resize(0, 0, this.SCENE_VIEW_SCALE * plotWidth,
          this.height);
      this.sceneViews[1].resize(this.SCENE_VIEW_SCALE * plotWidth, 0,
          this.SCENE_VIEW_SCALE * plotWidth, this.height);
    }
    else if (this.sceneViews.length === 3) {
      this.sceneViews[0].resize(0, 0,
          this.SCENE_VIEW_SCALE * plotWidth,
          this.SCENE_VIEW_SCALE * this.height);
      this.sceneViews[1].resize(this.SCENE_VIEW_SCALE * plotWidth, 0,
          this.SCENE_VIEW_SCALE * plotWidth,
          this.SCENE_VIEW_SCALE * this.height);
      this.sceneViews[2].resize(0, this.SCENE_VIEW_SCALE * this.height,
          plotWidth, this.SCENE_VIEW_SCALE * this.height);
    }
    else if (this.sceneViews.length === 4) {
      this.sceneViews[0].resize(0, 0, this.SCENE_VIEW_SCALE * plotWidth,
          this.SCENE_VIEW_SCALE * this.height);
      this.sceneViews[1].resize(this.SCENE_VIEW_SCALE * plotWidth, 0,
          this.SCENE_VIEW_SCALE * plotWidth,
          this.SCENE_VIEW_SCALE * this.height);
      this.sceneViews[2].resize(0, this.SCENE_VIEW_SCALE * this.height,
          this.SCENE_VIEW_SCALE * plotWidth,
          this.SCENE_VIEW_SCALE * this.height);
      this.sceneViews[3].resize(this.SCENE_VIEW_SCALE * plotWidth,
          this.SCENE_VIEW_SCALE * this.height,
          this.SCENE_VIEW_SCALE * plotWidth,
          this.SCENE_VIEW_SCALE * this.height);
    }
    else {
      throw Error('More than four views are currently not supported');
    }

    this.renderer.setSize(plotWidth, this.height);

    /* Resizing the tabs (view controllers) */

    // resize the grid according to the size of the container, since we are
    // inside the tabs we have to account for that lost space.
    var tabHeight = this.$plotMenu.height() * this.GRID_SCALE;

    // the tab list at the top takes up a variable amount of space and
    // without this, the table displayed below will have an odd scrolling
    // behaviour
    tabHeight -= this._$tabsList.height();

    // for each controller, we need to (1) trigger the resize method, and (2)
    // resize the height of the containing DIV tag (we don't need to resize the
    // width as this is already taken care of since it just has to fit the
    // available space).
    _.each(this.controllers, function(controller, index) {
      if (controller !== undefined) {
        $('#' + controller.identifier).height(tabHeight);

        var w = $('#' + controller.identifier).width(),
            h = $('#' + controller.identifier).height();

        controller.resize(w, h);
      }
    });

    //Set all scenes to needing update
    for (var i = 0; i < this.sceneViews.length; i++) {
      this.sceneViews[i].needsUpdate = true;
    }
  };

  /**
   *
   * Helper method to render sceneViews, gets called every time the browser
   * indicates we can render a new frame, however it only triggers the
   * appropriate rendering functions if something has changed since the last
   * frame.
   *
   */
  EmperorController.prototype.render = function() {
    var scope = this;
    $.each(this.sceneViews, function(i, sv) {
      if (sv.checkUpdate()) {
        scope.renderer.setViewport(0, 0, scope.width, scope.height);
        scope.renderer.clear();
        sv.render();
      }
    });
  };

  /**
   *
   * Helper method to assemble UI, completely independent of HTML template.
   * This method is called when the object is constructed.
   *
   * @private
   *
   */
  EmperorController.prototype._buildUI = function() {
    var scope = this;

    //FIXME: This only works for 1 scene plot view
    this.controllers.color = this.addTab(this.sceneViews[0].decViews,
                                         ColorViewController);
    this.controllers.visibility = this.addTab(this.sceneViews[0].decViews,
                                              VisibilityController);
    this.controllers.shape = this.addTab(this.sceneViews[0].decViews,
                                         ShapeController);
    this.controllers.axes = this.addTab(this.sceneViews[0].decViews,
                                        AxesController);
    this.controllers.scale = this.addTab(this.sceneViews[0].decViews,
        ScaleViewController);

    // We are tabifying this div, I don't know man.
    this._$tabsContainer.tabs({heightStyle: 'fill',
                               // The tabs on the plot space only get resized
                               // when they are visible, thus we subscribe to
                               // the event that's fired after a user selects a
                               // tab.  If you don't do this, the width and
                               // height of each of the view controllers will
                               // be wrong.  We also found that subscribing to
                               // document.ready() wouldn't work either as the
                               // resize callback couldn't be executed on a tab
                               // that didn't exist yet.
                               activate: function(event, ui) {
                                 scope.resize(scope.$divId.width(),
                                              scope.$divId.height());
                               }});

    // Set up the context menu
    this.$contextMenu = $.contextMenu({
      // only tie this selector to our own container div, otherwise with
      // multiple plots on the same screen, this callback gets confused
      selector: '#' + scope.$divId.attr('id') + ' .emperor-plot-wrapper',
      trigger: 'none',
      items: {
        'saveState': {
          name: 'Save current settings',
          icon: 'edit',
          callback: function(key, opts) {
            scope.saveConfig();
          }
        },
        'loadState': {
          name: 'Load saved settings',
          icon: 'paste',
          callback: function(key, opts) {
            if (!FileReader) {
              alert('Your browser does not support file loading. We ' +
                    'recommend using Google Chrome for full functionality.');
              return;
            }
            var file = $('<input type="file">');
            file.on('change', function(evt) {
              var f = evt.target.files[0];
              // With help from
              // http://www.htmlgoodies.com/beyond/javascript/read-text-files-using-the-javascript-filereader.html
              var r = new FileReader();
              r.onload = function(e) {
                try {
                  var json = JSON.parse(e.target.result);
                } catch (err) {
                  alert('File given is not a JSON parsable file.');
                  return;
                }
                try {
                  scope.loadConfig(json);
                } catch (err) {
                  alert('Error loading settings from file: ' + err.message);
                  return;
                }
              };
              r.readAsText(f);
            });
            file.click();
          }
        },
        'sep1': '---------',
        'saveImage': {
          name: 'Save Image (PNG)',
          icon: 'edit',
          callback: function(key, opts) {
            scope.screenshot();
          }
        }
      }
    });

    // Add shift+right click as the trigger for the context menu
    this.$plotSpace.on('contextmenu', function(e) {
      if (e.shiftKey) {
        var contextDiv = $('#' + scope.$divId.attr('id') +
                           ' .emperor-plot-wrapper');
        contextDiv.contextMenu({x: e.pageX, y: e.pageY});
      }
    });
  };

  /**
   *
   * Save the current canvas view to a new window
   *
   * @param {string} [type = png] What format to save the file as.
   *
   */
  EmperorController.prototype.screenshot = function(type) {
    type = type || 'png';
    // Render all scenes so it's rendered in same context as save
    for (var i = 0; i < this.sceneViews.length; i++) {
      this.sceneViews[i].render();
    }
    var c = this.renderer.domElement.toDataURL('image/' + type);
    // Create DOM-less download link and click it to start download
    var download = $('<a href="' + c + '" download="emperor.' + type + '">');
    download.get(0).click();
  };

  /**
   *
   * Write settings file for the current controller settings
   *
   * The format is as follows: a javascript object with the camera position
   * stored in the 'cameraPosition' key and the quaternion in the
   * 'cameraQuaternion' key. Each controller in this.controllers is then saved
   * by calling toJSON on them, and the resulting object saved under the same
   * key as the controllers object.
   *
   */
   EmperorController.prototype.saveConfig = function() {
    var saveinfo = {};
    // Assuming single sceneview for now
    sceneview = this.sceneViews[0];
    saveinfo.cameraPosition = sceneview.camera.position;
    saveinfo.cameraQuaternion = sceneview.camera.quaternion;
    // Save settings for each controller in the view
     _.each(this.controllers, function(controller, index) {
      if (controller !== undefined) {
        saveinfo[index] = controller.toJSON();
      }
    });

    // Save the file
    var blob = new Blob([JSON.stringify(saveinfo)], {type: 'text/json'});
    saveAs(blob, 'emperor-settings.json');
   };

  /**
   *
   * Load a settings file and set all controller variables.
   *
   * This method will trigger a rendering callback.
   *
   * @param {object} json Information about the emperor session to load.
   *
   */
   EmperorController.prototype.loadConfig = function(json) {
    //still assuming one sceneview for now
    var sceneview = this.sceneViews[0];

    sceneview.camera.position.set(json.cameraPosition.x,
                                  json.cameraPosition.y,
                                  json.cameraPosition.z);
    sceneview.camera.quaternion.set(json.cameraQuaternion._x,
                                    json.cameraQuaternion._y,
                                    json.cameraQuaternion._z,
                                    json.cameraQuaternion._w);

    //must call updates to reset for camera move
    sceneview.camera.updateProjectionMatrix();
    sceneview.control.update();

    //load the rest of the controller settings
     _.each(this.controllers, function(controller, index) {
      if (controller !== undefined) {
        controller.fromJSON(json[index]);
      }
    });
    sceneview.needsUpdate = true;
   };

  /**
   *
   * Helper method to resize the plots.
   *
   * @param {DecompositionView[]} dvdict Dictionary of DecompositionViews.
   * @param {EmperorViewControllerABC} viewConstructor Constructor of the view
   * controller.
   *
   */
  EmperorController.prototype.addTab = function(dvdict, viewConstructor) {
    // nothing but a temporary id
    var id = (Math.round(1000000 * Math.random())).toString();

    this._$tabsContainer.append("<div id='" + id +
                                "' class='emperor-tab-div' ></div>");
    $('#' + id).height(this.$plotMenu.height() - this._$tabsList.height());

    // dynamically instantiate the controller, see:
    // http://stackoverflow.com/a/8843181
    var params = [null, '#' + id, dvdict];
    var obj = new (Function.prototype.bind.apply(viewConstructor, params));

    // set the identifier of the div to the one defined by the object
    $('#' + id).attr('id', obj.identifier);

    // now add the list element linking to the container div with the proper
    // title
    this._$tabsList.append("<li><a href='#" + obj.identifier + "'>" +
                           obj.title + '</a></li>');

    return obj;
  };

  return EmperorController;
});
