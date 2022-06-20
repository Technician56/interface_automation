# -*- coding: utf-8 -*-
# @time    :2022/4/24 16:05
# @author  :陶同学
# @Wechat  :Choosen_Me
# @QQ      :2834358530
# @phone   :15355449708
# @file    :pytest_main.py
import sys

# sys.path.append(r"H://pyProjects/learn")
import os
import time

import pytest

if __name__ == '__main__':
    pytest.main()
    time.sleep(3)
    os.system("allure generate ./temps -o ./allure_report --clean")
