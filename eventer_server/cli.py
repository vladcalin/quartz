import json

import click

from eventer_server.service import EventerService
from eventer_server.models import set_db_parameters

DEFAULTS = {
    "database_url": "mongo://localhost:27017/eventer",
    "host": "0.0.0.0",
    "port": 8000,
    "registry": []
}


def get_config_value(config, key):
    return config.get(key, DEFAULTS[key])


@click.group()
def cli():
    pass


@cli.command("start")
@click.argument("config")
def start(config):
    with open(config) as f:
        cfg = json.load(f)
    set_db_parameters(get_config_value(cfg, "database_url"))
    service = EventerService(get_config_value(cfg, "host"), get_config_value(cfg, "port"),
                             get_config_value(cfg, "registry"))
    service.start()


SAMPLE_CONFIG = """{
    "database_url": "mongo://localhost:27017/eventer",

    "host": "127.0.0.1",
    "port": 8000,

    "registry": []
}"""


@cli.command("get_sample_config")
def get_sample_config():
    print(SAMPLE_CONFIG)
