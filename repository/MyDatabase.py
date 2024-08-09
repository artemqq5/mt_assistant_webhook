import pymysql
from pymysql import cursors

from private_config import PASSWORD_DATABASE, NAME_DATABASE


class MyDatabase:
    def __init__(self):
        self._connection = pymysql.connect(
            host="localhost",
            user="root",
            port=3306,
            autocommit=True,
            password=PASSWORD_DATABASE,
            db=NAME_DATABASE,
            charset="utf8mb4",
            cursorclass=cursors.DictCursor
        )

    def _insert(self, query, args=None):
        try:
            with self._connection as con:
                with con.cursor() as cursor:
                    return cursor.execute(query, args)
        except Exception as e:
            print(f"_insert: {e} | QUERY: {query}")

    def _insert_id(self, query, args=None):
        try:
            with self._connection as con:
                with con.cursor() as cursor:
                    cursor.execute(query, args)
                    cursor.execute("SELECT LAST_INSERT_ID();")
                    return cursor.fetchone().get('LAST_INSERT_ID()', None)
        except Exception as e:
            print(f"_insert: {e} | QUERY: {query}")

    def _update(self, query, args=None):
        try:
            with self._connection as con:
                with con.cursor() as cursor:
                    return cursor.execute(query, args)
        except Exception as e:
            print(f"_update: {e} | QUERY: {query}")

    def _delete(self, query, args=None):
        try:
            with self._connection as con:
                with con.cursor() as cursor:
                    return cursor.execute(query, args)
        except Exception as e:
            print(f"_delete: {e} | QUERY: {query}")

    def _select_one(self, query, args=None):
        try:
            with self._connection as con:
                with con.cursor() as cursor:
                    cursor.execute(query, args)
                    return cursor.fetchone()
        except Exception as e:
            print(f"_select_one: {e} | QUERY: {query}")

    def _select(self, query, args=None):
        try:
            with self._connection as con:
                with con.cursor() as cursor:
                    cursor.execute(query, args)
                    return cursor.fetchall()
        except Exception as e:
            print(f"_select: {e} | QUERY: {query}")

