from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)

import uqsemplanner.config

db = SQLAlchemy(app)

import uqsemplanner.database
import uqsemplanner.routes
