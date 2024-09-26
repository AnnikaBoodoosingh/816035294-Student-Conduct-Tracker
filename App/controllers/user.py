from App.models import User, Student, Review
from App.database import db
from datetime import date

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

def create_review(studentID, review_type, comments=None):
    student = Student.query.get(studentID)
    if not student:
        return None, "Student not found"
    
    review_date = date.today()
    
    new_review = Review(studentID=studentID, date=review_date, type=review_type, comments=comments)
    
    db.session.add(new_review)
    db.session.commit()
    
    return new_review, "Review created successfully"

def get_reviews_for_student(studentID):
    student = Student.query.get(studentID)
    if not student:
        return None, "Student not found"
    
    reviews = Review.query.filter_by(studentID=studentID).all()
    return reviews, "Reviews retrieved successfully"