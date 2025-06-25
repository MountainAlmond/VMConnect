from flask import Flask
from flask_migrate import Migrate
from models.engine import db
from models.user import User
from models.role import Role
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.vm_manage import vm_manage_bp
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import subprocess

def start_websockify_connections():
    """
    Запускает websockify для всех пользователей, у которых есть noVNC и VNC порты.
    """
    with app.app_context():
        users = User.query.all()  # Получаем всех пользователей из базы данных
        for user in users:
            if user.novnc_port and user.vnc_port:
                command = [
                    'websockify',
                    str(user.novnc_port),
                    f'0.0.0.0:{user.vnc_port}',
                    '--web', '/usr/share/novnc/'
                ]
                try:
                    subprocess.Popen(command)
                    print(f"Started websockify for user {user.username} on novnc_port {user.novnc_port}")
                except Exception as e:
                    print(f"Failed to start websockify for user {user.username}: {e}")


app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(vm_manage_bp)
# настройка политики CORS
CORS(app)  

if __name__ == '__main__':
    start_websockify_connections()  # Запускаем websockify для существующих пользователей
    # app.run(host='0.0.0.0', port=5000, ssl_context=('/etc/nginx/ssl/certificate.pem', '/etc/nginx/ssl/private_key.pem'))
    app.run(host='0.0.0.0', port=5000)
    