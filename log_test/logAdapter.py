import logging
import json
import logging.config


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, prefix, logger):
        super(LoggerAdapter, self).__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.prefix, msg), kwargs


if __name__ == '__main__':

    with open('logging.json', 'rt') as f:
        config = json.load(f)

    logging.config.dictConfig(config)

    logger = logging.getLogger("")

    logger = LoggerAdapter("add_info", logger)
    logger.info("test!!!")

    # logging.addLevelName(15, "DATA")
    # logging.DATA = 15
    #
    # logger.log(logging.DATA, "message")
