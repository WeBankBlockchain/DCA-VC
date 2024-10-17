import sys

from loguru import logger
from configparser import ConfigParser

config_file = 'config.conf'
cf = ConfigParser()
cf.read(config_file)
log_file_path = cf.get('log', "logFile")
app_monitor_path = cf.get('log', "monitorFile")
log_level = cf.get("log", "level")

class Log:
    def __init__(self):
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 输出到文件的格式,注释下面的add',则关闭日志写入
        self.logger.add(log_file_path, level=log_level,
                        filter=lambda record: "app" not in record["extra"],
                        format="[{level}]"
                               "[{time:YYYY-MM-DD HH:mm:ss.SSS}]"
                               "[{process.name}-{thread.name}] "  # 进程名
                               "{module}.{function}"  # 模块名.方法名
                               ":{line} | "  # 行号
                               "{message}",  # 日志内容
                        rotation="00:00",
                        retention="365 days",
                        compression = "gz",
                        enqueue = True)

        self.logger.add(app_monitor_path,
                        filter=lambda record: "app" in record["extra"],
                        level='INFO',
                        format="[{level}]"
                               "[{time:YYYY-MM-DD HH:mm:ss.SSS}]"
                               "[{process.name}-{thread.name}] "  # 进程名
                               "{message}",  # 日志内容
                        rotation="00:00",
                        retention="365 days",
                        compression = "gz",
                        enqueue = True)

    def get_logger(self):
        return self.logger

my_logger = Log().get_logger()


def ss():
    my_logger.info(2222222)
    my_logger.debug(2222222)
    my_logger.warning(2222222)
    my_logger.error(2222222)


if __name__ == '__main__':
    ss()

