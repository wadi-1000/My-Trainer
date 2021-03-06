from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())

    
    pass_secure = db.Column(db.String(255))
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
            
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)    
    
    def __repr__(self):
        return f'User {self.username}'
    
class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(255))
    users = db.relationship('User', backref = 'role', lazy="dynamic")
    
    def __repr__(self):
        return f'User {self.name}'   
    
class ExerciseInfo:
    '''
    Exercise info class to define exercise objects
    '''
    def __init__(self,id,name,description,category,license_author,creation_date):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.license_author = license_author
        self.creation_date = creation_date
        

       



    
    

      

    