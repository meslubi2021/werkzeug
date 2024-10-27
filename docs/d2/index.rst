Deploying to Production
=======================

While lightweight and easy to use, **Werkzeug's built-in development
server is not suitable for a production deployment**. It is not designed
to be particularly secure, stable, or efficient, and is may be missing
HTTP features that a production server should have. Instead, you should
use a production WSGI server and HTTP server.

Basic instructions for common WSGI and HTTP servers are listed here. If
you want to use a server not listed here, look up the server's
documentation about how to use a WSGI app with it, or how to use it as
a reverse proxy.

.. toctree::

    proxying
    uwsgi
    mod_wsgi

.. toctree::
    :caption: Topics:

    static
    unix-socket
    app-config
    daemon

.. toctree::
    :caption: Deprecated:

    fastcgi
    cgi
