import logging

from quartz.db.manager import CassandraClusterManager



class Users(object):
    session = None

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

    GET_USER_BY_NAME = """SELECT * FROM quartz.users WHERE username = %s"""
    GET_USER_BY_EMAIL = """SELECT * FROM quartz.users WHERE email = %s"""

    @classmethod
    def initialize_table_context(cls):
        cls.session = CassandraClusterManager.get_session()
        cls.create_table()
        # create the indexes
        cls.create_indexes()

    @classmethod
    def create_table(cls):
        logging.info("Creating table 'quartz.users'")
        cls.session.execute(cls.CREATE_TABLE)

    @classmethod
    def create_indexes(cls):
        for index_stmt in cls.INDEXES:
            cls.session.execute(index_stmt)

    @classmethod
    def create_user(cls, username, password, email):
        session = CassandraClusterManager.get_session()
        try:
            user = list(session.execute(cls.GET_USER_BY_NAME, (username,)))
        except Exception as e:
            print(e)
        return user
