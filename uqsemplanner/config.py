from uqsemplanner import app
import os

app.config.from_envvar('SEMPLANNER_SETTINGS')
app.config.update(
    DATABASE=os.path.join(app.root_path, 'uqsemplanner.db')
)
