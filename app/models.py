from . import db
from datetime import datetime

class Users(db.Model):
    user_id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255),unique = True)
    email = db.Column(db.String(255),unique = True)
    password = db.Column(db.String(255))
    mobile_no = db.Column(db.String(20))

    def __repr__(self):
        return f"<User {self.user_id}>"

class Messes(db.Model):
    mess_id = db.Column(db.String(255), primary_key=True)
    mess_name = db.Column(db.String(255))
    mess_username  =db.Column(db.String(255),unique = True)
    mess_email = db.Column(db.String(255),unique = True)
    password = db.Column(db.String(255))
    mess_address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    monthly_charges = db.Column(db.Float)
    cost_per_day = db.Column(db.Float)

    def __repr__(self):
        return f"<Mess {self.mess_id}>"

class Menu(db.Model):
    menu_id = db.Column(db.String(255), primary_key=True)
    mess_id = db.Column(db.String(255), db.ForeignKey('messes.mess_id'))
    menu_date = db.Column(db.Date)
    breakfast = db.Column(db.String(255))
    lunch = db.Column(db.String(255))
    dinner = db.Column(db.String(255))
    day = db.Column(db.String(20))
    description = db.Column(db.Text)
    mess = db.relationship('Messes', backref='menus') # Relationship to Messes

    def __repr__(self):
        return f"<Menu {self.menu_id}>"


class Payment(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'))
    mess_id = db.Column(db.String(255), db.ForeignKey('messes.mess_id'))
    bill_no = db.Column(db.String(255), db.ForeignKey('bills.bill_no'))
    pay_date = db.Column(db.Date)
    transaction_id = db.Column(db.String(255))
    payment_mode = db.Column(db.String(255))
    pay_status = db.Column(db.String(255))
    user = db.relationship('Users', backref='payments')  # Relationship to Users
    mess = db.relationship('Messes', backref='payments')  # Relationship to Messes
    bill = db.relationship('Bills', backref='payments')  # Relationship to Bills


    def __repr__(self):
        return f"<Payment {self.bill_no}>"


class Bills(db.Model):
    bill_no = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'))
    mess_id = db.Column(db.String(255), db.ForeignKey('messes.mess_id'))
    bill_month = db.Column(db.Date)
    bill_amount = db.Column(db.Float)
    bill_status = db.Column(db.String(255))
    prorated = db.Column(db.Boolean, default=False)
    user = db.relationship('Users', backref='bills') # Relationship to Users
    mess = db.relationship('Messes', backref='bills') # Relationship to Messes

    def __repr__(self):
        return f"<Bill {self.bill_no}>"

class UserMessEnroll(db.Model):
    __tablename__ = 'usermessenroll'
    enrollment_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'))
    mess_id = db.Column(db.String(255), db.ForeignKey('messes.mess_id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date, default=None)
    user = db.relationship('Users', backref='enrollments') # Relationship to Users
    mess = db.relationship('Messes', backref='enrollments') # Relationship to Messes

    def __repr__(self):
        return f"<Enrollment {self.enrollment_id}>"
    
class UserCounter(db.Model):
    __tablename__ = 'user_counter'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_user_number = db.Column(db.Integer, nullable=False)

    def __init__(self, last_user_number):
        self.last_user_number = last_user_number

    # Optional: you can create a method to increment and return the new user number
    def increment_user_number(self):
        self.last_user_number += 1
        db.session.commit()
        return self.last_user_number