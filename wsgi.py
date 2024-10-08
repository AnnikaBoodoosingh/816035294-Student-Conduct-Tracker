import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_student, get_student_by_name, get_student_by_id, create_review, get_reviews_for_student )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

student_cli = AppGroup('student', help='Student object commands')

@student_cli.command("create", help="Creates a student")
@click.argument("name")
@click.argument("email")
@click.argument("year")
@click.argument("program")
def create_student_command(name, email, year, program):
    student = create_student(name, email, year, program)
    print(f'Student {student.name} created!')


@student_cli.command("get", help="Get a student by name")
@click.argument("name")
def get_student_command(name):
    students = get_student_by_name(name)
    if students:
        for student in students:
            print(f'Found Student: ID: {student.studentID}, Name: {student.name}, Email: {student.email}, Year: {student.year}, Program: {student.program}')
    else:
        print("No students found with that name.")

@student_cli.command("get_by_id", help="Get a student by ID")
@click.argument("student_id", type=int)
def get_student_by_id_command(student_id):
    student = get_student_by_id(student_id)
    if student:
        print(f'Found Student: ID: {student.studentID}, Name: {student.name}, Email: {student.email}, Year: {student.year}, Program: {student.program}')
    else:
        print(f"No student found with ID: {student_id}.")

@student_cli.command("review", help="Create a review for a student")
@click.argument("student_id", type=int)
@click.argument("review_type")
@click.argument("comments", required=False, default=None)
def create_review_command(student_id, review_type, comments):
    review, message = create_review(student_id, review_type, comments)
    if review:
        print(f'Review created successfully for Student ID: {student_id}.')
    else:
        print(message)


@student_cli.command("reviews", help="View reviews for a student")
@click.argument("student_id", type=int)
def view_reviews_command(student_id):
    reviews, message = get_reviews_for_student(student_id)
    if not reviews:
        print(f"No reviews found for student with ID {student_id}.")
    else:
        for review in reviews:
            print(f'Review ID: {review.reviewID}, Type: {review.type}, Comments: {review.comments}, Date: {review.date.isoformat()}')


app.cli.add_command(student_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)