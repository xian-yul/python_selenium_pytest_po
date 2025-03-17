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
for num in range(0, 6):
    time.sleep(0.5)
    xiatou_name = util.get_random_chinese_characters(5)
    driver.find_elements(By.XPATH, "// button[@class='ant-btn ant-btn-primary']")[1].click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, "// input[@id='name']").send_keys(xiatou_name)
    driver.find_element(By.XPATH, "// div[@class='ant-select-selection__placeholder']").click()
    time.sleep(1)
    driver.find_elements(By.XPATH, "// li[@class='ant-select-dropdown-menu-item']")[0].click()
    driver.find_elements(By.XPATH, "// button[@class='ant-btn ant-btn-primary']")[2].click()
    time.sleep(0.5)
    print(num)
    num += 1
