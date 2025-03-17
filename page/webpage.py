#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
selenium基类
本文件存放了selenium基类的封装方法
"""
import time

import allure
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from common.readelement import Element
from config.conf import cm
from utils import times
from utils.log import Log
from utils.times import sleep

log = Log()
user = Element('JsbUserInfo')
assert_page_url = {'24_user_login': 'http://192.168.101.24:8090/user/login',
                   '24_user_login_after': 'http://192.168.101.24:8090/',
                   '24_opera_login': 'http://192.168.101.24:8050/user/login',
                   '20_opera_login': 'https://admdm.jinsubao.cn/user/login',
                   '24_opera_login_after': 'http://192.168.101.24:8050/dashboard',
                   '20_opera_login_after': 'https://admdm.jinsubao.cn/dashboard',
                   '24_seller_login': 'http://192.168.101.24:8070/user/login',
                   '20_seller_login': 'https://slrdm.jinsubao.cn/user/login',
                   '24_seller_login_after': 'http://192.168.101.24:8070/dashboard',
                   '20_seller_login_after': 'https://slrdm.jinsubao.cn/dashboard'}
page_url = {'24_user': 'http://192.168.101.24:8090', '20_user': 'https://demo.jinsubao.cn/',
            '24_seller': 'http://192.168.101.24:8070', '20_seller': 'https://slrdm.jinsubao.cn/',
            '24_opera': 'http://192.168.101.24:8050', '20_opera': 'https://admdm.jinsubao.cn/'}


class WebPage(object):
    """selenium基类"""

    def __init__(self, driver):
        self.driver = webdriver.Chrome()
        self.driver = driver
        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)

    def get_url(self, url):
        """打开网址并验证"""
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
        #     log.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(cm.LOCATE_MODE[name], value)

    def find_element(self, locator):
        """寻找单个元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)

    def find_elements(self, locator):
        """查找多个相同的元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        #   log.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator, txt):
        """输入(输入前先清空)"""
        sleep(0.5)
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)

    #  log.info("输入文本：{}".format(txt))

    def is_click(self, locator):
        """点击"""
        self.find_element(locator).click()
        sleep()

    #   log.info("点击元素：{}".format(locator))

    def element_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        #  log.info("获取文本：{}".format(_text))
        return _text

    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)

    @allure.step('截图')
    def base_get_img(self):
        self.driver.get_screenshot_as_file("./{}.png".format(time.strftime("%Y_%m_%d_%H_%M_%S")))

    @allure.step('切换标签页')
    def win_handles(self, num):
        self.driver.close()
        handles = self.driver.window_handles
        num = int(num)
        self.driver.switch_to.window(handles[num])
        sleep(0.2)

    @allure.step('界面滚动条下拉')
    def script(self, js_size):
        # js脚本 滚动条下拉
        js = "var q=document.documentElement.scrollTop=" + js_size
        self.driver.execute_script(js)

    def click_action(self, loc, num):
        text = 0
        ele = self.find_element(loc)
        while text < num:
            ActionChains(self.driver).click_and_hold(ele).perform()
            text += 1
        # 释放
        ActionChains(self.driver).release(ele).perform()

    def fail_info(self):
        self.base_get_img()
        log.error('当前url: ' + self.return_current_url())
        # self.driver.quit()

    @allure.step('返回当前url')
    def return_current_url(self):
        return self.driver.current_url

    @allure.step('单元素文本框输入')
    def input_clear_text(self, loc, text):
        loc_object = self.find_element(loc)  # 定位到文本框元素
        loc_object.clear()  # 文本框内容清空
        loc_object.send_keys(keys.Keys.CONTROL, "a")  # 键盘全选文本框内容
        for i in range(10):
            loc_object.send_keys(keys.Keys.BACKSPACE)  # 循环删除
        loc_object.send_keys(text)

    @allure.step('多元素文本框输入')
    def inputs_clear_text(self, loc, index, text):
        loc_object = self.find_elements(loc)[index]
        loc_object.clear()
        loc_object.send_keys(keys.Keys.CONTROL, "a")
        for i in range(10):
            loc_object.send_keys(keys.Keys.BACKSPACE)
        loc_object.send_keys(text)

    def script_top(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)  # 拖动到可见的元素去

    def implicitly_wait(self, wait_time):
        self.driver.implicitly_wait(wait_time)

    def opera_transverse_scrollto(self):
        js = 'document.getElementsByClassName("ant-table-body")[0].scrollLeft=20000'
        self.driver.execute_script(js)

    # 隐式等待 超时时间、轮询时间、等待条件 指定元素
    def WebDriverWait_Time_log(self, driver, over_time, polling_time, location):
        WebDriverWait(driver, over_time, polling_time).until(
            expected_conditions.element_to_be_clickable(location))

    # 隐式等待 超时时间、轮询时间、等待条件 指定标题
    def WebDriverWait_Time_title(self, driver, over_time, polling_time, title):
        WebDriverWait(driver, over_time, polling_time).until(
            expected_conditions.title_is(title))

    def user_login(self, phone, code, server):
        if server == '24':
            self.get_url(page_url['24_user'])
        else:
            self.get_url(page_url['20_user'])
        self.WebDriverWait_Time_title(self.driver, 3, 0.5, '首页')
        try:
            if server == '24':
                assert self.return_current_url() == assert_page_url['24_user_login']
            else:
                assert self.return_current_url() == assert_page_url['20_user_login']
        except AssertionError:
            log.error('断言出现异常')
            self.fail_info()
        log.info('买家首页界面断言成功')
        self.is_click(user['user_login_text'])
        self.WebDriverWait_Time_title(self.driver, 10, 0.5, '登录')
        try:
            if server == '24':
                assert self.return_current_url() == assert_page_url['24_user_login']
            else:
                assert self.return_current_url() == assert_page_url['20_user_login']
        except AssertionError:
            log.error('断言出现异常')
            self.fail_info()
        log.info('登录界面断言成功')
        self.input_text(user['user_login_phone'], phone)
        self.is_click(user['user_login_code_btn'])
        self.input_text(user['user_login_code_text'], code)
        self.is_click(user['user_login_submit'])
        try:
            if server == '24':
                assert self.return_current_url() == assert_page_url['24_user_login_after']
            else:
                assert self.return_current_url() == assert_page_url['20_user_login_after']
        except AssertionError:
            log.error('断言出现异常')
            self.fail_info()
        log.info('登录后界面断言成功、登录成功')

    def opera_login(self, phone, code, server):
        if server == '24':
            self.get_url(page_url['24_opera'])
        else:
            self.get_url(page_url['20_opera'])
        self.WebDriverWait_Time_title(self.driver, 3, 0.5, '登录')
        try:
            if server == '24':
                assert self.return_current_url() == assert_page_url['24_opera_login']
            else:
                assert self.return_current_url() == assert_page_url['20_opera_login']
        except AssertionError:
            log.error('断言出现异常')
            self.fail_info()
        log.info('运营登录界面断言成功')
        self.input_text(user['opera_login_phone'], phone)
        self.is_click(user['opera_login_code_btn'])
        self.input_text(user['opera_login_code_text'], code)
        self.is_click(user['opera_login_submit'])
        try:
            if server == '24':
                assert self.return_current_url() == assert_page_url['24_opera_login_after']
            else:
                assert self.return_current_url() == assert_page_url['20_opera_login_after']
        except AssertionError:
            log.error('断言出现异常')
            self.fail_info()
        log.info('登录后界面断言成功、登录成功')

    def seller_login(self, phone, code, server, login_type):
        if server == '24':
            self.get_url(page_url['24_seller'])
        else:
            self.get_url(page_url['20_seller'])
        # self.WebDriverWait_Time_title(self.driver, 10, 0.5, '登录')
        times.sleep(1)
        try:
            if server == '24':
                assert self.return_current_url() == assert_page_url['24_seller_login']
            else:
                assert self.return_current_url() == assert_page_url['20_seller_login']
        except AssertionError:
            log.error('断言出现异常')
            self.fail_info()
        log.info('卖家登录界面断言成功')
        times.sleep(0.5)
        if login_type == 1:
            self.is_click(user['seller_switch_login'])
            self.input_text(user['seller_login_name'], phone)
            self.input_text(user['seller_login_password'], code)
        else:
            self.input_text(user['seller_login_phone'], phone)
            self.is_click(user['seller_login_code_btn'])
            self.input_text(user['seller_login_code_text'], code)
        self.is_click(user['seller_login_submit'])
        times.sleep(0.5)
        self.find_elements(user['seller_login_code_pop'])[0].click()
        try:
            if server == '24':
                assert self.return_current_url() == assert_page_url['24_seller_login_after']
            else:
                assert self.return_current_url() == assert_page_url['20_seller_login_after']
        except AssertionError:
            log.error('断言出现异常')
            self.fail_info()
        log.info('登录后界面断言成功、登录成功')
