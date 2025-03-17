import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from page_object.JsbOperaProductAudit import JsbOperaProductAudit
from utils import util
from utils.log import Log

log = Log()

page_url = {'goods_list': 'http://192.168.101.24:8070/product-manage/products-list/raw',
            'goods_add_page': 'http://192.168.101.24:8070/product-manage/raw-provide-form'
    , 'opera_audit': 'http://192.168.101.24:8050/operateManage/goods-list/row-material-examine-table'}

chrome_options = Options()  # 创建一个事项
chrome_options.add_experimental_option("debuggerAddress", '127.0.0.1:9234')  # ip地址为第一步中在浏览器中输入的地址
driver = webdriver.Chrome(options=chrome_options)
for num in range(0, 5):
    time.sleep(0.5)
    driver.find_element(By.XPATH, "// button[@class='margin-b-16 ant-btn ant-btn-primary']").click()
    release_platform = driver.find_elements(By.XPATH, "// input[@class='ant-checkbox-input']")
    time.sleep(0.5)
    release_platform[0].click()
    release_platform[1].click()
    content = '测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告测试公告_' + str(
        num)
    driver.find_element(By.XPATH, "// textarea[@id='content']").send_keys(content)
    # driver.find_elements(By.XPATH, "// button[@class='ant-btn']")[0].click()
    time.sleep(0.5)
    # driver.find_elements(By.XPATH, "// label[@class='ant-radio-button-wrapper']")[0].click()
    # time.sleep(0.5)
    # driver.find_elements(By.XPATH, "// tr[@class='ant-table-row ant-table-row-level-0']")[0].click()
    # driver.find_elements(By.XPATH, "// button[@class='ant-btn ant-btn-primary']")[-1].click()
    # time.sleep(0.5)
    driver.find_element(By.XPATH, "// input[@id='day']").send_keys(1)
    driver.find_element(By.XPATH, "// button[@class='ant-btn ant-btn-primary']").click()
    print(num)
    num += 1
    time.sleep(0.5)
