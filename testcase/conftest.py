# -*- coding: utf-8 -*-
# @time    :2022/4/24 16:56
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :conftest.py
import pytest

from Interface_automation.pytest.testcase.commons.yaml_utils import clear_extract_yaml


@pytest.fixture(scope="session", autouse=True)
def clear_extract():
    clear_extract_yaml()
