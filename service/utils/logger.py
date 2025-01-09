import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from core.config import settings


# def setup_logger(name: str) -> logging.Logger:
#     logger = logging.getLogger(name)
#     logger.setLevel(settings.LOG_LEVEL)
#
#     # 创建日志目录
#     log_dir = Path(settings.LOG_DIR)
#     log_dir.mkdir(exist_ok=True)
#
#     # 文件处理器 - 按天切割，保留指定天数
#     file_handler = TimedRotatingFileHandler(
#         filename=log_dir / f"{name}.log",
#         when="midnight",
#         interval=1,
#         backupCount=settings.LOG_RETENTION_DAYS,
#         encoding="utf-8"
#     )
#
#     # 控制台处理器
#     console_handler = logging.StreamHandler()
#
#     # 设置格式
#     formatter = logging.Formatter(settings.LOG_FORMAT)
#     file_handler.setFormatter(formatter)
#     console_handler.setFormatter(formatter)
#
#     # 添加处理器
#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)
#
#     return logger
def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # 防止重复添加处理器
    if not logger.handlers:
        # 创建日志目录
        log_dir = Path(settings.LOG_DIR)
        log_dir.mkdir(exist_ok=True)

        # 文件处理器 - 按天切割，保留指定天数
        file_handler = TimedRotatingFileHandler(
            filename=log_dir / f"{name}.log",
            when="midnight",
            interval=1,
            backupCount=settings.LOG_RETENTION_DAYS,
            encoding="utf-8"
        )

        # 控制台处理器
        console_handler = logging.StreamHandler()

        # 设置格式
        formatter = logging.Formatter(settings.LOG_FORMAT)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # 禁用父级日志记录器传播
    logger.propagate = False

    return logger


main_log = setup_logger("main")
api_log = setup_logger("api")
user_log = setup_logger("user")
database_log = setup_logger("database")
file_log = setup_logger("file")
