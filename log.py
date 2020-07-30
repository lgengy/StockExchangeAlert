from datetime import datetime


class Log(object):
    """日志记录类"""

    def __init__(self, path, file_name, file_name_error):
        """初始化日志路径、一般日志文件名和错误日志文件名"""

        self.log_path = path
        self.file_name = file_name
        self.file_name_error = file_name_error

    def log_write(self, log_info):
        with open(self.log_path + "\\" + self.file_name, "at", encoding="UTF-8") as f:
            print(log_info.time + "> " + log_info.content, file=f)

    def log_error_write(self, log_info):
        with open(self.log_path + "\\" + self.file_name_error, "at", encoding="UTF-8") as f:
            print(log_info.time + "> " + log_info.content, file=f)

    class LogInfo(object):
        """日志信息类，保存日志写入时间和写入内容"""

        def __init__(self, content):
            self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            self.content = content


# log = Log("E:\\practice\\SSECrawier", "right", "wrong")

# log.log_write(log.LogInfo("我还是对的"))
# log.log_error_write(log.LogInfo("我还是错的"))
