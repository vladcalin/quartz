from cassandra.cluster import Cluster


class CassandraClusterManager(object):
    cluster = None
    session = None

    CREATE_NAMESPACE_CQL = """CREATE KEYSPACE IF NOT EXISTS quartz
                            WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};"""

    @classmethod
    def connect_to_cluster(cls, *ips):
        cls.cluster = Cluster(ips)
        cls.session = cls.create_session()
        cls.ensure_namespace()

    @classmethod
    def create_session(cls):
        return cls.cluster.connect("quartz")

    @classmethod
    def get_session(cls):
        return cls.session

    @classmethod
    def ensure_namespace(cls):
        session = cls.get_session()
        session.execute(cls.CREATE_NAMESPACE_CQL)
        session.execute("use quartz")


if __name__ == '__main__':
    CassandraClusterManager.connect_to_cluster("192.168.1.71")
