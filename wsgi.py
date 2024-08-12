import sys
import os

# Add the virtual environment's site-packages to sys.path
sys.path.insert(0, '/var/www/myappenv/venv/lib/python3.8/site-packages')

# Add your application's directory to the sys.path
sys.path.insert(0, '/var/www/myappenv')

# Set the environment variable to the virtual environment's path
os.environ['PYTHONHOME'] = '/var/www/myappenv'

# Import the Flask app
from app import app as application
