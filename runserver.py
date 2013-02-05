# app as application for wsgi
from myapp import app as application

application.run(debug=True)