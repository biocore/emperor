.. _js_integration:

.. index:: js_integration

Integrating Emperor's JavaScript API with other applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Emperor provides a rich API to manipulate the application live from the
browser. The majority of this functionality is provided by attribute (Color,
Visibility, Opacity, etc), or if needed the underlying `THREE` objects can
be accessed as needed. For more information, the documentation for the
``EmperorController`` and other JavaScript classes can be accessed `here
<../jsdoc/index.html>`_.


In general, users won't need to do low-level manipulation of visual aspects but
instead would like to subscribe to specific events and act as needed. For these
cases, Emperor provides access to the following events:

- When a sample is clicked (``click``).
- When a sample is double-clicked (``dblclick``).
- When a group of samples is selected (``select``).
- When the selected metadata category in a tab is changed (``category-changed``).
- When an attribute for a group of samples is changed (for example when a
  metadata value's color or visibility is changed) (``value-changed``).
- When a group of samples is double-clicked via a tab (``value-double-clicked``).
- For animations the following events are also published ``animation-started``,
  ``animation-new-frame-started``, ``animation-ended``, ``animation-paused``,
  and ``animation-cancelled``.


Subscribing to Events from a 3rd Party application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Custom code can be optionally executed via the ``Emperor.js_on_ready`` attribute.
For example to set callbacks when a sample is clicked you can insert the
following block of code.

.. code-block:: python

    # this JavaScript code is executed when the UI finishes loading
    callback = """
    plotView.on('click', function(sampleName){
      console.log('One sample was clicked', sampleName);
    });
    """
    # viz is an Emperor object, for example: viz = Emperor(...)
    viz.js_on_ready = callback


For convenience, this block is inserted in a closure with the following two
objects: ``EmperorController`` (``ec``) and a ``ScenePlotView3D``
(``plotView``). The first object orchestrates and organizes all the controllers
available in Emperor. ``plotView`` is mainly used to render plots and interact
with the rendered objects.

``plotView`` publishes a ``click``, ``dblclick``, and a ``select`` event when a
sample is clicked, double-clicked or when a group of samples is selected. The
block shows how you would subscribe to the ``dblclick`` and the ``select``
events.

.. code-block:: javascript

    plotView.on('dblclick', function(sampleName){
      console.log('One sample was double-clicked', sampleName);
    });
    plotView.on('select', function(samples, view){
      console.log(samples.length, 'samples were selected');
    });


The following example shows how to use the ``EmperorController`` (``ec``) to
subscribe to the following events:

- When a metadata category changes in the **color** tab.

- When a value changes in the **visibility** tab.

- When a metadata value is double-clicked in the **opacity** tab.


.. code-block:: javascript

    ec.controllers.color.addEventListener('category-changed',
                                          function(container){
      console.log('Name of the event', container.type);
      console.log('Selected metadata category', container.message.category);

      // this is an instance of the color controller
      console.log('Attribute controller', container.message.controller);
    });
    
    ec.controllers.visibility.addEventListener('value-changed',
                                               function(container){
      console.log('Name of the event', container.type);
      console.log('Selected category', container.message.category);

      // the new visibility attribute
      console.log('New attribute', container.message.attribute)

      // the group of samples affected by the change
      console.log('Group of samples', container.message.group)

      // this is an instance of the visibility controller
      console.log('Attribute controller', container.message.controller);
    });
    
    ec.controllers.opacity.addEventListener('value-double-clicked',
                                            function(container){
      console.log('Name of the event', container.type);

      // the attribute and name of the element that was double clicked
      console.log('Metadata group', container.message.category);
      console.log('Opacity value', container.message.attribute)

      // the group of samples that was double-clicked
      console.log('Group of samples', container.message.group)

      // this is an instance of the opacity controller
      console.log('Attribute controller', container.message.controller);
    });
