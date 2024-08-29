import sys
import time

from selenium.common.exceptions import NoSuchElementException

from page.webpage import WebPage
from selenium.webdriver.common.keys import Keys

from common.readelement import Element
from utils import util, times
from utils.log import Log
from utils.times import sleep

log = Log()
seller = Element('JsbSellerGoodsAdd')

page_url = {'24_raw_list': 'http://192.168.101.24:8070/product-manage/products-list/raw',
            '20_raw_list': 'https://slrdm.jinsubao.cn/product-manage/products-list/raw'}


class JsbSellerGoodAdd(WebPage):

    # 卖家登录并点击至原料添加列表
    def seller_login_click_menu(self, phone, code, server, login_type):
        self.seller_login(phone, code, server, login_type)
        self.is_click(seller['product_menu'])
        self.find_elements(seller['product_list'])[0].click()
        try:
            if server == 24:
                assert self.return_current_url() == page_url['24_raw_list']
            else:
                assert self.return_current_url() == page_url['20_raw_list']
        except AssertionError:
            log.error('断言失败')
            self.fail_info()
        log.info("界面断言成功已进入原料列表")

    # 从列表点击添加原料按钮
    def seller_goods_add_btn(self):
        times.sleep()
        self.find_elements(seller['product_goods_add_btn'])[0].click()
        times.sleep(0.5)
        self.find_elements(seller['product_goods_switch'])[0].click()

    # 点击智能搜索进入选择原料 并可进行搜索
    def seller_raw_number(self, raw_name, raw_number):
        times.sleep(0.5)
        log.info('当前选择牌号下标为：{}'.format(str(raw_number)))
        # 原料数据首次进入未进行加载时 默认能取到60条数据
        self.is_click(seller['product_search_btn'])
        if raw_name != '':
            self.find_elements(seller['product_search_text'])[-1].send_keys(raw_name)
            self.is_click(seller['product_search_submit'])
        raw = self.find_elements(seller['product_raw'])
        log.info('当前取到牌号数据数量{}'.format(str(len(raw))))
        grade_num = 0
        if raw_number >= len(raw):
            log.info('当前所要选择牌号下标位置大于已取到牌号数据 因此下拉加载刷新')
            while grade_num < 5:  # < x 为循环次数 加载原料选择
                raw = self.find_elements(seller['product_raw'])
                sleep()
                self.script_top(raw[-1])
                grade_num += 1
            log.info('下拉加载牌号数据 重新取到的牌号数据数量为:{}'.format(str(len(raw))))
        raw[raw_number].click()
        log.info('所选择原料为:{}'.format(raw[raw_number].text))

    # 配送范围选择 默认全部
    def seller_delivery_area(self):
        self.is_click(seller['product_mode_pickup'])
        times.sleep(0.5)
        self.is_click(seller['product_deliveryAreaName'])
        self.is_click(seller['product_deliveryAreaName_whole'])
        self.is_click(seller['product_deliveryArea_btn'])

    # 上传图片 填写商品概要 商品详情  点击下一步 完成第一页数据填写
    def seller_goods_detail(self, img_path, profiles, detail):
        time.sleep(0.5)
        self.script("1000")
        self.find_elements(seller['product_upload'])[1].send_keys(img_path)
        time.sleep(0.5)
        self.find_elements(seller['product_upload_cut_btn'])[1].click()
        times.sleep()
        self.find_elements(seller['product_upload_cut_btn'])[1].click()
        times.sleep(0.5)
        self.find_element(seller['product_profiles']).send_keys(profiles)
        self.script("5000")
        time.sleep(1)
        # self.input_text(seller['product_detail'], detail)
        self.find_elements(seller['product_next_step'])[2].click()

    # 填写现货信息
    def seller_goods_stock_info(self, stock, min_purchase, delivery_price, self_mention_price):
        time.sleep(0.5)
        self.input_clear_text(seller['product_goods_stock'], stock)
        self.input_clear_text(seller['product_goods_minPurchase'], min_purchase)
        self.find_elements(seller['product_payment_type'])[5].click()  # 选择配送类型的款到发货
        self.input_clear_text(seller['product_goods_deliveryPrice'], delivery_price)
        self.find_elements(seller['product_payment_type'])[7].click()  # 选择自提类型的款到发货
        self.input_clear_text(seller['product_goods_selfMentionPrice'], self_mention_price)

    # 填写基差信息
    def seller_basis_info(self, stock, min_purchase, handles_rate, min_protection_price, max_protection_price,
                          delivery_spill_price,
                          self_mention_spill_price, raw_number, img_path):
        time.sleep(0.5)
        self.find_elements(seller['product_mode_basis'])[1].click()  # 勾选基差选项
        try:
            basis_tips = self.find_element(seller['product_basis_tips'])
            log.error(basis_tips.text)
            self.find_elements(seller['product_previous_step'])[2].click()  # 返回上一页界面 重新选择原料
            raw_number += 1
            self.seller_raw_number('', raw_number)
            self.find_elements(seller['product_upload'])[1].send_keys(img_path)
            time.sleep(0.5)
            self.find_elements(seller['product_upload_cut_btn'])[1].click()
            times.sleep()
            self.find_elements(seller['product_upload_cut_btn'])[1].click()
            time.sleep(1)
            self.find_elements(seller['product_next_step'])[2].click()
        except Exception:
            log.info('所选牌号有基差合约 进行填写基差信息')
            self.is_click(seller['product_basis_tab'])
            purchase_num = self.find_elements(seller['product_basis_num'])[2].text
            surplus = util.remove_chinese(str(purchase_num))
            basis_surplus = surplus[1:]  # 剩余可发布基差量
            if float(stock) > float(basis_surplus):
                stock = 0.01
            elif float(basis_surplus) == 0:
                log.info('无剩余基差交易量可发布')
                sys.exit(0)
            self.input_clear_text(seller['product_basis_stock'], stock)
            self.input_clear_text(seller['product_basis_minPurchase'], min_purchase)
            self.find_elements(seller['product_basis_transaction_type'])[5].click()  # 4收盘可交易 5收盘不可交易 默认4
            self.find_elements(seller['product_basis_contract_type'])[7].click()  # 6失效下架 7失效切换 8自动切换 默认6
            self.input_clear_text(seller['product_basis_handlesRate'], handles_rate)
            contract_price = self.find_elements(seller['product_contract_price'])[1].text
            min_protection_price = int(contract_price) - 100
            max_protection_price = int(contract_price) + 300
            self.input_clear_text(seller['product_basis_minProtectionPrice'], min_protection_price)
            self.input_clear_text(seller['product_basis_maxProtectionPrice'], max_protection_price)
            self.input_clear_text(seller['product_basis_deliveryPrice'], delivery_spill_price)
            self.input_clear_text(seller['product_basis_selfMentionPrice'], self_mention_spill_price)

    # 进行提交商品信息 并进行断言判断 通过提交后的界面判断是否提交成功 不成功则返回上一步选择下一个原料 进行提交
    def seller_goods_add_submit(self, server, raw_number, img_path):
        times.sleep(0.5)
        self.find_elements(seller['product_goods_submit'])[0].click()
        times.sleep(1)
        try:
            if server == '24':
                assert self.return_current_url() == page_url['24_raw_list']
            else:
                assert self.return_current_url() == page_url['20_raw_list']
        except AssertionError:
            log.error('添加出错 或 重复添加  重新选择牌号')
            raw_number += 10
            self.find_elements(seller['product_previous_step'])[2].click()  # 返回上一页界面 重新选择原料
            self.seller_raw_number('', raw_number)
            self.find_elements(seller['product_upload'])[1].send_keys(img_path)
            time.sleep(0.5)
            self.find_elements(seller['product_upload_cut_btn'])[1].click()
            times.sleep()
            self.find_elements(seller['product_upload_cut_btn'])[1].click()
            time.sleep(1)
            self.find_elements(seller['product_next_step'])[2].click()
            self.seller_goods_add_submit(server, raw_number, img_path)
        raw_number += 1
        times.sleep()
        log.info('----------------------------------------------------------------------------------')
        return raw_number
