# -*- coding: utf-8 -*-
# @time    :2022/4/24 16:39
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :yaml_utils.py
import os
import random
import traceback

import yaml

from Interface_automation.pytest.testcase.commons.logger_utils import error
from Interface_automation.pytest.testcase.commons.parametrize_utils import ParametrizeUtils


# def get_object_path():
#     return os.getcwd().split("pytest")[0] + "pytest"

def get_object_path():
    return "H:/pyProjects/learn/Interface_automation/pytest"



def get_extract_yaml(key):
    with open(get_object_path() + "/extract.yaml", mode="r", encoding="utf-8") as file:
        return yaml.load(file, yaml.FullLoader)[key]


def set_extract_yaml(data):
    try:
        with open(get_object_path() + "/extract.yaml", mode="a", encoding="utf-8") as file:
            yaml.dump(data, stream=file, allow_unicode=True)
            # info("取值成功:" + str(data))
    except Exception as e:
        error("接口关联时写入值失败: " + traceback.format_exc())
        raise e


def clear_extract_yaml():
    with open(get_object_path() + "/extract.yaml", mode="w", encoding="utf-8") as file:
        file.truncate()


def get_testcase_yaml(path):
    try:
        with open(get_object_path() + path, mode="r", encoding="utf-8") as file:
            case_info = yaml.load(file, yaml.FullLoader)
            temp_list = []
            for case in case_info:
                if "parametrize" in case.keys():
                    temp_list += ParametrizeUtils().ddt(case)
                else:
                    temp_list += case_info
            return temp_list
    except Exception as e:
        error("获取测试用例异常:" + traceback.format_exc())
        raise e


# 得到sign中的值
def get_sign(node):
    with open(get_object_path() + "/config_yaml.yaml", mode="r", encoding="utf-8") as file:
        return yaml.load(file, yaml.FullLoader)["sign"][node]


def get_base_url(node):
    with open(get_object_path() + "/config_yaml.yaml", mode="r", encoding="utf-8") as file:
        return yaml.load(file, yaml.FullLoader)["base"][node]


# 获得随机数
def get_random_number(min_num, max_num):
    return str(random.randint(int(min_num), int(max_num)))
