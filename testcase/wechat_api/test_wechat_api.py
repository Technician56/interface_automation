# -*- coding: utf-8 -*-
# @time    :2022/4/24 16:15
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :test_wechat_api.py
import allure
import pytest

from Interface_automation.pytest.testcase.commons.requests_utils import RequestsUtils
from Interface_automation.pytest.testcase.commons.yaml_utils import get_testcase_yaml
from Interface_automation.pytest.testcase.terminal_loading.tcs_custom import TcsCustomUtils


@allure.epic("陶朝盛-项目")
@allure.feature("微信公众平台项目")
class TestWechatApi:

    @pytest.mark.parametrize("case_info", get_testcase_yaml("/testcase/wechat_api/wechat_get_access_token.yaml"))
    def test_get_access_token(self, case_info):
        RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)

    @pytest.mark.parametrize("case_info", get_testcase_yaml("/testcase/wechat_api/wechat_get_tags.yaml"))
    def test_get_tags(self, case_info):
        RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)

    @pytest.mark.parametrize("case_info", get_testcase_yaml("/testcase/wechat_api/wechat_create_tag.yaml"))
    def test_create_tag(self, case_info):
        RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)

    @pytest.mark.parametrize("case_info", get_testcase_yaml("/testcase/wechat_api/wechat_edit_tag.yaml"))
    def test_edit_tag(self, case_info):
        RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)

    @pytest.mark.parametrize("case_info", get_testcase_yaml("/testcase/wechat_api/wechat_delete_tag.yaml"))
    def test_delete_tag(self, case_info):
        RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)

    @pytest.mark.parametrize("case_info", get_testcase_yaml("/testcase/wechat_api/wechat_file_upload.yaml"))
    def test_file_upload(self, case_info):
        RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)

