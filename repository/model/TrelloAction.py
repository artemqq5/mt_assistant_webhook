class TrelloAction:
    def __init__(self, id_, desc, idBoard, idList, name, shortUrl, translationKey, customFieldItemIdValue, listAfterId,
                 listAfterText, comment, webhook_name):
        self.id = id_
        self.desc = desc
        self.idBoard = idBoard
        self.idList = idList
        self.name = name
        self.shortUrl = shortUrl
        self.translationKey = translationKey
        self.customFieldItemIdValue = customFieldItemIdValue
        self.listAfterId = listAfterId
        self.listAfterText = listAfterText
        self.comment = comment
        self.webhook_name = webhook_name

    def __str__(self):
        return (f"TrelloCard(ID: {self.id}\n\n"
                f"Name: {self.name}\n\n"
                f"Description: {self.desc}\n\n"
                f"Board ID: {self.idBoard}\n\n"
                f"List ID: {self.idList}\n\n"
                f"Short URL: {self.shortUrl}\n\n"
                f"Translation Key: {self.translationKey}\n\n"
                f"Custom Field Item ID Value: {self.customFieldItemIdValue}\n\n"
                f"List After ID: {self.listAfterId}\n\n"
                f"List After Text: {self.listAfterText})\n\n"
                f"Comment: ({self.comment}\n\n"
                f"Webhookname: ({self.webhook_name})")


