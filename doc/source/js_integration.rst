.. _js_integration:

.. index:: js_integration

Integrating Emperor's JavaScript API with other applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Emperor provides a rich API to manipulate the application live from the
browser. The majority of this functionality is provided by attribute (Color,
Visibility, Opacity, etc), or if needed the underlying `THREE` objects can
be accessed as needed. For more information, the documentation for the
`EmperorController` and other JavaScript classes can be accessed `here
<../jsdoc/index.html>`_.


In general, users won't need to do low-level manipulation of visual aspects but
instead would like to subscribe to specific events and act as needed. For these
cases, Emperor provides access to the following events:

- When a sample is clicked (`click`).
- When a sample is double-clicked (`dblclick`).
- When a group of samples is selected (`select`).
- When the selected metadata category in a tab is changed (`category-changed`).
- When an attribute for a group of samples is changed (for example when a
  metadata value's color or visibility is changed) (`value-changed`).
- When a group of samples is double-clicked via a tab (`value-double-clicked`).


Subscribing to Events from a 3rd Party application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For sample clicking, double-clicking and selection three special tags are
provided for users to insert their custom code:

- `/*__click_callback*/`: This callback receives an object with the sample that
  was clicked.
- `/*__dblclick_callback*/`: This callback receives an object with the sample
  that was double-clicked.
- `/*__select_callback*/`: This callback receives a list of the selected
  objects.

The rest of the callbacks are recommended to be written and inserted
via the `/*__custom_on_ready_code__*/`. This code is executed once all the
controllers have finished loading and can accept subscriptions to events.

The following example shows how we would subscribe to metadata category changes
in the **color** tab, **visibility** values changing for a metadata value, and
when a metadata value is double-clicked in the **opacity** table.

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


And in order to insert the custom code you can use Python's string replacement
operations:


.. code-block:: python

    viz = Emperor(...)

    # custom JS - this example prints the name of the sample when that sample is
    # clicked
    html = str(viz).replace('/*__custom_on_ready_code__*/', 'console.log(sample)')
