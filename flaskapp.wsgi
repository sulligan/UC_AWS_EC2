import sys
import os

# Add your project directory to the sys.path
project_home = '/home/ubuntu/flaskapp'
if project_home not in sys.path:
    sys.path.append(project_home)

# Set the FLASK_APP environment variable (this is optional)
os.environ['FLASK_APP'] = 'flaskapp.py'

# Import the application
from flaskapp import app as application
