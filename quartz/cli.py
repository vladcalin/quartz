import json
import sys
import os.path
import subprocess

import click

from quartz import __version__
from quartz.daemon import MasterDaemon

BANNER = """
          __ _ _   _  __ _ _ __| |_ ____
         / _` | | | |/ _` | '__| __|_  /
        | (_| | |_| | (_| | |  | |_ / /
         \__, |\__,_|\__,_|_|   \__/___|
            |_|

    Current version: {version}
""".format(version=__version__)

DEFAULTS = {
    "context": {
        "real_ip": "127.0.0.1",
        "service_registries": ["http://localhost:9000/api"]
    },
    "cassandra": {
        "nodes": ["127.0.0.1:9042"]
    },
    "quartz.webui": {
        "root": "/quartz",
        "instances": [
            {
                "host": "127.0.0.1",
                "port": 80,
                "accessible_at": "http://127.0.0.1:80",
            }, {
                "host": "127.0.0.1",
                "port": 443,
                "accessible_at": "http://127.0.0.1:80",
            }
        ]
    },
    "quartz.coremgmt": {
        "root": "/quartz/coremgmt/api",
        "instances": [
            {
                "host": "127.0.0.1",
                "port": 8000,
                "accessible_at": "http://127.0.0.1:8000",
            }
        ]
    },
    "quartz.notifier": {
        "root": "/quartz/notifier/api",
        "instances": [
            {
                "host": "127.0.0.1",
                "port": 8001,
                "accessible_at": "http://127.0.0.1:8001",
            }
        ]
    },
    "quartz.auth": {
        "root": "/quartz/auth/api",
        "instances": [
            {
                "host": "127.0.0.1",
                "port": 8002,
                "accessible_at": "http://127.0.0.1:8002",
            }
        ]
    },
    "quartz.plot": {
        "root": "/quartz/plot/api",
        "instances": [
            {
                "host": "127.0.0.1",
                "port": 8003,
                "accessible_at": "http://127.0.0.1:8003",
            }
        ]
    },
}


def print_banner(config_file):
    print(BANNER)
    print("")
    print("Using the configuration file '{0}'".format(os.path.abspath(config_file)))
    print("")


@click.group()
def cli():
    pass


def start_single_service(service_module, host, port, accessible_at, service_registry_list):
    cmd = [sys.executable, "-m", service_module, "start", "--host", host, "--port", port, "--accessible_at",
           accessible_at,
           "--service_registry"]
    cmd.extend(service_registry_list)
    return subprocess.Popen(cmd)


def start_services(name, config):
    return start_single_service("quartz.service.{}.service".format(name),
                                host=config.get("quartz.{}".format(name), "host"),
                                port=config.get("quartz.{}".format(name), "port"),
                                accessible_at=config.get("quartz.{}".format(name), "accessible_at"),
                                service_registry_list=config.get("services", "service_registry").split(","))


@cli.command("start", help="The INI configuration file with the desired parameters")
@click.argument("config")
def start(config):
    print_banner(config)
    with open(config) as f:
        jsonconfig = json.load(f)
    config = jsonconfig

    MasterDaemon(config).start_instances()


SAMPLE_CONFIG = json.dumps(DEFAULTS, indent=4, sort_keys=True)


@cli.command("init", help="Writes a sample configuration file to STDOUT. Can be used as template"
                          " for writing the actual configuration file")
def init():
    print(SAMPLE_CONFIG)
