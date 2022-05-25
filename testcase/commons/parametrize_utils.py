# -*- coding: utf-8 -*-
# @time    :2022/4/25 16:27
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :parametrize_utils.py
import json
import os
import traceback

import yaml

from Interface_automation.pytest.testcase.commons.logger_utils import error


class ParametrizeUtils:
    def ddt(self, case_info):
        try:
            case_list = []
            for key, value in case_info["parametrize"].items():
                # 将key拆分成表格的标题
                title_list = str(key).split("-")
                case_datas = self.get_parametrize_data(value)
                # 先判断标题是否相同
                if title_list == case_datas[0]:
                    for x in range(1, len(case_datas)):
                        case = self.ddt_replace(title_list, case_datas[x], case_info)
                        case_list.append(case)
                else:
                    raise Exception("数据驱动文件的标题与YAML文件中设置的标题不一致")

            return case_list
        except Exception as e:
            error("数据驱动方法ddt错误: " + traceback.format_exc())
            raise e

    @staticmethod
    def ddt_replace(title_list, datas, case_info):
        try:
            # 先判断标题与数据的长度是否一致
            if len(title_list) == len(datas):
                case_str = json.dumps(case_info)
                # 先判断
                for x in range(len(title_list)):
                    # 标题的名称
                    title_name = title_list[x]
                    # 标题名称对应的值
                    data_value = datas[x]
                    # 替换实现数据驱动数据更新---判断需要替换的值是否为数字
                    if isinstance(data_value, int) or isinstance(data_value, float):
                        case_str = case_str.replace('"$ddt{' + title_name + '}"', str(data_value))
                    else:
                        case_str = case_str.replace('$ddt{' + title_name + '}', data_value)
                return json.loads(case_str)
            else:
                raise Exception("标题的长度与数据的长度不一致")
        except Exception as e:
            error("数据驱动数据更新方法错误: " + traceback.format_exc())
            raise e

    @staticmethod
    def get_object_path():
        return os.getcwd().split("pytest")[0] + "pytest"

    def get_parametrize_data(self, path):
        try:
            with open(self.get_object_path() + path, mode="r", encoding="utf-8") as file:
                case_info = yaml.load(file, yaml.FullLoader)
                return case_info
        except Exception as e:
            error("获取数据驱动方法get_parametrize_data错误: " + traceback.format_exc())
            raise e

