import json
import sys
import os.path
import configparser
import subprocess

import click

from quartz import __version__
from quartz.db.manager import CassandraClusterManager

BANNER = """
          __ _ _   _  __ _ _ __| |_ ____
         / _` | | | |/ _` | '__| __|_  /
        | (_| | |_| | (_| | |  | |_ / /
         \__, |\__,_|\__,_|_|   \__/___|
            |_|

    Current version: {version}
""".format(version=__version__)

DEFAULT_INI = """
[cassandra]
host = 127.0.0.1:9042,127.0.0.2:9042

[services]

service_registry = http://127.0.0.1:8000/api

[quartz.webui]
host = 0.0.0.0
port = 80
root = /quartz
accessible_at = http://localhost/quartz/api

[quartz.coremgmt]
host = 0.0.0.0
port = 8000
root = /quartz/coremgmt/api
accessible_at = http://localhost/quartz/coremgmt/api

[quartz.plot]
host = 0.0.0.0
port = 8001
root = /quartz/plot/api
accessible_at = http://localhost/quartz/plot/api

[quartz.notifier]
host = 0.0.0.0
port = 8002
root = /quartz/notifier/api
accessible_at = http://localhost/quartz/notifier/api

inboxes = senderinbox

[quartz.auth]
host = 0.0.0.0
port = 80003
root = /quartz/auth/api
accessible_at = http://localhost/quartz/auth/api

"""


def print_banner(config_file):
    print(BANNER)
    print("")
    print("Using the configuration file '{0}'".format(os.path.abspath(config_file)))
    print("")


@click.group()
def cli():
    pass


def start_single_service(service_module, host, port, accessible_at, service_registry_list):
    cmd = [sys.executable, "-m", service_module, "start", "--host", host, "--port", port, "--accessible_at", accessible_at,
           "--service_registry"]
    cmd.extend(service_registry_list)
    subprocess.Popen(cmd)


def start_services(config):
    service_registries = config.get("services", "service_registry").split(",")
    start_single_service("quartz.service.webui.service",
                         host=config.get("quartz.webui", "host"),
                         port=config.get("quartz.webui", "port"),
                         accessible_at=config.get("quartz.webui", "accessible_at"),
                         service_registry_list=service_registries)
    print("Service quartz.webui started")


@cli.command("start", help="The INI configuration file with the desired parameters")
@click.argument("config")
def start(config):
    print_banner(config)
    config_parsed = configparser.ConfigParser()
    config_parsed.read(config)
    start_services(config_parsed)


SAMPLE_CONFIG = DEFAULT_INI


@cli.command("init", help="Writes a sample configuration file to STDOUT. Can be used as template"
                          " for writing the actual configuration file")
def init():
    print(SAMPLE_CONFIG)
