import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
logs_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
)
os.makedirs(logs_dir, exist_ok=True)

# Configure logger
logger = logging.getLogger("capstone")
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create file handler for more detailed logs
file_handler = RotatingFileHandler(
    os.path.join(logs_dir, "app.log"), maxBytes=10485760, backupCount=10  # 10MB
)
file_handler.setLevel(logging.INFO)

# Create formatters and add them to handlers
console_format = logging.Formatter("%(levelname)s: %(message)s")
file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


# Function to get the logger
def get_logger():
    return logger
