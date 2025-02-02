from flask import Blueprint, request, jsonify
from app.services.messes_service import MessService
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required

# Blueprint for mess-related routes
mess_bp = Blueprint('mess', __name__)

@mess_bp.route('/create_mess', methods=['POST'])
def create_mess():
    """Handles mess creation."""
    mess_data = request.json
    message, status = MessService.create_mess(mess_data)
    return jsonify(message), status

@mess_bp.route('/update_mess/<string:mess_id>', methods=['PUT'])
@jwt_required()  # Protect this route with JWT authentication
def update_mess(mess_id):
    """Handles updating mess details."""
    mess_data = request.json
    message, status = MessService.update_mess(mess_id, mess_data)
    return jsonify(message), status

@mess_bp.route('/users-enrolled/<string:mess_id>', methods=['GET'])
@jwt_required()  # Protect this endpoint with JWT authentication
def get_users_enrolled(mess_id):
    """Get all users enrolled in a specific mess."""
    response, status = MessService.get_users_enrolled_in_mess(mess_id)
    return jsonify(response), status

@mess_bp.route('/login_mess', methods=['POST'])
def login_mess():
    """Handles mess login."""
    login_data = request.json
    message, status = MessService.login_mess(login_data)
    return jsonify(message), status

@mess_bp.route('/get_all_messes', methods=['GET'])
@jwt_required()  # Protect this route with JWT authentication
def get_all_messes():
    """Handles fetching all messes."""
    message, status = MessService.get_all_messes()
    return jsonify(message), status

@mess_bp.route('/get_mess/<string:mess_id>', methods=['GET'])
@jwt_required()  # Protect this route with JWT authentication
def get_mess(mess_id):
    """Handles fetching a specific mess."""
    message, status = MessService.get_mess(mess_id)
    return jsonify(message), status

@mess_bp.route('/enroll-user',methods = ['POST'])
@jwt_required()
def enroll_user():
    data = request.get_json()
    response,status = MessService.enroll_user(user_id= data['user_id'],mess_id= data['mess_id'])
    return response,status