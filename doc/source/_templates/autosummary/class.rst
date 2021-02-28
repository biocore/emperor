{# This template was modified from scikit-bio's #}
{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% if attributes %}
   .. rubric:: Attributes

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}

   {% if built_in_methods %}
   .. rubric:: Built-ins

   .. autosummary::
      :toctree:
   {% for item in built_in_methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}

   {% if methods %}
   .. rubric:: Methods

   .. autosummary::
      :toctree:
   {% for item in methods %}
      {% if item != '__init__' %}
      ~{{ name }}.{{ item }}
      {% endif %}
   {%- endfor %}
   {% endif %}
