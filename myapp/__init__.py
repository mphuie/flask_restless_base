from flask import Flask
app = Flask(__name__)

from myapp.views import aview
from myapp.database import db_session

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()