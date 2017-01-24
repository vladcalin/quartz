import os
import time
import json
import base64

from tornado.web import RedirectHandler
from gemstone import MicroService, public_method

from quartz.handlers.index import IndexRequestHandler
from quartz.handlers.auth import RegisterRequestHandler
from quartz.db.users import Users


class QuartzService(MicroService):
    name = "quartz"
    host = "127.0.0.1"
    port = 8000

    api_token_header = "X-Api-Token"
    max_parallel_blocking_tasks = os.cpu_count()

    extra_handlers = [
        ("/", IndexRequestHandler),

        # register
        ("/register", RegisterRequestHandler)
    ]

    root_directory = os.path.dirname(os.path.abspath(__file__))
    # create your templates
    template_dir = os.path.join(root_directory, "html", "templates")

    # setup your static files
    static_dirs = [
        (r"/static", os.path.join(root_directory, "html", "static")),
    ]

    # service registries
    service_registry_urls = []
    service_registry_ping_interval = 30

    def __init__(self, host, port, registry=None, accessible_at=None):
        """
        Initializes some parameters of the Quartz service

        :param host: address to bind to
        :param port: port to bind to
        :param registry: a list of service registry hosts
        """
        super(QuartzService, self).__init__()
        self.host = host
        self.port = port
        if registry:
            self.service_registry_urls = registry
        if accessible_at:
            self.accessible_at = accessible_at

    @public_method
    def create_user(self, username, email, password):
        user_instance = Users.create_user(username, password, email)
        print(user_instance)
        return user_instance.id

    # Implement your token validation logic
    def api_token_is_valid(self, api_token):
        return True
