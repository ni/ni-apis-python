API Reference
=============

This page contains auto-generated API reference documentation.

.. toctree::
   :titlesonly:

   {% for page in pages | sort %}
   {% if (page.top_level_object or page.name.split('.') | length == 5) and page.display %}
   {{ page.include_path }}
   {% endif %}
   {% endfor %}
