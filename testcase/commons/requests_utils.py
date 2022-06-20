# -*- coding: utf-8 -*-
# @time    :2022/4/24 16:24
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :requests_utils.py
import json
import re
import time
import traceback

import jsonpath
import requests

from interface_automation.testcase.commons.decryption_utils import DecryptionUtils
from interface_automation.testcase.commons.logger_utils import info, error
from interface_automation.testcase.commons.yaml_utils import get_base_url, set_extract_yaml, get_sign, get_random_number


class RequestsUtils:
    session = requests.session()

    def __init__(self, obj):
        self.obj = obj

    # 规范测试用例
    def standard_yaml(self, case_info):
        try:
            info("-" * 30)
            if isinstance(case_info, dict):
                first_key = case_info.keys()
                # 一级关键字中必须包含name, base_url, request, validate
                if "name" in first_key and "base_url" in first_key and "request" in first_key and "validate" in first_key:
                    # request 下的 二级关键字必须包含 method，url
                    info(f"用例 {case_info['name']} 开始")
                    request_key = case_info["request"].keys()
                    if "method" in request_key and "url" in request_key:
                        # 判断是否需要进行签名操作
                        if "headers" in request_key:
                            if "sign" in case_info["request"]["headers"].keys():
                                case_info["request"]["headers"]["sign"] = self.custom_sign(case_info)

                        # 获得method, url
                        url = get_base_url(case_info["base_url"]) + case_info["request"].pop("url")
                        method = case_info["request"].pop("method")
                        # pop之后，case_info["request"]中剩下的元素全部为请求参数
                        # 发送请求, 得到结果
                        res = self.send_request(method=method, url=url, **case_info["request"])
                        # 获取res的json格式以及text格式
                        res_json = ""
                        try:
                            res_json = res.json()
                        except:
                            info("结果不支持json格式")
                        res_text = res.text
                        # 实现接口关联
                        if "extract" in first_key:
                            # info("------开始实现接口关联------")
                            for extract_key, extract_value in case_info["extract"].items():
                                if "(.*?)" in extract_value or "(.+?)" in extract_value:
                                    # 满足上述条件，进行正则表达式提取value
                                    zz_value = re.findall(extract_value, res_text)
                                    if zz_value:  # 如果提取到的结果不为空
                                        zz_value = zz_value[0]
                                        extract = {extract_key: zz_value}
                                        set_extract_yaml(extract)
                                elif "$" in extract_value:
                                    # 满足上述条件，进行jsonpath提取value
                                    jsonpath_value = jsonpath.jsonpath(res_json, extract_value)
                                    if jsonpath_value:  # 如果提取到的结果不为空
                                        jsonpath_value = jsonpath_value[0]
                                        extract = {extract_key: jsonpath_value}
                                        set_extract_yaml(extract)
                                else:
                                    info(f"该方式暂不支持:{extract_value}")
                            # info("------接口关联结束------")
                        # 断言
                        # 实际结果、预期结果、状态码
                        sj_result = res_json
                        yq_result = case_info["validate"]
                        status_code = res.status_code
                        self.res_validate(sj_result, yq_result, status_code)
                        info(f"用例 {case_info['name']} 结束")
                        info("------断言通过------")
                    else:
                        error("request下二级关键字缺失: 必须包含 method, url")
                        raise Exception("request下二级关键字缺失: 必须包含 method, url")
                else:
                    error("一级关键字缺失: 包含name, base_url, request, validate")
                    raise Exception("一级关键字缺失: 包含name, base_url, request, validate")
            else:
                error("用例格式不正确，需要字典类型")
                raise Exception("用例格式不正确，需要字典类型")
        except Exception as e:
            error("规范测试用例错误: " + traceback.format_exc())
            raise e

    # 发送请求
    def send_request(self, method, url, **request_args):
        try:
            # 如果在url中有"${" 和 "}",进行替换操作
            if "${" in url and "}" in url:
                # info("------开始执行URL热加载操作------")
                url = self.value_replace(url)
                # info("------URL热加载结束------")
            for key, value in request_args.items():
                if key in ["params", "data", "json", "headers"]:
                    # info(f"------开始执行{key}热加载操作------")
                    request_args[key] = self.value_replace(value)
                    # info(f"------{key}热加载结束------")
                elif key == "files":
                    for file_key, file_value in request_args[key].items():
                        request_args[key][file_key] = open(file_value, mode="rb")
            info("------开始发送接口请求------")
            info("请求方式: " + method)
            info("URL: " + url)
            info("请求参数:" + str(request_args))
            res = self.session.request(method=method, url=url, **request_args)
            info("请求结束-->\n实际结果--> " + res.text)
            return res
        except Exception as e:
            error("发送请求方法错误: " + traceback.format_exc())
            raise e

    # 热加载
    # 需要进行替换的位置: url, params, data, json, headers, validate
    # 替换的值的类型: int, float, str, list, dict
    def value_replace(self, data):
        try:
            # 先保存数据类型,后期需要将数据类型转换回来
            data_type = type(data)
            # 如果data的格式是dict 或者 list, 先将值转换成字符串
            if isinstance(data, dict) or isinstance(data, list):
                str_data = json.dumps(data)
            else:  # 如果不是，直接强转成字符串
                str_data = str(data)
            if "${" in str_data and "}" in str_data:
                # 替换操作
                for x in range(str_data.count("${")):
                    begin_index = str_data.index("${")
                    end_index = str_data.index("}", begin_index)
                    old_str = str_data[begin_index: end_index + 1]
                    func_name = old_str[2: old_str.index("(")]
                    func_args = old_str[old_str.index("(") + 1: old_str.index(")")]
                    if func_args:
                        args = func_args.split(",")
                        new_str = getattr(self.obj, func_name)(*args)
                    else:
                        new_str = getattr(self.obj, func_name)()
                    if isinstance(new_str, int) or isinstance(new_str, float):
                        str_data = str_data.replace('"' + old_str + '"', str(new_str))
                    else:
                        str_data = str_data.replace(old_str, str(new_str))
                    info("替换: " + str(old_str) + " ---> " + str(new_str))
            # 将数据类型进行还原
            if isinstance(data, dict) or isinstance(data, list):
                str_data = json.loads(str_data)
            else:
                str_data = data_type(str_data)
            return str_data
        except Exception as e:
            error("热加载方法错误: " + traceback.format_exc())
            raise e

    # 断言
    # 实际结果、预期结果、状态码
    def res_validate(self, sj_result, yq_result, status_code):
        try:
            if yq_result:
                # 对断言的预期结果进行热加载替换值
                # info("------断言热加载开始------")
                yq_result = self.value_replace(yq_result)
                # info("------断言热加载结束------")
                info("------断言开始------")
                for validate_args in yq_result:
                    for validate_key, validate_value in validate_args.items():
                        if validate_key == "equals":  # 相等断言
                            # info("开始判断相等断言:")
                            for equals_key, equals_value in validate_value.items():
                                if equals_key == "status_code":  # 状态断言
                                    try:
                                        assert equals_value == status_code
                                        info(f"状态断言成功: 状态码{equals_key} 等于 {status_code}")
                                    except AssertionError as e:
                                        info(f"状态断言失败: 状态码{equals_key} 不等于 {status_code}")
                                        raise e
                                else:  # 业务断言
                                    value_in_sj_result = jsonpath.jsonpath(sj_result, f'$..{equals_key}')
                                    if value_in_sj_result:
                                        try:
                                            assert equals_value in value_in_sj_result
                                            info(f"业务断言成功: {equals_key} 等于 {equals_value}")
                                        except AssertionError as e:
                                            info(f"业务断言失败: {equals_key} 不等于 {equals_value}")
                                            raise e
                                    else:
                                        try:
                                            assert equals_value in value_in_sj_result
                                        except AssertionError as e:
                                            info(f"业务断言失败: 不存在对应的key: {equals_key}")
                                            raise e
                        elif validate_key == "contains":  # 包含断言
                            # info("开始判断包含断言:")
                            try:
                                assert str(validate_value) in str(sj_result)
                                info(f"断言成功: 实际结果中存在:{validate_value}  --> 实际结果: {sj_result}")
                            except AssertionError as e:
                                info(f"断言失败: 实际结果中不存在:{validate_value}  --> 实际结果: {sj_result}")
                                raise e
                info("------断言结束------")
            else:
                raise Exception("请完善断言")
        except Exception as e:
            error("断言方法错误: " + traceback.format_exc())
            raise e

    # 签名
    def custom_sign(self, case_info):
        # 从配置文件中得到appid和appsecret
        appid = get_sign("appid")
        appsecret = get_sign("appsecret")
        nonce = get_random_number(1000000000, 9999999999)
        timestamp = str(int(time.time()))
        # 开始签名操作
        # 1. 获取参数，包括URL"?"之后的值，params，json，data中的值，合并成一个字典
        params_dict = {}
        params_str = ""
        request_param = case_info["request"]
        request_keys = case_info["request"].keys()
        # 获取URL中的参数,加入到字典中
        url_param = str(request_param["url"]).split("?")[1].split("&")
        for param in url_param:
            param_key = param[: param.index("=")]
            param_value = param[param.index("=") + 1:]
            params_dict[param_key] = param_value
        # 获得params，json，data中的参数,加入到字典中
        for key in request_keys:
            if key in ["params", "data", "json"]:
                params_dict.update(request_param[key])
        # 2. 将字典根据ASCII码进行排序
        params_dict = self.ascii_ordering_dict(params_dict)
        # 3. 将字典转换成由&和=拼接的格式
        for key, value in params_dict.items():
            params_str += key + "=" + value + "&"
        # 4. 头部拼接上 appsecret、appid
        params_str = f"appid={appid}&appsecret={appsecret}&{params_str}"
        # 5. 尾部拼接上 nonce流水、timestamp时间戳
        params_str = f"{params_str}nonce={nonce}&timestamp={timestamp}"
        # 6. 热加载将值进行替换
        params_str = self.value_replace(params_str)
        # 7. 将最终的值进行MD5加密
        params_str = DecryptionUtils().md5(params_str)
        return params_str

    # 将字典根据ASCII码进行排序
    @staticmethod
    def ascii_ordering_dict(ordered_dict):
        if isinstance(ordered_dict, dict):
            key_list = sorted(ordered_dict.keys())
            new_dict = {}
            for key in key_list:
                new_dict[key] = ordered_dict[key]
            return new_dict
