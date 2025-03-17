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

# opera = JsbOperaProductAudit(driver)
# opera.opera_product_menu(phone=13600136003, code=666666, server='24')
# for audit in range(0, 20):
#     opera.opera_product_audit(server='24', remark='自动化测试驳回')
# driver.find_elements(By.XPATH, "// input[@class='ant-checkbox-input']")[1].click()
# basis_tips = driver.find_element(By.XPATH, "// div[@class='ant-message-custom-content ant-message-warning']").text
# time.sleep(10)
# print(basis_tips)
for audit in range(0, 10):
    driver.find_elements(By.XPATH, "// button[@class='ant-btn']")[0].click()
    time.sleep(1)
    driver.find_element(By.XPATH, "// input[@id='tranAmount']").send_keys(100)
    time.sleep(0.5)
    driver.find_element(By.XPATH, "// input[@id='password']").send_keys(666666)
    time.sleep(0.5)
    driver.find_element(By.XPATH, "// button[@class='WithdrawButton ant-btn ant-btn-primary']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "// button[@class='ant-btn ant-btn-primary']").click()
    time.sleep(1)
