from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.engine import db
from models.role import Role
from models.user import User
from core.vm_manager import VMManager
import os
import psutil

NGINX_CONFIG_PATH = "/etc/nginx/nginx.conf"  # Путь к конфигурационному файлу Nginx

def generate_nginx_location(username, vnc_port):
    return f"""
    location /{username} {{
        proxy_pass http://127.0.0.1:{vnc_port}/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }}

    location /{username}/websockify {{
        proxy_pass http://127.0.0.1:{vnc_port}/websockify;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }}
    """
def remove_nginx_location(username):
    # Читаем текущий конфигурационный файл
    with open(NGINX_CONFIG_PATH, "r") as file:
        config = file.readlines()  # Читаем файл построчно

    # Флаги для отслеживания блоков location
    in_user_block = False
    updated_config = []

    for line in config:
        # Если находим начало блока location для пользователя
        if f"location /{username}" in line:
            in_user_block = True
            continue  # Пропускаем эту строку

        # Если находим конец блока location
        if in_user_block and "}" in line:
            in_user_block = False
            continue  # Пропускаем закрывающую скобку

        # Если мы не внутри блока location пользователя, добавляем строку в новый конфиг
        if not in_user_block:
            updated_config.append(line)

    # Записываем обновленный конфигурационный файл
    with open(NGINX_CONFIG_PATH, "w") as file:
        file.writelines(updated_config)

    # Перезагружаем Nginx
    os.system("sudo nginx -s reload")
    print(f"Nginx configuration updated and reloaded after removing {username}'s locations.")
    
def update_nginx_config(new_location_block):
    # Читаем текущий конфигурационный файл
    with open(NGINX_CONFIG_PATH, "r") as file:
        config = file.readlines()  # Читаем файл построчно

    # Находим последние две закрывающие скобки (}) в файле
    closing_braces_indices = [i for i, line in enumerate(config) if "}" in line.strip()]
    if len(closing_braces_indices) < 2:
        print("Not enough closing braces found in the Nginx config.")
        return

    # Позиция для вставки нового блока — перед предпоследней закрывающей скобкой
    insert_position = closing_braces_indices[-2]

    # Проверяем, что блок location еще не добавлен
    if any(new_location_block.strip() in line.strip() for line in config):
        print("Location block already exists in the Nginx config.")
        return

    # Вставляем новый блок location перед предпоследней закрывающей скобкой
    new_lines = [f"\n{line}\n" for line in new_location_block.split("\n") if line.strip()]
    config[insert_position:insert_position] = new_lines

    # Записываем обновленный конфигурационный файл
    with open(NGINX_CONFIG_PATH, "w") as file:
        file.writelines(config)

    # Перезагружаем Nginx
    os.system("sudo nginx -t && sudo nginx -s reload")
    print("Nginx configuration updated and reloaded.")



admin_bp = Blueprint('admin', __name__)
vm_manager = VMManager()

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.name != 'admin':
        return jsonify(msg="Admin access required"), 403

    users = User.query.all()
    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'role_id': user.role_id,
            'vm_name': user.vm_name,
            'novnc_port': user.novnc_port,
            'vnc_port': user.vnc_port,
        }
        for user in users
    ]
    return jsonify(users_data), 200

@admin_bp.route('/admin/create_user', methods=['POST'])
@jwt_required()  # Требуется JWT-токен для доступа
def admin_create_user():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.name != 'admin':
        return jsonify(msg="Admin access required"), 403

    #Проверяем, хватит ли у нас аппаратных ресурсов для нового пользователя
    # Запрашиваемые ресурсы для виртуальной машины
    requested_memory_mb = 4096  # 4 ГБ RAM
    requested_vcpu_count = 4    # 4 CPU
    requested_disk_size_gb = 30 # 30 ГБ дискового пространства

    available_memory_mb = psutil.virtual_memory().available // (1024 ** 2)
    available_cpu_count = psutil.cpu_count(logical=True)  
    available_disk_space_gb = psutil.disk_usage('/').free // (1024 ** 3)

    print(available_memory_mb)
    print(available_cpu_count)
    print(available_disk_space_gb)

    # if available_memory_mb < requested_memory_mb:
    #     return jsonify(msg=f"Not enough memory available. Required: {requested_memory_mb}MB, Available: {available_memory_mb}MB"), 400

    # if available_cpu_count < requested_vcpu_count:
    #     return jsonify(msg=f"Not enough CPU cores available. Required: {requested_vcpu_count}, Available: {available_cpu_count}"), 400

    # if available_disk_space_gb < requested_disk_size_gb:
    #     return jsonify(msg=f"Not enough disk space available. Required: {requested_disk_size_gb}GB, Available: {available_disk_space_gb}GB"), 400

    # Получаем данные из запроса
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'admin':
        return jsonify(msg='Only one user in system!'), 400


    # Проверяем, существует ли пользователь с таким именем
    if User.query.filter_by(username=username).first():
        return jsonify(msg='User already exists'), 400

    # Находим роль 'user'
    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        return jsonify(msg="User role not found"), 500

    # Создаем виртуальную машину для пользователя
    vm_name = f"vm_{username}"  # Генерируем имя виртуальной машины
    
    #возможно изменить настройки виртуальной машины
    result = vm_manager.create_vm(
        vm_name,
        memory_mb=requested_memory_mb,
        vcpu_count=requested_vcpu_count,
        disk_size_gb=requested_disk_size_gb,
        vnc_password = password)

    novnc_port = result.get("novnc_port")  # Получаем порт VNC из ответа VMManager
    vnc_port = result.get("vnc_port")  # Получаем порт VNC из ответа VMManager

    # Создаем нового пользователя
    new_user = User(
        username=username,
        role=user_role,                  # Назначаем роль 'user'
        vm_name=vm_name,                 # Имя виртуальной машины
        novnc_port=novnc_port,           # Порт noVNC
        vnc_port=vnc_port                # Порт VNC
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    location_block = generate_nginx_location(username, novnc_port)
    #криво встает новый location, иногда ломает конфиг
    update_nginx_config(location_block)

    return jsonify(msg=f'User {username} created successfully with VM {vm_name} and Nginx configured'), 201


@admin_bp.route('/admin/delete_user/<username>', methods=['DELETE'])
@jwt_required()  # Требуется JWT-токен для доступа
def delete_user(username):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.name != 'admin':
        return jsonify(msg="Admin access required"), 403
    user_to_delete = User.query.filter_by(username=username).first()
    if user_to_delete.role.name == 'admin':
        return jsonify(msg="Cannot delete admin"), 400
    if not user_to_delete:
        return jsonify(msg="User not found"), 404

    # Удаляем виртуальную машину пользователя
    if user_to_delete.vm_name:
        try:
            vm_manager.delete_vm(user_to_delete.vm_name)
        except Exception as e:
            return jsonify({'error': f'Failed to delete VM: {str(e)}'}), 500

    # Удаляем блоки location для пользователя из конфигурации Nginx
    try:
        remove_nginx_location(username)
    except Exception as e:
        return jsonify({'error': f'Failed to update Nginx configuration: {str(e)}'}), 500

    # Удаляем пользователя из базы данных
    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify(msg=f'User {username} and associated VM deleted successfully'), 200