import sys
import os

# Add your project directory to the Python path
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import your Flask app
from app import app as application

# Make sure app is in production mode
application.config['DEBUG'] = False

# For PythonAnywhere, ensure the app is ready
if __name__ == '__main__':
    application.run()
