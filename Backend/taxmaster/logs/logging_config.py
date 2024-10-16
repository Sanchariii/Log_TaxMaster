# logging_config.py
import logging
import json
from datetime import datetime
from pytz import UTC

# Create a custom logging handler
class JsonFileHandler(logging.FileHandler):
    def emit(self, record):
        log_entry = self.format(record)
        with open(self.baseFilename, 'a') as f:
            f.write(log_entry + '\n')

# Set up the logger
logger = logging.getLogger('jsonLogger')
logger.setLevel(logging.DEBUG)

# Create a file handler that logs messages in JSON format
json_handler = JsonFileHandler('json_logs.log')
json_handler.setLevel(logging.DEBUG)

# Create a custom formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'Username': record.username,
            'Log_id': record.log_id,
            'Timestamp': datetime.now(UTC).isoformat(),
            'Values': record.values
        }
        return json.dumps(log_record)

json_handler.setFormatter(JsonFormatter())
logger.addHandler(json_handler)
