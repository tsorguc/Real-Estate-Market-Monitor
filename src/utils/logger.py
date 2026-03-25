import logging
import os

# Ensure we log to the correct file in the root directory
log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../pipeline.log"))

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)