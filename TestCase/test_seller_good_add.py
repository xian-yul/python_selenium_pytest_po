#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time

import allure
import pytest

from page_object.JsbSellerGoodAdd import JsbSellerGoodAdd
from utils.log import Log
from utils.tool_util import time_lag

log = Log()


@allure.feature('卖家添加原料')
class TestOperaInspect:

    @allure.title('卖家添加原料流程')
    def test_seller_good_add(self, drivers):
        log.info('当前执行   添加原料    ')
        server = '20'
        seller_phone = '17200000005'
        seller = JsbSellerGoodAdd(drivers)
        code = 666666
        raw_name = ''
        img_path = 'E:\BaiduNetdiskDownload\素材\原料\ABS山东海江HJ15A\主图1.jpg'
        profiles = '我不是商品概要'
        detail = '商品没有详情'
        raw_stock = 100
        raw_min_purchase = '0.01'
        raw_delivery_price = 7890
        raw_self_mention_price = 6789
        basis_stock = 3
        basis_min_purchase = '0.01'
        delivery_spill_price = 50
        self_mention_spill_price = 30
        handsel_rate = 20
        min_protection_price = 0
        max_protection_price = 0
        login_type = 0
        add_type = 3  # 1现货 2基差 3现货+基差
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        seller.seller_login_click_menu(seller_phone, code, server, login_type)
        raw_number = 0
        for num in range(0, 20):
            seller.seller_goods_add_btn()
            seller.seller_raw_number(raw_name, raw_number)
            seller.seller_delivery_area()
            seller.seller_goods_detail(img_path, profiles, detail)
            if add_type == 3:
                seller.seller_goods_stock_info(raw_stock, raw_min_purchase, raw_delivery_price, raw_self_mention_price)
                seller.seller_basis_info(basis_stock, basis_min_purchase, handsel_rate, min_protection_price,
                                         max_protection_price,
                                         delivery_spill_price,
                                         self_mention_spill_price, raw_number, img_path)
            elif add_type == 1:
                seller.seller_goods_stock_info(raw_stock, raw_min_purchase, raw_delivery_price, raw_self_mention_price)
            else:
                seller.seller_basis_info(basis_stock, basis_min_purchase, handsel_rate, min_protection_price,
                                         max_protection_price,
                                         delivery_spill_price,
                                         self_mention_spill_price, raw_number, img_path)
            raw_number = seller.seller_goods_add_submit(server, raw_number, img_path)
            log.info(str(num))
            num += 1
        log.info('添加完毕 条数:{}'.format(str(num)))
        log.info("开始时间: " + current_time)
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        log.info("结束时间: " + now_time)
        lead_time = time_lag(now_time, current_time)
        log.info("共计使用时间: " + str(lead_time))


if __name__ == '__main__':
    pytest.main(['TestCase/test_seller_good_add.py'])
