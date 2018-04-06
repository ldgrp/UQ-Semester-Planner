from flask import Flask
app = Flask(__name__)

import uqsemplanner.config
import uqsemplanner.database
import uqsemplanner.views
