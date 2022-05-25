# -*- coding: utf-8 -*-
# @time    :2022/4/24 20:34
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :tcs_custom.py
import base64
import hashlib
import json
import os
import random
import time

import rsa
import yaml

from Interface_automation.pytest.testcase.commons.parametrize_utils import ParametrizeUtils


class TcsCustomUtils:
    # 得到绝对路径
    @staticmethod
    def get_abs_path():
        return os.getcwd().split("pytest")[0] + "pytest"

    # 获得extract中的变量值
    def get_extract_value(self, key):
        with open(self.get_abs_path() + "/extract.yaml", mode="r", encoding="utf-8") as file:
            return yaml.load(file, yaml.FullLoader)[key]

    # 得到sign中的值
    def get_sign(self, node):
        with open(self.get_abs_path() + "/config_yaml.yaml", mode="r", encoding="utf-8") as file:
            return yaml.load(file, yaml.FullLoader)["sign"][node]

    # 获得随机数
    @staticmethod
    def get_random_number(min_num, max_num):
        return str(random.randint(int(min_num), int(max_num)))


