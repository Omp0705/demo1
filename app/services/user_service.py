from app import db
from sqlalchemy.exc import IntegrityError
from flask import current_app
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Users,UserCounter

class UserService:

    @staticmethod
    def create_user(user_data):
        email = user_data['email']

        if Users.query.filter_by(email=email).first():
            return "User already exists", 400
        hashed_password = generate_password_hash(user_data.get('password'), method='pbkdf2:sha256', salt_length=8)
        new_user = Users(
            user_id = UserService.create_userid(),
            name  = user_data.get('name'),
            username = user_data.get('username'),
            email = user_data.get('email'),
            password = hashed_password,
            mobile_no = user_data.get('mobile_no')
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return "User created", 201  # HTTP status code 201 Created
        except IntegrityError:
            db.session.rollback()
            return "User already exists", 409  # HTTP status code 409 Conflict
        
    @staticmethod
    def getallusers():
         return Users.query.all()
    
    @staticmethod
    def get_user_by(**kwargs):
        """
        Fetch user based on provided keyword arguments.
        Supported kwargs: id, username, email.
        """
        if 'user_id' in kwargs:
            return Users.query.filter_by(user_id=kwargs['user_id']).first()
        elif 'username' in kwargs:
            return Users.query.filter_by(username=kwargs['username']).first()
        elif 'email' in kwargs:
            return Users.query.filter_by(email=kwargs['email']).first()
        else:
            return None
        
    # to login user JWT token will be returned 
    @staticmethod
    def authenticate_user(email, password):
        """Authenticates user and returns JWT token if successful."""
        user = Users.query.filter_by(email=email).first()
        
        # Use check_password_hash to verify the password
        if user and check_password_hash(user.password, password):
            # Generate JWT token
            token = jwt.encode({
                'id': user.user_id,
                'exp': datetime.utcnow() + timedelta(days=30)
            }, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")

            return {"status": 1, "token": token,"message" : "Login Success"}, 200
        return {"status": 0 ,"message": "Invalid credentials"}, 401
    
    @staticmethod
    def update_user(user_id, data):
        """Updates user details."""
        user = Users.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404
        
        # Update the user details
        if 'username' in data:
            user.username = data['username']
        
        if 'email' in data:
            user.email = data['email']
        if 'mobile_no' in data:
            user.mobile_no = data['mobile_no']
        if 'password' in data:
            # Hash the password before storing it
            user.password = generate_password_hash(data['password'])
        
        try:
            # Save changes to the database
            db.session.commit()
            return {"message": "User updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500
        
    # to auto generate user_id
    @staticmethod
    def create_userid():
        counter = UserCounter.query.first()  # Get the first record in the user_counter table

        if counter:
            new_number = counter.increment_user_number()  # Increment the user number
            return f"USER{new_number}"
        else:
            # If the table is empty, create the first entry
            new_counter = UserCounter(last_user_number=000)
            db.session.add(new_counter)
            db.session.commit()
            new_number = counter.increment_user_number  # Increment the user number
            return f"USER{new_number}"
    
    @staticmethod
    def user_to_dict(user):
        """Convert a user object to a dictionary."""
        return {
            "user_id": user.user_id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "mobile_no": user.mobile_no
        }

    @staticmethod
    def users_to_dict(users):
        """Convert a list of user objects to a list of dictionaries."""
        return [UserService.user_to_dict(user) for user in users]