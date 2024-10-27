Static Files
============

If your application has static files such as JavaScript, CSS, and
images, it will be more efficient to let the HTTP server serve them
directly rather than going through the Python application.

Assuming the static files are expected to be available under the
``/static/`` URL, and are stored at ``/home/project/code/static/``, the
HTTP server can be configured to serve them directly.


Nginx
-----

Within the ``server`` block, add the following:

.. code-block:: nginx

    location /static {
        alias /home/project/code/static;
    }


Apache
------

Add the following to the config:

.. code-block::

    Alias /static/ /home/project/code/static/
