class TrelloAction:
    def __init__(self, id_, desc, idBoard, idList, name, shortUrl, translationKey, customFieldItemIdValue, listAfterId,
                 listAfterText):
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

    def __str__(self):
        return (f"TrelloCard(ID: {self.id}\n\nName: {self.name}\n\nDescription: {self.desc}\n\n"
                f"Board ID: {self.idBoard}\n\nList ID: {self.idList}\n\nShort URL: {self.shortUrl}\n\n"
                f"Translation Key: {self.translationKey}\n\nCustom Field Item ID Value: {self.customFieldItemIdValue}"
                f"\n\nList After ID: {self.listAfterId}\n\nList After Text: {self.listAfterText})")
