Installation and configuration
==============================

Requirements
------------

In order to run this service, you need the following software:

- MongoDB server (you gan grab it from https://www.mongodb.com/download-center?jmp=nav )
- Python 3.5 or newer (you can grab it from https://www.python.org/downloads/ )
- If the Python interpreter comes without the pip package installed,
  you need to install it ( https://bootstrap.pypa.io/get-pip.py )


Installation from sources
-------------------------

Clone the sources ::

    git clone https://github.com/vladcalin/quartz.git

Install the sources ::

    cd quartz
    python setup.py install

After this, you can type the following command to display the help ::

    quartz --help

Configuration
-------------

The projects needs a JSON file with the configuration. Such a file can be
automatically generated with the command ::

    eventer init > eventer_config.json

The configuration contains a JSON object with key-value pairs representing
various options for the platform.

- ``"database_url"`` - specifies where the MongoDB is listening. Must respect the format
  ``"mongo://<host>:<port>/<dbname>"``. Defaults to ``"mongo://localhost:27017/eventer"
- ``"host"`` - an address where the service will be available. Defaults to ``"0.0.0.0"``
- ``"port"`` - a port where the service will listen. Defaults to 8000
- ``"service_registries"`` - a list of HTTP endpoints where a service registry listens. Check out the
  `pymicroservice <http://pymicroservice.readthedocs.io/en/latest/interacting_with_services.html#using-a-service-registry>`_
  documentation for more info on service registries.

Starting the service
--------------------

In order to start the service, run the command ::

    eventer start eventer_config.json

After that, the service will be accessible at ``http://<host>:<port>/`` (depending on the values from the
configuration file).