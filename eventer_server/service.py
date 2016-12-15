import os

from tornado.web import RequestHandler
from tornado.gen import coroutine

from pymicroservice.core.microservice import PyMicroService
from pymicroservice.core.decorators import public_method, private_api_method
from eventer_server import __version__


class IndexHandler(RequestHandler):
    @coroutine
    def get(self):
        self.render("index.html", version=__version__)


class EventerService(PyMicroService):
    name = "eventer_server"
    host = "127.0.0.1"
    port = 8000

    api_token_header = "X-Api-Token"
    max_parallel_blocking_tasks = os.cpu_count()

    extra_handlers = [
        ("/eventer", IndexHandler),
    ]

    # create your templates
    template_dir = os.path.join("html", "templates")

    # setup your static files
    static_dirs = [
        (r"/static", os.path.join("html", "static")),
    ]

    # service registries
    service_registry_urls = []
    service_registry_ping_interval = 30

    def __init__(self):
        self._values = {}
        super(EventerService, self).__init__()

    @public_method
    def say_hello(self, name):
        return "hello {}".format(name)

    @private_api_method
    def say_private_hello(self, name):
        """
        Retrieves a value that was previously stored.
        """
        return "Private hello {0}".format(name)

    # Implement your token validation logic
    def api_token_is_valid(self, api_token):
        return True


if __name__ == '__main__':
    service = EventerService()
    service.start()
