import os
import time

while True:
    print('start webhook handler')
    try:
        os.system("python3 /home/ftpuser/webhook_handler/main.py")
    except Exception as e:
        print(f'exception in start: {e}') 
    print('crash')
    time.sleep(5)
