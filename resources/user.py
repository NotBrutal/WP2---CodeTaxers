from flask import request
from flask_bcrypt import generate_password_hash
from db import DB
from datetime import datetime
import string
import random # define the random module
# from flask_jwt_extended import (
#     jwt_required,
#     create_access_token,
#     get_jwt_identity
# )
from datetime import date

def test():
    return{'message':'start server'}, 201 

def create_teacher():
    args = request.json
    hashed_password = generate_password_hash(args['teacher_password'])

    qry = '''
    INSERT INTO
        `teachers`
            (`display_name`, `username`, `teacher_password`, `date_created`, `is_admin`)
            VALUES(:display_name, :username, :teacher_password, :date_created, :is_admin)
    '''
    data = {
        "display_name": args["display_name"], 
        "username": args["username"],
        "teacher_password": hashed_password,
        "date_created": datetime.now(),
        "is_admin": 0
    }
    try:
        id = DB.insert(qry, data)
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')

    return {'message': 'success', 'id': id}, 201

def create_user():
    args = request.json
    hashed_password = generate_password_hash(args['password'])

    qry = '''
    INSERT INTO
        `users`
            (`email`, `password`, `firstname`, `lastname`)
            VALUES(:email, :password, :firstname, :lastname)
    '''
    data = {
        "email": args["email"], 
        "password": hashed_password,
        "firstname": args["firstname"],
        "lastname": args["lastname"]
    }
    try:
        id = DB.insert(qry, data)
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')

    return {'message': 'success', 'id': id}, 201

def get_user():

    qry = '''
    SELECT * FROM users
    '''
   
    try:
        rows = DB.all(qry)
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')

    return {'message': 'success', 'rows': rows}, 201