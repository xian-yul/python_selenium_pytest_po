import time

from selenium.common.exceptions import NoSuchElementException

from page.webpage import WebPage
from selenium.webdriver.common.keys import Keys

from common.readelement import Element
from utils import util, times
from utils.log import Log
from utils.times import sleep

log = Log()
opera = Element('JsbOperaProductAudit')

assert_page_url = {
    '24_product_audit_list': 'http://192.168.101.24:8050/operateManage/goods-list/row-material-examine-table',
    '20_product_audit_list': 'https://admdm.jinsubao.cn/operateManage/goods-list/row-material-examine-table',
    '24_product_audit_detail': 'http://192.168.101.24:8050/operateManage/goods-list/raw-examine-detail',
    '20_product_audit_detail': 'https://admdm.jinsubao.cn/operateManage/goods-list/raw-examine-detail'}


class JsbOperaProductAudit(WebPage):

    # 运营登录并进入商品审核界面
    def opera_product_menu(self, phone, code, server):
        self.opera_login(phone, code, server)
        time.sleep(0.5)
        self.is_click(opera['opera_product_audit'])
        self.find_elements(opera['opera_product_audit_menu'])[1].click()
        try:
            if server == '24':
                assert self.return_current_url() == assert_page_url['24_product_audit_list']
            else:
                assert self.return_current_url() == assert_page_url['20_product_audit_list']
        except AssertionError:
            log.error('商品审核列表界面断言错误')
            self.fail_info()
        log.info('商品审核列表界面断言成功 进入下一步')

    # 运营进行商品审核
    def opera_product_audit(self, server, remark):
        times.sleep(0.5)
        try:
            self.find_elements(opera['opera_product_audit_btn'])[0].click()
        except NoSuchElementException:
            log.error('无可审核的商品 退出')
            self.fail_info()
        try:
            if server == '24':
                assert self.return_current_url() in assert_page_url['24_product_audit_detail']
            else:
                assert self.return_current_url() in assert_page_url['20_product_audit_detail']
        except AssertionError:
            log.error('商品审核界面断言错误 审核失败')
            self.fail_info()
        log.info('商品审核界面断言成功 进入下一步')
        self.is_click(opera['opera_product_audit_adopt'])
        try:
            if server == '24':
                assert self.return_current_url() in assert_page_url['24_product_audit_list']
            else:
                assert self.return_current_url() in assert_page_url['20_product_audit_list']
        except AssertionError:
            log.error('商品列表界面断言错误 审核失败 进行驳回操作')
            self.is_click(opera['opera_product_audit_danger'])
            self.input_text(opera['opera_product_audit_danger_remark'], remark)
            self.find_elements(opera['opera_product_audit_danger_btn'])[1].click()
            self.opera_product_audit(server, remark)
        log.info('商品列表界面断言成功 商品审核成功')
