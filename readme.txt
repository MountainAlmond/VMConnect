1) Создайте базу в СУБД PostgreSQL в соответствии с файлом config.py в разделе backend
Пример:<SQLALCHEMY_DATABASE_URI = 'postgresql://login:password!@localhost:5433/attackbase'>
2) Сделайте скрипты deploy.sh и start-stop.sh исполняемыми - <chmod +x (имя скрипта)>
3) Запустите скрипт deploy.sh - он проверит и установит зависимости необходимые для запуска программного средства
4) Запустите скрипт start-stop.sh - следуйте его инструкциям для запуска/остановки программного средства

ВНИМАНИЕ! Все скрипты должны запускаться от пользвоателя с правами root.
Также необходимо сгенерировать ключ и сертификат SSL для Nginx. Ниже приведена базовая конфигурация
nginx.conf

user www-data;

events {
    # Настройки событий (оставьте пустым, если не требуется)
}

http {
    server {
        listen 443 ssl http2;
        server_name localhost;
        client_max_body_size 10G;

        # Пути к SSL-сертификатам
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/private_key.pem;
	#location / {
#        proxy_pass http://localhost:3000;
        #proxy_set_header Host $host;
        #proxy_set_header X-Real-IP $remote_addr;
        #proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        #proxy_set_header X-Forwarded-Proto $scheme;
    #}

    }
}
