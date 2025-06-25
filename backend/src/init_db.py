#Скрипт инициализации базы данных (создание Администратора с паролем по умолчанию и его роли)

from models.engine import db
from models.user import User
from models.role import Role
from flask import Flask
from config import Config
from werkzeug.security import generate_password_hash

# Создаем экземпляр приложения Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_admin_user_and_role():
    with app.app_context():  # Создаем контекст приложения
        # Инициализация базы данных (если еще не инициализирована)
        db.create_all()

        # Создаем роль 'admin', если она еще не существует
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(
                name='admin',
                description='Administrator role',
                routes=['/admin/create_user', '/admin/dashboard']  # Маршруты, доступные администратору
            )
            db.session.add(admin_role)
            db.session.commit()
            print("Admin role created successfully.")
        else:
            print("Admin role already exists.")

        # Создаем роль 'user', если она еще не существует
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(
                name='user',
                description='Regular user role',
                routes=[]  # Обычные пользователи не имеют доступа к административным маршрутам
            )
            db.session.add(user_role)
            db.session.commit()
            print("User role created successfully.")
        else:
            print("User role already exists.")

        # Проверяем, существует ли пользователь 'admin'
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Создаем пользователя 'admin'
            admin_user = User(
                username='admin',
                role=admin_role  # Назначаем роль 'admin'
            )
            admin_user.set_password('admin')  # Устанавливаем пароль

            db.session.add(admin_user)
            db.session.commit()

            print("Admin user created successfully with role 'admin'.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    # Выполняем функцию создания администратора и роли
    create_admin_user_and_role()