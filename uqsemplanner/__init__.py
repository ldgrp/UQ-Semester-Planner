from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

import uqsemplanner.config
import uqsemplanner.database
import uqsemplanner.routes
