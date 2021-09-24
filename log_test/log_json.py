import logging
import logging.config
import json
import os

with open('logging.json', 'rt') as f:
    config = json.load(f)

logging.config.dictConfig(config)

logger = logging.getLogger()
logger.info("test!")
logger = logging.getLogger("my_module")
logger.error("hi")
