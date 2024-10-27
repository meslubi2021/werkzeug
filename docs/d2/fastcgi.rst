FastCGI (Deprecated)
====================

.. warning::

    This is documented for historic reasons, but you should not deploy
    with this method in a modern setting. It is better to use a WSGI
    server.

`FastCGI`_ is an improvement on CGI that keeps the application process
running and communicates with a binary protocol. While it is more
efficient than CGI, it is not common or well supported in Python. You
will have a better experience using a WSGI server instead.


Python
------

Create a virtualenv. Install `flup`_, which provides a FastCGI server
implementation.

.. code-block:: text

    $ python3 -m venv venv
    $ ./venv/bin/pip install -r requirements.txt
    $ ./venv/bin/pip install flup

Create a Python script that imports your application and runs it with
:class:`flup.server.fcgi.WSGIServer`.

.. code-block:: python
    :caption: /home/project/code/fcgi_handler.py

    from flup.server.fcgi import WSGIHandler
    from project import app

    WSGIHandler(app, bindAddress=("localhost", 8080)).run()

Run the application. Flup doesn't output anything, so you'll just see
a blank space after it starts. It needs to remain running in the
background, see :doc:`daemon` for more robust solutions.

.. code-block:: text

    $ python3 fcgi_handler.py


Nginx
-----

Nginx has FastCGI support built in, but requires some configuration to
set ``PATH_INFO`` and ``SCRIPT_NAME`` correctly.

To serve at the root:

.. code-block:: nginx

    location /static/ {
        alias /home/project/code/static;
    }

    location / {
        include fastcgi_params;
        fastcgi_param SCRIPT_NAME "";
        fastcgi_param PATH_INFO $fastcgi_script_name;
        fastcgi_pass localhost:8080;
    }

When serving under a path, use ``fastcgi_split_path_info`` to split
``PATH_INFO`` from ``SCRIPT_NAME``.

.. code-block:: nginx

    location /fcgi {
        fastcgi_split_path_info ^(/fcgi)(.*)$;
        include fastcgi_params;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_pass localhost:8080;
    }

Apache
------

The modern way to use FastCGI in Apache is to enable mod_proxy_fcgi,
which extends mod_proxy to understand the FastCGI protocol. Uncomment
or add the following lines:

.. code-block:: apache
    :caption: /etc/httpd/conf/httpd.conf

    LoadModule proxy_module modules/mod_proxy.so
    LoadModule proxy_fcgi_module modules/mod_proxy_fcgi.so

Apache requires some configuration to set ``PATH_INFO`` and
``SCRIPT_NAME`` correctly.

To serve the application at the root:

.. code-block:: apache

    Alias /static/ /home/project/code/static/

    ProxyPass / fcgi://localhost:8080/
    ProxyFCGISetEnvIf true SCRIPT_NAME
    ProxyFCGISetEnvIf true proxy-fcgi-pathinfo full

To serve under a path:

.. code-block:: apache

    ProxyPass /fcgi fcgi://localhost:8080
    ProxyFCGISetEnvIf true SCRIPT_NAME /fcgi
    ProxyFCGISetEnvIf true proxy-fcgi-pathinfo full

.. _FastCGI: https://en.wikipedia.org/wiki/FastCGI
.. _flup: https://pypi.org/project/flup/
