import json
import os
import time

import redis
from redis.exceptions import ConnectionError


class RedisManager:
    _RATE_LIMITS = None
    ratelimits = None
    
    def __init__(self):
        # Инициализация перенесена сюда из class-level
        self._RATE_LIMITS = [tuple(limit) for limit in json.loads(os.getenv("RATE_LIMITS", "[]"))]
        
    @classmethod
    def run(cls):
        """Подключение к Redis (без запуска сервера)"""
        retries = 5
        while retries > 0:
            try:
                cls.ratelimits = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'localhost'),
                    port=int(os.getenv('REDIS_PORT')),
                    db=0,
                    password=os.getenv('REDIS_PASS'),
                    socket_connect_timeout=5,
                    retry_on_timeout=True,
                    decode_responses=True  # автоматически декодировать ответы в UTF-8
                )
                # Проверка соединения
                cls.ratelimits.ping()
                print("Successfully connected to Redis")
                break
            except (ConnectionError, Exception) as e:
                print(f"Failed to connect to Redis (attempt {6-retries}/5): {e}")
                retries -= 1
                if retries > 0:
                    time.sleep(2)  # Подождем перед следующей попыткой
                else:
                    raise Exception("Could not connect to Redis after 5 attempts")

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
        """Закрытие соединения с Redis"""
        if cls.ratelimits:
            try:
                cls.ratelimits.close()
                print("Redis connection closed")
            except Exception as e:
                print(f"Error closing Redis connection: {e}")
        else:
            print("No Redis connection to close")
