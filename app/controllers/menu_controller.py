from flask import Blueprint, request, jsonify
from app.services.menu_service import MenuService

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/create-menu', methods=['POST'])
def create_menu():
    data = request.get_json()
    response, status = MenuService.create_menu(data)
    return jsonify(response), status

@menu_bp.route('/update-menu/<string:menu_id>', methods=['PUT'])
def update_menu(menu_id):
    data = request.get_json()
    response, status = MenuService.update_menu(menu_id, data)
    return jsonify(response), status

@menu_bp.route('/delete-menu/<string:menu_id>', methods=['DELETE'])
def delete_menu(menu_id):
    response, status = MenuService.delete_menu(menu_id)
    return jsonify(response), status

@menu_bp.route('/get-all-menus/<string:mess_id>', methods=['GET'])
def get_all_menus(mess_id):
    response, status = MenuService.get_all_menus(mess_id=mess_id)
    return jsonify(response), status
