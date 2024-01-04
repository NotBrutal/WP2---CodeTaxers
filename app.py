from flask import Flask
# from flask_jwt_extended import JWTManager
from flask_cors import CORS
from db import DB
from resources.user import test, create_teacher, create_user, get_user, get_specific_notes, create_notes
app = Flask(__name__)
app.debug = True

# Enable cors on the server
CORS(app)

# Register the JWT manager
#app.config['JWT_SECRET_KEY'] = 'super-secret' # Change this!
#jwt = JWTManager(app)
# ============================ Routes ============================

# JWT routes
app.add_url_rule('/test', None, test, methods=['GET'])
app.add_url_rule('/get_user', None, get_user, methods=['GET'])
app.add_url_rule('/get_specific_notes/<int:note_id>', None, get_specific_notes, methods=['GET'])
app.add_url_rule('/create_teacher', None, create_teacher, methods=['POST'])
app.add_url_rule('/create_user', None, create_user, methods=['POST'])
app.add_url_rule('/create_notes', None, create_notes, methods=['POST'])






# Start app
if __name__ == '__main__':
    DB.create()
    app.run()