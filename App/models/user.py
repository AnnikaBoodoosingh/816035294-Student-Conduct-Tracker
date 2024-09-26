from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Student(db.Model):
    studentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    year = db.Column(db.String(20), nullable=False)
    program = db.Column(db.String(100), nullable=False)

    reviews = db.relationship('Review', backref='student', lazy=True)

    def __init__(self, name, email, year, program):
        self.name = name
        self.email = email
        self.year = year
        self.program = program

    def get_json(self):
        return {
            'studentID': self.studentID,
            'name': self.name,
            'email': self.email,
            'year': self.year,
            'program': self.program
        }


class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)   
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50), nullable=False)  
    comments = db.Column(db.String(500), nullable=True)

    def __init__(self, studentID, date, type, comments=None):
        self.studentID = studentID
        self.date = date
        self.type = type
        self.comments = comments

    def get_json(self):
        return {
            'reviewID': self.reviewID,
            'studentID': self.studentID,
            'date': self.date.isoformat(),
            'type': self.type,
            'comments': self.comments
        }