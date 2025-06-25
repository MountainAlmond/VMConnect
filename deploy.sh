#!/bin/bash

# --- Проверка наличия необходимых инструментов ---
echo "=== Проверяю наличие необходимых инструментов ==="

# Проверка python3-venv
if ! python3 -m venv --help &> /dev/null; then
    echo "Ошибка: python3-venv не установлен. Установите его и повторите попытку."
    exit 1
else
    echo "python3-venv установлен."
fi

# Проверка npm
if ! command -v npm &> /dev/null; then
    echo "Ошибка: npm не установлен. Установите его и повторите попытку."
    exit 1
else
    echo "npm установлен."
fi

# Проверка nginx
if ! command -v nginx &> /dev/null; then
    echo "Ошибка: nginx не установлен. Установите его и повторите попытку."
    exit 1
else
    echo "nginx установлен."
fi

# Проверка openssl
if ! command -v openssl &> /dev/null; then
    echo "Ошибка: openssl не установлен. Установите его и повторите попытку."
    exit 1
else
    echo "openssl установлен."
fi

# --- Настройка и запуск фронтенда ---
echo "=== Настраиваю фронтенд ==="

# Переход в папку frontend/src
cd frontend/src || { echo "Ошибка: Папка frontend/src не найдена"; exit 1; }

# Установка зависимостей через npm
echo "Устанавливаю зависимости для фронтенда..."
npm install || { echo "Ошибка: Не удалось установить зависимости для фронтенда"; exit 1; }

# Запуск фронтенда в фоновом режиме
echo "Запускаю фронтенд..."
npm start &
FRONTEND_PID=$!
echo "Фронтенд запущен (PID: $FRONTEND_PID)."

# Возвращаемся в корень проекта
cd ../..

# --- Настройка и запуск бэкенда ---
echo "=== Настраиваю бэкенд ==="

# Переход в папку backend
cd backend || { echo "Ошибка: Папка backend не найдена"; exit 1; }

# Создание виртуального окружения Python
echo "Создаю виртуальное окружение для бэкенда..."
python3 -m venv env || { echo "Ошибка: Не удалось создать виртуальное окружение"; exit 1; }

# Активация виртуального окружения
echo "Активирую виртуальное окружение..."
source env/bin/activate || { echo "Ошибка: Не удалось активировать виртуальное окружение"; exit 1; }

# Установка зависимостей из requirements.txt
echo "Устанавливаю зависимости для бэкенда..."
pip install -r requirements.txt || { echo "Ошибка: Не удалось установить зависимости для бэкенда"; exit 1; }

# Переход в подпапку backend/src
cd src || { echo "Ошибка: Папка backend/src не найдена"; exit 1; }

# Запуск Python-приложения
echo "Запускаю бэкенд..."
python3 app.py &
BACKEND_PID=$!
echo "Бэкенд запущен (PID: $BACKEND_PID)."

# --- Завершение скрипта ---
echo "=== Все сервисы запущены ==="
echo "Для остановки фронтенда выполните: kill $FRONTEND_PID"
echo "Для остановки бэкенда выполните: kill $BACKEND_PID"