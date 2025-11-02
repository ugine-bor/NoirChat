import time
import threading
from typing import List, Dict


class LongPollManager:
    """Менеджер для простого long-polling.

    Клиенты будут опрашивать `/poll?since=<timestamp>` и получать
    массив сообщений, каждый элемент: {'message': str, 'timestamp': float}.
    Если новых сообщений нет — сервер будет ждать до `timeout` секунд,
    после чего вернёт пустой список.
    """

    def __init__(self, redis_manager, log_manager, data_manager):
        self.redis = redis_manager
        self.log = log_manager
        self.data = data_manager
        self.cond = threading.Condition()

    def publish_message(self, message: str, token: str = '') -> float:
        """Сохранить сообщение в БД и уведомить ожидающих клиентов.

        Args:
            message: текст сообщения
            token: токен пользователя, отправившего сообщение
        Returns:
            timestamp: временная метка сообщения
        """
        ts = time.time()
        # Записываем сообщение в БД с токеном отправителя
        self.data.query_db(
            "INSERT INTO messages (message, timestamp, token) VALUES (?, ?, ?)",
            (message, ts, token)
        )
        try:
            self.log.log('message', message)
        except Exception:
            # логирование не критично
            pass

        # Уведомляем всех ожидающих long-poll клиентов
        with self.cond:
            self.cond.notify_all()

        return ts

    def _fetch_new(self, since: float) -> List[Dict]:
        """Запросить сообщения из БД, у которых timestamp > since."""
        rows = self.data.query_db(
            "SELECT message, timestamp FROM messages WHERE timestamp > ? ORDER BY timestamp ASC",
            (since,)
        )
        # rows — список кортежей (message, timestamp)
        return [{'message': r[0], 'timestamp': float(r[1])} for r in rows]

    def wait_for_messages(self, since: float, timeout: float = 25.0) -> List[Dict]:
        """Ожидание новых сообщений: если есть — вернуть сразу, иначе ждать до timeout секунд."""
        # Сначала попробуем вернуть немедленно, чтобы не блокировать лишний раз
        new = self._fetch_new(since)
        if new:
            return new

        # Ждём уведомления о новых сообщениях
        with self.cond:
            self.cond.wait(timeout=timeout)

        # После пробуждения — попробуем снова взять новые
        return self._fetch_new(since)
