from uqsemplanner import app
import os

app.config.from_envvar('SEMPLANNER_SETTINGS')
app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(app.root_path, 'uqsemplanner.db')
)
