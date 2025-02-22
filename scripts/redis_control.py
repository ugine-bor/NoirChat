import json
import os
import subprocess
import time

import redis


class RedisManager:
    dump = os.getenv('REDIS_DUMP')
    time.sleep(5)
    ratelimits = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0,
                             password=os.getenv('REDIS_PASS'))
    _RATE_LIMITS = [tuple(limit) for limit in json.loads(os.getenv("RATE_LIMITS", "[]"))]
    redis_process = None

    def __init__(self):
        pass

    @classmethod
    def run(cls):
        command = [
            os.getenv('REDIS_SERVER'),
            os.getenv('REDIS_CONF')
        ]

        cls.redis_process = subprocess.Popen(command)

    def ratelimit(self, token):
        now = time.time()
        pipe = self.ratelimits.pipeline()

        for window, limit in self._RATE_LIMITS:
            key = f"{token}:{window}"
            cutoff = now - window
            pipe.zremrangebyscore(key, 0, cutoff)

            pipe.zadd(key, {now: now})

            pipe.expire(key, window)

            pipe.zcount(key, cutoff, now)

        results = pipe.execute()

        for i, (window, limit) in enumerate(self._RATE_LIMITS):
            request_count = results[i * 4 + 3]
            if request_count > limit:
                return window

        return False

    @classmethod
    def disconnect(cls):
        try:
            cls.redis_process.terminate()
        except Exception as e:
            print("Error_Redis_disconnect", e)

        print("Redis stopped.")
