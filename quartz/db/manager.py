from cassandra.cluster import Cluster
from cassandra.cqlengine import connection


class CassandraClusterManager(object):
    @classmethod
    def connect_to_cluster(cls, *ips):
        connection.setup(list(ips), "quartz")
