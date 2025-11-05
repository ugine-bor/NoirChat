#!/bin/bash

source venv/bin/activate

echo "Запуск Redis..."
redis-server Redis/redis_no_comments.conf &
REDIS_PID=$!

sleep 2

echo "Запуск NoirChat..."
python main.py

cleanup() {
    echo "STOP STOP STOP STOP"
    kill $REDIS_PID
    kill $I2PD_PID
    deactivate
    exit
}

trap cleanup SIGINT SIGTERM

wait
