from app import db
from app.models import Users,Messes,UserMessEnroll
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, current_app
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload 

class MessService:
    
    @staticmethod
    def create_mess(data):
        """Creates a new mess."""
        try:
            # Check if the mess with same username or email already exists
            existing_mess = Messes.query.filter((Messes.mess_username == data['mess_username']) | (Messes.mess_email == data['mess_email'])).first()
            if existing_mess:
                return {"message": "Mess username or email already exists", "status":400}, 400
            hash_password = generate_password_hash(data.get('password'), method='pbkdf2:sha256', salt_length=8)
            # Create new Mess instance
            new_mess = Messes(
                mess_id=data['mess_id'],
                mess_name=data['mess_name'],
                mess_username=data['mess_username'],
                mess_email=data['mess_email'],
                password = hash_password,
                mess_address=data['mess_address'],
                city=data['city'],
                monthly_charges=data['monthly_charges'],
                cost_per_day=data['cost_per_day']
            )
            db.session.add(new_mess)
            db.session.commit()

            return {"message": "Mess created successfully", "status": 201}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}","status": 500}, 500

    @staticmethod
    def update_mess(mess_id, data):
        """Updates an existing mess."""
        mess = Messes.query.get(mess_id)
        if not mess:
            return {"message": "Mess not found"}, 404
        
        try:
            # Update fields if provided in the request
            if 'mess_name' in data:
                mess.mess_name = data['mess_name']
            if 'mess_username' in data:
                existing_mess = Messes.query.filter(Messes.mess_username == data['mess_username'], Messes.mess_id != mess_id).first()
                if existing_mess:
                    return {"message": "Mess username already taken"}, 400
                mess.mess_username = data['mess_username']
            if 'mess_email' in data:
                existing_mess = Messes.query.filter(Messes.mess_email == data['mess_email'], Messes.mess_id != mess_id).first()
                if existing_mess:
                    return {"message": "Mess email already taken"}, 400
                mess.mess_email = data['mess_email']
            if 'mess_address' in data:
                mess.mess_address = data['mess_address']
            if 'city' in data:
                mess.city = data['city']
            if 'monthly_charges' in data:
                mess.monthly_charges = data['monthly_charges']
            if 'cost_per_day' in data:
                mess.cost_per_day = data['cost_per_day']

            # Save the changes
            db.session.commit()
            return {"message": "Mess updated successfully", "status": 200}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}","status":500}, 500

    @staticmethod
    def login_mess(data):
        """Authenticates mess and returns JWT token if successful."""
        mess = Messes.query.filter_by(mess_email=data['mess_email']).first()
        if mess and check_password_hash(mess.password, data['password']):
            # Generate JWT token
            token = jwt.encode({
                'sub': mess.mess_id,
                'exp': datetime.utcnow() + timedelta(days=30)
            }, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")

            return {"message": "Login Success","token": token,"status":200}, 200
        return {"message": "Invalid username or password","token": "","status":401}, 401

    @staticmethod
    def get_mess_by_id(mess_id):
        """Fetch a single mess by its ID."""
        mess = Messes.query.get(mess_id)
        if mess:
            return {"mess": MessService.mess_to_dict(mess),"message": "Mess found"}, 200
        return {"mess": "","message": "Mess not found"}, 404
    
    # enroll a user in particular mess
    @staticmethod
    def enroll_user(user_id, mess_id):
        """Enroll a user in a mess."""
        # Check if the user exists
        user = Users.query.filter_by(user_id=user_id).first()
        if not user:
            return {"message": "User not registered","status": 404}, 404

        # Check if the user is already enrolled in another mess
        existing_enrollment = UserMessEnroll.query.filter_by(user_id=user_id).first()
        if existing_enrollment:
            return {"message": "User already enrolled in another mess","status": 400}, 400

        # Enroll the user
        enrollment = UserMessEnroll(user_id=user_id, mess_id=mess_id, start_date=datetime.utcnow(), end_date=None)
        db.session.add(enrollment)
        db.session.commit()

        return {"message": "User enrolled successfully","status": 201}, 201
    
    @staticmethod
    def get_users_enrolled_in_mess(mess_id):
        """Fetch all users enrolled in a particular mess."""
        # Query to get all users enrolled in the specified mess
        enrollments = (
            UserMessEnroll.query.filter_by(mess_id=mess_id)
            .options(joinedload(UserMessEnroll.user))  # If you have a relationship defined
            .all()
        )

        # Prepare a list to store user details
        enrolled_users = []
        for enrollment in enrollments:
            user = enrollment.user  # Assuming a relationship is set up
            enrolled_users.append({
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "enrollment_id": enrollment.enrollment_id,
                "start_date": enrollment.start_date,
                "end_date": enrollment.end_date,
            })

        return {"users": enrolled_users, "status": 200}, 200
    
    @staticmethod
    def get_all_messes():
        """Fetch all messes."""
        messes = Messes.query.all()
        return {"messes": [MessService.mess_to_dict(mess) for mess in messes]}, 200

    @staticmethod
    def mess_to_dict(mess):
        """Helper method to convert Mess object to a dictionary."""
        return {
            'mess_id': mess.mess_id,
            'mess_name': mess.mess_name,
            'mess_username': mess.mess_username,
            'mess_email': mess.mess_email,
            'mess_address': mess.mess_address,
            'city': mess.city,
            'monthly_charges': mess.monthly_charges,
            'cost_per_day': mess.cost_per_day
        }
