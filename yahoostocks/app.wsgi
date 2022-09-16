#! /usr/bin/python3.8

import sys

sys.path.insert(0, '/var/www/flask/a')
#sys.path.insert(0, '/var/www/flask/a/venv/bin/activate_this.py')
#activate_this = '/var/www/flask/a/venv/bin/activate_this.py'

#with open(activate_this) as file_:
#with open(activate_this) as file:
#  exec(file.read(), dict(__file__=activate_this))

from app import app as application