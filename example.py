from pprint import pformat

from werkzeug.exceptions import NotFound
from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.wrappers import Request
from werkzeug.wrappers import Response

map = Map(rules=[Rule("/test", endpoint="test")])


@Request.application
def app(request):
    adapter = map.bind_to_environ(request.environ)
    try:
        current = adapter.match()
    except NotFound:
        current = None
    url = adapter.build("test")
    return Response(f"{pformat(request.environ)}\n{current}\n{url}")


if __name__ == "__main__":
    from flup.server.fcgi import WSGIServer

    WSGIServer(app, bindAddress="fcgi.sock", umask=0o111).run()
