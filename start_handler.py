import os
import time

while True:
    print('start webhook handler trello')
    try:
        os.system("python3.10 /home/ftpuser/trello_webhook/main.py")
    except Exception as e:
        print(f'exception in start: {e}') 
    print('crash')
    time.sleep(5)
