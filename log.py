import logging
import logging.handlers
from pathlib import Path


class Log(object):
    """日志类，封装了python自带的logging"""

    def __init__(self, log_directory, log_name):
        self.__log_directory = log_directory
        self.__log_name = log_name
        if not Path(log_directory).exists():
            Path(log_directory).mkdir()

    def log_initialize(self):
        self.logger = logging.getLogger(self.__log_name)
        self.logger.setLevel(logging.DEBUG)

        fileHandler = logging.handlers.RotatingFileHandler(
            self.__log_directory + self.__log_name + ".log", mode="a", maxBytes=1024*1024*2, backupCount=20, encoding="UTF-8")

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")
        fileHandler.setFormatter(formatter)

        self.logger.addHandler(fileHandler)


# log = Log("E:\\practice\\SSECrawier\\log\\", "StockExchangeAlert")
# log.log_initialize()
# for i in range(1000):
#     log.logger.info("我是第" + str(i) + "号")
