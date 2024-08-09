from repository.MyDatabase import MyDatabase


class MainRepository(MyDatabase):

    def __init__(self):
        super().__init__()

    def user_by_card_tech(self, id_card):
        query = "SELECT * FROM `cards_tech` WHERE `id_card` = %s;"
        return self._select_one(query, (id_card,))

    def user_by_card_creo(self, id_card):
        query = "SELECT * FROM `cards_creo` WHERE `id_card` = %s;"
        return self._select_one(query, (id_card,))

    def users_by_dep(self, dep_user):
        query = "SELECT * FROM `users` WHERE `dep_user` = %s;"
        return self._select(query, (dep_user,))

    def tech_by_card_id(self, card_id):
        query = "SELECT * FROM `cards_tech` WHERE `id_card` = %s;"
        return self._select_one(query, (card_id, ))
