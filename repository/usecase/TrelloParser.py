from repository.model.TrelloAction import TrelloAction


class TrelloParser:

    @staticmethod
    def parse_trello_response(data):
        # Безпечне отримання значень з використанням get()
        customFieldItem = data.get('action', {}).get('data', {}).get('customFieldItem')

        # Ініціалізація змінних з перевіркою на None
        customFieldItemIdValue = customFieldItem.get('idValue', None) if customFieldItem else None

        listAfter = data.get('action', {}).get('data', {}).get('listAfter')
        listAfterId = listAfter.get('id', None) if listAfter else None
        listAfterText = listAfter.get('name', None) if listAfter else None

        commentData = data.get('action', {}).get('data', {})
        comment = commentData.get('text', None) if commentData else None

        model = data.get('model', {})
        id_ = data.get('action', {}).get('data', {}).get('card', {}).get('id', None)
        desc = model.get('desc', None)
        idBoard = model.get('idBoard', None)
        idList = data.get('action', {}).get('display', {}).get("entities", {}).get("list", {}).get("id", {})
        name = data.get('action', {}).get('data', {}).get('card', {}).get('name', None)
        shortUrl = data.get('action', {}).get('data', {}).get('card', {}).get('shortLink', None)

        actionDisplay = data.get('action', {}).get('display', {})
        translationKey = actionDisplay.get('translationKey', None)

        webhookData = data.get('webhook', {})
        webhookName = webhookData.get('description', '').split("_")[0] if webhookData else None

        return TrelloAction(
            id_=id_,
            desc=desc,
            idBoard=idBoard,
            idList=idList,
            name=name,
            shortUrl=f"https://trello.com/c/{shortUrl}",
            translationKey=translationKey,
            customFieldItemIdValue=customFieldItemIdValue,
            listAfterId=listAfterId,
            listAfterText=listAfterText,
            comment=comment,
            webhook_name=webhookName
        )

