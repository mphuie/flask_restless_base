# app as application for wsgi
from myapp import app as application

application.run(host='0.0.0.0', debug=True)