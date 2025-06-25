#!/bin/bash

# --- Функция для запуска фронтенда ---
start_frontend() {
    echo "=== Запускаю фронтенд ==="
    cd frontend/src || { echo "Ошибка: Папка frontend/src не найдена"; exit 1; }
    npm start &
    FRONTEND_PID=$!
    echo "Фронтенд запущен (PID: $FRONTEND_PID)."
}

# --- Функция для остановки фронтенда ---
stop_frontend() {
    echo "=== Останавливаю фронтенд ==="
    pkill -f "npm start" || { echo "Фронтенд уже не запущен."; return; }
    echo "Фронтенд остановлен."
}

# --- Функция для запуска бэкенда ---
start_backend() {
    echo "=== Запускаю бэкенд ==="
    cd backend || { echo "Ошибка: Папка backend не найдена"; exit 1; }

    # Активация виртуального окружения
    if [ ! -d "env" ]; then
        echo "Ошибка: Виртуальное окружение 'env' не найдено. Создайте его сначала."
        exit 1
    fi
    source env/bin/activate || { echo "Ошибка: Не удалось активировать виртуальное окружение"; exit 1; }

    # Переход в подпапку src и запуск приложения
    cd src || { echo "Ошибка: Папка backend/src не найдена"; exit 1; }
    python3 app.py &
    BACKEND_PID=$!
    echo "Бэкенд запущен (PID: $BACKEND_PID)."
}

# --- Функция для остановки бэкенда ---
stop_backend() {
    echo "=== Останавливаю бэкенд ==="
    pkill -f "python3 app.py" || { echo "Бэкенд уже не запущен."; return; }
    echo "Бэкенд остановлен."
}

# --- Основной скрипт ---
echo "Что вы хотите сделать? (Введите 1 или 2)"
echo "1. Запустить сервисы"
echo "2. Остановить сервисы"
read -p "Выберите действие: " action

if [[ $action -eq 1 ]]; then
    echo "Какой сервис вы хотите запустить? (Введите 1, 2 или 3)"
    echo "1. Фронтенд"
    echo "2. Бэкенд"
    echo "3. Оба"
    read -p "Выберите сервис: " service

    if [[ $service -eq 1 ]]; then
        start_frontend
    elif [[ $service -eq 2 ]]; then
        start_backend
    elif [[ $service -eq 3 ]]; then
        start_frontend
        start_backend
    else
        echo "Неверный выбор сервиса."
        exit 1
    fi

elif [[ $action -eq 2 ]]; then
    echo "Какой сервис вы хотите остановить? (Введите 1, 2 или 3)"
    echo "1. Фронтенд"
    echo "2. Бэкенд"
    echo "3. Оба"
    read -p "Выберите сервис: " service

    if [[ $service -eq 1 ]]; then
        stop_frontend
    elif [[ $service -eq 2 ]]; then
        stop_backend
    elif [[ $service -eq 3 ]]; then
        stop_frontend
        stop_backend
    else
        echo "Неверный выбор сервиса."
        exit 1
    fi

else
    echo "Неверный выбор действия."
    exit 1
fi