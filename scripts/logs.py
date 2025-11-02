from dotenv import load_dotenv

import json
import os

load_dotenv()


class LogManager:
    msg_log = os.getenv('MESSAGES')
    system_log = os.getenv('SYSTEM')

    def __init__(self):
        pass

    def log(self, token, message, msg_time, ratelimit_sec=0):
        try:
            if ratelimit_sec == 0:
                with open(self.msg_log, 'a') as f:
                    json.dump({'token': token, 'time': msg_time, 'message': message}, f)
                    f.write('\n')
            else:
                with open(self.system_log, 'a') as f:
                    json.dump({'token': token, 'time': msg_time, 'message': message, 'ratelimit_sec': ratelimit_sec}, f)
                    f.write('\n')

        except Exception as e:
            print("Log_Error:", e)
