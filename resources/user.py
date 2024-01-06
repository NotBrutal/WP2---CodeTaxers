from flask import request
from flask_bcrypt import generate_password_hash
from db import DB
from datetime import datetime
from flask import Flask, jsonify

from lib.testgpt.testgpt import TestGPT, FakeTestGPT
import string
import openai
from dotenv import load_dotenv
import os
from openai import RateLimitError
from flask_bcrypt import check_password_hash
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity
)


import random # define the random module

# from flask_jwt_extended import (
#     jwt_required,
#     create_access_token,
#     get_jwt_identity
# )
from datetime import date

def test():
    return{'message':'start server'}, 201 

def teacher_login():
        # Get data from request
    display_name = request.json.get('display_name', None)
    teacher_password = request.json.get('teacher_password', None)

    # Get user from database
    qry = 'SELECT * FROM `teachers` WHERE `display_name` = :display_name'
    user = DB.one(qry, {'display_name': display_name})

    # Check if user exists and password is correct
    if not user or not check_password_hash(user['teacher_password'], teacher_password):
        return {'message': 'invalid credentials'}, 401
    
    # Delete password from user (should not be sent back!)
    del user['teacher_password']

    # Create JWT
    access_token = create_access_token(user)
    return jsonify(access_token = access_token, message = 'success'), 200

def user_login():
    # Get data from request
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Get user from database
    qry = 'SELECT * FROM `users` WHERE `email` = :email'
    user = DB.one(qry, {'email': email})

    # Check if user exists and password is correct
    if not user or not check_password_hash(user['password'], password):
        return {'message': 'invalid credentials'}, 401
    
    # Delete password from user (should not be sent back!)
    del user['password']

    # Create JWT
    access_token = create_access_token(user)
    return jsonify(access_token = access_token, message = 'success'), 200
    

@jwt_required()
def me():
    user = get_jwt_identity()
    return jsonify(user=user, message='success'), 200

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

def get_teachers():
    qry = '''
    SELECT * FROM teachers
    '''
   
    try:
        rows = DB.all(qry)
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')

    return {'message': 'success', 'rows': rows}, 201

def get_specific_teacher(teacher_id):
    qry = '''
    SELECT * FROM teachers WHERE teacher_id = ?
    '''
   
    try:
        rows = DB.all(qry, (teacher_id,))
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')

    return {'message': 'success', 'rows': rows}, 201

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

def get_specific_notes(note_id):
    
    qry = '''
    SELECT notes.note_id , notes.title, notes.note_source, notes.is_public, teachers.display_name, notes.category_id,  categories.omschrijving, notes.date_created
    FROM notes
    INNER JOIN teachers 
    on notes.teacher_id = teachers.teacher_id
    INNER JOIN categories 
    ON notes.category_id= categories.category_id

    WHERE note_id =?
	
    '''

    try:
        rows = DB.all(qry, (note_id,))
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')

    return {'message': 'success', 'rows': rows}, 201

def insert_question():
    args = request.json

    qry = '''
    INSERT INTO
        `questions`
            (`note_id`, `exam_question`, `date_created`)
            VALUES(:note_id, :exam_question, :date_created)
    '''
    data = {
        "note_id": args["note_id"], 
        "exam_question": args["exam_question"],
        "date_created": args["date_created"]
    }
    try:
        id = DB.insert(qry, data)
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')

    return {'message': 'success', 'id': id}, 201



def create_question():
    #ik pak open question uit de request in de frontend en voeg het toe in een var die ik daarna met een andere endpoint in de db 


    if not request.is_json:
        return {'message': 'Invalid request, JSON expected'}, 400

    # Get the open question from the JSON request body
    request_data = request.get_json()
    open_question = request_data.get('open_question')

   
    api_key = os.getenv("API_KEY")
    test_gpt = TestGPT(api_key)
    generated_question = test_gpt.generate_open_question(note=open_question)


    return {'message': 'success', 'generated_question': generated_question}, 201

def get_notes(note_id):
    qry = '''
    SELECT notes.note_id , notes.note
    FROM notes
    WHERE note_id = ?
    
    '''

    try:
        rows = DB.all(qry, (note_id,))
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')

    return {'message': 'success', 'rows': rows}, 201


def get_questions():
    qry = '''
     SELECT * FROM questions
        '''
    
    try:
        rows = DB.all(qry)
    except Exception:
        print('Er is een probleem opgetreden, contact de admin.')
    
    return {'message': 'success', 'rows': rows}, 201

