import requests

from private_config import BOT_TOKEN
from repository.MainRepository import MainRepository


class NotificationTech:

    def __init__(self):
        self.URL_MESSAGE = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    def new_task_no_bot(self, name, url, id_user):
        try:
            users = [user['id_user'] for user in MainRepository().users_by_dep("admin")] + id_user
            if users is not None:
                for user in users:
                    json_data_pass = {
                        "chat_id": user,
                        "parse_mode": "html",
                        "text": f"<b>Нова задача! (поставлена не через бот)</b>\n{name}\n\n{url}"
                    }
                    requests.request(method='POST', url=self.URL_MESSAGE, data=json_data_pass)

        except Exception as e:
            print(f"new_task_no_bot tech: {e}")

    def task_change_status(self, id_card, name, url, status):
        try:
            user = MainRepository().user_by_card_tech(id_card)
            if user is not None:
                json_data_pass = {
                    "chat_id": user['id_user'],
                    "parse_mode": "html",
                    "text": f"<b>{name}</b>\n\nЗадача змінили статус на {status}!\n\n{url}"
                }
                requests.request(method='POST', url=self.URL_MESSAGE, data=json_data_pass)
        except Exception as e:
            print(f"task_change_status_notify (tech): {e}")

    def task_in_proccess(self, id_card, name, url):
        try:
            user = MainRepository().user_by_card_tech(id_card)
            if user is not None:
                json_data_pass = {
                    "chat_id": user['id_user'],
                    "parse_mode": "html",
                    "text": f"<b>{name}</b>\n\nЗадачу щойно взяли у роботу 🟠\n\n{url}"
                }
                requests.request(method='POST', url=self.URL_MESSAGE, data=json_data_pass)
        except Exception as e:
            print(f"task_in_proccess_notify tech: {e}")

    def task_wait(self, id_card, name, url):
        try:
            user = MainRepository().user_by_card_tech(id_card)
            if user is not None:
                json_data_pass = {
                    "chat_id": user['id_user'],
                    "parse_mode": "html",
                    "text": f"<b>{name}</b>\n\nЗадачу щойно перемістили у список очікування 🟡\n\n{url}"
                }
                requests.request(method='POST', url=self.URL_MESSAGE, data=json_data_pass)
        except Exception as e:
            print(f"task_wait_notify tech: {e}")

    def task_done(self, id_card, name, url):
        try:
            user = MainRepository().user_by_card_tech(id_card)
            if user is not None:
                json_data_pass = {
                    "chat_id": user['id_user'],
                    "parse_mode": "html",
                    "text": f"<b>{name}</b>\n\nЗадача позначена як виконана 🟢\n\n{url}"
                }
                requests.request(method='POST', url=self.URL_MESSAGE, data=json_data_pass)
        except Exception as e:
            print(f"task_done_notify tech: {e}")

    def comment_task(self, name, url, comment, users):
        try:
            if users is not None:
                for user in users:
                    json_data_pass = {
                        "chat_id": user,
                        "parse_mode": "html",
                        "text": f"<b>Новий коментар до задачі!</b>\n{name}\n\n{comment}\n\n{url}"
                    }
                    requests.request(method='POST', url=self.URL_MESSAGE, data=json_data_pass)

        except Exception as e:
            print(f"comment_task_notify tech: {e}")
