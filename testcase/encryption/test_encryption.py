# -*- coding: utf-8 -*-
# @time    :2022/4/25 20:23
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :test_encryption.py
import pytest

from interface_automation.testcase.commons.requests_utils import RequestsUtils
from interface_automation.testcase.commons.yaml_utils import get_testcase_yaml
from interface_automation.testcase.terminal_loading.tcs_custom import TcsCustomUtils


class TestEncryption:

    # @pytest.mark.parametrize("case_info", get_testcase_yaml("./testcase/encryption/encryption_md5.yaml"))
    # def test_md5_encryption(self, case_info):
    #     RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)
    #
    # @pytest.mark.parametrize("case_info", get_testcase_yaml("./testcase/encryption/encryption_base64.yaml"))
    # def test_base64_encryption(self, case_info):
    #     RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)

    # @pytest.mark.parametrize("case_info", get_testcase_yaml("./testcase/encryption/test_rsa_encryption.yaml"))
    # def test_rsa_encryption(self, case_info):
    #     RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)
    #

    @pytest.mark.parametrize("case_info", get_testcase_yaml("./testcase/encryption/sign.yaml"))
    def test_sign(self, case_info):
        RequestsUtils(TcsCustomUtils()).standard_yaml(case_info)

