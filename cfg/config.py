from cfg.private_config import *

DEBUG_MODE = True

if DEBUG_MODE:
    # telegram
    URL_MESSAGE = f"https://api.telegram.org/bot{local_telegram_token}/sendMessage"

    # database
    CONNECTION_PASSWORD = local_password_connection
    DB_NAME = local_name_db

    # trello
    list_tech_done = list_tech_done_local
    list_creo_done = list_creo_done_local
    list_from_tech = idList_tech_test
    list_from_creo = idList_creo_test
    list_tech_gleb = "6691678871a5be4f5dd4e689"
    list_tech_egor = "669167941c8f949834c119e8"
    list_tech_proccess = "669167c30507a9f7da09b6f5"

    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello

    COMPLETED_STATUS_TRELLO = SERVER_COMPLETED_STATUS_TRELLO
    ACTIVE_STATUS_TRELLO = SERVER_ACTIVE_STATUS_TRELLO

else:
    # telegram
    URL_MESSAGE = f"https://api.telegram.org/bot{server_telegram_token}/sendMessage"

    # database
    CONNECTION_PASSWORD = server_password_connection
    DB_NAME = server_name_db

    # trello
    list_tech_done = list_tech_done
    list_creo_done = list_creo_done
    list_from_tech = idList_tech
    list_from_creo = idList_creo

    list_tech_gleb = "6694dfe37ee4e6933c27b2c0"
    list_tech_egor = "6694dfe9678fac0a7745a537"
    list_tech_proccess = "63454720b7975012f53b1451"

    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello

    COMPLETED_STATUS_TRELLO = SERVER_COMPLETED_STATUS_TRELLO
    ACTIVE_STATUS_TRELLO = SERVER_ACTIVE_STATUS_TRELLO
