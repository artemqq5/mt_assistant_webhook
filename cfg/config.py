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

    list_tech_gleb = list_tech_gleb_test
    list_tech_egor = list_tech_egor_test
    list_tech_proccess = list_tech_proccess_test

    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello

    COMPLETED_STATUS_TRELLO = TEST_COMPLETED_STATUS_TRELLO
    ACTIVE_STATUS_TRELLO = TEST_ACTIVE_STATUS_TRELLO

else:
    # telegram
    URL_MESSAGE = f"https://api.telegram.org/bot{server_telegram_token}/sendMessage"

    # database
    CONNECTION_PASSWORD = server_password_connection
    DB_NAME = server_name_db

    # trello
    list_tech_done = list_tech_done_server
    list_creo_done = list_creo_done_server
    list_from_tech = idList_tech
    list_from_creo = idList_creo

    list_tech_gleb = list_tech_gleb_server
    list_tech_egor = list_tech_egor_server
    list_tech_proccess = list_tech_proccess_server

    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello

    COMPLETED_STATUS_TRELLO = SERVER_COMPLETED_STATUS_TRELLO
    ACTIVE_STATUS_TRELLO = SERVER_ACTIVE_STATUS_TRELLO
