from flask import Flask
from flask_cors import CORS
from db import DB
from resources.user import test
app = Flask(__name__)
app.debug = True

# Enable cors on the server
CORS(app)


# ============================ Routes ============================

# JWT routes
app.add_url_rule('/test', None, test, methods=['GET'])



# Start app
if __name__ == '__main__':
    DB.create()
    app.run()