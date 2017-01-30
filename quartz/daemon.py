import sys
import subprocess
import time

from quartz.util import get_logger


class MasterDaemon(object):
    def __init__(self, configuration):
        self.config = configuration

        self.service_registries = self.config["context"]["service_registries"]

        self.logger = get_logger("quartz.localdaemon")
        self.logger.debug("Initializing")
        self.processes = []

    def start_instances(self):
        services = [
            "webui", "auth", "coremgmt", "plot", "notifier"
        ]

        for service in services:
            required_instances = self._get_required_instances(service)
            for instance in required_instances:
                proc = self.start_single_instance(service, instance)
                self.processes.append(proc)

        self.monitor_services()

    def _get_required_instances(self, service_name):
        return self.config["quartz." + service_name]["instances"]

    def start_single_instance(self, service_name, instance_params):
        cmd = [sys.executable, "-m", "quartz.service.{}.service".format(service_name),
               "start", "--host", instance_params["host"], "--port", str(instance_params["port"]),
               "--accessible_at", instance_params["accessible_at"], "--service_registry"]
        cmd.extend(self.service_registries)

        proc = subprocess.Popen(cmd, shell=True)
        self.logger.debug(cmd)
        self.logger.info("Started service {} (PID: {})".format(service_name, proc.pid))
        return proc

    def monitor_services(self):
        while True:
            if any([x.returncode is not None for x in self.processes]):
                self.logger.debug("At least one service is down. Exiting")
                self.shutdown()
                exit(-1)
            time.sleep(1)

    def shutdown(self):
        self.kill_services()

    def kill_services(self):
        for service_proc in self.processes:
            self.logger.warning("Terminating {}".format(service_proc.pid))
            service_proc.terminate()
