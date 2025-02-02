from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

# Blueprint for user-related routes
user_bp = Blueprint('user', __name__)

# to create a user or register user
@user_bp.route('/create_user', methods=['POST'])
def create_user():
    """Handles user creation."""
    user_data = request.json
    message, status = UserService.create_user(user_data)
    return jsonify({"message" : message, "status":status}), status

# to get a specific user
@user_bp.route('/get_user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    username = request.args.get('username')
    email = request.args.get('email')
    # Fetch user based on provided parameters (id, username, or email)
    user = None
    if user_id:
        user = UserService.get_user_by(user_id=user_id)
    elif username:
        user = UserService.get_user_by(username=username)
    elif email:
        user = UserService.get_user_by(email=email)

    if user:
        return jsonify(UserService.user_to_dict(user)), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@user_bp.route('/login', methods = ['POST'])
def user_login():
    data = request.json
    json_response,status_code = UserService.authenticate_user(data['email'],data['password'])
    return json_response,status_code

@user_bp.route('/update-user',methods = ['POST'])
def update_user():
    user_id = request.args.get('user_id')
    data = request.json
    json_res,status = UserService.update_user(user_id=user_id,data=data)
    return json_res,status
