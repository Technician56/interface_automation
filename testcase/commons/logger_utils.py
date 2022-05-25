# -*- coding: utf-8 -*-
# @time    :2022/4/25 9:06
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :logger_utils.py
import datetime
import logging
import os
import time

from Interface_automation.pytest.testcase.commons.config_utils import ConfigUtils


class LoggerUtils:

    def create_logger(self, name="logger"):
        # 创建一个日志器, 全局的级别为DEBUG
        logger = logging.getLogger(name)
        logger.level = logging.DEBUG
        if not logger.handlers:
            # 获得config.yaml中的logger信息
            logger_config = ConfigUtils().get_logger_config()
            # 获得处理器的格式
            formatter = logging.Formatter(fmt=logger_config["formatter"], datefmt=logger_config["datefmt"])
            # 获取路径，判断是否存在: 不存在先创建
            log_file = ConfigUtils().get_abs_path() + logger_config["path"]
            log_name = f"/log_{str(datetime.datetime.today().strftime('%Y%m%d'))}.log"
            log_path = log_file + log_name
            if not os.access(log_file, os.F_OK):
                os.makedirs(log_file)
            # 新增文件处理器
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            # 读取文件处理器的级别，并设置
            file_level = self.set_level(logger_config["log_level"])
            file_handler.setLevel(file_level)
            # # 新增文件过滤器
            # file_handler.addFilter()

            # 新增控制台处理器.设置格式器，日志级别为INFO
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(logging.INFO)

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
        return logger

    # 根据读取到的信息设置返回级别
    @staticmethod
    def set_level(msg):
        msg = str(msg).lower()
        if msg == "debug":
            return logging.DEBUG
        elif msg == "info":
            return logging.INFO
        elif msg == "warning" or msg == "warn":
            return logging.WARN
        elif msg == "error":
            return logging.ERROR
        elif msg == "critical":
            return logging.CRITICAL
        else:
            return logging.DEBUG


def debug(msg):
    LoggerUtils().create_logger().debug(msg)


def info(msg):
    LoggerUtils().create_logger().info(msg)


def warn(msg):
    LoggerUtils().create_logger().warn(msg)


def warning(msg):
    LoggerUtils().create_logger().warning(msg)


def error(msg):
    LoggerUtils().create_logger().error(msg)


def critical(msg):
    LoggerUtils().create_logger().critical(msg)




if __name__ == '__main__':
    LoggerUtils().create_logger().info("111")
