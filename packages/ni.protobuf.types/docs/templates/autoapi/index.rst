API Reference
=============

This page contains auto-generated API reference documentation.

..
   Custom index: reference https://github.com/readthedocs/sphinx-autoapi/issues/298
   Add the top most levels in "ni.protobuf.X" to the index file
   This is needed because we don't have __init__.py file in ni
   and ni/protobuf package as we use nested implicit namespace packages.

.. toctree::
   :titlesonly:

   {% for page in pages | sort %}
   {% if (page.top_level_object or page.name.split('.') | length == 3) and page.display %}
   {{ page.short_name | capitalize }} <{{ page.include_path }}>
   {% endif %}
   {% endfor %}