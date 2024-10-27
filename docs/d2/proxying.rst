Proxying
========

When you run many common WSGI servers, they start a local HTTP server
listening on a TCP port like 8000. Despite providing this built-in HTTP
server, it is preferable to place a dedicated HTTP server between the
local server and the internet. This is because a dedicated HTTP server
is good at handling the behavior of HTTP and TLS, while a WSGI server is
good at managing a WSGI application.

The examples below use `Gunicorn`_, but the instructions should be
similar for any WSGI server. Consult your chosen WSGI server's docs for
more information.

Python
------

Create a virtualenv. Install a WSGI server such as `Gunicorn`_.

.. code-block:: text

    $ python3 -m venv venv
    $ ./venv/bin/pip install -r requirements.txt
    $ ./venv/bin/pip install gunicorn

The HTTP will set some headers to let the application know how it's
connected to the outside world. The WSGI app needs to be wrapped with
the :class:`~werkzeug.middleware.proxy_fix.ProxyFix` middleware to use
this information. Create a Python file to configure the app.

.. code-block:: python
    :caption: /home/project/wsgi_setup.py

    from werkzeug.middleware.proxy_fix import ProxyFix
    from project import app

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

Run Gunicorn with some workers and point it at the configured app. It
needs to remain running in the background, see :doc:`daemon`.

.. code-block:: text

    $ gunicorn -b localhost:8000 -w 4 wsgi_setup:app


Nginx
-----

To serve at the root:

.. code-block:: nginx

    location /static/ {
        alias /home/project/code/static;
    }

    location / {
    }

When serving under a path, use ``fastcgi_split_path_info`` to split
``PATH_INFO`` from ``SCRIPT_NAME``.

.. code-block:: nginx

    location /api {
        proxy_set_header X-Forwarded-Host $host:$server_port;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://localhost:8080;
        proxy_redirect off;
    }

Apache
------

To enable mod_proxy, uncomment or add the following line:

.. code-block:: apache
    :caption: /etc/httpd/conf/httpd.conf

    LoadModule proxy_module modules/mod_proxy.so

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

.. _Gunicorn:: https://gunicorn.org/
