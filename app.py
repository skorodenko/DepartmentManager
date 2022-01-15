import sys
import logging
from department_app import init_app
init_app()

from department_app import app


file_handler = logging.FileHandler(filename="department_app.log", mode="w")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

logger = app.logger
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.DEBUG)

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.addHandler(file_handler)
werkzeug_logger.addHandler(console_handler)
werkzeug_logger.setLevel(logging.DEBUG)
