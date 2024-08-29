#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

import allure
import pytest

from page_object.JsbOperaProductAudit import JsbOperaProductAudit
from utils.log import Log
from utils.tool_util import time_lag

log = Log()


@allure.feature('运营审核商品')
class TestOperaProductAudit:

    @allure.title('商品审核')
    def test_seller_good_add(self, drivers):
        log.info('当前执行   商品审核    ')
        server = '24'
        opera_phone = '13600136003'
        opera = JsbOperaProductAudit(drivers)
        code = 666666
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        opera.opera_product_menu(opera_phone, code, server)
        for num in range(0, 50):
            opera.opera_product_audit(server, remark='自动化测试驳回')
            num += 1
        log.info('审核完毕 条数:{}'.format(str(num)))
        log.info("开始时间: " + current_time)
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        log.info("结束时间: " + now_time)
        lead_time = time_lag(now_time, current_time)
        log.info("共计使用时间: " + str(lead_time))


if __name__ == '__main__':
    pytest.main(['TestCase/test_opera_product_audit.py'])
