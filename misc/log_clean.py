# log cleaner
import os
import subprocess
import time

import dotenv

import redis

dotenv.load_dotenv()

msg_log = "../" + os.getenv('MESSAGES')  # path to jsonl
system_log = "../" + os.getenv('SYSTEM')  # path to jsonl

command = [
    "../" + os.getenv('REDIS_SERVER'),
    "../" + os.getenv('REDIS_CONF')
]

redis_process = subprocess.Popen(command)
r = redis.Redis(host=os.getenv('HOST'), port=os.getenv('REDIS_PORT'), db=0, password=os.getenv('REDIS_PASS'))
time.sleep(1)


def delete_log(logs):
    for log in logs:
        answer = input(f'Clean {log}? (y/n): ')
        if answer == 'y':
            with open(log, 'w') as f:
                f.write('')
            print(f'{log} was cleaned.')
        else:
            print(f'{log} cleaning canceled.')


def clean_redis():
    answer = input("Clean Redis? (y/n): ").strip().lower()
    if answer == 'y':
        r.flushdb()
        print("Redis cleaned.")
    else:
        print("Redis cleaning canceled.")


delete_log((msg_log, system_log))

clean_redis()

redis_process.terminate()
