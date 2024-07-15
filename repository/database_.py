import pymysql

from cfg.config import CONNECTION_PASSWORD, DB_NAME


class MyDatabase:
    def __init__(self):
        self._connection = pymysql.connect(
            host="localhost",
            user="root",
            port=3306,
            autocommit=True,
            password=CONNECTION_PASSWORD,
            db=DB_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_id_user_by_card_id(self, table_name, id_card):
        try:
            with self._connection as connection:
                with connection.cursor() as cursor:
                    select_card = f"SELECT * FROM `{table_name}` WHERE `id_card` = %s;"
                    print(select_card)
                    cursor.execute(select_card, (id_card,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"get_id_user_by_card_id() {e}")
            return None

    def get_users_by_dep(self, dep):
        try:
            with self._connection as connection:
                with connection.cursor() as cursor:
                    select_user = "SELECT * FROM `users` WHERE `dep_user` = %s;"

                    cursor.execute(select_user, dep)
                    return cursor.fetchall()
        except Exception as e:
            print(f"get_users_by_dep() {e}")
            return None
