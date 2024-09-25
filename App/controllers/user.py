from App.models import User, Student
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def create_student(name, email, year, program):
    new_student = Student(name=name, email=email, year=year, program=program)
    db.session.add(new_student)
    db.session.commit()
    return new_student   

def get_student_by_name(name):
    return Student.query.filter(Student.name.like(f"%{name}%")).all()  

def get_student_by_id(student_id):
    return Student.query.get(student_id)
