from flask import Flask, jsonify, Blueprint, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from core.vm_manager import VMManager
from models.user import db, User

vm_manage_bp = Blueprint('vm_manage', __name__)


# Получаем экземпляр VMManager через функцию
vm_manager = VMManager()

@vm_manage_bp.route('/api/vm/create', methods=['POST'])
@jwt_required()  # Требуется JWT-токен для доступа
def create_vm():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.name != 'admin':
        return jsonify(msg="Admin access required"), 403
    data = request.json
    vm_name = data.get('name')
    memory_mb = data.get('memory', 1024)  # По умолчанию 1 ГБ
    vcpu_count = data.get('vcpu', 1)      # По умолчанию 1 CPU
    disk_size_gb = data.get('disk_size', 10)  # По умолчанию 10 ГБ

    if not vm_name:
        return jsonify({'error': 'Name is required'}), 400

    try:
        result = vm_manager.create_vm(vm_name, memory_mb, vcpu_count, disk_size_gb)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vm_manage_bp.route('/api/vm/delete/<vm_name>', methods=['GET'])
@jwt_required()  # Требуется JWT-токен для доступа
def delete_vm(vm_name):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.name != 'admin':
        return jsonify(msg="Admin access required"), 403
    try:
        result = vm_manager.delete_vm(vm_name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vm_manage_bp.route('/api/vm/active-list')
@jwt_required()  # Требуется JWT-токен для доступа
def list_active_vm():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.name != 'admin':
        return jsonify(msg="Admin access required"), 403
    return jsonify(vm_manager.list_active_vm())

@vm_manage_bp.route('/api/vm/inactive-list')
@jwt_required()  # Требуется JWT-токен для доступа
def list_inactive_vm():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.name != 'admin':
        return jsonify(msg="Admin access required"), 403
    return jsonify(vm_manager.list_inactive_vm())

@vm_manage_bp.route('/api/vm/start/<vm_name>', methods=['POST'])
@jwt_required()  # Требуется JWT-токен для доступа
def start_vm(vm_name):
    """
    Роут для запуска ВМ по имени.
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь пользователем
    if current_user.role.name != 'user':
        return jsonify(msg="User access required"), 403
    try:
        result = vm_manager.start_vm(vm_name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vm_manage_bp.route('/api/vm/stop/<vm_name>', methods=['POST'])
@jwt_required()  # Требуется JWT-токен для доступа
def stop_vm(vm_name):
    """
    Роут для остановки ВМ по имени.
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь пользователем
    print(current_user.role.name, 'suka')
    if current_user.role.name != 'user':
        return jsonify(msg="User access required"), 403
    try:
        result = vm_manager.stop_vm(vm_name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vm_manage_bp.route('/api/vm/detach-iso/<vm_name>', methods=['POST'])
@jwt_required()  # Требуется JWT-токен для доступа
def detach_iso_vm(vm_name):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь пользователем
    if current_user.role.name != 'user':
        return jsonify(msg="User access required"), 403
    return jsonify(vm_manager.detach_iso(vm_name)), 200

@vm_manage_bp.route('/api/vm/hot-detach-iso/<vm_name>', methods=['GET'])
@jwt_required()  # Требуется JWT-токен для доступа
def hot_detach_iso_vm(vm_name):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь пользователем
    if current_user.role.name != 'user':
        return jsonify(msg="User access required"), 403
    return jsonify(vm_manager.hot_detach_iso(vm_name))

