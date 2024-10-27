CGI (Deprecated)
================

.. warning::

    This is documented for historic reasons, but you should not deploy
    with this method in a modern setting. It is not efficient and is
    difficult to debug. It is better to use a WSGI server.

`CGI`_ is an old protocol for executing a web application. A script is
executed with environment variables describing the request. The script
prints to ``stdout`` to generate a response. CGI is inefficient because
it requires starting the Python process for every request, there is no
persistent server process.

These instructions are for Apache. Nginx does not support CGI.

Python
------

Create a virtualenv.

.. code-block:: text

    $ python3 -m venv venv
    $ ./venv/bin/pip install -r requirements.txt

Create a Python script that imports your application and runs it with
:class:`wsgiref.handlers.CGIHandler`. The comment on the first line
tells the script to run using the project's virtualenv.

.. code-block:: python
    :caption: /home/project/code/cgi_handler.py

    #!/home/project/venv/bin/python
    from wsgiref.handlers import CGIHandler
    from project import app

    CGIHandler().run(app)

Mark the script executable:

.. code-block:: text

    $ chmod +x cgi_handler.py

Apache
------

Enable the CGI module by uncommenting or adding the following lines:

.. code-block:: apache
    :caption: /etc/httpd/conf/httpd.conf

    <IfModule !mpm_prefork_module>
        LoadModule cgid_module modules/mod_cgid.so
    </IfModule>
    <IfModule mpm_prefork_module>
        LoadModule cgi_module modules/mod_cgi.so
    </IfModule>

Configure Apache using the `ScriptAlias`_ directive. This maps a URL
path to the ``cgi_handler.py`` executable.

.. code-block:: apache

    Alias /static/ /home/project/code/static/

    ScriptAlias / /home/project/code/cgi_handler.py/

    <Directory /home/project/code>
        <Files cgi_handler.py>
            Require all granted
        </Files>
    </Directory>

    <Directory /home/project/code/static>
        Require all granted
    </Directory>

To serve the application under a path, change the ``ScriptAlias``:

.. code-block:: apache

    ScriptAlias /app /home/project/code/cgi_handler.py

.. _CGI: https://en.wikipedia.org/wiki/Common_Gateway_Interface
.. _ScriptAlias: https://httpd.apache.org/docs/current/mod/mod_alias.html#scriptalias
