from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models.engine import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # Связь с ролью
    vm_name = db.Column(db.String(80), nullable=True)  # Имя виртуальной машины
    novnc_port = db.Column(db.Integer, nullable=True)  # Порт noVNC
    vnc_port = db.Column(db.Integer, nullable=True)    # Порт VNC
    role = db.relationship('Role', backref='users')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2')

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def has_route_access(self, route):
        """
        Проверяет, имеет ли пользователь доступ к указанному маршруту через свою роль.
        :param route: Строка с именем маршрута (например, '/admin/dashboard').
        :return: True, если есть доступ, иначе False.
        """
        if not self.role:
            return False
        return route in self.role.routes