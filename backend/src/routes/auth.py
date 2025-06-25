from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import db, User
from core.vm_manager import VMManager

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()
vm_manager = VMManager()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, username=username), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    # Проверяем, что все необходимые данные предоставлены
    if not username or not old_password or not new_password:
        return jsonify({"msg": "Missing required fields"}), 400

    # Находим пользователя в базе данных
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Проверяем старый пароль
    if not user.check_password(old_password):
        return jsonify({"msg": "Old password is incorrect"}), 400

    # Обновляем пароль пользователя
    user.set_password(new_password)
    db.session.commit()

    # Меняем пароль VNC для виртуальной машины, если она существует
    vm_name = user.vm_name  # Получаем имя виртуальной машины из модели пользователя
    if vm_name:
        try:
            # Изменяем пароль VNC для указанной виртуальной машины
            vm_manager.change_vnc_password(vm_name=vm_name, new_password=new_password)

            #нужно выключить и включить ВМ, чтобы обновилась XML-конфига, дописать ребут?)
            vm_manager.stop_vm(vm_name=vm_name)
            vm_manager.start_vm(vm_name=vm_name)
            return jsonify({
                "msg": "Password changed successfully",
                "vnc_msg": f"VNC password for VM '{vm_name}' updated successfully"
            }), 200

        except Exception as e:
            # Если возникла ошибка при изменении пароля VNC, возвращаем её
            return jsonify({
                "msg": "Password changed successfully, but failed to update VNC password",
                "error": str(e)
            }), 500
    else:
        return jsonify({
            "msg": "Password changed successfully",
            "vnc_msg": "No virtual machine associated with this user"
        }), 200
