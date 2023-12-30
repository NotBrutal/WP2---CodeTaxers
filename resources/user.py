from flask import request
from flask_bcrypt import generate_password_hash
from db import DB
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
        "date_created": args["date_created"],
        "is_admin": args["is_admin"]
    }
    try:
        id = DB.insert(qry, data)
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')

    return {'message': 'success', 'id': id}, 201