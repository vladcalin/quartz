from quartz.db.manager import CassandraClusterManager


class Users(object):
    session = CassandraClusterManager.get_session()

    CREATE_TABLE = """CREATE TABLE IF NOT EXISTS quartz.users (
      id uuid PRIMARY KEY,
      username text,
      first_name text,
      last_name text,
      password blob,
      email text,
      date_joined timestamp,
      last_seen timestamp,
      active boolean,
      projects set<uuid>
    )
    """
    INDEXES = [
        "CREATE INDEX IF NOT EXISTS index_users_email ON quartz.users (email)",
        "CREATE INDEX IF NOT EXISTS index_users_username ON quartz.users (useraname)",
    ]

    @classmethod
    def create_user_table(cls):
        cls.session.execute(cls.CREATE_TABLE)

        # create the indexes
        for index_stmt in cls.INDEXES:
            cls.session.execute(index_stmt)
