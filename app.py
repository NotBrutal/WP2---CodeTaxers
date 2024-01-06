from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from db import DB
from dotenv import load_dotenv
import os
from resources.user import test, create_teacher, create_user, get_user, get_specific_notes, create_question, get_notes, get_teachers, get_specific_teacher, user_login, me, teacher_login,insert_question, get_questions
app = Flask(__name__)
app.debug = True

# Enable cors on the server
CORS(app)

# Register the JWT manager
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_TOKEN_SECRET") # Change this!
jwt = JWTManager(app)
# ============================ Routes ============================

# JWT routes
app.add_url_rule('/test', None, test, methods=['GET'])
app.add_url_rule('/get_user', None, get_user, methods=['GET'])
app.add_url_rule('/get_specific_notes/<int:note_id>', None, get_specific_notes, methods=['GET'])
app.add_url_rule('/get_notes/<int:note_id>', None, get_notes, methods=['GET'])
app.add_url_rule('/get_teachers', None, get_teachers, methods=['GET'])
app.add_url_rule('/get_specific_teachers/<int:teacher_id>', None, get_specific_teacher, methods=['GET'])
app.add_url_rule('/get_questions', None, get_questions, methods=['GET'])
app.add_url_rule('/me', None, me, methods=['GET'])
app.add_url_rule('/create_teacher', None, create_teacher, methods=['POST'])
app.add_url_rule('/create_user', None, create_user, methods=['POST'])
app.add_url_rule('/create_question', None, create_question, methods=['POST'])
app.add_url_rule('/user_login', None, user_login, methods=['POST'])
app.add_url_rule('/teacher_login', None, teacher_login, methods=['POST'])
app.add_url_rule('/insert_question', None, insert_question, methods=['POST'])

# ============================ Main ============================

# Start app
if __name__ == '__main__':
    DB.create()
    app.run()