import psycopg2
from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher


class DB:
    CLEAR_DB_QUERY = """
        TRUNCATE TABLE api_user, api_resource CASCADE
    """

    CREATE_USER_QUERY = """
        INSERT INTO api_user (id, email, password, is_admin)
        SELECT coalesce(max(id), 0) + 10000, %s, %s, %s
        FROM api_user
        RETURNING id;
    """

    def __init__(self, **params):
        self._params = params
        self._conn = None
        self._cur = None

    @property
    def conn(self):
        if self._conn is None:
            raise Exception("Connection not inited.")

        return self._conn

    @property
    def cur(self):
        if self._conn is None:
            raise Exception("Connection not inited.")

        return self._cur

    def connect(self):
        self._conn = psycopg2.connect(**self._params)
        self._conn.set_session(autocommit=True)
        self._cur = self._conn.cursor()

    def clear_db(self):
        self.cur.execute(self.CLEAR_DB_QUERY)

    def create_superuser(self, email, password):
        self.cur.execute(
            self.CREATE_USER_QUERY,
            (email, make_password(password, hasher=PBKDF2PasswordHasher()), True),
        )
        return self.cur.fetchone()[0]

    def create_user(self, email, password):
        self.cur.execute(
            self.CREATE_USER_QUERY,
            (email, make_password(password, hasher=PBKDF2PasswordHasher()), False),
        )
        return self.cur.fetchone()[0]
