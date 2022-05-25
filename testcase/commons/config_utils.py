# -*- coding: utf-8 -*-
# @time    :2022/4/25 14:06
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :config_utils.py
import os

import yaml


class ConfigUtils:
    # @staticmethod
    # def get_abs_path():
    #     return os.getcwd().split("pytest")[0] + "pytest"

    @staticmethod
    def get_abs_path():
        return "H:/pyProjects/learn/Interface_automation/pytest"

    def get_logger_config(self):
        with open(self.get_abs_path() + "/config_yaml.yaml", mode="r", encoding="utf-8") as file:
            return yaml.load(file, yaml.FullLoader)["logger"]
